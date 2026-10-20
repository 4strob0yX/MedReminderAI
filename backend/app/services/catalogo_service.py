import re
import unicodedata

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.mongo import registrar_evento_mongo
from app.models.alergia import AlergiaUsuario
from app.models.medicamento import Medicamento
from app.schemas.medicamento import MedicamentoCatalogoItem, VerificarAlergiasOut

# Catálogo precargado de medicamentos comunes para autocompletado y validación clínica
CATALOGO_CLINICO: list[MedicamentoCatalogoItem] = [
    MedicamentoCatalogoItem(
        nombre="Paracetamol 500 mg",
        principio_activo="Paracetamol",
        familia="Analgésicos y antipiréticos",
        dosis_sugerida="500 mg",
        forma_farmaceutica="Comprimidos / Cápsulas",
        forma_sugerida="comprimidos",
        color_sugerido="blanco",
        instrucciones_sugeridas="Tomar con un vaso lleno de agua. Puede tomarse con o sin alimentos.",
        proposito="Alivio de dolor leve a moderado y fiebre",
        contraindicaciones="Hipersensibilidad al paracetamol, insuficiencia hepática grave o hepatitis activa.",
        es_critico_defecto=False,
    ),
    MedicamentoCatalogoItem(
        nombre="Ibuprofeno 400 mg",
        principio_activo="Ibuprofeno",
        familia="AINEs",
        dosis_sugerida="400 mg",
        forma_farmaceutica="Comprimidos / Cápsulas",
        forma_sugerida="comprimidos",
        color_sugerido="naranja",
        instrucciones_sugeridas="Tomar siempre con alimentos o leche para proteger el estómago.",
        proposito="Desinflamatorio y alivio de dolor muscular o articular",
        contraindicaciones="Alergia a AINEs o aspirina, úlcera gastroduodenal activa, insuficiencia renal o cardíaca severa.",
        es_critico_defecto=False,
    ),
    MedicamentoCatalogoItem(
        nombre="Ibuprofeno 600 mg",
        principio_activo="Ibuprofeno",
        familia="AINEs",
        dosis_sugerida="600 mg",
        forma_farmaceutica="Comprimidos / Cápsulas",
        forma_sugerida="comprimidos",
        color_sugerido="rosa",
        instrucciones_sugeridas="Tomar inmediatamente después de comer con abundante agua.",
        proposito="Inflamación aguda y dolor moderado",
        contraindicaciones="Alergia a AINEs o aspirina, úlcera péptica activa, hemorragia gastrointestinal.",
        es_critico_defecto=False,
    ),
    MedicamentoCatalogoItem(
        nombre="Amoxicilina 500 mg",
        principio_activo="Amoxicilina",
        familia="Penicilinas / Betalactámicos",
        dosis_sugerida="500 mg",
        forma_farmaceutica="Comprimidos / Cápsulas",
        forma_sugerida="capsulas",
        color_sugerido="rojo_blanco",
        instrucciones_sugeridas="Completar todo el ciclo antibiótico a la hora exacta aunque se sienta mejor.",
        proposito="Infección bacteriana (Antibiótico)",
        contraindicaciones="Alergia a penicilinas, cefalosporinas o betalactámicos. Antecedente de ictericia.",
        es_critico_defecto=True,
    ),
    MedicamentoCatalogoItem(
        nombre="Amoxicilina con Ácido Clavulánico 875/125 mg",
        principio_activo="Amoxicilina / Clavulanato",
        familia="Penicilinas / Betalactámicos",
        dosis_sugerida="875 mg",
        forma_farmaceutica="Comprimidos / Cápsulas",
        forma_sugerida="comprimidos",
        color_sugerido="blanco",
        instrucciones_sugeridas="Tomar al inicio de una comida para reducir molestias gastrointestinales.",
        proposito="Infección bacteriana respiratoria o dental",
        contraindicaciones="Hipersensibilidad a betalactámicos o penicilinas. Disfunción hepática previa por amoxicilina.",
        es_critico_defecto=True,
    ),
    MedicamentoCatalogoItem(
        nombre="Aspirina 100 mg (Ácido Acetilsalicílico)",
        principio_activo="Ácido Acetilsalicílico",
        familia="AINEs / Antiagregantes",
        dosis_sugerida="100 mg",
        forma_farmaceutica="Comprimidos / Cápsulas",
        forma_sugerida="comprimidos",
        color_sugerido="blanco",
        instrucciones_sugeridas="Tomar después de los alimentos con un vaso de agua.",
        proposito="Prevención cardiovascular / Antiagregante",
        contraindicaciones="Alergia a salicilatos o AINEs, diátesis hemorrágica, úlcera gástrica activa.",
        es_critico_defecto=True,
    ),
    MedicamentoCatalogoItem(
        nombre="Omeprazol 20 mg",
        principio_activo="Omeprazol",
        familia="Inhibidores de la bomba de protones",
        dosis_sugerida="20 mg",
        forma_farmaceutica="Comprimidos / Cápsulas",
        forma_sugerida="capsulas",
        color_sugerido="morado",
        instrucciones_sugeridas="Tomar en ayunas 30 minutos antes del desayuno sin masticar la cápsula.",
        proposito="Protector gástrico y control de reflujo",
        contraindicaciones="Hipersensibilidad a omeprazol o benzimidazoles. Coadministración con nelfinavir.",
        es_critico_defecto=False,
    ),
    MedicamentoCatalogoItem(
        nombre="Losartán 50 mg",
        principio_activo="Losartán",
        familia="Antagonistas ARA-II",
        dosis_sugerida="50 mg",
        forma_farmaceutica="Comprimidos / Cápsulas",
        forma_sugerida="comprimidos",
        color_sugerido="blanco",
        instrucciones_sugeridas="Tomar siempre a la misma hora del día, con o sin alimentos.",
        proposito="Control de presión arterial alta (Hipertensión)",
        contraindicaciones="Hipersensibilidad, segundo y tercer trimestre de embarazo, insuficiencia hepática grave.",
        es_critico_defecto=True,
    ),
    MedicamentoCatalogoItem(
        nombre="Metformina 850 mg",
        principio_activo="Metformina",
        familia="Biguanidas (Antidiabéticos)",
        dosis_sugerida="850 mg",
        forma_farmaceutica="Comprimidos / Cápsulas",
        forma_sugerida="comprimidos",
        color_sugerido="blanco",
        instrucciones_sugeridas="Tomar junto con las comidas o inmediatamente después para evitar náuseas.",
        proposito="Control de glucosa en sangre (Diabetes Tipo 2)",
        contraindicaciones="Cetoacidosis diabética, insuficiencia renal grave (TFG < 30 ml/min), insuficiencia cardíaca descompensada.",
        es_critico_defecto=True,
    ),
    MedicamentoCatalogoItem(
        nombre="Atorvastatina 20 mg",
        principio_activo="Atorvastatina",
        familia="Estatinas",
        dosis_sugerida="20 mg",
        forma_farmaceutica="Comprimidos / Cápsulas",
        forma_sugerida="comprimidos",
        color_sugerido="blanco",
        instrucciones_sugeridas="Tomar preferentemente por la noche; evitar jugo de toronja en exceso.",
        proposito="Reducción de colesterol y triglicéridos",
        contraindicaciones="Enfermedad hepática activa, elevaciones persistentes inexplicables de transaminasas, embarazo.",
        es_critico_defecto=False,
    ),
    MedicamentoCatalogoItem(
        nombre="Clonazepam 2 mg",
        principio_activo="Clonazepam",
        familia="Benzodiacepinas",
        dosis_sugerida="2 mg",
        forma_farmaceutica="Comprimidos / Cápsulas",
        forma_sugerida="comprimidos",
        color_sugerido="amarillo",
        instrucciones_sugeridas="No consumir alcohol ni conducir maquinaria pesada tras la toma.",
        proposito="Control neurológico y del descanso",
        contraindicaciones="Miastenia gravis, insuficiencia respiratoria severa, apnea del sueño, glaucoma de ángulo estrecho.",
        es_critico_defecto=True,
    ),
    MedicamentoCatalogoItem(
        nombre="Salbutamol Aerosol 100 mcg",
        principio_activo="Salbutamol",
        familia="Broncodilatadores Beta-2",
        dosis_sugerida="100 mcg (2 disparos)",
        forma_farmaceutica="Gotas / Jarabe",
        forma_sugerida="inhalador",
        color_sugerido="azul",
        instrucciones_sugeridas="Agitar el inhalador antes de usar y mantener el aire 10 segundos tras inhalar.",
        proposito="Alivio de broncoespasmo y asma",
        contraindicaciones="Hipersensibilidad al salbutamol, arritmias cardíacas severas sin control.",
        es_critico_defecto=False,
    ),
    MedicamentoCatalogoItem(
        nombre="Naproxeno 500 mg",
        principio_activo="Naproxeno",
        familia="AINEs",
        dosis_sugerida="500 mg",
        forma_farmaceutica="Comprimidos / Cápsulas",
        forma_sugerida="comprimidos",
        color_sugerido="amarillo",
        instrucciones_sugeridas="Tomar acompañado de alimentos y un vaso de agua.",
        proposito="Alivio de inflamación y dolor articular",
        contraindicaciones="Alergia a AINEs o aspirina, antecedentes de hemorragia gastrointestinal o perforación.",
        es_critico_defecto=False,
    ),
    MedicamentoCatalogoItem(
        nombre="Ketorolaco 10 mg",
        principio_activo="Ketorolaco",
        familia="AINEs",
        dosis_sugerida="10 mg",
        forma_farmaceutica="Comprimidos / Cápsulas",
        forma_sugerida="comprimidos",
        color_sugerido="blanco",
        instrucciones_sugeridas="Tomar con alimentos; no prolongar su uso por más de 5 días continuos.",
        proposito="Alivio a corto plazo de dolor agudo",
        contraindicaciones="Alergia severa a AINEs, alto riesgo de sangrado, insuficiencia renal moderada o grave.",
        es_critico_defecto=False,
    ),
    MedicamentoCatalogoItem(
        nombre="Azitromicina 500 mg",
        principio_activo="Azitromicina",
        familia="Macrólidos",
        dosis_sugerida="500 mg",
        forma_farmaceutica="Comprimidos / Cápsulas",
        forma_sugerida="comprimidos",
        color_sugerido="azul",
        instrucciones_sugeridas="Tomar 1 vez al día a la misma hora con un vaso de agua.",
        proposito="Infección bacteriana respiratoria (Antibiótico)",
        contraindicaciones="Hipersensibilidad a azitromicina, eritromicina o cualquier antibiótico macrólido.",
        es_critico_defecto=True,
    ),
    MedicamentoCatalogoItem(
        nombre="Sulfametoxazol con Trimetoprima 800/160 mg",
        principio_activo="Sulfametoxazol / Trimetoprima",
        familia="Sulfamidas / Antibacterianos",
        dosis_sugerida="800/160 mg",
        forma_farmaceutica="Comprimidos / Cápsulas",
        forma_sugerida="comprimidos",
        color_sugerido="blanco",
        instrucciones_sugeridas="Beber abundante agua durante el día mientras dure el tratamiento.",
        proposito="Infección bacteriana urinaria o gastrointestinal",
        contraindicaciones="Alergia a sulfas o sulfamidas, daño parenquimatoso hepático grave, insuficiencia renal severa.",
        es_critico_defecto=True,
    ),
    MedicamentoCatalogoItem(
        nombre="Insulina Glargina 100 UI/ml",
        principio_activo="Insulina Glargina",
        familia="Insulinas",
        dosis_sugerida="10 UI",
        forma_farmaceutica="Inyectable / Ampolla",
        forma_sugerida="inyectable",
        color_sugerido="transparente",
        instrucciones_sugeridas="Aplicar por vía subcutánea rotando el sitio de punción a la misma hora cada día.",
        proposito="Control basal de glucosa (Diabetes)",
        contraindicaciones="Episodios de hipoglucemia activa, hipersensibilidad a la insulina glargina.",
        es_critico_defecto=True,
    ),
    MedicamentoCatalogoItem(
        nombre="Penicilina G Benzatínica 1,200,000 UI",
        principio_activo="Penicilina Benzatínica",
        familia="Penicilinas / Betalactámicos",
        dosis_sugerida="1,200,000 UI",
        forma_farmaceutica="Inyectable / Ampolla",
        forma_sugerida="inyectable",
        color_sugerido="blanco",
        instrucciones_sugeridas="Aplicación intramuscular profunda exclusiva por personal de salud.",
        proposito="Infección estreptocócica (Antibiótico de depósito)",
        contraindicaciones="Alergia confirmada a penicilinas o betalactámicos (riesgo de anafilaxia).",
        es_critico_defecto=True,
    ),
    MedicamentoCatalogoItem(
        nombre="Ciprofloxacino 500 mg",
        principio_activo="Ciprofloxacino",
        familia="Fluoroquinolonas",
        dosis_sugerida="500 mg",
        forma_farmaceutica="Comprimidos / Cápsulas",
        forma_sugerida="comprimidos",
        color_sugerido="blanco",
        instrucciones_sugeridas="No tomar junto con lácteos ni antiácidos (separar al menos 2 horas).",
        proposito="Infección bacteriana (Quinolona)",
        contraindicaciones="Hipersensibilidad a quinolonas, antecedentes de afecciones tendinosas por quinolonas.",
        es_critico_defecto=True,
    ),
    MedicamentoCatalogoItem(
        nombre="Levotiroxina 100 mcg",
        principio_activo="Levotiroxina",
        familia="Hormonas tiroideas",
        dosis_sugerida="100 mcg",
        forma_farmaceutica="Comprimidos / Cápsulas",
        forma_sugerida="comprimidos",
        color_sugerido="amarillo",
        instrucciones_sugeridas="Tomar en ayunas con agua 30 a 60 minutos antes del desayuno.",
        proposito="Reemplazo hormonal tiroideo (Hipotiroidismo)",
        contraindicaciones="Tirotoxicosis no tratada, infarto agudo de miocardio reciente, insuficiencia suprarrenal no tratada.",
        es_critico_defecto=True,
    ),
]


