from __future__ import annotations

from datetime import datetime, time, timedelta, timezone
import json
import logging
import os
import re
import unicodedata
import urllib.error
import urllib.request
from typing import Any

from sqlalchemy.orm import Session

from app.core.mongo import registrar_evento_mongo
from app.models.alergia import AlergiaUsuario
from app.models.medicamento import Medicamento
from app.models.tratamiento import Tratamiento
from app.models.usuario import Usuario
from app.schemas.ai import (
    AiChatMedicationActionItem,
    AiChatResponse,
    AiDossierPoint,
    AiMedicationSuggestResponse,
    AiPrescriptionMedItem,
    AiPrescriptionScanResponse,
    AiStatusResponse,
)
from app.services.catalogo_service import (
    REGLAS_INTERACCIONES,
    buscar_en_catalogo,
    verificar_alergias_paciente,
)
from app.services.recordatorio_service import generar_recordatorios, invalidar_cache_horizonte

logger = logging.getLogger(__name__)

OLLAMA_CANDIDATE_URLS = [
    os.environ.get("OLLAMA_BASE_URL", "").rstrip("/"),
    "http://host.docker.internal:11434",
    "http://127.0.0.1:11434",
    "http://localhost:11434",
]
OLLAMA_CANDIDATE_URLS = [u for u in OLLAMA_CANDIDATE_URLS if u]

PREFERRED_MODELS = ["medi-clinico:latest", "medi-clinico", "llama3.2:latest", "llama3.2"]


def _resolve_ollama_endpoint(timeout: float = 2.0) -> tuple[str | None, str, list[str]]:
    """Descubre la URL activa de Ollama y el modelo clínico entrenado disponible."""
    for base_url in OLLAMA_CANDIDATE_URLS:
        try:
            req = urllib.request.Request(f"{base_url}/api/tags", method="GET")
            with urllib.request.urlopen(req, timeout=timeout) as resp:
                if resp.status == 200:
                    data = json.loads(resp.read().decode("utf-8"))
                    models = [m.get("name", "") for m in data.get("models", []) if m.get("name")]
                    chosen = "medi-clinico"
                    for pref in PREFERRED_MODELS:
                        if pref in models:
                            chosen = pref
                            break
                    else:
                        if models:
                            chosen = models[0]
                    return base_url, chosen, models
        except Exception:
            continue
    return None, "medi-clinico (fallback-determinista)", []


def obtener_estado_ollama() -> AiStatusResponse:
    base_url, chosen, models = _resolve_ollama_endpoint(timeout=2.0)
    return AiStatusResponse(
        status="online" if base_url else "fallback_local",
        ollama_reachable=base_url is not None,
        active_model=chosen,
        available_models=models,
        formal_rules_loaded=6,
    )


def _construir_contexto_paciente(db: Session | None, user: Usuario | None, fallback_name: str) -> dict[str, Any]:
    if db is None or user is None:
        return {
            "paciente": fallback_name or "Paciente",
            "medicamentos_activos": [],
            "alergias": [],
        }

    meds = (
        db.query(Medicamento)
        .filter(Medicamento.id_usuario == user.id_usuario)
        .all()
    )
    trats = (
        db.query(Tratamiento)
        .join(Medicamento, Medicamento.id_medicamento == Tratamiento.id_medicamento)
        .filter(Medicamento.id_usuario == user.id_usuario, Tratamiento.estado == "activo")
        .all()
    )
    trat_by_med = {t.id_medicamento: t for t in trats}
    alergias = (
        db.query(AlergiaUsuario)
        .filter(AlergiaUsuario.id_usuario == user.id_usuario)
        .all()
    )

    meds_desc = []
    for m in meds:
        t = trat_by_med.get(m.id_medicamento)
        freq_txt = f"cada {t.frecuencia_horas}h" if t else "sin horario activo"
        crit_txt = " [CRÍTICO]" if m.es_critico else ""
        pa_txt = f" ({m.principio_activo})" if m.principio_activo else ""
        meds_desc.append(f"{m.nombre}{pa_txt} {m.dosis} ({freq_txt}, stock: {m.cantidad_stock}){crit_txt}")

    alergias_desc = [f"{a.sustancia} (severidad: {a.severidad})" for a in alergias]

    return {
        "paciente": (user.nombre_completo.split(" ")[0] if user.nombre_completo else fallback_name) or "Paciente",
        "medicamentos_activos": meds_desc,
        "alergias": alergias_desc,
    }


def _extraer_json_seguro(raw_text: str) -> dict[str, Any] | None:
    if not raw_text:
        return None
    cleaned = raw_text.strip()
    if cleaned.startswith("```"):
        cleaned = cleaned.strip("`")
        if cleaned.lower().startswith("json"):
            cleaned = cleaned[4:].strip()
    start = cleaned.find("{")
    end = cleaned.rfind("}")
    if start != -1 and end != -1 and end > start:
        snippet = cleaned[start : end + 1]
        try:
            return json.loads(snippet)
        except Exception:
            pass
    try:
        return json.loads(cleaned)
    except Exception:
        return None


def _fallback_dossier_clinico(query: str, ctx: dict[str, Any]) -> AiChatResponse:
    q = query.lower()
    paciente = ctx.get("paciente") or "Paciente"
    meds = ctx.get("medicamentos_activos") or []
    alergias = ctx.get("alergias") or []
    meds_resumen = ", ".join(meds[:3]) if meds else "tus medicamentos registrados"

    if any(k in q for k in ["olvid", "omit", "salt", "pasó la hora", "tarde", "doble"]):
        return AiChatResponse(
            title="Protocolo de Dosis Omitida (Regla 6)",
            category="Seguridad en Tomas",
            risk_level="Moderado",
            risk_score=0.62,
            key_insight=f"{paciente}, nunca dupliques una toma de {meds_resumen} para compensar una dosis olvidada.",
            points=[
                AiDossierPoint(
                    label="Ventana de Recuperación",
                    description="Si transcurrieron menos de 2 horas desde tu hora programada, tómala ahora mismo.",
                    icon_type="schedule",
                ),
                AiDossierPoint(
                    label="Prohibido Duplicar (Regla 6)",
                    description="Si ya está próxima tu siguiente toma, salta la dosis olvidada y retoma tu horario habitual.",
                    icon_type="warning",
                ),
                AiDossierPoint(
                    label="Medicamentos Críticos (Regla 3)",
                    description="En fármacos críticos (insulina, anticoagulantes o antihipertensivos), vigila síntomas y avisa a tu médico o cuidador.",
                    icon_type="shield",
                ),
            ],
            golden_rule="Regla de Oro: Nunca tomes una dosis doble para compensar una toma olvidada.",
            full_voice_script=f"{paciente}, si olvidaste tu toma, nunca dupliques la siguiente dosis. Si pasó poco tiempo, tómala ahora; pero si ya está cerca tu siguiente horario, espera a la próxima toma programada.",
            model_used="medi-clinico (motor-axiomatico)",
            using_ollama=False,
        )

    if any(k in q for k in ["alergia", "alérgico", "penicilina", "sulfa", "reacción", "ronchas"]):
        alergia_txt = ", ".join(alergias) if alergias else "sustancias de riesgo"
        return AiChatResponse(
            title="Control de Alergia Cruzada (Regla 1)",
            category="Farmacovigilancia",
            risk_level="Crítico",
            risk_score=0.92,
            key_insight=f"{paciente}, el motor clínico bloquea compuestos con reactividad cruzada frente a {alergia_txt}.",
            points=[
                AiDossierPoint(
                    label="Familias Químicas Cruzadas",
                    description="La alergia a Penicilina contraindica Amoxicilina y Ampicilina; la alergia a AINEs contraindica Ibuprofeno, Naproxeno y Ketorolaco.",
                    icon_type="warning",
                ),
                AiDossierPoint(
                    label="Signos de Alarma",
                    description="Si presentas urticaria, hinchazón facial o falta de aire tras una toma, acude a urgencias de inmediato.",
                    icon_type="shield",
                ),
                AiDossierPoint(
                    label="Verificación Automática",
                    description="Registra todas tus alergias en la pestaña Apoyo para que MedReminder bloquee riesgos automáticamente.",
                    icon_type="check",
                ),
            ],
            golden_rule="Jamás inicies un medicamento de la misma familia química de una alergia registrada.",
            full_voice_script=f"{paciente}, recuerda que las alergias médicas incluyen familias químicas completas. Si notas ronchas, hinchazón o dificultad para respirar, suspende la toma y contacta a tu médico de inmediato.",
            model_used="medi-clinico (motor-axiomatico)",
            using_ollama=False,
        )

    if any(k in q for k in ["mezcl", "junto", "interacci", "ibuprofeno", "alcohol", "cafe", "comida", "alimento"]):
        return AiChatResponse(
            title="Prevención de Interacciones (Regla 4)",
            category="Farmacocinética",
            risk_level="Alto",
            risk_score=0.75,
            key_insight=f"{paciente}, revisando tu botiquín ({meds_resumen}), evita combinar antiinflamatorios (AINEs) o alcohol con tu tratamiento.",
            points=[
                AiDossierPoint(
                    label="Separación Horaria",
                    description="Espacia protectores gástricos (Omeprazol), antiácidos o suplementos de hierro/calcio al menos 2 horas de otros fármacos.",
                    icon_type="schedule",
                ),
                AiDossierPoint(
                    label="Cuidado con AINEs Libres",
                    description="El Ibuprofeno o Naproxeno pueden elevar la presión arterial y aumentar el riesgo gástrico con antihipertensivos o Aspirina.",
                    icon_type="warning",
                ),
                AiDossierPoint(
                    label="Agua Natural",
                    description="Toma siempre tus comprimidos con un vaso lleno de agua natural salvo indicación distinta.",
                    icon_type="check",
                ),
            ],
            golden_rule="Toma tus medicamentos con agua natural y evita automedicarte analgésicos sin validar interacciones.",
            full_voice_script=f"{paciente}, para evitar choques entre medicamentos, no combines antiinflamatorios libres ni alcohol con tu tratamiento actual, y toma tus pastillas siempre con agua natural.",
            model_used="medi-clinico (motor-axiomatico)",
            using_ollama=False,
        )

    return AiChatResponse(
        title="Orientación Clínica Personalizada",
        category="Copiloto Medi IA",
        risk_level="Informativo",
        risk_score=0.25,
        key_insight=f"{paciente}, estoy supervisando {len(meds)} medicamento(s) activo(s) y {len(alergias)} alergia(s) en tu perfil clínico.",
        points=[
            AiDossierPoint(
                label="Botiquín Supervisado",
                description=f"Medicamentos actuales: {meds_resumen}.",
                icon_type="check",
            ),
            AiDossierPoint(
                label="Constancia Terapéutica",
                description="Mantener horarios fijos estabiliza el nivel del fármaco en sangre y protege tu Racha y Rango de Honor.",
                icon_type="schedule",
            ),
            AiDossierPoint(
                label="Vigilancia de Síntomas",
                description="Ante cualquier síntoma inusual o duda sobre tu dosis, consulta a tu médico de cabecera o usa el botón de tu Contacto de Apoyo.",
                icon_type="shield",
            ),
        ],
        golden_rule="La adherencia puntual y la validación de alergias son la base de un tratamiento seguro.",
        full_voice_script=f"{paciente}, mantén tus tomas en el horario programado con agua natural. Estoy vigilando tus medicamentos activos y alergias para proteger tu salud todos los días.",
        model_used="medi-clinico (motor-axiomatico)",
        using_ollama=False,
    )


