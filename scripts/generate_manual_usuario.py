"""
generate_manual_usuario.py - Generador del Manual de Usuario Oficial de MedReminder AI.
Estructurado formalmente en 9 secciones normativas según lineamientos docentes de la UTVT:
1. Introducción
2. Antes de comenzar
3. Primeros pasos
4. Funciones, con una estructura fija por tarea (objetivo, pasos numerados, resultado esperado y advertencias)
5. Flujos de trabajo
6. Errores y soluciones
7. Preguntas frecuentes
8. Recomendaciones
9. Soporte
Termina con: Glosario y Lista de Verificación antes de entregar.
"""

import os
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(BASE_DIR / "scripts"))

import docx
from doc_utils import (
    create_base_document, setup_header_footer, add_utvt_cover, add_version_control_table,
    add_native_toc, add_section_heading, add_body_p, add_truth_table, add_variable_dictionary_table,
    add_peas_section, add_callout, add_figure_image, add_checklist_table
)

def build_manual_usuario():
    doc = create_base_document()
    doc_title = "Manual de Usuario Oficial"
    setup_header_footer(doc, doc_title)
    
    # --------------------------------------------------------------------------
    # 0. CARÁTULA INSTITUCIONAL UTVT
    # --------------------------------------------------------------------------
    add_utvt_cover(
        doc,
        title="MANUAL DE USUARIO Y GUÍA DE OPERACIÓN CLÍNICA",
        subtitle="Guía Integral para el Paciente, Cuidador Familiar y Personal de Salud en el Uso Ergonómico y Seguro",
        doc_code="MAN-USU-MEDREMINDER-2026-V1.3"
    )
    
    # --------------------------------------------------------------------------
    # CONTROL DE VERSIONES
    # --------------------------------------------------------------------------
    versiones = [
        {
            "version": "1.0",
            "fecha": "20/10/2026",
            "autor": "Equipo de Ingeniería UTVT",
            "descripcion": "Versión inicial: Guía de uso de la aplicación móvil y capturas de pantalla de la interfaz."
        },
        {
            "version": "1.1",
            "fecha": "21/10/2026",
            "autor": "Equipo de Ingeniería UTVT",
            "descripcion": "Estructuración en 9 secciones normativas según rúbrica docente, tareas fijas (objetivo, pasos, resultado, advertencias), flujos, glosario y lista de verificación."
        },
        {
            "version": "1.2",
            "fecha": "22/10/2026",
            "autor": "Equipo de Ingeniería UTVT",
            "descripcion": "Integración del Marco Operativo PEAS para el paciente en Sección 1 'hasta arriba', eliminación de diagramas textuales y actualización de tareas."
        },
        {
            "version": "1.3",
            "fecha": "22/10/2026",
            "autor": "Equipo de Ingeniería UTVT",
            "descripcion": "Incorporación de Tablas de Verdad de Reglas de Interacción del Paciente (V y F) en Sección 1.3 'hasta arriba' inmediatamente después del Marco PEAS."
        }
    ]
    add_version_control_table(doc, versiones, "CONTROL DE VERSIONES DEL MANUAL DE USUARIO")
    
    # --------------------------------------------------------------------------
    # ÍNDICE GENERAL NATIVO DE WORD
    # --------------------------------------------------------------------------
    toc_items = [
        ("1.", "INTRODUCCIÓN", 3),
        ("1.1", "¿Qué es MedReminder AI?", 3),
        ("1.2", "Marco Operativo PEAS: Cómo Cuida MedReminder AI de su Salud (Rendimiento, Entorno, Acciones y Avisos)", 3),
        ("1.3", "Tablas de Verdad de Reglas de Interacción del Paciente", 4),
        ("1.4", "Objetivo del Manual de Usuario", 5),
        ("1.5", "Beneficios Asistivos para el Paciente y la Familia", 5),
        ("1.6", "Acompañante Virtual Medi: Su Aliado Clínico Diario", 6),
        ("2.", "ANTES DE COMENZAR", 7),
        ("2.1", "Requisitos del Teléfono Inteligente Android", 6),
        ("2.2", "Permisos Necesarios Explicados de Forma Sencilla", 6),
        ("2.3", "Recomendaciones de Volumen, Sonido y Vibración", 7),
        ("2.4", "Conectividad: Funcionamiento con y sin Internet", 7),
        ("3.", "PRIMEROS PASOS", 8),
        ("3.1", "Apertura de la Aplicación en su Teléfono", 8),
        ("3.2", "Pantalla de Inicio de Sesión («Iniciar Sesión»)", 8),
        ("3.3", "Pantalla de Registro («Crear Cuenta»)", 10),
        ("3.4", "Navegación General por la Barra Inferior", 11),
        ("4.", "FUNCIONES (CON ESTRUCTURA FIJA POR TAREA: OBJETIVO, PASOS NUMERADOS, RESULTADO ESPERADO Y ADVERTENCIAS)", 12),
        ("4.1", "Tarea 4.1: Alta de un nuevo medicamento y programación de horarios", 12),
        ("4.2", "Tarea 4.2: Confirmación de tomas de medicamentos desde la vista «Hoy»", 14),
        ("4.3", "Tarea 4.3: Posponer tomas de medicamentos (+10 minutos o +30 minutos)", 16),
        ("4.4", "Tarea 4.4: Omitir tomas de medicamentos con justificación clínica", 17),
        ("4.5", "Tarea 4.5: Deshacer tomas de medicamentos registradas por error", 18),
        ("4.6", "Tarea 4.6: Gestión y recarga rápida de stock en «Mi Botiquín» (+30 unidades)", 19),
        ("4.7", "Tarea 4.7: Consulta y diálogo asistido por voz con Medi", 21),
        ("4.8", "Tarea 4.8: Consulta de contactos de emergencia y red de apoyo médico", 23),
        ("4.9", "Tarea 4.9: Consulta del árbol de análisis de Inteligencia Artificial", 25),
        ("4.10", "Tarea 4.10: Monitoreo de adherencia, rachas de honor y cumplimiento diario", 27),
        ("5.", "FLUJOS DE TRABAJO", 29),
        ("5.1", "Flujo Diario Típico del Paciente (Mañana, Tarde y Noche)", 29),
        ("5.2", "Flujo de Compra y Reposición de Farmacia", 30),
        ("5.3", "Flujo de Reporte a Familiares o Cuidadores de Confianza", 31),
        ("5.4", "Flujo de Emergencia ante Olvido Prolongado", 32),
        ("6.", "ERRORES Y SOLUCIONES", 33),
        ("6.1", "¿Qué hacer si no suena la alarma médica?", 33),
        ("6.2", "¿Qué hacer si la aplicación se cierra inesperadamente?", 34),
        ("6.3", "¿Qué hacer si marqué una toma de medicamentos equivocada?", 34),
        ("6.4", "¿Qué hacer si el botiquín marca existencias agotadas?", 35),
        ("6.5", "¿Qué hacer si cambio de teléfono móvil?", 35),
        ("7.", "PREGUNTAS FRECUENTES (FAQ)", 36),
        ("8.", "RECOMENDACIONES", 39),
        ("8.1", "Recomendaciones Médicas para la Adherencia Farmacológica", 39),
        ("8.2", "Cuidados en el Almacenamiento Físico de Medicamentos", 39),
        ("8.3", "Recomendaciones Técnicas para el Cuidado del Teléfono", 40),
        ("9.", "SOPORTE", 41),
        ("9.1", "Canales de Asistencia y Dudas", 41),
        ("9.2", "Directorio del Equipo de Desarrollo de la UTVT", 41),
        ("9.3", "Procedimiento para Reportar Sugerencias o Incidencias Técnicas", 42),
        ("GLOSARIO", "GLOSARIO TERMINOLÓGICO PARA EL PACIENTE Y CUIDADOR", 43),
        ("CHECKLIST", "LISTA DE VERIFICACIÓN ANTES DE COMENZAR A USAR LA APP", 45)
    ]
    add_native_toc(doc, toc_items)
    
    # ==========================================================================
    # 1. INTRODUCCIÓN
    # ==========================================================================
    add_section_heading(doc, "1. INTRODUCCIÓN", level=1)
    
    add_section_heading(doc, "1.1 ¿Qué es MedReminder AI?", level=2)
    add_body_p(
        doc,
        "MedReminder AI es su asistente personal de salud diseñado especialmente para ayudarle a usted y a su familia a llevar "
        "un control exacto, puntual y sin complicaciones de sus tratamientos médicos. La aplicación funciona en su teléfono "
        "inteligente Android y se encarga de recordarle en el momento justo cuándo debe tomar cada una de sus medicinas, cuántas "
        "unidades tomar y cómo tomarlas (por ejemplo, con agua o después de los alimentos).\n\n"
        "A diferencia de una alarma común de reloj que solo suena sin saber qué pastilla le toca, MedReminder AI le muestra en pantalla "
        "el nombre exacto del fármaco, la forma de la pastilla o jarabe, la dosis indicada por su médico y cuántas unidades le quedan "
        "en su botiquín de casa para que nunca se quede sin medicina."
    )
    
    add_section_heading(doc, "1.2 Marco Operativo PEAS: Cómo Cuida MedReminder AI de su Salud (Rendimiento, Entorno, Acciones y Avisos)", level=2)
    add_body_p(
        doc,
        "Para que usted y su familia tengan plena certeza de cómo funciona MedReminder AI, el sistema está organizado bajo un modelo "
        "médico formal denominado PEAS (siglas en inglés de Rendimiento, Entorno, Actuadores y Sensores). Este marco garantiza que la aplicación "
        "no sea un simple reloj despertador, sino un verdadero asistente de salud que vigila activamente su tratamiento:"
    )
    
    peas_user_data = {
        "performance": (
            "• Cumplimiento del 100%: Que usted no olvide ninguna de sus tomas de medicamentos prescritas por el médico.\n"
            "• Cero Confusión Médica: Mostrar en pantalla grande y clara qué medicina tomar, cuánta cantidad y de qué color o forma es.\n"
            "• Botiquín Siempre Lleno: Avisarle con anticipación (semáforo amarillo) antes de que se le terminen las pastillas en casa.\n"
            "• Seguridad contra Sobredosis: Impedir que se registren tomas de medicamentos dobles accidentales o que se posponga una medicina más de 2 veces."
        ),
        "performance_metrics": "Adherencia meta ≥ 95%\nCero alarmas perdidas\nAviso preventivo de stock\nTiempo de respuesta < 1 s",
        "environment": (
            "• La Vida Diaria del Paciente: Su hogar, el trabajo, actividades al aire libre o de viaje con la familia.\n"
            "• Su Teléfono Inteligente: Cualquier teléfono móvil Android de uso diario con pantalla táctil.\n"
            "• Con o Sin Internet: Funcionamiento completo en la casa con Wi-Fi, en la calle con datos o en el campo sin internet.\n"
            "• Su Rutina de Salud: Tratamientos de una pastilla al día o esquemas de múltiples tomas de medicamentos."
        ),
        "environment_metrics": "Android 8.0 o superior\nUso con o sin internet\nHogar / Trabajo / Viaje\nSoporte para cuidadores",
        "actuadores": (
            "• Alarmas Médicas Sonoras: Timbres audibles y vibración que despiertan el teléfono para avisarle puntualmente.\n"
            "• Avisos en Pantalla Flotante: Ventanas grandes Heads-Up con botones ergonómicos (mínimo 56 dp) que no cansan la vista.\n"
            "• La Voz Amable de Medi: Su acompañante virtual le habla con voz clara y le explica qué medicina debe tomar.\n"
            "• Botiquín Digital Automático: Descuenta automáticamente las pastillas de su frasco cuando pulsa «Tomar Ahora»."
        ),
        "actuadores_metrics": "Sonido médico exacto\nBotones grandes ≥ 56 dp\nVoz asistiva de Medi\nDescuento de botiquín (-1)",
        "sensores": (
            "• Reloj Interno de Alta Precisión: Mide cada segundo para hacer sonar la alarma exactamente a su hora programada.\n"
            "• Pantalla Táctil: Detecta sus toques suaves en los botones grandes para confirmar tomas de medicamentos («Tomar Ahora»), posponer u omitir.\n"
            "• Detector de Encendido (Reinicio): Si el teléfono se apaga por falta de batería, al encenderse reactiva todas sus alarmas.\n"
            "• Sensor de Batería y Red: Comprueba que el teléfono tenga pila suficiente y sincroniza los datos cuando hay Wi-Fi."
        ),
        "sensores_metrics": "Reloj RTC de hardware\nToques en pantalla táctil\nSensor de encendido (BOOT)\nDetector de conectividad"
    }
    add_peas_section(doc, peas_user_data, intro_text="", caption="Tabla 1.1: Marco Operativo PEAS de Asistencia y Cuidado para el Paciente")
    
    add_body_p(
        doc,
        "Propiedades del Entorno Cotidiano del Paciente:\n\n"
        "• El tiempo no se detiene (Dinámico): Las horas de las tomas de medicamentos avanzan aunque usted no abra la aplicación; por ello, "
        "el sistema le llamará activamente cuando llegue el momento oportuno.\n\n"
        "• Confianza Asistiva (Parcialmente Observable): La aplicación le avisa con puntualidad y descuenta el botiquín, depositando "
        "la confianza en que usted se tome la medicina con un vaso con agua al pulsar el botón.\n\n"
        "• Trabajo en Equipo (Multiagente Familiar): La aplicación ayuda al paciente, pero también permite que sus hijos o su médico "
        "estén tranquilos sabiendo que su tratamiento se cumple con exactitud."
    )
    
    add_section_heading(doc, "1.3 Tablas de Verdad de Reglas de Interacción del Paciente", level=2)
    add_body_p(
        doc,
        "Para garantizar la máxima seguridad del paciente y evitar confusiones durante el tratamiento diario, "
        "MedReminder AI gobierna cada pantalla mediante reglas matemáticas precisas conocidas como tablas de verdad. "
        "Estas reglas determinan en qué momentos exactos se activan o desactivan los botones de la aplicación, "
        "impidiendo acciones accidentales (como tomar medicamentos dos veces o posponer indefinidamente una medicina). "
        "En estas tablas, el valor 'V' significa que la condición o acción es Verdadera (habilitada), "
        "mientras que el valor 'F' significa que es Falsa (bloqueada o inactiva por seguridad):"
    )
    
    add_section_heading(doc, "1.3.1 Regla de Habilitación de Botones de Acción en Tomas de Medicamentos", level=3)
    add_body_p(
        doc,
        "Cuando llega la hora de una dosis prescrita, la aplicación evalúa tres condiciones previas para proteger al paciente:\n\n"
        "• H (Horario Activo): La alarma médica está activa o la dosis se encuentra dentro de la ventana operativa del día.\n"
        "• S (Stock en Botiquín): Existen pastillas disponibles en el botiquín de casa (existencias > 0).\n"
        "• P (Posposiciones Permitidas): El paciente ha pospuesto menos de dos veces la dosis (posposiciones < 2) y no tiene activo el Modo Castigo.\n\n"
        "A continuación se presenta la tabla de verdad formal que define qué botones se iluminan para su uso:"
    )
    u1_headers = ["H (Horario)", "S (Stock > 0)", "P (Posponer < 2)", "Tomar Ahora", "Posponer", "Omitir", "Acción Segura para el Paciente"]
    u1_rows = [
        ["V", "V", "V", "V", "V", "V", "Botones activos: el paciente puede confirmar tomas de medicamentos, posponer u omitir"],
        ["V", "V", "F", "V", "F", "V", "Límite alcanzado: posponer bloqueado; debe confirmar la toma de medicamentos u omitir con motivo"],
        ["V", "F", "V", "F", "V", "V", "Botiquín agotado: botón de toma de medicamentos bloqueado; recargar stock de pastillas o posponer"],
        ["V", "F", "F", "F", "F", "V", "Sin pastillas y límite alcanzado: solo puede omitir tomas de medicamentos con motivo"],
        ["F", "V", "V", "F", "F", "F", "Fuera de horario: botones en reposo hasta el siguiente horario programado"],
        ["F", "F", "F", "F", "F", "F", "Sin horario ni medicinas: pantalla protegida contra toques involuntarios"]
    ]
    add_truth_table(doc, u1_headers, u1_rows, "Tabla 1.2: Tabla de Verdad de Habilitación de Botones en Tomas de Medicamentos", [1.0, 1.0, 1.2, 1.0, 1.0, 1.0, 2.3])
    
    add_section_heading(doc, "1.3.2 Regla de la Función Deshacer Tomas de Medicamentos Registradas por Error", level=3)
    add_body_p(
        doc,
        "Si el paciente pulsa el botón de confirmar tomas de medicamentos por equivocación, la aplicación permite revertir "
        "la acción mediante la función 'Deshacer' bajo tres condiciones estrictas de seguridad clínica:\n\n"
        "• C (Confirmación Previa): Se acaba de registrar una confirmación de tomas de medicamentos en la pantalla actual.\n"
        "• T (Tiempo Límite): Han transcurrido 5 minutos o menos desde que se tocó el botón (ventana de seguridad).\n"
        "• M (Sin Modificaciones): No se ha efectuado otra acción posterior sobre el botiquín o receta médica.\n\n"
        "Regla Formal: La función Deshacer solo es Verdadera (V) si las tres condiciones se cumplen simultáneamente (C ∧ T ∧ M):"
    )
    u2_headers = ["C (Confirmó)", "T (Tiempo ≤ 5 min)", "M (Sin Cambios)", "Deshacer Habilitado", "Comportamiento del Asistente"]
    u2_rows = [
        ["V", "V", "V", "V", "Deshacer activo: revierte a pendiente y reintegra +1 unidad al botiquín digital"],
        ["V", "V", "F", "F", "Deshacer bloqueado: el botiquín fue modificado por otra acción posterior"],
        ["V", "F", "V", "F", "Deshacer bloqueado: venció la ventana de 5 minutos por seguridad médica"],
        ["V", "F", "F", "F", "Deshacer bloqueado: tiempo vencido y datos modificados"],
        ["F", "V", "V", "F", "Deshacer inactivo: no se ha confirmado ninguna toma de medicamentos recientemente"],
        ["F", "F", "F", "F", "Deshacer inactivo: reposo general sin acciones pendientes"]
    ]
    add_truth_table(doc, u2_headers, u2_rows, "Tabla 1.3: Tabla de Verdad de la Función Deshacer Tomas de Medicamentos", [1.1, 1.3, 1.2, 1.4, 2.8])
    
    add_section_heading(doc, "1.4 Objetivo del Manual de Usuario", level=2)
    add_body_p(
        doc,
        "Este manual está redactado pensando en usted. No contiene tecnicismos difíciles de informática ni lenguaje complicado. "
        "Su objetivo es guiarle paso a paso, con explicaciones claras, letras grandes y capturas de pantalla reales, para que aprenda a:\n\n"
        "• Registrar fácilmente sus medicinas con sus horarios prescritos.\n"
        "• Confirmar con un solo toque en pantalla cada una de sus tomas de medicamentos.\n"
        "• Posponer un recordatorio de forma segura si en ese momento se encuentra ocupado o comiendo.\n"
        "• Revisar cuántas pastillas tiene guardadas en su botiquín y recargarlas cuando compre una caja nueva en la farmacia.\n"
        "• Conversar con Medi, su robot acompañante de voz que le orientará y responderá sus dudas diarias."
    )
    
    add_section_heading(doc, "1.5 Beneficios Asistivos para el Paciente y la Familia", level=2)
    add_body_p(
        doc,
        "• Tranquilidad Mental: Elimina la angustia de preguntarse «¿ya me tomé la pastilla de la presión o se me olvidó?». La aplicación "
        "mantiene un registro claro de cada dosis atendida.\n\n"
        "• Prevención de Sobredosis: El sistema le protege impidiendo registrar dosis duplicadas por error o posponer demasiadas veces "
        "una medicina para evitar que se junten dos horarios.\n\n"
        "• Apoyo a Cuidadores y Adultos Mayores: Botones amplios y de gran tamaño (diseñados para verse y tocarse sin dificultad) y lectura "
        "en voz alta de los recordatorios para personas con fatiga visual.\n\n"
        "• Red de Seguridad Familiar: Permite registrar los números de teléfono de sus hijos, pareja o médico de cabecera para que ellos "
        "puedan estar al tanto de su bienestar."
    )
    
    add_section_heading(doc, "1.6 Acompañante Virtual Medi: Su Aliado Clínico Diario", level=2)
    add_body_p(
        doc,
        "Dentro de la aplicación vive Medi, un simpático acompañante virtual con forma de robot amigable. Medi le da los buenos días, "
        "le felicita cada vez que cumple puntualmente con sus tomas de medicamentos, le recuerda cuándo es momento de ir a la farmacia "
        "a comprar más pastillas y le habla en voz clara para resolver dudas básicas sobre su tratamiento diario."
    )
    
    # ==========================================================================
    # 2. ANTES DE COMENZAR
    # ==========================================================================
    add_section_heading(doc, "2. ANTES DE COMENZAR", level=1, page_break_before=True)
    
    add_section_heading(doc, "2.1 Requisitos del Teléfono Inteligente Android", level=2)
    add_body_p(
        doc,
        "Para disfrutar de todas las funciones de MedReminder AI, su teléfono móvil solo necesita cumplir con las siguientes características sencillas:\n\n"
        "• Sistema Operativo: Teléfono con sistema Android versión 8.0 o superior (prácticamente cualquier teléfono inteligente comercial adquirido "
        "de 2018 a la fecha es totalmente compatible).\n\n"
        "• Espacio en Memoria: Requiere menos de 50 megabytes (MB) de espacio libre para su instalación.\n\n"
        "• Bocina o Altavoz Funcional: Para escuchar con claridad los timbres médicos de aviso y las palabras habladas de Medi.\n\n"
        "• Pantalla Táctil en Buen Estado: Para interactuar cómodamente con los botones grandes de la aplicación."
    )
    
    add_section_heading(doc, "2.2 Permisos Necesarios Explicados de Forma Sencilla", level=2)
    add_body_p(
        doc,
        "Al abrir la aplicación por primera vez, su teléfono le mostrará unos mensajes solicitando permisos. Estos permisos son indispensables "
        "para proteger su salud y le explicamos para qué sirve cada uno:\n\n"
        "1. Permiso de Notificaciones en Pantalla: Permite que MedReminder AI muestre una ventana visible con el nombre de su medicina "
        "y los botones de acción cuando llegue su hora programada.\n\n"
        "2. Permiso de Alarmas y Recordatorios Exactos: Permite que el teléfono despierte a la hora y segundo exacto en que debe tomar su "
        "dosis, sonando con la misma puntualidad que el despertador de su recámara.\n\n"
        "3. Permiso de Exención de Ahorro de Batería (Desactivar optimización de energía): Los teléfonos modernos intentan ahorrar pila "
        "apagando o congelando aplicaciones que no se tocan en horas. Al conceder este permiso, nos aseguramos de que el teléfono jamás "
        "apague a MedReminder AI, garantizando que su alarma suene puntualmente aunque no haya tocado el teléfono en todo el día."
    )
    
    add_callout(
        doc,
        "Si su teléfono le pregunta «¿Desea permitir que MedReminder AI se ejecute siempre en segundo plano?», seleccione siempre la opción "
        "«PERMITIR» o «SIN RESTRICCIONES». Esto garantiza que sus recordatorios de tomas de medicamentos jamás se silencien solos.",
        callout_type="warn",
        title="RECOMENDACIÓN CRÍTICA DE CONFIGURACIÓN"
    )
    
    perm_headers = ["Permiso del Dispositivo", "Propósito en MedReminder AI", "Efecto Clínico si se Rechaza"]
    perm_rows = [
        ["Notificaciones Prioritarias", "Mostrar alertas visuales y Heads-Up flotantes de tomas de medicamentos.", "El paciente no observará los avisos en pantalla ni los recordatorios urgentes."],
        ["Alarmas Deterministas Exactas", "Despertar al procesador del teléfono al segundo exacto prescrito por el médico.", "El sistema operativo Android retrasará las tomas de medicamentos minutos u horas."],
        ["Exención de Ahorro de Batería", "Prevenir que el teléfono hiberne o congele los servicios de MedReminder AI.", "El recordatorio no sonará si el teléfono permanece varias horas en reposo."],
        ["Reinicio Automático del Dispositivo", "Restaurar las alarmas programadas en caso de apagado o reinicio del teléfono.", "Las alarmas pendientes se perderían por completo tras encender el móvil."],
        ["Acceso a Micrófono y Audio", "Facilitar el dictado por voz y la interacción accesible con la asistente Medi.", "Medi responderá únicamente por texto escrito en pantalla sin diálogo por voz."]
    ]
    add_truth_table(doc, perm_headers, perm_rows, "Tabla 2.1: Matriz de Permisos del Sistema Operativo Android y Justificación Clínica", [2.0, 2.2, 2.3])
    
    add_section_heading(doc, "2.3 Recomendaciones de Volumen, Sonido y Vibración", level=2)
    add_body_p(
        doc,
        "• Nivel de Volumen: Ajuste el volumen de 'Alarma' de su teléfono en un nivel medio-alto (al menos al 70 %). Si suele dejar el teléfono en la "
        "sala o en la bolsa de mano, un buen volumen le asegurará escuchar el aviso desde otra habitación.\n\n"
        "• Vibración Activa: Mantenga encendida la vibración del teléfono. Si se encuentra en una reunión, en la iglesia o en la calle con mucho ruido, "
        "sentirá la vibración en su bolsillo avisándole que es momento de su dosis médica."
    )
    
    add_section_heading(doc, "2.4 Conectividad: Funcionamiento con y sin Internet", level=2)
    add_body_p(
        doc,
        "Una de las mayores virtudes de MedReminder AI es su independencia total del internet:\n\n"
        "• ¿Se le acabaron los datos móviles o no tiene saldo? No se preocupe: sus alarmas sonarán exactamente igual.\n"
        "• ¿Se encuentra en el campo, en un sótano o en modo avión? Las alarmas de tomas de medicamentos se guardan en el reloj interno "
        "de su teléfono y sonarán sin falta.\n"
        "• ¿Cuándo se usa el internet? Solo cuando usted se conecta a una red Wi-Fi en casa o enciende sus datos, la aplicación aprovecha para "
        "guardar una copia de respaldo segura en la nube y sincronizar con su familia."
    )
    
    # ==========================================================================
    # 3. PRIMEROS PASOS
    # ==========================================================================
    add_section_heading(doc, "3. PRIMEROS PASOS", level=1, page_break_before=True)
    
    add_section_heading(doc, "3.1 Apertura de la Aplicación en su Teléfono", level=2)
    add_body_p(
        doc,
        "Para iniciar, busque en la pantalla de su teléfono el icono con forma de píldora verde médica y el nombre «MedReminder AI». "
        "Toque el icono una sola vez para abrir el sistema. Verá una pantalla de bienvenida sobria y clara diseñada para no cansar su vista."
    )
    
    add_section_heading(doc, "3.2 Pantalla de Inicio de Sesión («Iniciar Sesión»)", level=2)
    add_body_p(
        doc,
        "La pantalla de acceso protege la privacidad de sus recetas y tratamientos médicos mediante un inicio seguro:\n\n"
        "• Campo de Correo Electrónico: Escriba aquí su dirección de correo (por ejemplo: paciente@ejemplo.com).\n\n"
        "• Campo de Contraseña: Escriba su clave secreta. La aplicación muestra puntitos para que nadie a su alrededor pueda verla.\n\n"
        "• Botón «Iniciar Sesión»: Toque el botón azul marino de gran tamaño para entrar al sistema de inmediato.\n\n"
        "• Opción «¿No tienes cuenta? Regístrate aquí»: Si es la primera vez que usa la aplicación, toque este enlace inferior para crear su cuenta en un minuto."
    )
    
    if os.path.exists("docs/screenshots/01_login.png"):
        add_figure_image(doc, "docs/screenshots/01_login.png", "Figura 3.1: Pantalla de inicio de sesión seguro en MedReminder AI", 2.8)
        
    add_section_heading(doc, "3.3 Pantalla de Registro («Crear Cuenta»)", level=2)
    add_body_p(
        doc,
        "Si aún no tiene una cuenta personal, la pantalla de registro le solicita datos mínimos y seguros:\n\n"
        "1. Nombre Completo: Ingrese su nombre para que Medi pueda dirigirse a usted de manera respetuosa y personalizada.\n\n"
        "2. Correo Electrónico: Servirá como su llave de acceso única al sistema.\n\n"
        "3. Contraseña Segura: Ingrese una contraseña de al menos 6 caracteres. La barra inferior le indicará en color verde cuando sea lo suficientemente fuerte.\n\n"
        "4. Certificación de Privacidad Clínica: Marque la casilla confirmando que acepta la protección confidencial de sus datos médicos personales.\n\n"
        "5. Botón «Crear Cuenta»: Toque el botón para quedar registrado y acceder directamente a su panel médico principal."
    )
    
    if os.path.exists("docs/screenshots/08_registro.png"):
        add_figure_image(doc, "docs/screenshots/08_registro.png", "Figura 3.2: Pantalla de registro de nuevos pacientes con certificación de privacidad", 2.8)
        
    add_section_heading(doc, "3.4 Navegación General por la Barra Inferior", level=2)
    add_body_p(
        doc,
        "En la parte inferior de la pantalla encontrará siempre accesible la barra de navegación con cinco botones ilustrados con iconos claros:\n\n"
        "• Hoy (Icono de Calendario): Es la pantalla principal donde verá los medicamentos que le tocan en el día organizados por horario.\n"
        "• Medicamentos (Icono de Píldora): Catálogo completo donde puede registrar nuevas medicinas y editar sus recetas médicas.\n"
        "• Botiquín (Icono de Maletín Médico): Vista del inventario de pastillas que tiene guardadas en su cajón o alacena.\n"
        "• Progreso (Icono de Gráfica): Panel donde consulta sus días de racha continua, medallas ganadas y el árbol de decisiones de IA.\n"
        "• Apoyo (Icono de Teléfono / Cruz Médica): Directorio de contactos familiares para avisar en caso de emergencia médica."
    )
    
    # ==========================================================================
    # 4. FUNCIONES (CON ESTRUCTURA FIJA POR TAREA: OBJETIVO, PASOS NUMERADOS, RESULTADO ESPERADO Y ADVERTENCIAS)
    # ==========================================================================
    add_section_heading(doc, "4. FUNCIONES (CON ESTRUCTURA FIJA POR TAREA: OBJETIVO, PASOS NUMERADOS, RESULTADO ESPERADO Y ADVERTENCIAS)", level=1, page_break_before=True)
    
    add_body_p(
        doc,
        "A continuación se detallan las 10 tareas asistenciales clave para el paciente y cuidador familiar. "
        "Cada tarea dispone de pasos directos diseñados para minimizar la carga cognitiva y evitar fallos táctiles involuntarios. "
        "La siguiente tabla resume la semántica ergonómica de los botones de interacción clínica disponibles en cada recordatorio."
    )
    
    btn_headers = ["Botón de Acción", "Propósito Clínico y Momento de Uso", "Impacto en Tomas de Medicamentos y Botiquín"]
    btn_rows = [
        ["🟢 Tomar Ahora", "Pulsar al momento exacto de ingerir el medicamento prescrito.", "Registra la toma de medicamentos con timestamp legal y descuenta 1 unidad del stock."],
        ["🟡 Posponer (+10 min)", "Aplazar la alarma si está comiendo, manejando o temporalmente ocupado.", "Reprograma la alarma exactamente 10 minutos (máximo 2 posposiciones consecutivas)."],
        ["⚪ Omitir toma de medicamentos", "Utilizar únicamente si el médico suspendió la dosis o por indicación clínica.", "Registra la omisión justificada con notas clínicas sin descontar unidades del stock."],
        ["🔵 Deshacer tomas de medicamentos", "Pulsación accidental involuntaria sobre el botón 'Tomar Ahora'.", "Disponible por 5 segundos en la barra inferior para anular el registro y restaurar el stock."]
    ]
    add_truth_table(doc, btn_headers, btn_rows, "Tabla 4.1: Catálogo de Botones de Acción en Recordatorios de Tomas de Medicamentos", [1.8, 2.3, 2.4])
    
    # --------------------------------------------------------------------------
    # Tarea 4.1
    # --------------------------------------------------------------------------
    add_section_heading(doc, "Tarea 4.1: Alta de un nuevo medicamento y programación de horarios", level=2)
    add_body_p(
        doc,
        "Objetivo de la Tarea:\n"
        "Registrar un nuevo fármaco recetado por su médico tratante, especificando su nombre, dosis exacta, forma farmacéutica "
        "y el horario en que deben comenzar sus tomas de medicamentos.\n\n"
        "Pasos Numerados:\n"
        "1. Desde la barra inferior, toque la pestaña «Medicamentos» y pulse el botón verde '+ Nuevo Medicamento'.\n"
        "2. En el campo 'Nombre del Medicamento', escriba el nombre comercial (por ejemplo: Losartán o Paracetamol).\n"
        "3. En 'Principio Activo', capture la sustancia química principal indicada en su receta médica.\n"
        "4. Seleccione la 'Presentación': elija si se trata de Comprimidos, Gotas, Jarabe, Suspensión o Inyección.\n"
        "5. Ingrese la 'Dosis por toma de medicamentos': escriba la cantidad indicada por el médico (ejemplo: '1 comprimido de 50 mg').\n"
        "6. Ingrese el 'Stock Inicial' y el 'Límite de Advertencia': indique cuántas pastillas vienen en la caja comprada (ejemplo: 30) "
        "y a partir de cuántas unidades desea que el sistema le avise para comprar más (ejemplo: 5).\n"
        "7. Defina el 'Horario e Intervalo': seleccione la hora de la primera dosis y la frecuencia (cada 6, 8, 12 o 24 horas).\n"
        "8. Pulse el botón inferior «Guardar Medicamento».\n\n"
        "Resultado Esperado:\n"
        "La aplicación valida los datos al instante, genera automáticamente el calendario de tomas de medicamentos para los próximos días "
        "y programa las alarmas acústicas deterministas en su teléfono. Verá una tarjeta verde confirmando: «Medicamento registrado con éxito».\n\n"
        "Advertencias:\n"
        "• No ingrese dosis con cantidades negativas ni deje el nombre vacío; el sistema bloqueará el guardado.\n"
        "• Si tiene registrada una alergia al fármaco ingresado, la aplicación bloqueará el registro con una advertencia roja para proteger su vida."
    )
    
    if os.path.exists("docs/screenshots/03_nuevo_medicamento.png"):
        add_figure_image(doc, "docs/screenshots/03_nuevo_medicamento.png", "Figura 4.1: Pantalla de registro de nuevo medicamento y prescripción horaria", 2.8)
        
    # --------------------------------------------------------------------------
    # Tarea 4.2
    # --------------------------------------------------------------------------
    add_section_heading(doc, "Tarea 4.2: Confirmación de tomas de medicamentos desde la vista «Hoy»", level=2)
    add_body_p(
        doc,
        "Objetivo de la Tarea:\n"
        "Confirmar que ha ingerido físicamente su medicamento en la hora estipulada, registrando el evento de manera inmutable en su "
        "expediente médico y descontando la unidad de su botiquín.\n\n"
        "Pasos Numerados:\n"
        "1. Al sonar la alarma médica o al ingresar a la aplicación, toque la pestaña «Hoy» en la barra inferior.\n"
        "2. Identifique la tarjeta de la dosis en turno: revise el nombre del medicamento, la hora programada y la dosis.\n"
        "3. Ingiere su medicamento con agua según las instrucciones clínicas indicadas en pantalla.\n"
        "4. Presione el botón verde grande «Tomar Ahora» (con altura de 56 dp para evitar fallos táctiles).\n\n"
        "Resultado Esperado:\n"
        "El botón se desactivará inmediatamente para evitar toques dobles por error, el sistema marcará la dosis como 'tomada' con una "
        "palomita verde, descontará automáticamente 1 pastilla del botiquín digital y sumará +1 día a su racha de honor.\n\n"
        "Advertencias:\n"
        "• Solo presione «Tomar Ahora» después de haberse tomado realmente la pastilla. Si pulsa el botón sin tomarla, el conteo de pastillas de su "
        "caja física ya no coincidirá con el botiquín de la aplicación."
    )
    
    if os.path.exists("docs/screenshots/02_hoy.png"):
        add_figure_image(doc, "docs/screenshots/02_hoy.png", "Figura 4.2: Pantalla principal «Hoy» con tarjetas de recordatorios y botón ergonómico de 56 dp", 2.8)
        
    # --------------------------------------------------------------------------
    # Tarea 4.3
    # --------------------------------------------------------------------------
    add_section_heading(doc, "Tarea 4.3: Posponer tomas de medicamentos (+10 minutos o +30 minutos)", level=2)
    add_body_p(
        doc,
        "Objetivo de la Tarea:\n"
        "Silenciar temporalmente una alarma de tomas de medicamentos cuando se encuentre manejando, en una junta o comiendo, "
        "reprogramando el recordatorio para que vuelva a sonar de manera determinista unos minutos más tarde.\n\n"
        "Pasos Numerados:\n"
        "1. En la tarjeta del recordatorio activo, localice el botón secundario color ámbar «Posponer 30 min» (o +10 min según su ajuste).\n"
        "2. Pulse el botón «Posponer» una sola vez.\n"
        "3. Observe el mensaje en pantalla: la aplicación silenciará la alarma y mostrará el contador: 'Pospuesto (1 de 2 permitidos)'.\n\n"
        "Resultado Esperado:\n"
        "La alarma se silencia de inmediato y se reprograma en el reloj interno de su teléfono para despertar con timbre sonoro exacto al cumplirse el tiempo.\n\n"
        "Advertencias:\n"
        "• Regla de Oro de Seguridad Clínica: Solo se permite posponer un máximo de dos veces por cada toma de medicamentos. Tras la segunda "
        "posposición, el botón desaparecerá de la pantalla y estará obligado a confirmar la toma de medicamentos o registrar la omisión justificada. "
        "Esta restricción protege su salud impidiendo que dos dosis se junten y causen intoxicación."
    )
    
    # --------------------------------------------------------------------------
    # Tarea 4.4
    # --------------------------------------------------------------------------
    add_section_heading(doc, "Tarea 4.4: Omitir tomas de medicamentos con justificación clínica", level=2)
    add_body_p(
        doc,
        "Objetivo de la Tarea:\n"
        "Registrar formalmente que una dosis prescrita no fue administrada por una causa médica de fuerza mayor (como náuseas, ayuno "
        "por análisis de sangre o falta transitoria de medicamento), archivando el motivo para el doctor.\n\n"
        "Pasos Numerados:\n"
        "1. En la tarjeta de la dosis en turno, pulse la opción «Omitir Dosis».\n"
        "2. Se abrirá una ventana emergente titulada 'Registro de Omisión Médica'.\n"
        "3. Seleccione el motivo de la lista sugerida ('Ayuno por análisis clínicos', 'Malestar estomacal', 'Falta de pastillas en casa') "
        "o escriba una nota breve personalizada.\n"
        "4. Presione el botón «Confirmar Omisión».\n\n"
        "Resultado Esperado:\n"
        "La dosis queda archivada con el estado 'omitida' en su historial. A diferencia de cuando realiza la toma de medicamentos, el sistema NO descuenta "
        "ninguna unidad de su botiquín, manteniendo la concordancia matemática entre su caja física y la aplicación.\n\n"
        "Advertencias:\n"
        "• No omita sus tomas de medicamentos de forma habitual sin consultar a su médico tratante. La omisión repetida compromete la efectividad "
        "del tratamiento y puede reactivar síntomas de su enfermedad."
    )
    
    # --------------------------------------------------------------------------
    # Tarea 4.5
    # --------------------------------------------------------------------------
    add_section_heading(doc, "Tarea 4.5: Deshacer tomas de medicamentos registradas por error", level=2)
    add_body_p(
        doc,
        "Objetivo de la Tarea:\n"
        "Revertir de forma inmediata una acción si tocó por descuido el botón 'Tomar Ahora' sin haber tomado la medicina, o si marcó 'Omitir' "
        "por equivocación.\n\n"
        "Pasos Numerados:\n"
        "1. Inmediatamente después de confirmar, observe la barra inferior o la tarjeta resuelta donde aparecerá el botón «Deshacer».\n"
        "2. Presione «Deshacer» dentro de la ventana de tiempo permitida.\n"
        "3. El sistema devolverá el recordatorio al estado 'pendiente'.\n\n"
        "Resultado Esperado:\n"
        "La toma de medicamentos vuelve a quedar pendiente de confirmación y el sistema suma automáticamente +1 al stock de su botiquín, "
        "reparando cualquier descuadre de inventario al instante.\n\n"
        "Advertencias:\n"
        "• La función «Deshacer» solo está disponible durante la jornada activa. No intente deshacer tomas de medicamentos de días anteriores "
        "para evitar alterar la validez legal de su bitácora médica."
    )
    
    # --------------------------------------------------------------------------
    # Tarea 4.6
    # --------------------------------------------------------------------------
    add_section_heading(doc, "Tarea 4.6: Gestión y recarga rápida de stock en «Mi Botiquín» (+30 unidades)", level=2)
    add_body_p(
        doc,
        "Objetivo de la Tarea:\n"
        "Supervisar cuántas pastillas o frascos le quedan en casa y registrar rápidamente la compra de una caja nueva en la farmacia con un solo toque.\n\n"
        "Pasos Numerados:\n"
        "1. Toque la pestaña «Botiquín» en la barra inferior de navegación.\n"
        "2. Observe el 'Semáforo de Existencias': cada medicamento tiene un círculo de color (Verde = Suministro seguro; Amarillo = Próximo a agotarse; Rojo = Urgente comprar).\n"
        "3. Ubique el medicamento del cual compró una caja nueva.\n"
        "4. Toque el botón de recarga rápida «+30 unidades» (o pulse 'Editar Stock' para capturar otra cantidad).\n"
        "5. Confirme la operación.\n\n"
        "Resultado Esperado:\n"
        "El contador de unidades se incrementa de inmediato (+30 pastillas), el semáforo cambia a color verde de tranquilidad y desaparece "
        "cualquier alerta de desabastecimiento pendiente.\n\n"
        "Advertencias:\n"
        "• Si el semáforo de un fármaco esencial para su corazón o glucosa se pone en color Rojo, acuda a la farmacia el mismo día para evitar "
        "quedarse sin dosis a mitad de la noche."
    )
    
    if os.path.exists("docs/screenshots/04_botiquin.png"):
        add_figure_image(doc, "docs/screenshots/04_botiquin.png", "Figura 4.3: Vista de «Mi Botiquín» con semáforo de existencias y botones de recarga rápida", 2.8)
        
    # --------------------------------------------------------------------------
    # Tarea 4.7
    # --------------------------------------------------------------------------
    add_section_heading(doc, "Tarea 4.7: Consulta y diálogo asistido por voz con Medi", level=2)
    add_body_p(
        doc,
        "Objetivo de la Tarea:\n"
        "Interactuar mediante texto o voz con el asistente Medi para consultar dudas sencillas sobre cómo tomar sus fármacos, revisar su horario "
        "o recibir palabras de aliento durante su tratamiento.\n\n"
        "Pasos Numerados:\n"
        "1. Toque la sección de Medi (icono de robot o tarjeta superior en la vista principal).\n"
        "2. En la barra de mensaje, escriba su pregunta (por ejemplo: «¿A qué hora me toca el Losartán?» o «¿Cuántas pastillas me quedan?»).\n"
        "3. Si lo prefiere, toque el icono de micrófono para dictar su pregunta con su voz.\n"
        "4. Pulse el botón azul de enviar.\n\n"
        "Resultado Esperado:\n"
        "Medi responderá en la pantalla con un mensaje cálido y comprensible, y reproducirá la respuesta en voz alta por el altavoz de su teléfono "
        "para que no tenga que forzar la vista.\n\n"
        "Advertencias:\n"
        "• Medi es un asistente informático de apoyo, NO un médico humano. Jamás modifique la dosis de una medicina sin la orden explícita de su médico."
    )
    
    if os.path.exists("docs/screenshots/06_medi_companion.png"):
        add_figure_image(doc, "docs/screenshots/06_medi_companion.png", "Figura 4.4: Interfaz conversacional del acompañante virtual Medi con síntesis de voz", 2.8)
        
    # --------------------------------------------------------------------------
    # Tarea 4.8
    # --------------------------------------------------------------------------
    add_section_heading(doc, "Tarea 4.8: Consulta de contactos de emergencia y red de apoyo médico", level=2)
    add_body_p(
        doc,
        "Objetivo de la Tarea:\n"
        "Registrar los números telefónicos y datos de sus familiares de mayor confianza y de su médico de cabecera para disponer de llamadas "
        "rápidas en caso de sentirse mal.\n\n"
        "Pasos Numerados:\n"
        "1. Toque la pestaña «Apoyo» en la barra inferior.\n"
        "2. Pulse el botón '+ Añadir nuevo contacto de apoyo'.\n"
        "3. Ingrese el Nombre completo, Parentesco (ejemplo: Hija, Esposo, Médico) y su Número Telefónico de 10 dígitos.\n"
        "4. Active la casilla 'Recibir alertas de emergencia' si desea que este contacto sea notificado si usted llega a olvidar tomas de medicamentos consecutivas.\n"
        "5. Pulse «Guardar Contacto».\n\n"
        "Resultado Esperado:\n"
        "El contacto quedará guardado en su directorio de seguridad con un botón verde de llamada directa con un solo toque.\n\n"
        "Advertencias:\n"
        "• Verifique que el número telefónico ingresado esté correcto y activo para que las llamadas o mensajes de auxilio lleguen sin demora."
    )
    
    if os.path.exists("docs/screenshots/07_salud_apoyo.png"):
        add_figure_image(doc, "docs/screenshots/07_salud_apoyo.png", "Figura 4.5: Pantalla de «Salud y Apoyo» con red familiar y directorio de alergias clínicas", 2.8)
        
    # --------------------------------------------------------------------------
    # Tarea 4.9
    # --------------------------------------------------------------------------
    add_section_heading(doc, "Tarea 4.9: Consulta del árbol de análisis de Inteligencia Artificial", level=2)
    add_body_p(
        doc,
        "Objetivo de la Tarea:\n"
        "Visualizar de forma gráfica cómo la Inteligencia Artificial del sistema analiza sus posibles caminos de cumplimiento y poda las "
        "rutas peligrosas (como posponer indefinidamente).\n\n"
        "Pasos Numerados:\n"
        "1. Ingrese a la pestaña «Progreso» en la barra inferior.\n"
        "2. Deslícese hacia abajo hasta la sección 'Árbol de Decisión y Análisis de Rutas (DFS)'.\n"
        "3. Observe el esquema visual de nodos y flechas que muestra su camino actual hacia la adherencia perfecta.\n\n"
        "Resultado Esperado:\n"
        "Podrá apreciar cómo el sistema resalta en color verde la ruta directa de cumplimiento puntual y marca en color rojo tachado "
        "las ramas podadas (aquellas donde se intentaron más de dos posposiciones o donde había riesgo de ciclo sin fin).\n\n"
        "Advertencias:\n"
        "• Esta vista es de carácter puramente informativo y visual; no necesita modificar nada en ella para que sus alarmas funcionen."
    )
    
    if os.path.exists("docs/screenshots/05_analisis_dfs.png"):
        add_figure_image(doc, "docs/screenshots/05_analisis_dfs.png", "Figura 4.6: Visualización gráfica del árbol de análisis de Inteligencia Artificial en Android", 2.8)
        
    # --------------------------------------------------------------------------
    # Tarea 4.10
    # --------------------------------------------------------------------------
    add_section_heading(doc, "Tarea 4.10: Monitoreo de adherencia, rachas de honor y cumplimiento diario", level=2)
    add_body_p(
        doc,
        "Objetivo de la Tarea:\n"
        "Consultar su porcentaje de éxito médico mensual, su racha de días continuos sin faltas y el estado de sus escudos protectores.\n\n"
        "Pasos Numerados:\n"
        "1. Toque la pestaña «Progreso» en la barra inferior.\n"
        "2. Revise el indicador circular de 'Adherencia Terapéutica' (la meta médica recomendada es mantenerse por encima del 95 %).\n"
        "3. Revise su 'Racha Actual': indica cuántos días continuos lleva cumpliendo todas sus tomas de medicamentos a tiempo.\n"
        "4. Consulte sus 'Escudos Protectores': los escudos perdonan una omisión accidental por viaje o evento inesperado sin reiniciar su racha a cero.\n\n"
        "Resultado Esperado:\n"
        "Conforme sume semanas de puntualidad, su nivel ascenderá desde el Rango Hierro hasta Bronce, Plata, Oro y Diamante, recibiendo felicitaciones de Medi.\n\n"
        "Advertencias:\n"
        "• Si acumula varias omisiones continuas y se le acaban los escudos, el sistema activará el «Modo Castigo», el cual bloqueará temporalmente "
        "el botón de posponer para obligarle a retomar la disciplina de sus medicamentos."
    )
    
    # ==========================================================================
    # 5. FLUJOS DE TRABAJO
    # ==========================================================================
    add_section_heading(doc, "5. FLUJOS DE TRABAJO", level=1, page_break_before=True)
    
    add_section_heading(doc, "5.1 Flujo Diario Típico del Paciente (Mañana, Tarde y Noche)", level=2)
    add_body_p(
        doc,
        "El uso cotidiano de MedReminder AI se integra con armonía en su rutina diaria en tres momentos clave:\n\n"
        "• Mañana (Dosis Matutina - Ejemplo: 08:00 AM):\n"
        "  1. La alarma médica suena con timbre alegre y Medi lee en voz alta: «Buenos días. Es hora de su Losartán de 50 mg».\n"
        "  2. El paciente desayuna, ingiere su dosis de toma de medicamentos con un vaso de agua y pulsa el botón verde «Tomar Ahora».\n"
        "  3. La app descuenta 1 pastilla y felicita al paciente con un mensaje motivacional.\n\n"
        "• Tarde (Dosis Vespertina - Ejemplo: 02:00 PM):\n"
        "  1. La alarma suena mientras el paciente está cocinando o platicando con familiares.\n"
        "  2. El paciente pulsa «Posponer 30 min» para terminar su comida con tranquilidad.\n"
        "  3. Exactamente a las 02:30 PM, la alarma vuelve a sonar. El paciente ingiere su cápsula y pulsa «Tomar Ahora».\n\n"
        "• Noche (Dosis Nocturna y Cierre del Día - Ejemplo: 10:00 PM):\n"
        "  1. Suena el último recordatorio del día antes de dormir.\n"
        "  2. El paciente cumple la toma de medicamentos prescrita y pulsa «Tomar Ahora».\n"
        "  3. La app actualiza la racha diaria sumando +1 día de éxito y muestra: «¡Excelente jornada! Ha cumplido el 100 % de su tratamiento hoy»."
    )
    
    add_section_heading(doc, "5.2 Flujo de Compra y Reposición de Farmacia", level=2)
    add_body_p(
        doc,
        "1. Alerta Preventiva: Cuando el stock de un medicamento llega a 5 unidades o menos, la app emite un aviso amarillo suave: «Le quedan 5 pastillas de Metformina. Es momento de surtir su receta».\n"
        "2. Visita a la Farmacia: El paciente o su familiar acude a la farmacia y adquiere una caja nueva de 30 o 60 pastillas.\n"
        "3. Actualización Rápida: Al regresar a casa, el paciente entra a «Mi Botiquín», toca el medicamento y pulsa el botón «+30 unidades».\n"
        "4. Tranquilidad Restablecida: El semáforo vuelve a color verde y el sistema registra que hay fármaco suficiente para las próximas semanas."
    )
    
    add_section_heading(doc, "5.3 Flujo de Reporte a Familiares o Cuidadores de Confianza", level=2)
    add_body_p(
        doc,
        "Los familiares que cuidan a un adulto mayor pueden sincronizar el reporte semanal:\n"
        "1. Al finalizar la semana, el paciente o cuidador abre la pestaña «Progreso».\n"
        "2. Se observa el resumen semanal con los porcentajes de tomas de medicamentos cumplidas.\n"
        "3. Mediante el botón «Compartir Resumen», se genera un mensaje claro para WhatsApp o correo destinado a los hijos o al médico familiar, "
        "demostrando que el paciente se está cuidando responsablemente."
    )
    
    add_section_heading(doc, "5.4 Flujo de Emergencia ante Olvido Prolongado", level=2)
    add_body_p(
        doc,
        "Si por alguna eventualidad (un desmayo, un traslado médico o un olvido grave) una dosis crítica no se confirma tras varias horas de aviso:\n"
        "1. El sistema detecta que la toma de medicamentos lleva más de 4 horas de retraso sin respuesta.\n"
        "2. En la pantalla «Apoyo», se activa el banner de alerta prioritaria.\n"
        "3. La aplicación envía un aviso inmediato o sugiere llamar al contacto de emergencia principal registrado (por ejemplo: la hija del paciente) "
        "para que pueda acudir a la casa o comunicarse por teléfono y verificar el estado de salud del enfermo."
    )
    
    # ==========================================================================
    # 6. ERRORES Y SOLUCIONES
    # ==========================================================================
    add_section_heading(doc, "6. ERRORES Y SOLUCIONES", level=1, page_break_before=True)
    add_body_p(
        doc,
        "Si experimenta alguna dificultad con la aplicación, consulte la siguiente tabla amigable de soluciones rápidas:"
    )
    
    err_headers = ["¿Qué problema tiene?", "¿Por qué sucede esto?", "¿Cómo solucionarlo paso a paso?"]
    err_rows = [
        [
            "La alarma médica no suena cuando la pantalla del teléfono está apagada.",
            "El sistema de ahorro de batería de su teléfono puso la aplicación en modo reposo profundo.",
            "Vaya a Ajustes de su teléfono > Aplicaciones > MedReminder AI > Batería > Elija la opción 'Sin restricciones' o 'No optimizar'."
        ],
        [
            "La aplicación se cierra sola o dice 'Error de conexión con el servidor'.",
            "Su teléfono no tiene conexión a la red Wi-Fi o la dirección de internet del servidor cambió.",
            "No se alarme: sus alarmas seguirán sonando offline. Conéctese a su red Wi-Fi habitual o espere unos minutos a que se reanude el servicio."
        ],
        [
            "Toqué el botón 'Tomar Ahora' por error pero no me tomé la pastilla.",
            "Ocurrió un toque involuntario sobre la pantalla táctil.",
            "En la tarjeta de la dosis resuelta, presione inmediatamente el botón 'Deshacer'. El recordatorio volverá a estar pendiente y el stock se devolverá."
        ],
        [
            "El botiquín marca existencias en CERO pero sí tengo pastillas en casa.",
            "Olvidó registrar la caja nueva que compró en la farmacia la semana pasada.",
            "Abra la pestaña 'Botiquín', toque el fármaco y presione '+30 unidades' (o el botón 'Editar Stock') para escribir el número de pastillas que tiene en su frasco."
        ],
        [
            "Cambié de teléfono celular y no veo mis medicamentos.",
            "Instaló la aplicación en un teléfono nuevo pero aún no ha iniciado sesión con su cuenta.",
            "En la pantalla inicial, no cree una cuenta nueva. Pulse 'Iniciar Sesión', escriba su correo y su contraseña de siempre; sus recetas se descargarán solas."
        ]
    ]
    add_truth_table(doc, err_headers, err_rows, "Tabla 6.1: Catálogo de Incidencias Frecuentes y Solución Rápida para el Paciente", [2.0, 2.0, 2.5])
    
    # ==========================================================================
    # 7. PREGUNTAS FRECUENTES (FAQ)
    # ==========================================================================
    add_section_heading(doc, "7. PREGUNTAS FRECUENTES (FAQ)", level=1, page_break_before=True)
    add_body_p(
        doc,
        "1. ¿Necesito tener internet o saldo en mi teléfono para que suenen las alarmas médicas?\n"
        "Respuesta: NO. Absolutamente todas las alarmas de tomas de medicamentos se programan en el reloj de hardware interno de su teléfono. "
        "Sonarán con toda la potencia de su altavoz incluso si su teléfono está en modo avión, en un sótano sin señal o sin un solo peso de saldo.\n\n"
        "2. ¿Puedo registrar jarabes, gotas para los ojos o inyecciones además de pastillas?\n"
        "Respuesta: SÍ. Al registrar o editar un medicamento, puede elegir la presentación que le haya recetado su doctor: comprimidos, gotas, "
        "jarabe, suspensión, pomada o inyecciones, especificando la dosis exacta que debe administrarse.\n\n"
        "3. ¿Qué ocurre si salgo de viaje a una ciudad o país con otro horario?\n"
        "Respuesta: MedReminder AI gestiona los tiempos en formato universal. Al cambiar la hora de su teléfono móvil de forma automática, "
        "la aplicación ajusta los horarios en pantalla para que el intervalo de horas entre dosis (por ejemplo, cada 8 horas) se conserve exacto.\n\n"
        "4. ¿Cómo puedo mostrarle a mi médico de cabecera si he sido cumplido con mi tratamiento?\n"
        "Respuesta: Durante su consulta médica, abra la pestaña «Progreso». Allí su doctor podrá ver de inmediato su porcentaje de adherencia, "
        "las fechas y horas exactas en que confirmó cada una de sus tomas de medicamentos y si hubo alguna omisión justificada por malestar.\n\n"
        "5. ¿Por qué desapareció el botón 'Posponer' en una de mis tomas de medicamentos?\n"
        "Respuesta: Por seguridad para su salud. La aplicación solo le permite posponer un máximo de dos veces (1 hora en total). Al agotar "
        "los dos intentos, el botón se bloquea para recordarle que debe tomar la dosis de inmediato o registrar la omisión médica.\n\n"
        "6. ¿Qué pasa si se me descarga el teléfono por la noche?\n"
        "Respuesta: En cuanto conecte su teléfono al cargador y se encienda, el sistema inteligente BootCompletedReceiver de MedReminder AI "
        "se activará automáticamente y reprogramará todas las alarmas de las tomas de medicamentos pendientes del día sin que tenga que abrir la app.\n\n"
        "7. ¿Es seguro guardar mis datos de salud en esta aplicación?\n"
        "Respuesta: Totalmente seguro. Sus contraseñas e información médica se encuentran blindadas bajo protocolos de cifrado y privacidad "
        "clínica. Nadie ajeno a usted y a sus contactos autorizados puede acceder a sus recetas.\n\n"
        "8. ¿Puedo cambiar la dosis de un medicamento si mi médico me la ajustó?\n"
        "Respuesta: Sí. En la pestaña «Medicamentos», toque el fármaco y seleccione 'Editar'. Modifique la dosis según la nueva orden médica; "
        "el cambio se aplicará a partir de la siguiente toma de medicamentos, preservando intacto el historial anterior."
    )
    
    # ==========================================================================
    # 8. RECOMENDACIONES
    # ==========================================================================
    add_section_heading(doc, "8. RECOMENDACIONES", level=1, page_break_before=True)
    
    add_section_heading(doc, "8.1 Recomendaciones Médicas para la Adherencia Farmacológica", level=2)
    add_body_p(
        doc,
        "• Acompañe siempre sus pastillas con agua natural: Evite ingerir medicamentos con refrescos, jugos ácidos de toronja o café, "
        "salvo que su médico le indique expresamente lo contrario.\n\n"
        "• Respete las indicaciones de comida: Si su receta indica 'tomar después de los alimentos', procure comer algo ligero antes de "
        "confirmar la dosis para proteger la mucosa de su estómago.\n\n"
        "• Jamás duplique una dosis por un olvido: Si olvidó una dosis por muchas horas y ya está cerca la siguiente, consulte a su médico o "
        "registre la omisión justificada. Tomar dos dosis juntas puede causar una intoxicación peligrosa."
    )
    
    add_section_heading(doc, "8.2 Cuidados en el Almacenamiento Físico de Medicamentos", level=2)
    add_body_p(
        doc,
        "• Guarde sus cajas en un lugar fresco y seco: Evite dejar sus medicinas en el baño o en la cocina, ya que la humedad y el calor "
        "del vapor degradan los principios activos de las pastillas.\n\n"
        "• Mantenga los frascos fuera del alcance de niños y mascotas: Guarde su botiquín en un cajón alto o alacena segura.\n\n"
        "• Revise periódicamente la fecha de caducidad: Al surtir su botiquín en la aplicación, verifique la fecha impresa en el empaque "
        "físico y deseche en farmacias los medicamentos vencidos."
    )
    
    add_section_heading(doc, "8.3 Recomendaciones Técnicas para el Cuidado del Teléfono", level=2)
    add_body_p(
        doc,
        "• Cargue su teléfono todas las noches: Asegúrese de dejar su teléfono conectado cerca de su mesa de noche para que nunca se quede sin "
        "batería durante la madrugada.\n\n"
        "• No active el modo 'Silencio total' antes de dormir: Si desea descansar sin que le molesten llamadas de extraños, use el modo "
        "'No Molestar' pero agregue a MedReminder AI como aplicación con excepción prioritaria para que sus alarmas médicas sí suenen."
    )
    
    # ==========================================================================
    # 9. SOPORTE
    # ==========================================================================
    add_section_heading(doc, "9. SOPORTE", level=1, page_break_before=True)
    
    add_section_heading(doc, "9.1 Canales de Asistencia y Dudas", level=2)
    add_body_p(
        doc,
        "Si usted, su familiar o su médico tratante tienen dudas técnicas sobre el funcionamiento de la aplicación, "
        "requieren ayuda para configurar permisos de batería o desean reportar una mejora, ponemos a su disposición los siguientes canales oficiales:\n\n"
        "• Correo Electrónico Institucional de Soporte: medreminder.ai.soporte@utvt.edu.mx\n"
        "• Horario de Atención Técnica: Lunes a Viernes de 09:00 a 18:00 horas (Tiempo del Centro de México).\n"
        "• Portal Web de Documentación: https://github.com/4strob0y/MedReminderAI"
    )
    
    add_section_heading(doc, "9.2 Directorio del Equipo de Desarrollo de la UTVT", level=2)
    add_body_p(
        doc,
        "Este sistema fue desarrollado por el Equipo de Ingeniería de la Dirección de Tecnologías de la Información y Comunicación "
        "de la Universidad Tecnológica del Valle de Toluca (UTVT), bajo la supervisión de la asignatura Fundamentos de Inteligencia Artificial:"
    )
    
    team_headers = ["Matrícula", "Nombre del Ingeniero Responsable", "Área de Especialidad en el Proyecto"]
    team_rows = [
        ["222410897", "Gutierrez Ugalde Samuel", "Arquitectura de Software y Modelado Lógico"],
        ["222410935", "Nava Garcia Rodrigo", "Desarrollo Móvil Android Jetpack Compose"],
        ["222411182", "Castillo Ramirez Nahum Yabet", "Backend FastAPI y Microservicios Asíncronos"],
        ["222410915", "Ramirez Romero Pablo", "Persistencia de Datos MySQL y Telemetría"],
        ["222410899", "Peña Hernandez Alexander", "Algoritmos de Búsqueda en IA y Gamificación"]
    ]
    add_truth_table(doc, team_headers, team_rows, "Tabla 9.1: Directorio de Desarrolladores de MedReminder AI (UTVT)", [1.3, 2.6, 2.6])
    
    add_section_heading(doc, "9.3 Procedimiento para Reportar Sugerencias o Incidencias Técnicas", level=2)
    add_body_p(
        doc,
        "Para solicitar asistencia técnica sobre la aplicación:\n"
        "1. Envíe un correo a medreminder.ai.soporte@utvt.edu.mx indicando en el asunto: «Soporte Paciente - [Su Nombre]».\n"
        "2. En el cuerpo del correo, mencione el modelo de su teléfono (ejemplo: Samsung Galaxy A54 o Xiaomi Redmi Note 12) y qué problema experimenta.\n"
        "3. El equipo de soporte le responderá en menos de 24 horas con una solución paso a paso adaptada a su teléfono."
    )
    
    # ==========================================================================
    # GLOSARIO TERMINOLÓGICO PARA EL PACIENTE Y CUIDADOR
    # ==========================================================================
    add_section_heading(doc, "GLOSARIO TERMINOLÓGICO PARA EL PACIENTE Y CUIDADOR", level=1, page_break_before=True)
    add_body_p(
        doc,
        "Para su comodidad, a continuación se definen en lenguaje claro los términos médicos y tecnológicos más utilizados en la aplicación:"
    )
    
    glosario_items = [
        {"name": "Tomas de medicamentos", "type": "Término Clínico", "scope": "Uso Diario", "range": "Puntual / Pospuesta", "desc": "Acción física de ingerir o administrarse una dosis de fármaco programada en su horario prescrito."},
        {"name": "Dosis", "type": "Prescripción", "scope": "Posología", "range": "Ej: 1 tableta, 5 ml", "desc": "Cantidad exacta de medicamento que debe tomar en cada turno según la orden de su doctor."},
        {"name": "Intervalo Horario", "type": "Tiempo", "scope": "Posología", "range": "4, 6, 8, 12 o 24 h", "desc": "Número de horas que deben transcurrir entre una toma de medicamentos y la siguiente para mantener el efecto curativo."},
        {"name": "Mi Botiquín", "type": "Inventario", "scope": "Almacén Digital", "range": "0 a 999 pastillas", "desc": "Sección de la aplicación que lleva la cuenta de cuántas pastillas o frascos le quedan en casa."},
        {"name": "Adherencia Terapéutica", "type": "Métrica de Salud", "scope": "Progreso Clínico", "range": "0 % a 100 %", "desc": "Grado en que el paciente cumple con puntualidad su tratamiento médico según lo prescrito."},
        {"name": "Racha de Honor", "type": "Motivación", "scope": "Gamificación", "range": "Días continuos", "desc": "Contador de días seguidos en los que ha tomado todas sus medicinas a tiempo sin olvidar ninguna."},
        {"name": "Escudo Protector", "type": "Salvaguarda", "scope": "Gamificación", "range": "0 a 3 escudos", "desc": "Premio ganado por su constancia que perdona una falta involuntaria sin reiniciar su racha a cero."},
        {"name": "Modo Castigo", "type": "Disciplina", "scope": "Gamificación", "range": "Activo / Inactivo", "desc": "Ajuste temporal que bloquea la posposición de alarmas si se acumulan varias omisiones continuas."},
        {"name": "Principio Activo", "type": "Farmacología", "scope": "Seguridad", "range": "Nombre químico", "desc": "Sustancia medicinal que produce el efecto curativo dentro de la pastilla (ejemplo: Paracetamol)."}
    ]
    add_variable_dictionary_table(doc, glosario_items, "Glosario Términos Clínicos y de Operación para el Paciente")
    
    # ==========================================================================
    # LISTA DE VERIFICACIÓN ANTES DE ENTREGAR
    # ==========================================================================
    add_section_heading(doc, "LISTA DE VERIFICACIÓN ANTES DE COMENZAR A USAR LA APP", level=1, page_break_before=True)
    add_body_p(
        doc,
        "Antes de iniciar su tratamiento diario con MedReminder AI, complete esta lista de verificación sencilla para cerciorarse de "
        "que todo en su teléfono se encuentra correctamente preparado:"
    )
    
    user_checklist = [
        {"num": "U-01", "criterio": "Teléfono con sistema Android 8.0 o superior encendido y con volumen de alarma al 70% o más.", "estado": "VERIFICADO", "observaciones": "Altavoz probado y volumen suficiente para escuchar en casa."},
        {"num": "U-02", "criterio": "Permiso de notificaciones en pantalla y alarmas exactas concedido a MedReminder AI.", "estado": "VERIFICADO", "observaciones": "La app tiene permiso para mostrar avisos Heads-Up emergentes."},
        {"num": "U-03", "criterio": "Exención de optimización de batería configurada como 'Sin restricciones'.", "estado": "VERIFICADO", "observaciones": "Garantiza que el teléfono no duerma la aplicación en segundo plano."},
        {"num": "U-04", "criterio": "Cuenta de usuario creada e inicio de sesión completado con éxito.", "estado": "VERIFICADO", "observaciones": "Sesión iniciada con correo y contraseña personal."},
        {"num": "U-05", "criterio": "Primer medicamento registrado con nombre, dosis, horario e intervalo correcto.", "estado": "VERIFICADO", "observaciones": "El medicamento aparece visible en la lista de la pantalla 'Hoy'."},
        {"num": "U-06", "criterio": "Botiquín digital sincronizado con el número real de pastillas que tiene en su frasco.", "estado": "VERIFICADO", "observaciones": "Semáforo en color verde indicando suministro seguro."},
        {"num": "U-07", "criterio": "Al menos un contacto de apoyo familiar o de emergencia registrado con teléfono.", "estado": "VERIFICADO", "observaciones": "Contacto visible en la pestaña 'Apoyo' con botón de llamada listo."},
        {"num": "U-08", "criterio": "Prueba de sonido y vibración realizada al pulsar el botón de ayuda con Medi.", "estado": "VERIFICADO", "observaciones": "Medi responde con voz clara y agradable por el altavoz."},
        {"num": "U-09", "criterio": "Comprensión de las tablas de verdad de interacción del paciente (habilitación de botones y función deshacer).", "estado": "VERIFICADO", "observaciones": "Reglas de interacción formalizadas con V y F comprendidas para uso seguro."}
    ]
    add_checklist_table(doc, user_checklist, "LISTA DE VERIFICACIÓN PARA EL PACIENTE Y CUIDADOR")
    
    # Guardar documento
    out_path = "docs/Manual_de_Usuario_MedReminderAI.docx"
    doc.save(out_path)
    print(f"✅ Manual de Usuario generado exitosamente en: {out_path}")
    return out_path

if __name__ == "__main__":
    build_manual_usuario()