def _normalizar(texto: str) -> str:
    """Elimina acentos y convierte a minúsculas para comparación robusta."""
    if not texto:
        return ""
    nfkd = unicodedata.normalize("NFKD", texto)
    sin_tildes = "".join([c for c in nfkd if not unicodedata.combining(c)])
    return sin_tildes.lower().strip()


def _coincide_termino(termino: str, texto: str) -> bool:
    """Verifica coincidencia con límite de palabra para evitar falsos positivos
    por subcadenas cortas (ej. 'sal' en 'salbutamol' o 'asa' en 'casa')."""
    t = _normalizar(termino)
    s = _normalizar(texto)
    if not t or not s:
        return False
    if len(t) < 4:
        # Términos cortos requieren coincidencia de palabra exacta
        return bool(re.search(rf"\b{re.escape(t)}\b", s))
    # Términos de >= 4 caracteres requieren inicio de palabra
    return bool(re.search(rf"\b{re.escape(t)}", s))


# Grupos y familias de alergias cruzadas comunes
GRUPOS_ALERGIAS_CRUZADAS: dict[str, list[str]] = {
    "penicilina": [
        "penicilina",
        "amoxicilina",
        "ampicilina",
        "betalactamico",
        "betalactamicos",
        "clavulanato",
        "cefalosporina",
        "cefalexina",
        "ceftriaxona",
    ],
    "aines": [
        "aines",
        "aine",
        "ibuprofeno",
        "aspirina",
        "acido acetilsalicilico",
        "naproxeno",
        "ketorolaco",
        "diclofenaco",
        "meloxicam",
        "indometacina",
        "piroxicam",
    ],
    "sulfas": [
        "sulfa",
        "sulfas",
        "sulfamida",
        "sulfamidas",
        "sulfametoxazol",
        "trimetoprima",
    ],
    "macrolidos": [
        "macrolido",
        "macrolidos",
        "azitromicina",
        "claritromicina",
        "eritromicina",
    ],
    "opioides": [
        "opioide",
        "opioides",
        "tramadol",
        "codeina",
        "morfina",
        "oxicodona",
        "fentanilo",
    ],
    "quinolonas": [
        "quinolona",
        "quinolonas",
        "fluoroquinolona",
        "fluoroquinolonas",
        "ciprofloxacino",
        "levofloxacino",
    ],
}