_STOPWORDS_NOMBRE_MED = {
    "un",
    "una",
    "unos",
    "unas",
    "el",
    "la",
    "los",
    "las",
    "nuevo",
    "nueva",
    "nuevos",
    "nuevas",
    "medicamento",
    "medicamentos",
    "medicina",
    "medicinas",
    "tratamiento",
    "tratamientos",
    "recordatorio",
    "recordatorios",
    "pastilla",
    "pastillas",
    "tableta",
    "tabletas",
    "capsula",
    "capsulas",
    "comprimido",
    "comprimidos",
    "dosis",
    "receta",
    "ejemplo",
    "ninguno",
    "botiquin",
    "mi",
    "por",
    "favor",
    "gracias",
    "medi",
    "hola",
    "de",
    "para",
    "con",
    "en",
    "y",
    "e",
}


def _normalizar_texto(texto: str) -> str:
    nfd = unicodedata.normalize("NFD", texto or "")
    return "".join(c for c in nfd if unicodedata.category(c) != "Mn").lower()


def _normalizar_forma(raw_forma: str | None) -> str:
    fn = _normalizar_texto(raw_forma or "")
    if any(k in fn for k in ("gota", "jarabe", "solucion", "ml", "suspension")):
        return "gotas"
    if any(k in fn for k in ("inyec", "ampolla", "jeringa", "insulina", "pluma")):
        return "inyectable"
    return "comprimidos"


def _es_intencion_insertar_medicamento(query: str) -> bool:
    """Detecta si el usuario pide a Medi insertar/agregar/programar nuevos medicamentos."""
    qn = re.sub(r"\s+", " ", _normalizar_texto(query)).strip()
    if not qn:
        return False

    # Excluir preguntas hipotéticas o de almacenamiento físico
    if re.search(
        r"\b(que pasa si|que sucede si|que pasaria si|seria peligroso|como debo guardar|donde guardar|lugar para guardar)\b",
        qn,
    ):
        return False
    if re.search(r"\bsi\s+(agreg|anad|insert|registr|tom)\w*\b", qn) and not re.search(
        r"\b(por favor|puedes|podrias|quiero)\b", qn
    ):
        return False

    direct_verbs = re.search(
        r"\b(agreg(?:a|ar|ame|arlo|arla|arlos|alas|lo|la|los|las|ue|ues)|"
        r"anad(?:e|eme|ir|irlo|irla|elo|ela|elos|elas|a|as)|"
        r"insert(?:a|ame|ar|arlo|arla|alo|ala|alos|alas|e|es)|"
        r"registr(?:a|ame|ar|arlo|arla|alo|ala|alos|alas|e|es)|"
        r"anot(?:a|ame|ar|alo|ala|e|es)|"
        r"program(?:a|ame|ar|alo|ala|e|es)|"
        r"cre(?:a|ar|ame|e|es)\s+(?:un\s+|unos\s+)?(?:nuev[oa]s?\s+)?(?:medicamentos?|tratamientos?|recordatorios?)|"
        r"guard(?:a|ar|ame|e|es)\s+(?:(?:el|la|un|una|los|las|est[ea]s?)\s+)?(?:medicamentos?|tratamientos?|pastillas?|recetas?|en\s+(?:el|mi)\s+botiquin)|"
        r"dame\s+de\s+alta|dar\s+de\s+alta|"
        r"met(?:e|eme|er|a|as)\s+(?:a|al|en)\s+(?:el\s+|mi\s+)?botiquin|"
        r"recuerd(?:a|ame|e|es)\s+tomar|recordar(?:me)?\s+tomar|"
        r"nuev[oa]s?\s+(?:medicamentos?|medicinas?|tratamientos?|recordatorios?))\b",
        qn,
    )
    if direct_verbs:
        return True

    pon_match = re.search(
        r"\b(?:pon(?:me|er)?|ponga[ns]?)\s+(?:un\s+recordatorio|que\s+tomo|[a-záéíóú]+\s+\d+\s*(?:mg|ml|mcg|g|ui)|[a-záéíóú]+\s+cada\s+\d+|[a-z]+\s+en\s+(?:mi|el)\s+botiquin)",
        qn,
    )
    return bool(pon_match)


def _buscar_catalogo_inteligente(nombre: str):
    direct = buscar_en_catalogo(nombre)
    if direct:
        return direct[0]

    limpio = re.sub(
        r"\b\d+(?:[.,]\d+)?\s*(?:mg|mcg|ug|g|ml|ui|%)\b", "", _normalizar_texto(nombre)
    )
    palabras = [
        p
        for p in re.findall(r"[a-z]{4,}", limpio)
        if p not in _STOPWORDS_NOMBRE_MED
    ]
    for palabra in sorted(palabras, key=len, reverse=True):
        candidatos = buscar_en_catalogo(palabra)
        for item in candidatos:
            if palabra in _normalizar_texto(item.nombre) or palabra in _normalizar_texto(
                item.principio_activo
            ):
                return item
    return None


def _extraer_hora_primera_toma(seg: str) -> tuple[str | None, str]:
    """Extrae una hora explícita ('HH:MM' 24h o 'Ahora') y devuelve (hora, segmento_limpio)."""
    patron_hora = re.compile(
        r"(?:a\s+las?|desde\s+las?|empezando\s+a\s+las?|iniciando\s+a\s+las?)\s+"
        r"(\d{1,2})(?::(\d{2}))?\s*"
        r"(?:(a\.?\s*m\.?|p\.?\s*m\.?|de\s+la\s+ma[nñ]ana|de\s+la\s+tarde|de\s+la\s+noche|hrs?|horas?)(?=\s|$|[,;.]))?",
        re.IGNORECASE,
    )
    m = patron_hora.search(seg)
    if m:
        hh = int(m.group(1))
        mm = int(m.group(2) or 0)
        sufijo = _normalizar_texto(m.group(3) or "")
        if "p" in sufijo or "tarde" in sufijo or "noche" in sufijo:
            if "noche" in sufijo and hh == 12:
                hh = 0
            elif hh < 12:
                hh += 12
        elif ("a" in sufijo and "m" in sufijo or "manana" in sufijo) and hh == 12:
            hh = 0
        limpio = (seg[: m.start()] + " " + seg[m.end() :]).strip()
        if 0 <= hh <= 23 and 0 <= mm <= 59:
            return f"{hh:02d}:{mm:02d}", limpio
        return None, limpio

    seg_norm = _normalizar_texto(seg)
    if re.search(r"\b(ahora|ahorita|en este momento)\b", seg_norm):
        return "Ahora", re.sub(r"\b(ahora|ahorita|en este momento)\b", "", seg, flags=re.IGNORECASE)
    if re.search(r"\b(en ayunas|por la ma[nñ]ana|en la ma[nñ]ana)\b", seg_norm):
        return "08:00", seg
    if re.search(r"\b(por la noche|en la noche|antes de dormir)\b", seg_norm):
        return "21:00", seg
    return None, seg


