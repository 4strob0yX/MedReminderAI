import unicodedata
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.alergia import AlergiaUsuario
from app.schemas.medicamento import MedicamentoCatalogoItem, VerificarAlergiasOut

# Catálogo precargado de medicamentos comunes para autocompletado y validación clínica
CATALOGO_CLINICO: list[MedicamentoCatalogoItem] = [
    MedicamentoCatalogoItem(
        nombre="Paracetamol 500 mg",
        principio_activo="Paracetamol",
        familia="Analgésicos y antipiréticos",
        dosis_sugerida="500 mg",
        forma_farmaceutica="Comprimidos / Cápsulas",
        contraindicaciones="Hipersensibilidad al paracetamol, insuficiencia hepática grave o hepatitis activa.",
        es_critico_defecto=False,
    ),
    MedicamentoCatalogoItem(
        nombre="Ibuprofeno 400 mg",
        principio_activo="Ibuprofeno",
        familia="AINEs",
        dosis_sugerida="400 mg",
        forma_farmaceutica="Comprimidos / Cápsulas",
        contraindicaciones="Alergia a AINEs o aspirina, úlcera gastroduodenal activa, insuficiencia renal o cardíaca severa.",
        es_critico_defecto=False,
    ),
    MedicamentoCatalogoItem(
        nombre="Ibuprofeno 600 mg",
        principio_activo="Ibuprofeno",
        familia="AINEs",
        dosis_sugerida="600 mg",
        forma_farmaceutica="Comprimidos / Cápsulas",
        contraindicaciones="Alergia a AINEs o aspirina, úlcera péptica activa, hemorragia gastrointestinal.",
        es_critico_defecto=False,
    ),
    MedicamentoCatalogoItem(
        nombre="Amoxicilina 500 mg",
        principio_activo="Amoxicilina",
        familia="Penicilinas / Betalactámicos",
        dosis_sugerida="500 mg",
        forma_farmaceutica="Comprimidos / Cápsulas",
        contraindicaciones="Alergia a penicilinas, cefalosporinas o betalactámicos. Antecedente de ictericia.",
        es_critico_defecto=True,  # Los antibióticos no deben posponerse arbitrariamente
    ),
    MedicamentoCatalogoItem(
        nombre="Amoxicilina con Ácido Clavulánico 875/125 mg",
        principio_activo="Amoxicilina / Clavulanato",
        familia="Penicilinas / Betalactámicos",
        dosis_sugerida="875 mg",
        forma_farmaceutica="Comprimidos / Cápsulas",
        contraindicaciones="Hipersensibilidad a betalactámicos o penicilinas. Disfunción hepática previa por amoxicilina.",
        es_critico_defecto=True,
    ),
    MedicamentoCatalogoItem(
        nombre="Aspirina 100 mg (Ácido Acetilsalicílico)",
        principio_activo="Ácido Acetilsalicílico",
        familia="AINEs / Antiagregantes",
        dosis_sugerida="100 mg",
        forma_farmaceutica="Comprimidos / Cápsulas",
        contraindicaciones="Alergia a salicilatos o AINEs, diátesis hemorrágica, úlcera gástrica activa.",
        es_critico_defecto=True,
    ),
    MedicamentoCatalogoItem(
        nombre="Omeprazol 20 mg",
        principio_activo="Omeprazol",
        familia="Inhibidores de la bomba de protones",
        dosis_sugerida="20 mg",
        forma_farmaceutica="Comprimidos / Cápsulas",
        contraindicaciones="Hipersensibilidad a omeprazol o benzimidazoles. Coadministración con nelfinavir.",
        es_critico_defecto=False,
    ),
    MedicamentoCatalogoItem(
        nombre="Losartán 50 mg",
        principio_activo="Losartán",
        familia="Antagonistas ARA-II",
        dosis_sugerida="50 mg",
        forma_farmaceutica="Comprimidos / Cápsulas",
        contraindicaciones="Hipersensibilidad, segundo y tercer trimestre de embarazo, insuficiencia hepática grave.",
        es_critico_defecto=True,  # Antihipertensivo crítico
    ),
    MedicamentoCatalogoItem(
        nombre="Metformina 850 mg",
        principio_activo="Metformina",
        familia="Biguanidas (Antidiabéticos)",
        dosis_sugerida="850 mg",
        forma_farmaceutica="Comprimidos / Cápsulas",
        contraindicaciones="Cetoacidosis diabética, insuficiencia renal grave (TFG < 30 ml/min), insuficiencia cardíaca descompensada.",
        es_critico_defecto=True,
    ),
    MedicamentoCatalogoItem(
        nombre="Atorvastatina 20 mg",
        principio_activo="Atorvastatina",
        familia="Estatinas",
        dosis_sugerida="20 mg",
        forma_farmaceutica="Comprimidos / Cápsulas",
        contraindicaciones="Enfermedad hepática activa, elevaciones persistentes inexplicables de transaminasas, embarazo.",
        es_critico_defecto=False,
    ),
    MedicamentoCatalogoItem(
        nombre="Clonazepam 2 mg",
        principio_activo="Clonazepam",
        familia="Benzodiacepinas",
        dosis_sugerida="2 mg",
        forma_farmaceutica="Comprimidos / Cápsulas",
        contraindicaciones="Miastenia gravis, insuficiencia respiratoria severa, apnea del sueño, glaucoma de ángulo estrecho.",
        es_critico_defecto=True,  # Control estricto de dosis
    ),
    MedicamentoCatalogoItem(
        nombre="Salbutamol Aerosol 100 mcg",
        principio_activo="Salbutamol",
        familia="Broncodilatadores Beta-2",
        dosis_sugerida="100 mcg (2 disparos)",
        forma_farmaceutica="Gotas / Jarabe",
        contraindicaciones="Hipersensibilidad al salbutamol, arritmias cardíacas severas sin control.",
        es_critico_defecto=False,
    ),
    MedicamentoCatalogoItem(
        nombre="Naproxeno 500 mg",
        principio_activo="Naproxeno",
        familia="AINEs",
        dosis_sugerida="500 mg",
        forma_farmaceutica="Comprimidos / Cápsulas",
        contraindicaciones="Alergia a AINEs o aspirina, antecedentes de hemorragia gastrointestinal o perforación.",
        es_critico_defecto=False,
    ),
    MedicamentoCatalogoItem(
        nombre="Ketorolaco 10 mg",
        principio_activo="Ketorolaco",
        familia="AINEs",
        dosis_sugerida="10 mg",
        forma_farmaceutica="Comprimidos / Cápsulas",
        contraindicaciones="Alergia severa a AINEs, alto riesgo de sangrado, insuficiencia renal moderada o grave.",
        es_critico_defecto=False,
    ),
    MedicamentoCatalogoItem(
        nombre="Azitromicina 500 mg",
        principio_activo="Azitromicina",
        familia="Macrólidos",
        dosis_sugerida="500 mg",
        forma_farmaceutica="Comprimidos / Cápsulas",
        contraindicaciones="Hipersensibilidad a azitromicina, eritromicina o cualquier antibiótico macrólido.",
        es_critico_defecto=True,
    ),
    MedicamentoCatalogoItem(
        nombre="Sulfametoxazol con Trimetoprima 800/160 mg",
        principio_activo="Sulfametoxazol / Trimetoprima",
        familia="Sulfamidas / Antibacterianos",
        dosis_sugerida="800/160 mg",
        forma_farmaceutica="Comprimidos / Cápsulas",
        contraindicaciones="Alergia a sulfas o sulfamidas, daño parenquimatoso hepático grave, insuficiencia renal severa.",
        es_critico_defecto=True,
    ),
    MedicamentoCatalogoItem(
        nombre="Insulina Glargina 100 UI/ml",
        principio_activo="Insulina Glargina",
        familia="Insulinas",
        dosis_sugerida="10 UI",
        forma_farmaceutica="Inyectable / Ampolla",
        contraindicaciones="Episodios de hipoglucemia activa, hipersensibilidad a la insulina glargina.",
        es_critico_defecto=True,  # Altamente crítico
    ),
    MedicamentoCatalogoItem(
        nombre="Penicilina G Benzatínica 1,200,000 UI",
        principio_activo="Penicilina Benzatínica",
        familia="Penicilinas / Betalactámicos",
        dosis_sugerida="1,200,000 UI",
        forma_farmaceutica="Inyectable / Ampolla",
        contraindicaciones="Alergia confirmada a penicilinas o betalactámicos (riesgo de anafilaxia).",
        es_critico_defecto=True,
    ),
    MedicamentoCatalogoItem(
        nombre="Ciprofloxacino 500 mg",
        principio_activo="Ciprofloxacino",
        familia="Fluoroquinolonas",
        dosis_sugerida="500 mg",
        forma_farmaceutica="Comprimidos / Cápsulas",
        contraindicaciones="Hipersensibilidad a quinolonas, antecedentes de afecciones tendinosas por quinolonas.",
        es_critico_defecto=True,
    ),
    MedicamentoCatalogoItem(
        nombre="Levotiroxina 100 mcg",
        principio_activo="Levotiroxina",
        familia="Hormonas tiroideas",
        dosis_sugerida="100 mcg",
        forma_farmaceutica="Comprimidos / Cápsulas",
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


def buscar_en_catalogo(query: str | None) -> list[MedicamentoCatalogoItem]:
    """Busca medicamentos en el catálogo por nombre, principio activo o familia."""
    if not query or not query.strip():
        return CATALOGO_CLINICO[:10]  # Primeros 10 como sugerencia por defecto

    q_norm = _normalizar(query)
    resultados = []
    for item in CATALOGO_CLINICO:
        n_norm = _normalizar(item.nombre)
        p_norm = _normalizar(item.principio_activo)
        f_norm = _normalizar(item.familia)

        if q_norm in n_norm or q_norm in p_norm or q_norm in f_norm:
            resultados.append(item)

    return resultados


def verificar_alergias_paciente(
    db: Session, id_usuario: int, nombre: str, principio_activo: str | None = None
) -> VerificarAlergiasOut:
    """Verifica si el medicamento ingresado o seleccionado entra en conflicto
    con alguna alergia registrada del paciente en la base de datos."""
    alergias = db.scalars(
        select(AlergiaUsuario).where(AlergiaUsuario.id_usuario == id_usuario)
    ).all()

    if not alergias:
        return VerificarAlergiasOut(tiene_conflicto=False)

    nombre_norm = _normalizar(nombre)
    principio_norm = _normalizar(principio_activo or "")

    for alergia in alergias:
        sustancia_norm = _normalizar(alergia.sustancia)

        # 1. Coincidencia directa de texto
        coincide_directo = (
            sustancia_norm in nombre_norm
            or (principio_norm and sustancia_norm in principio_norm)
            or nombre_norm in sustancia_norm
            or (principio_norm and principio_norm in sustancia_norm)
        )

        if coincide_directo:
            return VerificarAlergiasOut(
                tiene_conflicto=True,
                alerta=f"⚠️ ALERTA DE ALERGIA: Tienes registrada una alergia a '{alergia.sustancia}'. Tomar '{nombre}' puede provocar una reacción {alergia.severidad.upper()}.",
                alergia_detectada=alergia.sustancia,
                severidad=alergia.severidad,
            )

        # 2. Coincidencia por grupo cruzado (ej. Penicilina vs Amoxicilina, AINEs vs Ibuprofeno)
        for grupo, miembros in GRUPOS_ALERGIAS_CRUZADAS.items():
            sustancia_en_grupo = any(
                m in sustancia_norm or sustancia_norm in m for m in miembros
            )
            if sustancia_en_grupo:
                # Comprobar si el medicamento actual pertenece a este mismo grupo
                med_en_grupo = any(
                    m in nombre_norm or (principio_norm and m in principio_norm)
                    for m in miembros
                )
                if med_en_grupo:
                    return VerificarAlergiasOut(
                        tiene_conflicto=True,
                        alerta=f"⚠️ ALERTA DE REACTIVIDAD CRUZADA: Tienes registrada una alergia a '{alergia.sustancia}' (grupo {grupo.upper()}). '{nombre}' pertenece a esta familia y está contraindicado.",
                        alergia_detectada=alergia.sustancia,
                        severidad=alergia.severidad,
                    )

    return VerificarAlergiasOut(tiene_conflicto=False)