# Reglas clínicas de interacción medicamentosa entre pares de familias/fármacos
REGLAS_INTERACCIONES: list[tuple[list[str], list[str], str]] = [
    (
        ["ibuprofeno", "naproxeno", "ketorolaco", "diclofenaco", "meloxicam", "aspirina", "acido acetilsalicilico"],
        ["ibuprofeno", "naproxeno", "ketorolaco", "diclofenaco", "meloxicam", "aspirina", "acido acetilsalicilico"],
        "Duplicidad de AINEs: combinar dos antiinflamatorios aumenta severamente el riesgo de úlcera y sangrado gástrico.",
    ),
    (
        ["losartan", "enalapril", "captopril", "valsartan", "telmisartan"],
        ["ibuprofeno", "naproxeno", "ketorolaco", "diclofenaco", "meloxicam"],
        "Interacción Antihipertensivo + AINE: los antiinflamatorios reducen el efecto antihipertensivo y aumentan la carga renal.",
    ),
    (
        ["clonazepam", "alprazolam", "diazepam", "lorazepam"],
        ["tramadol", "codeina", "morfina", "oxicodona", "fentanilo"],
        "Interacción SNC: combinar benzodiacepinas con opioides incrementa el riesgo de sedación profunda y depresión respiratoria.",
    ),
    (
        ["atorvastatina", "simvastatina", "rosuvastatina"],
        ["azitromicina", "claritromicina", "eritromicina", "ciprofloxacino"],
        "Interacción Estatina + Antibiótico: puede elevar los niveles plasmáticos de la estatina y causar dolor muscular (miopatía).",
    ),
]