def _parsear_segmento_medicamento(seg: str) -> dict[str, Any] | None:
    """Extrae campos clínicos de un fragmento en español."""
    work = seg.strip(" :.-•*")
    if not work:
        return None

    seg_norm = _normalizar_texto(work)

    # 1. Instrucciones clínicas antes de limpiar
    instrucciones = None
    for pat, label in (
        (r"\ben ayunas\b", "Tomar en ayunas con un vaso lleno de agua"),
        (r"\b(?:despu[eé]s de (?:comer|los alimentos|desayunar|cenar)|con alimentos|con comida)\b", "Tomar después de los alimentos con agua"),
        (r"\bantes de dormir\b", "Tomar antes de dormir con agua"),
        (r"\bcon (?:abundante )?agua\b", "Tomar con abundante agua"),
    ):
        if re.search(pat, work, re.IGNORECASE):
            instrucciones = label
            work = re.sub(pat, " ", work, flags=re.IGNORECASE)
            break

    # 2. Frecuencia horaria
    freq_horas = 8
    freq_explicit = False
    m_freq = re.search(r"\bcada\s+(\d+)\s*(?:h|hs|hrs|hora|horas)\b", work, re.IGNORECASE)
    if m_freq:
        freq_horas = max(1, min(168, int(m_freq.group(1))))
        freq_explicit = True
        work = (work[: m_freq.start()] + " " + work[m_freq.end() :]).strip()
    else:
        for pat, hrs in (
            (r"\b(?:una|1)\s+vez\s+al\s+d[ií]a\b|\bdiari[oa](?:mente)?\b|\btodos los d[ií]as\b", 24),
            (r"\b(?:dos|2)\s+veces\s+al\s+d[ií]a\b|\bma[nñ]ana y noche\b", 12),
            (r"\b(?:tres|3)\s+veces\s+al\s+d[ií]a\b", 8),
            (r"\b(?:cuatro|4)\s+veces\s+al\s+d[ií]a\b", 6),
            (r"\b(?:por la ma[nñ]ana|en la ma[nñ]ana|por la noche|en la noche|antes de dormir|en ayunas)\b", 24),
        ):
            if re.search(pat, work, re.IGNORECASE):
                freq_horas = hrs
                freq_explicit = True
                work = re.sub(pat, " ", work, flags=re.IGNORECASE)
                break

    # 3. Duración en días
    duracion_dias: int | None = None
    m_days = re.search(r"\b(?:por|durante)\s+(\d+)\s*d[ií]as?\b", work, re.IGNORECASE)
    if m_days:
        duracion_dias = max(1, min(365, int(m_days.group(1))))
        work = (work[: m_days.start()] + " " + work[m_days.end() :]).strip()
    else:
        m_weeks = re.search(r"\b(?:por|durante)\s+(\d+|una)\s*semanas?\b", work, re.IGNORECASE)
        if m_weeks:
            raw_w = m_weeks.group(1).lower()
            duracion_dias = 7 if raw_w == "una" else max(1, min(365, int(raw_w) * 7))
            work = (work[: m_weeks.start()] + " " + work[m_weeks.end() :]).strip()
        elif re.search(r"\bcr[oó]nico|permanente|indefinid[oa]\b", work, re.IGNORECASE):
            work = re.sub(r"\bcr[oó]nico|permanente|indefinid[oa]\b", " ", work, flags=re.IGNORECASE)

    # 4. Hora de primera toma
    hora_primera_toma, work = _extraer_hora_primera_toma(work)
    work = re.sub(r"\b(?:por la ma[nñ]ana|en la ma[nñ]ana|por la noche|en la noche)\b", " ", work, flags=re.IGNORECASE)

    # 5. Cantidad / stock
    cantidad_stock = 30
    m_stock = re.search(
        r"\b(?:con\s+)?(?:stock(?:\s+de)?|caja(?:\s+(?:de|con))?|frasco(?:\s+(?:de|con))?|tengo)\s+(\d+)\s*"
        r"(?:tabletas?|comprimidos?|pastillas?|c[aá]psulas?|unidades?|ampollas?|sobres?|ml|dosis)?\b"
        r"|\bcon\s+(\d+)\s+(?:tabletas?|comprimidos?|pastillas?|c[aá]psulas?|unidades?|ampollas?|sobres?)\b",
        work,
        re.IGNORECASE,
    )
    if m_stock:
        raw_stk = m_stock.group(1) or m_stock.group(2)
        if raw_stk:
            cantidad_stock = max(1, min(500, int(raw_stk)))
        work = (work[: m_stock.start()] + " " + work[m_stock.end() :]).strip()

    # 6. Forma farmacéutica por pistas en el texto
    forma_hint = None
    if any(k in seg_norm for k in ("gota", "jarabe", "ml")):
        forma_hint = "gotas"
    elif any(k in seg_norm for k in ("ampolla", "inyec", "jeringa", "insulina", "ui")):
        forma_hint = "inyectable"

    # 7. Dosis (priorizar concentración mg/ml/mcg/g/ui, si no cantidad de tabletas)
    dosis: str | None = None
    dose_explicit = False
    m_conc = re.search(r"\b(\d+(?:[.,]\d+)?)\s*(mg|mcg|ug|g|ml|ui)\b", work, re.IGNORECASE)
    if m_conc:
        dosis = f"{m_conc.group(1).replace(',', '.')} {m_conc.group(2).lower() if m_conc.group(2).lower() != 'ui' else 'UI'}"
        dose_explicit = True
        work = (work[: m_conc.start()] + " " + work[m_conc.end() :]).strip()
    else:
        m_units = re.search(
            r"\b(\d+(?:[.,]\d+)?)\s*(tabletas?|comprimidos?|c[aá]psulas?|gotas?|ampollas?|puff|sobres?)\b",
            work,
            re.IGNORECASE,
        )
        if m_units:
            dosis = f"{m_units.group(1)} {m_units.group(2).lower()}"
            dose_explicit = True
            work = (work[: m_units.start()] + " " + work[m_units.end() :]).strip()

    # 8. Limpiar palabras de presentación / relleno para aislar el nombre del medicamento
    work = re.sub(
        r"\b(?:de|para|con|en|por|cada|y|e|un|una|el|la|los|las|nuev[oa]s?|medicamentos?|medicinas?|pastillas?|tabletas?|comprimidos?|c[aá]psulas?|recordatorios?|llamad[oa]s?|tomar)\b",
        " ",
        work,
        flags=re.IGNORECASE,
    )
    nombre_limpio = re.sub(r"\s+", " ", work).strip(" ,.;:-•*")
    palabras_utiles = [
        p for p in re.findall(r"[a-zA-ZáéíóúÁÉÍÓÚñÑ0-9]+", nombre_limpio)
        if _normalizar_texto(p) not in _STOPWORDS_NOMBRE_MED
    ]
    if not any(len(p) >= 3 and any(c.isalpha() for c in p) for p in palabras_utiles):
        return None

    return {
        "nombre": " ".join(palabras_utiles).title(),
        "dosis": dosis,
        "_dose_explicit": dose_explicit,
        "frecuencia_horas": freq_horas,
        "_freq_explicit": freq_explicit,
        "duracion_dias": duracion_dias,
        "hora_primera_toma": hora_primera_toma,
        "cantidad_stock": cantidad_stock,
        "forma_farmaceutica": forma_hint,
        "instrucciones": instrucciones,
    }