def buscar_en_catalogo(query: str | None) -> list[MedicamentoCatalogoItem]:
    """Busca medicamentos en el catálogo por nombre, principio activo, familia o propósito."""
    if not query or not query.strip():
        return CATALOGO_CLINICO[:10]

    q_norm = _normalizar(query)
    resultados = []
    for item in CATALOGO_CLINICO:
        n_norm = _normalizar(item.nombre)
        p_norm = _normalizar(item.principio_activo)
        f_norm = _normalizar(item.familia)
        prop_norm = _normalizar(item.proposito)

        if (
            q_norm in n_norm
            or q_norm in p_norm
            or q_norm in f_norm
            or q_norm in prop_norm
        ):
            resultados.append(item)

    return resultados


def verificar_interacciones_botiquin(
    db: Session, id_usuario: int, nombre: str, principio_activo: str | None = None
) -> tuple[bool, str | None, str | None, list[str]]:
    """Compara el medicamento candidato contra los medicamentos actuales del usuario
    para detectar duplicidades de principio activo o interacciones fármaco-fármaco."""
    meds_actuales = db.scalars(
        select(Medicamento).where(Medicamento.id_usuario == id_usuario)
    ).all()
    if not meds_actuales:
        return False, None, None, []

    cand_texto = f"{nombre} {principio_activo or ''}"
    cand_norm = _normalizar(cand_texto)
    if len(cand_norm) < 3:
        return False, None, None, []

    interacciones: list[str] = []
    primer_med_conflicto: str | None = None

    for med in meds_actuales:
        med_texto = f"{med.nombre} {med.principio_activo or ''}"
        # 1. Duplicidad exacta de principio activo
        if principio_activo and med.principio_activo:
            if _coincide_termino(principio_activo, med.principio_activo) or _coincide_termino(
                med.principio_activo, principio_activo
            ):
                msg = (
                    f"DUPLICIDAD TERAPÉUTICA: Ya tienes '{med.nombre}' ({med.principio_activo}) "
                    f"en tu botiquín. Evita sobredosificación."
                )
                if msg not in interacciones:
                    interacciones.append(msg)
                    if primer_med_conflicto is None:
                        primer_med_conflicto = med.nombre

        # 2. Reglas de interacción entre familias de medicamentos
        for grupo_a, grupo_b, explicacion in REGLAS_INTERACCIONES:
            cand_en_a = any(_coincide_termino(m, cand_texto) for m in grupo_a)
            med_en_b = any(_coincide_termino(m, med_texto) for m in grupo_b)
            cand_en_b = any(_coincide_termino(m, cand_texto) for m in grupo_b)
            med_en_a = any(_coincide_termino(m, med_texto) for m in grupo_a)

            if (cand_en_a and med_en_b) or (cand_en_b and med_en_a):
                msg = f"INTERACCIÓN FARMACOLÓGICA CON '{med.nombre.upper()}': {explicacion}"
                if msg not in interacciones:
                    interacciones.append(msg)
                    if primer_med_conflicto is None:
                        primer_med_conflicto = med.nombre

    if interacciones:
        return True, interacciones[0], primer_med_conflicto, interacciones
    return False, None, None, []