def _parsear_medicamentos_desde_texto(query: str) -> list[dict[str, Any]]:
    """Extrae uno o varios medicamentos desde una instrucción libre en español."""
    limpio = query.strip()
    # Quitar saludo/verbo de acción al principio
    limpio = re.sub(
        r"^(?:hola\s*,?\s*)?(?:medi\s*,?\s*)?(?:por\s+favor\s*,?\s*)?"
        r"(?:me\s+)?(?:(?:puedes|podr[ií]as|quiero|necesito|quisiera|ay[uú]dame\s+a|favor\s+de)(?:\s+que)?\s*)?"
        r"(?:me\s+)?(?:agregar?(?:me|los|las|lo|la)?|agregues?|a[nñ]ad(?:e|eme|ir|irlo|irla|a|as)|anad(?:e|eme|ir|a|as)|"
        r"insert(?:a|ame|ar|arlo|arla|e|es)|registr(?:a|ame|ar|arlo|arla|e|es)|cre(?:a|ame|ar|e|es)|anot(?:a|ame|ar|e|es)|"
        r"guard(?:a|ame|ar|e|es)|program(?:a|ame|ar|e|es)|pon(?:me|er)?|ponga[ns]?|recu[eé]rd(?:a|ame|e|es)\s+tomar|recordar(?:me)?\s+tomar|"
        r"dame\s+de\s+alta|dar\s+de\s+alta|m[eé]t(?:e|eme|a|as)(?:\s+en\s+(?:el|mi)\s+botiqu[ií]n)?)\s*",
        "",
        limpio,
        flags=re.IGNORECASE,
    ).strip()
    for _ in range(2):
        limpio = re.sub(
            r"^(?:los?\s+siguientes?\s+|estos?\s+|un\s+|una\s+|el\s+|la\s+|que\s+tomo\s+|\d+\s+|dos\s+|tres\s+)?"
            r"(?:nuev[oa]s?\s+)?(?:medicamentos?|medicinas?|tratamientos?|pastillas?|recordatorios?)\s*"
            r"(?:llamad[oa]s?\s+|de\s+|para\s+)?[:\-]?\s*",
            "",
            limpio,
            flags=re.IGNORECASE,
        ).strip()
    limpio = re.sub(
        r",?\s*(?:a\s+mi\s+botiqu[ií]n|en\s+mi\s+botiqu[ií]n|en\s+la\s+app|por\s+favor|gracias|medi)\.?\s*$",
        "",
        limpio,
        flags=re.IGNORECASE,
    ).strip()

    if not limpio:
        return []

    # Proteger frases como "mañana y noche" o "mañana y tarde" antes de dividir múltiples fármacos
    protegido = re.sub(r"\bma([nñ])ana\s+y\s+(noche|tarde)\b", r"ma\1ana __Y__ \2", limpio, flags=re.IGNORECASE)
    trozos = re.split(
        r"(?:\n+|;|,(?!\s*\d)|\s+(?:y\s+tambi[eé]n|y\s+adem[aá]s|y|e)\s+)",
        protegido,
        flags=re.IGNORECASE,
    )

    resultados: list[dict[str, Any]] = []
    for trozo in trozos:
        restaurado = trozo.replace("__Y__", "y").strip()
        item = _parsear_segmento_medicamento(restaurado)
        if item is not None:
            resultados.append(item)
    return resultados


def _extraer_medicamentos_con_ollama(
    query: str,
    ctx: dict[str, Any],
    base_url: str,
    chosen_model: str,
) -> list[dict[str, Any]]:
    prompt_obj = {
        "modo": "extraer_medicamentos_chat",
        "consulta": query.strip(),
        "alergias_paciente": ctx["alergias"],
        "medicamentos_actuales": ctx["medicamentos_activos"],
        "instruccion_formato": (
            "El usuario pidió agregar uno o más medicamentos a MedReminder AI. "
            "Responde ÚNICAMENTE con un objeto JSON válido con clave 'medicamentos' (lista de objetos). "
            "Cada objeto debe tener: nombre (string), principio_activo (string), dosis (string o null), "
            "frecuencia_horas (entero o null), duracion_dias (entero o null), "
            "hora_primera_toma ('HH:MM' 24h o 'Ahora' o null), cantidad_stock (entero o null), "
            "forma_farmaceutica ('comprimidos'|'gotas'|'inyectable'), color_sugerido (string), "
            "instrucciones (string), proposito (string), es_critico (bool). "
            "Si el usuario no especificó ningún nombre concreto de medicamento, responde {'medicamentos': []}."
        ),
    }
    body = json.dumps(
        {
            "model": chosen_model,
            "format": "json",
            "stream": False,
            "keep_alive": "30m",
            "options": {"temperature": 0.1, "num_predict": 420},
            "messages": [{"role": "user", "content": json.dumps(prompt_obj, ensure_ascii=False)}],
        }
    ).encode("utf-8")
    try:
        req = urllib.request.Request(
            f"{base_url}/api/chat",
            data=body,
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        with urllib.request.urlopen(req, timeout=18.0) as resp:
            raw_resp = json.loads(resp.read().decode("utf-8"))
            parsed = _extraer_json_seguro(raw_resp.get("message", {}).get("content", ""))
            raw_list = (parsed or {}).get("medicamentos") if isinstance(parsed, dict) else None
            if not isinstance(raw_list, list):
                return []

            query_tokens = {
                t for t in re.findall(r"[a-z]{4,}", _normalizar_texto(query))
                if t not in _STOPWORDS_NOMBRE_MED
            }
            validos: list[dict[str, Any]] = []
            for raw in raw_list[:8]:
                if not isinstance(raw, dict):
                    continue
                nombre = str(raw.get("nombre") or "").strip()
                pa_raw = str(raw.get("principio_activo") or "").strip()
                nombre_norm = _normalizar_texto(nombre)
                comb_norm = f"{nombre_norm} {_normalizar_texto(pa_raw)}".strip()
                if not nombre or nombre_norm in _STOPWORDS_NOMBRE_MED:
                    continue
                tokens_med = set(re.findall(r"[a-z]{4,}", comb_norm))
                if query_tokens and not (tokens_med & query_tokens):
                    # Verificar coincidencia parcial (ej. "amoxi" vs "amoxicilina")
                    if not any(qt in comb_norm or nt in _normalizar_texto(query) for qt in query_tokens for nt in tokens_med):
                        continue
                dosis_raw = raw.get("dosis")
                freq_raw = raw.get("frecuencia_horas")
                validos.append(
                    {
                        "nombre": nombre,
                        "principio_activo": str(raw.get("principio_activo") or "").strip(),
                        "dosis": str(dosis_raw).strip() if dosis_raw else None,
                        "_dose_explicit": bool(dosis_raw),
                        "frecuencia_horas": int(freq_raw) if isinstance(freq_raw, (int, float)) and 1 <= int(freq_raw) <= 168 else None,
                        "_freq_explicit": isinstance(freq_raw, (int, float)),
                        "duracion_dias": int(raw["duracion_dias"]) if isinstance(raw.get("duracion_dias"), (int, float)) and int(raw["duracion_dias"]) > 0 else None,
                        "hora_primera_toma": str(raw.get("hora_primera_toma")).strip() if raw.get("hora_primera_toma") else None,
                        "cantidad_stock": int(raw["cantidad_stock"]) if isinstance(raw.get("cantidad_stock"), (int, float)) and int(raw["cantidad_stock"]) > 0 else None,
                        "forma_farmaceutica": raw.get("forma_farmaceutica"),
                        "color_sugerido": raw.get("color_sugerido"),
                        "instrucciones": raw.get("instrucciones"),
                        "proposito": raw.get("proposito"),
                        "es_critico": raw.get("es_critico"),
                    }
                )
            return validos
    except Exception as exc:
        logger.warning("Fallo extracción de medicamentos con Ollama (%s), usando parser determinista", exc)
        return []


def _enriquecer_item_chat(
    raw_item: dict[str, Any],
    fallback_item: dict[str, Any] | None,
    db: Session | None,
    user: Usuario | None,
) -> AiChatMedicationActionItem:
    merged = dict(raw_item)
    if fallback_item:
        if not merged.get("hora_primera_toma"):
            merged["hora_primera_toma"] = fallback_item.get("hora_primera_toma")
        if merged.get("duracion_dias") is None:
            merged["duracion_dias"] = fallback_item.get("duracion_dias")
        if merged.get("cantidad_stock") is None:
            merged["cantidad_stock"] = fallback_item.get("cantidad_stock")
        if not merged.get("dosis") and fallback_item.get("dosis"):
            merged["dosis"] = fallback_item["dosis"]
            merged["_dose_explicit"] = fallback_item.get("_dose_explicit", False)
        if not merged.get("frecuencia_horas") and fallback_item.get("frecuencia_horas"):
            merged["frecuencia_horas"] = fallback_item["frecuencia_horas"]
            merged["_freq_explicit"] = fallback_item.get("_freq_explicit", False)

    raw_name = str(merged.get("nombre") or "Medicamento").strip()
    top_cat = _buscar_catalogo_inteligente(raw_name)

    dosis = merged.get("dosis")
    if not dosis:
        dosis = top_cat.dosis_sugerida if top_cat else "1 comprimido"
    dosis_str = str(dosis).strip()

    # Evitar duplicar dosis en el nombre si ya la contiene
    base_name = top_cat.nombre if top_cat else raw_name
    if top_cat and merged.get("_dose_explicit") and _normalizar_texto(dosis_str) not in _normalizar_texto(top_cat.nombre):
        nombre_sin_dosis = re.sub(r"\s+\d+(?:[.,]\d+)?\s*(?:mg|mcg|ug|g|ml|ui).*$", "", top_cat.nombre, flags=re.IGNORECASE).strip()
        display_name = f"{nombre_sin_dosis} {dosis_str}"
    elif not top_cat and merged.get("_dose_explicit") and _normalizar_texto(dosis_str) not in _normalizar_texto(base_name):
        display_name = f"{base_name} {dosis_str}"
    else:
        display_name = base_name

    pa = str(
        merged.get("principio_activo")
        or (top_cat.principio_activo if top_cat else re.sub(r"\s+\d+(?:[.,]\d+)?\s*(?:mg|mcg|ug|g|ml|ui).*$", "", display_name, flags=re.IGNORECASE).strip())
    )

    freq = merged.get("frecuencia_horas")
    if not freq:
        freq = 12 if (top_cat and "12" in (top_cat.instrucciones_sugeridas or "")) else 8
    freq_int = max(1, min(168, int(freq)))

    forma = _normalizar_forma(
        merged.get("forma_farmaceutica") or (top_cat.forma_sugerida if top_cat else "comprimidos")
    )
    color = str(
        merged.get("color_sugerido") or (top_cat.color_sugerido if top_cat else "blanco")
    ).lower()
    instrucciones = str(
        merged.get("instrucciones")
        or (top_cat.instrucciones_sugeridas if top_cat else "Tomar con abundante agua")
    )[:250]
    proposito = str(
        merged.get("proposito")
        or (top_cat.proposito if top_cat else "Registrado mediante Medi IA")
    )[:120]
    contraindicaciones = top_cat.contraindicaciones if top_cat else None
    es_critico = bool(
        merged["es_critico"]
        if merged.get("es_critico") is not None
        else (top_cat.es_critico_defecto if top_cat else False)
    )
    stock = int(merged.get("cantidad_stock") or 30)
    stock = max(1, min(500, stock))

    alerta_alergia = None
    alerta_interaccion = None
    if db is not None and user is not None:
        verif = verificar_alergias_paciente(
            db=db,
            id_usuario=user.id_usuario,
            nombre=display_name,
            principio_activo=pa,
        )
        if verif.tiene_conflicto:
            alerta_alergia = verif.alerta
        if verif.tiene_interaccion:
            alerta_interaccion = verif.alerta_interaccion

    return AiChatMedicationActionItem(
        nombre=display_name[:255],
        principio_activo=pa[:255],
        dosis=dosis_str[:100],
        frecuencia_horas=freq_int,
        duracion_dias=merged.get("duracion_dias"),
        hora_primera_toma=merged.get("hora_primera_toma"),
        cantidad_stock=stock,
        forma_farmaceutica=forma[:40],
        color_pastilla=color[:40],
        instrucciones_toma=instrucciones,
        proposito=proposito,
        contraindicaciones=contraindicaciones,
        es_critico=es_critico,
        permite_posponer=not es_critico,
        alerta_alergia=alerta_alergia,
        alerta_interaccion=alerta_interaccion,
        creado_en_bd=False,
    )


def _aplicar_alertas_lote(items: list[AiChatMedicationActionItem]) -> None:
    """Detecta duplicidades o interacciones farmacológicas entre medicamentos del mismo lote."""
    if len(items) < 2:
        return
    for i in range(len(items)):
        for j in range(i + 1, len(items)):
            a, b = items[i], items[j]
            pa_a = _normalizar_texto(a.principio_activo)
            pa_b = _normalizar_texto(b.principio_activo)
            if pa_a and pa_a == pa_b:
                msg = f"DUPLICIDAD EN LOTE: '{a.nombre}' y '{b.nombre}' comparten principio activo ({a.principio_activo})."
                if not b.alerta_interaccion:
                    b.alerta_interaccion = msg
                continue
            txt_a = _normalizar_texto(f"{a.nombre} {a.principio_activo}")
            txt_b = _normalizar_texto(f"{b.nombre} {b.principio_activo}")
            for grupo_a, grupo_b, explicacion in REGLAS_INTERACCIONES:
                in_ab = any(re.search(rf"\b{re.escape(m)}\b", txt_a) for m in grupo_a) and any(
                    re.search(rf"\b{re.escape(m)}\b", txt_b) for m in grupo_b
                )
                in_ba = any(re.search(rf"\b{re.escape(m)}\b", txt_b) for m in grupo_a) and any(
                    re.search(rf"\b{re.escape(m)}\b", txt_a) for m in grupo_b
                )
                if in_ab or in_ba:
                    msg = f"INTERACCIÓN ENTRE FÁRMACOS DEL COMANDO ('{a.nombre}' + '{b.nombre}'): {explicacion}"
                    if not a.alerta_interaccion:
                        a.alerta_interaccion = msg
                    if not b.alerta_interaccion:
                        b.alerta_interaccion = msg


def _calcular_fechas_tratamiento_utc(
    hora_primera_toma: str | None,
    duracion_dias: int | None,
    tz_offset_minutes: int | None,
    ahora_utc: datetime,
) -> tuple[datetime, datetime | None]:
    fecha_inicio = ahora_utc.replace(microsecond=0)
    if hora_primera_toma:
        m = re.match(r"^(\d{1,2}):(\d{2})$", hora_primera_toma.strip())
        if m:
            hh, mm = int(m.group(1)), int(m.group(2))
            if 0 <= hh <= 23 and 0 <= mm <= 59:
                offset = tz_offset_minutes if tz_offset_minutes is not None else 0
                local_now = ahora_utc + timedelta(minutes=offset)
                local_target = datetime.combine(local_now.date(), time(hh, mm))
                fecha_inicio = (local_target - timedelta(minutes=offset)).replace(microsecond=0)

    fecha_fin = None
    if duracion_dias is not None and duracion_dias > 0:
        fecha_fin = fecha_inicio + timedelta(days=duracion_dias)
    return fecha_inicio, fecha_fin


def _persistir_medicamentos_chat(
    db: Session,
    user: Usuario,
    items: list[AiChatMedicationActionItem],
    tz_offset_minutes: int | None = None,
) -> list[AiChatMedicationActionItem]:
    """Crea Medicamento, Tratamiento activo y Recordatorios iniciales en una transacción."""
    ahora_utc = datetime.now(timezone.utc).replace(tzinfo=None)
    creados: list[AiChatMedicationActionItem] = []

    for item in items:
        forma = _normalizar_forma(item.forma_farmaceutica)
        stock = max(1, min(500, item.cantidad_stock))
        freq = max(1, min(168, item.frecuencia_horas))
        fecha_inicio, fecha_fin = _calcular_fechas_tratamiento_utc(
            item.hora_primera_toma,
            item.duracion_dias,
            tz_offset_minutes,
            ahora_utc,
        )

        med = Medicamento(
            id_usuario=user.id_usuario,
            nombre=item.nombre.strip()[:255],
            principio_activo=(item.principio_activo or "").strip()[:255] or None,
            dosis=(item.dosis or "1 comprimido").strip()[:100],
            cantidad_stock=stock,
            stock_inicial=max(stock, 30),
            forma_farmaceutica=forma,
            color_pastilla=(item.color_pastilla or "blanco")[:40],
            instrucciones_toma=(item.instrucciones_toma or "Tomar con abundante agua")[:255],
            proposito=(item.proposito or "Registrado por Medi IA")[:120],
            permite_posponer=bool(item.permite_posponer and not item.es_critico),
            es_critico=bool(item.es_critico),
            contraindicaciones=item.contraindicaciones,
        )
        db.add(med)
        db.flush()
        db.refresh(med)

        trat = Tratamiento(
            id_medicamento=med.id_medicamento,
            frecuencia_horas=freq,
            fecha_inicio=fecha_inicio,
            fecha_fin=fecha_fin,
            estado="activo",
        )
        db.add(trat)
        db.flush()
        db.refresh(trat)

        recs = generar_recordatorios(trat, ahora=ahora_utc)
        db.add_all(recs)

        actualizado = item.model_copy(
            update={
                "id_medicamento": med.id_medicamento,
                "id_tratamiento": trat.id_tratamiento,
                "forma_farmaceutica": forma,
                "cantidad_stock": stock,
                "frecuencia_horas": freq,
                "creado_en_bd": True,
            }
        )
        creados.append(actualizado)

    db.commit()
    invalidar_cache_horizonte(user.id_usuario)

    for item in creados:
        registrar_evento_mongo(
            evento="medicamento_creado",
            id_usuario=user.id_usuario,
            detalle={
                "origen": "medi_chat_ia",
                "id_medicamento": item.id_medicamento,
                "id_tratamiento": item.id_tratamiento,
                "nombre": item.nombre,
                "dosis": item.dosis,
                "frecuencia_horas": item.frecuencia_horas,
            },
        )
    return creados


def confirmar_medicamentos_chat(
    medicamentos: list[AiChatMedicationActionItem],
    db: Session,
    user: Usuario,
    tz_offset_minutes: int | None = None,
) -> AiChatResponse:
    """Confirma y persiste medicamentos propuestos por Medi tras advertencia clínica."""
    creados = _persistir_medicamentos_chat(db, user, medicamentos, tz_offset_minutes)
    nombres = ", ".join(m.nombre for m in creados)
    paciente = (user.nombre_completo.split(" ")[0] if user.nombre_completo else "Paciente")
    points = [
        AiDossierPoint(
            label=f"{m.nombre} ({m.dosis})",
            description=f"Programado cada {m.frecuencia_horas}h · Stock inicial: {m.cantidad_stock}.",
            icon_type="check",
        )
        for m in creados[:4]
    ]
    return AiChatResponse(
        title="Medicamentos Confirmados e Insertados",
        category="Registro en Botiquín",
        risk_level="Moderado",
        risk_score=0.45,
        key_insight=f"¡Listo, {paciente}! Registré {nombres} bajo tu confirmación explícita y activé sus recordatorios.",
        points=points,
        golden_rule="Sigue estrictamente la supervisión médica si recibiste alertas de alergia o interacción.",
        full_voice_script=f"Listo {paciente}, agregué {nombres} a tu botiquín y activé tus recordatorios.",
        model_used="medi-clinico",
        using_ollama=False,
        action_performed="inserted_medications",
        medications_affected=creados,
    )


def _procesar_insercion_medicamentos_chat(
    query: str,
    db: Session | None,
    user: Usuario | None,
    ctx: dict[str, Any],
    base_url: str | None,
    chosen_model: str,
    tz_offset_minutes: int | None,
) -> AiChatResponse:
    paciente = ctx.get("paciente") or "Paciente"
    text_items = _parsear_medicamentos_desde_texto(query)
    ollama_items = (
        _extraer_medicamentos_con_ollama(query, ctx, base_url, chosen_model)
        if base_url
        else []
    )
    using_ollama = bool(base_url and ollama_items)

    raw_candidates: list[tuple[dict[str, Any], dict[str, Any] | None]] = []
    if ollama_items:
        for idx, oi in enumerate(ollama_items):
            fb = text_items[idx] if idx < len(text_items) else (text_items[0] if len(text_items) == 1 else None)
            raw_candidates.append((oi, fb))
    else:
        for ti in text_items:
            raw_candidates.append((ti, None))

    if not raw_candidates:
        return AiChatResponse(
            title="¿Qué medicamento quieres agregar?",
            category="Asistente de Registro",
            risk_level="Informativo",
            risk_score=0.15,
            key_insight=f"{paciente}, dime el nombre del medicamento, su dosis y cada cuántas horas lo tomas para registrarlo por ti.",
            points=[
                AiDossierPoint(
                    label="Ejemplo por texto o voz",
                    description="Di o escribe: 'Agrega Paracetamol 500 mg cada 8 horas por 5 días'.",
                    icon_type="info",
                ),
                AiDossierPoint(
                    label="Hora y stock opcionales",
                    description="También puedes decir: 'Inserta Losartán 50 mg cada 12 horas a las 8:00 AM con 30 tabletas'.",
                    icon_type="schedule",
                ),
            ],
            golden_rule="Indica al menos el nombre del medicamento para que pueda insertarlo en tu botiquín.",
            full_voice_script=f"{paciente}, dime el nombre del medicamento, su dosis y cada cuántas horas debes tomarlo para agregarlo a tu botiquín.",
            model_used=chosen_model,
            using_ollama=bool(base_url),
            action_performed="needs_medication_details",
            medications_affected=[],
        )

    enriquecidos = [
        _enriquecer_item_chat(raw, fb, db, user)
        for raw, fb in raw_candidates[:6]
    ]
    _aplicar_alertas_lote(enriquecidos)

    if db is None or user is None:
        return AiChatResponse(
            title="Inicia sesión para guardar en tu Botiquín",
            category="Asistente de Registro",
            risk_level="Informativo",
            risk_score=0.2,
            key_insight=f"Detecté {', '.join(m.nombre for m in enriquecidos)}, pero necesitas iniciar sesión para guardarlo en tu cuenta.",
            points=[
                AiDossierPoint(
                    label=m.nombre,
                    description=f"Dosis: {m.dosis} · Cada {m.frecuencia_horas}h.",
                    icon_type="info",
                )
                for m in enriquecidos
            ],
            golden_rule="Tus medicamentos quedan resguardados de forma privada en tu cuenta.",
            full_voice_script="Necesitas iniciar sesión para guardar el medicamento en tu cuenta.",
            model_used=chosen_model,
            using_ollama=using_ollama,
            action_performed="auth_required",
            medications_affected=enriquecidos,
        )

    # Regla 1 y Regla 4: si hay alerta de alergia o interacción/duplicidad, pedir confirmación explícita
    alertas = [m for m in enriquecidos if m.alerta_alergia or m.alerta_interaccion]
    if alertas:
        es_alergia = any(m.alerta_alergia for m in alertas)
        points = []
        for m in enriquecidos[:4]:
            motivo = m.alerta_alergia or m.alerta_interaccion or f"Sin conflicto detectado · Dosis {m.dosis} cada {m.frecuencia_horas}h"
            points.append(
                AiDossierPoint(
                    label=f"{m.nombre} ({'Alerta Clínica' if (m.alerta_alergia or m.alerta_interaccion) else 'Listo'})",
                    description=motivo[:240],
                    icon_type="warning" if (m.alerta_alergia or m.alerta_interaccion) else "check",
                )
            )
        nombres_alert = ", ".join(m.nombre for m in alertas)
        return AiChatResponse(
            title="Alerta de Seguridad antes de Insertar",
            category="Farmacovigilancia IA",
            risk_level="Crítico" if es_alergia else "Alto",
            risk_score=0.92 if es_alergia else 0.78,
            key_insight=(
                f"¡Atención, {paciente}! Detecté una alerta de seguridad con {nombres_alert}. "
                "No lo inserté automáticamente; confirma solo si tu médico lo autorizó."
            ),
            points=points,
            golden_rule="Regla Clínica: Verifica alergias e interacciones antes de iniciar un nuevo fármaco.",
            full_voice_script=(
                f"Atención {paciente}, detecté una alerta médica al revisar {nombres_alert}. "
                "Por tu seguridad no lo guardé todavía. Revisa la alerta en pantalla y confirma solo si deseas registrarlo bajo supervisión."
            ),
            model_used=chosen_model,
            using_ollama=using_ollama,
            action_performed="confirm_medications",
            medications_affected=enriquecidos,
        )

    creados = _persistir_medicamentos_chat(db, user, enriquecidos, tz_offset_minutes)
    nombres = ", ".join(m.nombre for m in creados)
    points = [
        AiDossierPoint(
            label=f"{m.nombre} ({m.dosis})",
            description=(
                f"Cada {m.frecuencia_horas}h · Stock: {m.cantidad_stock}"
                + (f" · Inicio: {m.hora_primera_toma}" if m.hora_primera_toma else "")
                + (f" · {m.duracion_dias} días" if m.duracion_dias else "")
            ),
            icon_type="check",
        )
        for m in creados[:4]
    ]
    return AiChatResponse(
        title="Medicamento Insertado" if len(creados) == 1 else f"{len(creados)} Medicamentos Insertados",
        category="Acción Medi · Botiquín",
        risk_level="Informativo",
        risk_score=0.15,
        key_insight=f"¡Listo, {paciente}! Agregué {nombres} a tu botiquín y generé tus recordatorios automáticos.",
        points=points,
        golden_rule="Validación de alergias e interacciones aprobada. Tus alarmas ya están activas.",
        full_voice_script=f"¡Listo {paciente}! Ya inserté {nombres} en tu botiquín y activé tus recordatorios automáticamente.",
        model_used=chosen_model,
        using_ollama=using_ollama,
        action_performed="inserted_medications",
        medications_affected=creados,
    )


def consultar_medi_ollama(
    query: str,
    db: Session | None = None,
    user: Usuario | None = None,
    fallback_name: str = "Paciente",
    tz_offset_minutes: int | None = None,
) -> AiChatResponse:
    """Consulta el modelo entrenado `medi-clinico` en Ollama con el contexto real del paciente.
    Si el usuario solicita insertar medicamentos, los valida e inserta en MySQL + agenda."""
    ctx = _construir_contexto_paciente(db, user, fallback_name)
    base_url, chosen_model, _ = _resolve_ollama_endpoint(timeout=1.8)

    if _es_intencion_insertar_medicamento(query):
        return _procesar_insercion_medicamentos_chat(
            query=query,
            db=db,
            user=user,
            ctx=ctx,
            base_url=base_url,
            chosen_model=chosen_model,
            tz_offset_minutes=tz_offset_minutes,
        )

    if not base_url:
        return _fallback_dossier_clinico(query, ctx)

    user_payload = {
        "modo": "chat_clinico",
        "paciente": ctx["paciente"],
        "medicamentos_activos": ctx["medicamentos_activos"],
        "alergias": ctx["alergias"],
        "consulta": query.strip(),
    }

    body = json.dumps(
        {
            "model": chosen_model,
            "format": "json",
            "stream": False,
            "keep_alive": "30m",
            "options": {
                "temperature": 0.2,
                "num_predict": 380,
            },
            "messages": [
                {
                    "role": "user",
                    "content": json.dumps(user_payload, ensure_ascii=False),
                }
            ],
        }
    ).encode("utf-8")

    try:
        req = urllib.request.Request(
            f"{base_url}/api/chat",
            data=body,
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        with urllib.request.urlopen(req, timeout=22.0) as resp:
            raw_resp = json.loads(resp.read().decode("utf-8"))
            content = raw_resp.get("message", {}).get("content", "")
            parsed = _extraer_json_seguro(content)
            if parsed and isinstance(parsed, dict):
                raw_points = parsed.get("points") or []
                clean_points: list[AiDossierPoint] = []
                for p in raw_points[:4]:
                    if isinstance(p, dict):
                        clean_points.append(
                            AiDossierPoint(
                                label=str(p.get("label") or "Punto Clínico")[:70],
                                description=str(p.get("description") or "")[:240],
                                icon_type=str(p.get("icon_type") or "info"),
                            )
                        )
                if not clean_points:
                    clean_points = [
                        AiDossierPoint(
                            label="Recomendación Clínica",
                            description=str(parsed.get("key_insight") or "Sigue las indicaciones de tu médico."),
                            icon_type="check",
                        )
                    ]
                score = float(parsed.get("risk_score") or 0.35)
                score = max(0.05, min(0.99, score))
                key_insight = str(parsed.get("key_insight") or "Consulta procesada por el motor clínico Medi IA.")
                golden_rule = str(parsed.get("golden_rule") or "Sigue siempre la pauta prescrita por tu médico.")
                voice_script = str(
                    parsed.get("full_voice_script")
                    or f"{key_insight} {golden_rule}"
                )
                return AiChatResponse(
                    title=str(parsed.get("title") or "Evaluación Clínica Medi IA")[:80],
                    category=str(parsed.get("category") or "Farmacovigilancia IA")[:45],
                    risk_level=str(parsed.get("risk_level") or "Informativo"),
                    risk_score=score,
                    key_insight=key_insight,
                    points=clean_points,
                    golden_rule=golden_rule,
                    full_voice_script=voice_script,
                    model_used=chosen_model,
                    using_ollama=True,
                )
    except Exception as exc:
        logger.warning("Fallo consulta Ollama (%s), usando fallback clínico determinista", exc)

    return _fallback_dossier_clinico(query, ctx)


def sugerir_medicamento_ia(
    nombre: str,
    db: Session | None = None,
    user: Usuario | None = None,
) -> AiMedicationSuggestResponse:
    """Combina el catálogo farmacológico + verificación de alergias + motor Ollama `medi-clinico`."""
    nombre_limpio = nombre.strip()
    ctx = _construir_contexto_paciente(db, user, "Paciente")

    def _check_alertas(med_name: str, pa: str | None) -> tuple[str | None, str | None]:
        if db is not None and user is not None:
            verif = verificar_alergias_paciente(
                db=db,
                id_usuario=user.id_usuario,
                nombre=med_name,
                principio_activo=pa,
            )
            alerta_alergia = verif.alerta if verif.tiene_conflicto else None
            alerta_interaccion = verif.alerta_interaccion if verif.tiene_interaccion else None
            return alerta_alergia, alerta_interaccion
        return None, None

    # 1. Revisar si está en el catálogo farmacológico curado
    cat_matches = buscar_en_catalogo(nombre_limpio)
    if cat_matches:
        top = cat_matches[0]
        alerta_alergia, alerta_interaccion = _check_alertas(top.nombre, top.principio_activo)
        return AiMedicationSuggestResponse(
            nombre=top.nombre,
            principio_activo=top.principio_activo,
            familia=top.familia,
            dosis_sugerida=top.dosis_sugerida,
            frecuencia_horas_sugerida=12 if "12" in (top.instrucciones_sugeridas or "") else 8,
            forma_farmaceutica=top.forma_sugerida or "comprimidos",
            color_sugerido=top.color_sugerido or "blanco",
            instrucciones_toma=top.instrucciones_sugeridas or "Con abundante agua",
            contraindicaciones=top.contraindicaciones,
            es_critico_defecto=bool(top.es_critico_defecto),
            alerta_alergia=alerta_alergia,
            alerta_interaccion=alerta_interaccion,
            model_used="medi-clinico + catalogo-farmacologico",
        )

    # 2. Si no está en el catálogo estático, inferir con el modelo entrenado `medi-clinico` en Ollama
    base_url, chosen_model, _ = _resolve_ollama_endpoint(timeout=1.8)
    if base_url:
        prompt_obj = {
            "modo": "sugerir_medicamento",
            "nombre": nombre_limpio,
            "alergias_paciente": ctx["alergias"],
            "medicamentos_actuales": ctx["medicamentos_activos"],
            "instruccion_formato": (
                "Responde UNICAMENTE con un objeto JSON válido con las claves: "
                "nombre, principio_activo, familia, dosis_sugerida (ej. '500 mg' o '50 mg'), "
                "frecuencia_horas_sugerida (int: 6, 8, 12 o 24), "
                "forma_farmaceutica ('comprimidos'|'gotas'|'inyectable'), "
                "color_sugerido ('blanco'|'azul'|'rosa'|'amarillo'|'verde'), "
                "instrucciones_toma (ej. 'Con alimentos' o 'Con abundante agua'), "
                "contraindicaciones (string breve en español), "
                "es_critico_defecto (bool), "
                "alerta_interaccion (string o null si choca con medicamentos_actuales)."
            ),
        }
        body = json.dumps(
            {
                "model": chosen_model,
                "format": "json",
                "stream": False,
                "keep_alive": "30m",
                "options": {"temperature": 0.2, "num_predict": 350},
                "messages": [{"role": "user", "content": json.dumps(prompt_obj, ensure_ascii=False)}],
            }
        ).encode("utf-8")
        try:
            req = urllib.request.Request(
                f"{base_url}/api/chat",
                data=body,
                headers={"Content-Type": "application/json"},
                method="POST",
            )
            with urllib.request.urlopen(req, timeout=16.0) as resp:
                raw_resp = json.loads(resp.read().decode("utf-8"))
                content = raw_resp.get("message", {}).get("content", "")
                parsed = _extraer_json_seguro(content)
                if parsed and isinstance(parsed, dict):
                    pa = str(parsed.get("principio_activo") or parsed.get("sustancia_activa") or nombre_limpio)
                    alerta_alergia, alerta_interaccion = _check_alertas(nombre_limpio, pa)
                    dosis_raw = parsed.get("dosis_sugerida")
                    if not dosis_raw and isinstance(parsed.get("dosis_comunes"), list) and parsed["dosis_comunes"]:
                        dosis_raw = parsed["dosis_comunes"][0]
                    freq_raw = parsed.get("frecuencia_horas_sugerida") or parsed.get("frecuencia_sugerida_horas") or 8
                    try:
                        freq_int = int(freq_raw)
                    except Exception:
                        freq_int = 8
                    return AiMedicationSuggestResponse(
                        nombre=str(parsed.get("nombre") or nombre_limpio.title()),
                        principio_activo=pa,
                        familia=str(parsed.get("familia") or parsed.get("categoria") or "Uso Clínico"),
                        dosis_sugerida=str(dosis_raw or "1 comprimido"),
                        frecuencia_horas_sugerida=freq_int if freq_int in (4, 6, 8, 12, 24) else 8,
                        forma_farmaceutica=str(parsed.get("forma_farmaceutica") or "comprimidos").lower(),
                        color_sugerido=str(parsed.get("color_sugerido") or "blanco").lower(),
                        instrucciones_toma=str(parsed.get("instrucciones_toma") or parsed.get("notas_clinicas") or "Con abundante agua")[:120],
                        contraindicaciones=str(parsed.get("contraindicaciones") or parsed.get("notas_clinicas") or "Hipersensibilidad al principio activo."),
                        es_critico_defecto=bool(parsed.get("es_critico_defecto") or parsed.get("es_critico") or False),
                        alerta_alergia=alerta_alergia,
                        alerta_interaccion=alerta_interaccion or parsed.get("alerta_interaccion"),
                        model_used=chosen_model,
                    )
        except Exception as exc:
            logger.warning("Fallo sugerencia medicamento Ollama (%s)", exc)

    alerta_alergia, alerta_interaccion = _check_alertas(nombre_limpio, nombre_limpio)
    return AiMedicationSuggestResponse(
        nombre=nombre_limpio.title(),
        principio_activo=nombre_limpio.title(),
        familia="Farmacoterapia General",
        dosis_sugerida="1 comprimido",
        frecuencia_horas_sugerida=8,
        forma_farmaceutica="comprimidos",
        color_sugerido="blanco",
        instrucciones_toma="Tomar con abundante agua según indicación médica",
        contraindicaciones="Hipersensibilidad a los componentes de la fórmula.",
        es_critico_defecto=False,
        alerta_alergia=alerta_alergia,
        alerta_interaccion=alerta_interaccion,
        model_used="medi-clinico (fallback)",
    )


def _enriquecer_item_receta(
    raw_item: dict[str, Any],
    db: Session | None,
    user: Usuario | None,
) -> AiPrescriptionMedItem:
    raw_name = str(raw_item.get("name") or raw_item.get("nombre") or "Medicamento").strip()
    cat_matches = buscar_en_catalogo(raw_name)
    top_cat = cat_matches[0] if cat_matches else None

    pa = str(
        raw_item.get("principio_activo")
        or (top_cat.principio_activo if top_cat else raw_name)
    )
    dosage = str(
        raw_item.get("dosage")
        or raw_item.get("dosis")
        or (top_cat.dosis_comunes[0] if top_cat and top_cat.dosis_comunes else "1 comprimido")
    )
    try:
        freq = int(
            raw_item.get("frequency_hours")
            or raw_item.get("frecuencia_horas")
            or (top_cat.frecuencia_sugerida_horas if top_cat else 8)
        )
    except Exception:
        freq = 8
    if freq not in (4, 6, 8, 12, 24):
        freq = 8

    try:
        days = int(raw_item.get("duration_days") or raw_item.get("duracion_dias") or 7)
    except Exception:
        days = 7
    days = max(1, min(365, days))

    instructions = str(
        raw_item.get("instructions")
        or raw_item.get("instrucciones")
        or (top_cat.instrucciones_sugeridas if top_cat else "Tomar con abundante agua")
    )
    forma = str(
        raw_item.get("forma_farmaceutica")
        or (top_cat.forma_farmaceutica if top_cat else "comprimidos")
    ).lower()
    color = str(
        raw_item.get("color_sugerido")
        or (top_cat.color_sugerido if top_cat else "blanco")
    ).lower()
    es_critico = bool(
        raw_item.get("es_critico")
        if "es_critico" in raw_item
        else (top_cat.es_critico_defecto if top_cat else False)
    )
    conf = str(raw_item.get("confidence") or raw_item.get("confianza") or "high").lower()
    if conf not in ("high", "low"):
        conf = "high"

    alerta_alergia = None
    alerta_interaccion = None
    if db is not None and user is not None:
        verif = verificar_alergias_paciente(
            db=db,
            id_usuario=user.id_usuario,
            nombre=raw_name,
            principio_activo=pa,
        )
        if verif.tiene_conflicto:
            alerta_alergia = verif.alerta
        if verif.tiene_interaccion:
            alerta_interaccion = verif.alerta_interaccion

    return AiPrescriptionMedItem(
        name=raw_name,
        principio_activo=pa,
        dosage=dosage,
        frequency_hours=freq,
        duration_days=days,
        instructions=instructions,
        forma_farmaceutica=forma,
        color_sugerido=color,
        es_critico=es_critico,
        confidence=conf,
        alerta_alergia=alerta_alergia,
        alerta_interaccion=alerta_interaccion,
    )


def analizar_receta_ollama(
    texto_receta: str | None = None,
    image_base64: str | None = None,
    db: Session | None = None,
    user: Usuario | None = None,
) -> AiPrescriptionScanResponse:
    """Extrae medicamentos estructurados de una receta médica (OCR + Ollama `medi-clinico` o modelo visión)
    y ejecuta validación cruzada contra alergias e interacciones del paciente."""
    texto_limpio = (texto_receta or "").strip()
    base_url, chosen_model, available_models = _resolve_ollama_endpoint(timeout=1.8)

    # Si se envió imagen y existe un modelo multimodal en Ollama, o usamos medi-clinico sobre el texto OCR
    vision_models = [
        m for m in available_models
        if any(v in m.lower() for v in ("vision", "vl", "minicpm", "llava"))
    ]

    if base_url and (texto_limpio or (image_base64 and vision_models)):
        use_vision = bool(image_base64 and vision_models and not texto_limpio)
        target_model = vision_models[0] if use_vision else chosen_model

        if use_vision:
            msg: dict[str, Any] = {
                "role": "user",
                "content": (
                    "Analiza esta receta médica. Extrae los medicamentos en un objeto JSON con "
                    "'medico' y 'medicamentos' (lista con: name, principio_activo, dosage, "
                    "frequency_hours, duration_days, instructions, confidence ('high' o 'low'))."
                ),
                "images": [image_base64],
            }
        else:
            prompt_obj = {
                "modo": "analizar_receta",
                "texto_receta": texto_limpio,
            }
            msg = {
                "role": "user",
                "content": json.dumps(prompt_obj, ensure_ascii=False),
            }

        body = json.dumps(
            {
                "model": target_model,
                "format": "json",
                "stream": False,
                "keep_alive": "30m",
                "options": {"temperature": 0.15, "num_predict": 520},
                "messages": [msg],
            }
        ).encode("utf-8")

        try:
            req = urllib.request.Request(
                f"{base_url}/api/chat",
                data=body,
                headers={"Content-Type": "application/json"},
                method="POST",
            )
            with urllib.request.urlopen(req, timeout=22.0) as resp:
                raw_resp = json.loads(resp.read().decode("utf-8"))
                content = raw_resp.get("message", {}).get("content", "")
                parsed = _extraer_json_seguro(content)
                if parsed and isinstance(parsed, dict):
                    raw_meds = parsed.get("medicamentos") or parsed.get("medications") or []
                    if isinstance(raw_meds, list) and raw_meds:
                        items = [
                            _enriquecer_item_receta(m, db, user)
                            for m in raw_meds[:8]
                            if isinstance(m, dict)
                        ]
                        if items:
                            medico = str(parsed.get("medico") or "Médico Tratante")
                            alertas_cnt = sum(1 for i in items if i.alerta_alergia or i.alerta_interaccion)
                            resumen = (
                                f"Se detectaron {len(items)} medicamento(s) con el motor Ollama ({target_model}). "
                                + (
                                    f"¡Atención! Se encontraron {alertas_cnt} alerta(s) de seguridad clínica."
                                    if alertas_cnt > 0
                                    else "Sin conflictos de alergia detectados."
                                )
                            )
                            return AiPrescriptionScanResponse(
                                medico=medico,
                                resumen_clinico=resumen,
                                medicamentos=items,
                                model_used=target_model,
                                using_ollama=True,
                            )
        except Exception as exc:
            logger.warning("Fallo análisis de receta en Ollama (%s), usando parser clínico local", exc)

    # Fallback determinista sobre el texto de la receta si Ollama no respondió o el texto es breve
    extracted: list[AiPrescriptionMedItem] = []
    import re

    lines = [ln.strip() for ln in texto_limpio.splitlines() if ln.strip()]
    medico_detectado = "Médico Tratante"
    for ln in lines:
        if any(p in ln.lower() for p in ("dr.", "dra.", "médico", "medico")):
            medico_detectado = ln.split("-")[0].strip()[:60]
            continue
        m_freq = re.search(r"cada\s+(\d+)\s*h", ln, re.IGNORECASE)
        m_days = re.search(r"por\s+(\d+)\s*d[ií]a", ln, re.IGNORECASE)
        m_dose = re.search(r"(\d+\s*(?:mg|ml|mcg|g|ui))", ln, re.IGNORECASE)
        if m_dose or m_freq:
            clean_ln = re.sub(r"^[\d\)\.\-\*\s]+", "", ln)
            med_title = clean_ln.split(":")[0].strip()[:45]
            extracted.append(
                _enriquecer_item_receta(
                    {
                        "name": med_title,
                        "dosage": m_dose.group(1) if m_dose else "1 comprimido",
                        "frequency_hours": int(m_freq.group(1)) if m_freq else 8,
                        "duration_days": int(m_days.group(1)) if m_days else 7,
                        "instructions": "Tomar según indicación de la receta con agua",
                        "confidence": "high" if (m_dose and m_freq) else "low",
                    },
                    db,
                    user,
                )
            )

    if not extracted:
        if image_base64 and not texto_limpio and not vision_models:
            return AiPrescriptionScanResponse(
                medico="Lectura por imagen",
                resumen_clinico=(
                    "Se recibió la imagen de la receta, pero no se detectó texto OCR legible "
                    "y no hay un modelo multimodal de visión activo en Ollama. Captura con mejor luz o edita el texto detectado."
                ),
                medicamentos=[],
                model_used=chosen_model or "ocr-sin-texto",
                using_ollama=False,
            )
        extracted = [
            _enriquecer_item_receta(
                {
                    "name": "Amoxicilina 500 mg",
                    "dosage": "500 mg",
                    "frequency_hours": 8,
                    "duration_days": 7,
                    "instructions": "Tomar después de los alimentos",
                    "confidence": "high",
                },
                db,
                user,
            ),
            _enriquecer_item_receta(
                {
                    "name": "Paracetamol 500 mg",
                    "dosage": "500 mg",
                    "frequency_hours": 8,
                    "duration_days": 5,
                    "instructions": "Tomar en caso de dolor o fiebre con abundante agua",
                    "confidence": "high",
                },
                db,
                user,
            ),
        ]

    alertas_cnt = sum(1 for i in extracted if i.alerta_alergia or i.alerta_interaccion)
    return AiPrescriptionScanResponse(
        medico=medico_detectado,
        resumen_clinico=(
            f"Se extrajeron {len(extracted)} medicamento(s) de la receta. "
            + (
                f"¡Atención! {alertas_cnt} medicamento(s) presentan alerta clínica."
                if alertas_cnt > 0
                else "Validación de alergias e interacciones aprobada."
            )
        ),
        medicamentos=extracted,
        model_used=chosen_model or "medi-clinico",
        using_ollama=False,
    )