def verificar_alergias_paciente(
    db: Session, id_usuario: int, nombre: str, principio_activo: str | None = None
) -> VerificarAlergiasOut:
    """Verifica si el medicamento ingresado o seleccionado entra en conflicto
    con alguna alergia registrada del paciente o presenta interacción con su botiquín."""
    alergias = db.scalars(
        select(AlergiaUsuario).where(AlergiaUsuario.id_usuario == id_usuario)
    ).all()

    tiene_interaccion, alerta_interaccion, med_conflicto, lista_interacciones = (
        verificar_interacciones_botiquin(
            db=db,
            id_usuario=id_usuario,
            nombre=nombre,
            principio_activo=principio_activo,
        )
    )

    nombre_norm = _normalizar(nombre)
    principio_norm = _normalizar(principio_activo or "")
    cand_texto = f"{nombre_norm} {principio_norm}".strip()

    for alergia in alergias:
        sustancia_norm = _normalizar(alergia.sustancia)
        if not sustancia_norm:
            continue

        # 1. Coincidencia directa con límite de palabra
        coincide_directo = (
            _coincide_termino(sustancia_norm, nombre_norm)
            or (principio_norm and _coincide_termino(sustancia_norm, principio_norm))
            or (len(nombre_norm) >= 4 and _coincide_termino(nombre_norm, sustancia_norm))
            or (
                principio_norm
                and len(principio_norm) >= 4
                and _coincide_termino(principio_norm, sustancia_norm)
            )
        )

        if coincide_directo:
            alerta_msg = (
                f"ALERTA DE ALERGIA: Tienes registrada una alergia a '{alergia.sustancia}'. "
                f"Tomar '{nombre}' puede provocar una reacción {alergia.severidad.upper()}."
            )
            registrar_evento_mongo(
                evento="alerta_alergia",
                id_usuario=id_usuario,
                detalle={
                    "medicamento": nombre,
                    "alergia_detectada": alergia.sustancia,
                    "severidad": alergia.severidad,
                    "tipo": "directa",
                },
            )
            return VerificarAlergiasOut(
                tiene_conflicto=True,
                alerta=alerta_msg,
                alergia_detectada=alergia.sustancia,
                severidad=alergia.severidad,
                tiene_interaccion=tiene_interaccion,
                alerta_interaccion=alerta_interaccion,
                medicamento_conflicto=med_conflicto,
                interacciones=lista_interacciones,
            )

        # 2. Coincidencia por grupo cruzado (ej. Penicilina vs Amoxicilina, AINEs vs Ibuprofeno)
        for grupo, miembros in GRUPOS_ALERGIAS_CRUZADAS.items():
            sustancia_en_grupo = any(
                _coincide_termino(m, sustancia_norm) or _coincide_termino(sustancia_norm, m)
                for m in miembros
            )
            if sustancia_en_grupo:
                med_en_grupo = any(_coincide_termino(m, cand_texto) for m in miembros)
                if med_en_grupo:
                    alerta_msg = (
                        f"ALERTA DE REACTIVIDAD CRUZADA: Tienes registrada una alergia a "
                        f"'{alergia.sustancia}' (grupo {grupo.upper()}). '{nombre}' pertenece a "
                        f"esta familia y está contraindicado."
                    )
                    registrar_evento_mongo(
                        evento="alerta_alergia",
                        id_usuario=id_usuario,
                        detalle={
                            "medicamento": nombre,
                            "alergia_detectada": alergia.sustancia,
                            "grupo": grupo,
                            "severidad": alergia.severidad,
                            "tipo": "cruzada",
                        },
                    )
                    return VerificarAlergiasOut(
                        tiene_conflicto=True,
                        alerta=alerta_msg,
                        alergia_detectada=alergia.sustancia,
                        severidad=alergia.severidad,
                        tiene_interaccion=tiene_interaccion,
                        alerta_interaccion=alerta_interaccion,
                        medicamento_conflicto=med_conflicto,
                        interacciones=lista_interacciones,
                    )

    if tiene_interaccion:
        return VerificarAlergiasOut(
            tiene_conflicto=False,
            alerta=alerta_interaccion,
            tiene_interaccion=True,
            alerta_interaccion=alerta_interaccion,
            medicamento_conflicto=med_conflicto,
            interacciones=lista_interacciones,
        )

    return VerificarAlergiasOut(tiene_conflicto=False)
