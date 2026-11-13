#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script generador del documento oficial de Product Backlog para MedReminder AI.
Punto medio equilibrado: claro, profesional, natural y sin tecnicismos extravagantes ni coloquialismos informales.
Institución: Universidad Tecnológica del Valle de Toluca (UTVT)
Asignatura: Formulación de Proyectos de Tecnología
Docente: I.C. Héctor Pérez Paulín
Grupo: ITIID-73
"""

import os
import subprocess
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn

DOCS_DIR = "/Users/4strob0y/Developer/MedReminderAI/docs"
PORTADA_SRC = os.path.join(DOCS_DIR, "Portada.docx")
DOCX_OUT = os.path.join(DOCS_DIR, "Documento_Backlog_MedReminderAI_UTVT.docx")
HTML_OUT = os.path.join(DOCS_DIR, "Documento_Backlog_MedReminderAI_UTVT.html")
PDF_OUT = os.path.join(DOCS_DIR, "Documento_Backlog_MedReminderAI_UTVT.pdf")

LOGO_UTVT = os.path.join(DOCS_DIR, "logo_utvt.png")
LOGO_EDOMEX = os.path.join(DOCS_DIR, "logo_edomex.png")

# Paleta de color institucional y balanceada
C_NAVY = RGBColor(27, 54, 93)       # #1B365D - Azul UTVT
C_TEAL = RGBColor(14, 128, 116)     # #0E8074 - Verde Clínico
C_TEXT = RGBColor(40, 44, 52)       # #282C34 - Texto base
C_MUTED = RGBColor(100, 116, 139)   # #64748B - Gris
C_GREEN = RGBColor(22, 163, 74)     # #16A34A - Verde acento
C_WHITE = RGBColor(255, 255, 255)

HEX_NAVY = "1B365D"
HEX_TEAL = "0E8074"
HEX_LIGHT_BG = "F8FAFC"
HEX_CARD_BG = "F0FDF4"
HEX_BORDER = "CBD5E1"
HEX_MUTED_BG = "F1F5F9"
HEX_DONE_BG = "DCFCE7"
HEX_GREEN = "16A34A"

# --- Datos del Backlog Completo (10 Épicas y 30 Historias) en tono balanceado ---
EPICAS_DATA = [
    {
        "num": "1",
        "nombre": "Infraestructura Base, Servicios Docker y Red Local",
        "objetivo": "Configurar los contenedores de base de datos y backend para un despliegue ágil, asegurando la comunicación entre la aplicación móvil y el servidor tanto en la universidad como en entornos domésticos.",
        "historias": [
            {
                "id": "HU-01",
                "nombre": "Contenedores Docker para API y Base de Datos",
                "como": "equipo de desarrollo",
                "quiero": "iniciar el servidor FastAPI y la base de datos MySQL con un solo comando ('docker compose up -d')",
                "para": "mantener el mismo entorno de ejecución en todas las computadoras del equipo y evitar fallas de configuración manual",
                "criterios": "El backend y MySQL inician en menos de 30 segundos con volumen persistente y puerto 8005 disponible.",
                "prioridad": "Must",
                "puntos": 5
            },
            {
                "id": "HU-02",
                "nombre": "Estructuración de Base de Datos Relacional",
                "como": "desarrollador de backend",
                "quiero": "definir tablas normalizadas para usuarios, medicamentos, tratamientos y recordatorios con integridad referencial",
                "para": "almacenar la información médica de forma segura, evitando registros huérfanos o datos duplicados",
                "criterios": "El script SQL inicializa las tablas con llaves foráneas y tipos de datos validados.",
                "prioridad": "Must",
                "puntos": 5
            },
            {
                "id": "HU-03",
                "nombre": "Detección Dinámica de Red y Fallback de IP",
                "como": "estudiante que prueba la app en el aula y en casa",
                "quiero": "que la app Android detecte automáticamente la dirección IP del servidor según la red conectada (WiFi escolar, hotspot o red local)",
                "para": "evitar modificar la configuración de red y recompilar el proyecto cada vez que cambiamos de espacio de trabajo",
                "criterios": "Sondeo de conectividad con timeout rápido (400 ms) y conmutación automática sin cierre inesperado.",
                "prioridad": "Should",
                "puntos": 3
            }
        ]
    },
    {
        "num": "2",
        "nombre": "Autenticación, Seguridad y Perfiles de Usuario",
        "objetivo": "Asegurar el acceso confiable al sistema, proteger los datos médicos del paciente y habilitar la vinculación entre el usuario y su familiar cuidador.",
        "historias": [
            {
                "id": "HU-04",
                "nombre": "Registro de Paciente con Fecha de Nacimiento",
                "como": "usuario nuevo",
                "quiero": "registrarme indicando mi fecha de nacimiento",
                "para": "que el sistema determine mi rango de edad y adapte automáticamente el tamaño de letra, botones y tolerancia de alarmas",
                "criterios": "Cálculo automático de grupo etario al registrarse (jóvenes, adultos o adultos mayores >60 años).",
                "prioridad": "Must",
                "puntos": 3
            },
            {
                "id": "HU-05",
                "nombre": "Inicio de Sesión Seguro con JWT y Contraseñas Cifradas",
                "como": "paciente registrado",
                "quiero": "iniciar sesión con mi correo electrónico y contraseña",
                "para": "proteger mi expediente médico y asegurar que solo personas autorizadas puedan consultar mis medicamentos",
                "criterios": "Cifrado seguro mediante bcrypt y emisión de token JWT con vigencia definida.",
                "prioridad": "Must",
                "puntos": 5
            },
            {
                "id": "HU-06",
                "nombre": "Diferenciación de Roles: Paciente y Familiar Cuidador",
                "como": "familiar a cargo del cuidado de un paciente",
                "quiero": "vincular mi cuenta como Cuidador responsable",
                "para": "dar seguimiento al cumplimiento de los medicamentos y recibir avisos inmediatos en caso de omisiones",
                "criterios": "Vinculación directa en base de datos con panel de supervisión de tomas en tiempo real.",
                "prioridad": "Must",
                "puntos": 5
            }
        ]
    },
    {
        "num": "3",
        "nombre": "Gestión del Botiquín Virtual e Inventario Farmacológico",
        "objetivo": "Proporcionar al paciente un registro ordenado de los medicamentos disponibles en el hogar y prevenir desabastos mediante control de stock.",
        "historias": [
            {
                "id": "HU-07",
                "nombre": "Alta y Registro de Medicamentos en el Botiquín",
                "como": "paciente con tratamientos prescritos",
                "quiero": "registrar mis medicamentos indicando nombre, dosis, presentación (pastilla, jarabe, inyección) y unidades disponibles",
                "para": "mantener un catálogo digital organizado de todo el medicamento con el que cuento en casa",
                "criterios": "Formulario con selector visual de presentación y validación numérica de dosis y piezas.",
                "prioridad": "Must",
                "puntos": 5
            },
            {
                "id": "HU-08",
                "nombre": "Autocompletado Predictivo de Nombres Farmacológicos",
                "como": "paciente que desconoce la ortografía exacta de un fármaco",
                "quiero": "recibir sugerencias automáticas de nombres comunes (ej. Paracetamol, Metformina, Losartán) al escribir tres letras",
                "para": "agilizar el registro y evitar errores de escritura en sustancias médicas",
                "criterios": "Desplegable reactivo con catálogo base de medicamentos de uso frecuente en México.",
                "prioridad": "Should",
                "puntos": 3
            },
            {
                "id": "HU-09",
                "nombre": "Descuento Automático de Inventario y Alerta de Stock Bajo",
                "como": "paciente o cuidador",
                "quiero": "que cada toma confirmada descuente una unidad del botiquín y me advierta cuando queden 3 pastillas o menos",
                "para": "adquirir el medicamento con anticipación en la farmacia y evitar la interrupción del tratamiento",
                "criterios": "Disminución atómica de stock y cambio visual a estado amarillo de advertencia.",
                "prioridad": "Must",
                "puntos": 5
            }
        ]
    },
    {
        "num": "4",
        "nombre": "Programación de Tratamientos y Cronograma Diario ('Hoy')",
        "objetivo": "Calcular de manera precisa los horarios de toma a partir de la prescripción médica y ofrecer una vista diaria clara y cronológica.",
        "historias": [
            {
                "id": "HU-10",
                "nombre": "Cálculo Automático de Tomas según Frecuencia y Duración",
                "como": "paciente con prescripción médica",
                "quiero": "indicar la fecha de inicio, la frecuencia en horas (cada 8, 12 o 24 hrs) y los días de duración del tratamiento",
                "para": "que la aplicación genere todos los recordatorios del periodo sin tener que programar cada alarma individualmente",
                "criterios": "Generación consistente de registros con fecha y hora en base de datos sin duplicidades.",
                "prioridad": "Must",
                "puntos": 8
            },
            {
                "id": "HU-11",
                "nombre": "Visualización del Cronograma Diario en Pantalla 'Hoy'",
                "como": "paciente al iniciar el día",
                "quiero": "ver una lista ordenada por horario con los medicamentos programados únicamente para la fecha actual",
                "para": "identificar con rapidez las dosis de la mañana, tarde y noche sin confusiones con días posteriores",
                "criterios": "Tarjetas informativas con nombre del medicamento, dosis, hora y estado (Pendiente, Tomada, Pospuesta).",
                "prioridad": "Must",
                "puntos": 5
            },
            {
                "id": "HU-12",
                "nombre": "Confirmación Inmediata de Toma Realizada",
                "como": "paciente",
                "quiero": "presionar un botón visible que registre la toma de mi dosis en un solo toque",
                "para": "dejar constancia de la toma oportuna y tener la certeza de no haber omitido ni duplicado la medicación",
                "criterios": "Actualización inmediata del estado a 'Tomada' en menos de 200 ms y descuento correspondiente en inventario.",
                "prioridad": "Must",
                "puntos": 3
            }
        ]
    },
    {
        "num": "5",
        "nombre": "Alarmas Nativas de Alta Prioridad y Resiliencia Fuera de Línea",
        "objetivo": "Garantizar la activación puntual y acústica de la alarma independientemente del estado de bloqueo del móvil, modos de ahorro de energía o ausencia de internet.",
        "historias": [
            {
                "id": "HU-13",
                "nombre": "Disparo Determinista en Pantalla Completa (AlarmManager)",
                "como": "paciente con el teléfono bloqueado o guardado",
                "quiero": "que la pantalla se encienda a pantalla completa con sonido y vibración a la hora exacta de la toma",
                "para": "escuchar y ver el recordatorio aun si el dispositivo se encuentra en modo de reposo profundo (Doze Mode)",
                "criterios": "Implementación con AlarmManager exacto y Full-Screen Intent; activación en un rango menor a ±2 segundos.",
                "prioridad": "Crítica",
                "puntos": 8
            },
            {
                "id": "HU-14",
                "nombre": "Activación Prioritaria en Modo Silencio para Medicamentos Críticos",
                "como": "paciente con condiciones delicadas (hipertensión o diabetes)",
                "quiero": "que los medicamentos clasificados como críticos suenen mediante el canal de alarma del sistema, aun con el móvil en silencio",
                "para": "evitar omitir una dosis vital por un descuido en la configuración de volumen del teléfono",
                "criterios": "Canal de audio USAGE_ALARM configurado para omitir restricciones de no molestar en dosis críticas.",
                "prioridad": "Must",
                "puntos": 5
            },
            {
                "id": "HU-15",
                "nombre": "Operación Totalmente Fuera de Línea (Modo Offline)",
                "como": "paciente en zonas con poca cobertura o sin datos móviles",
                "quiero": "que todas las alarmas programadas sigan funcionando normalmente sin conexión a internet",
                "para": "mantener la seguridad del tratamiento sin depender del estado del servicio de red móvil",
                "criterios": "Almacenamiento y programación local determinista en el dispositivo Android.",
                "prioridad": "Crítica",
                "puntos": 5
            }
        ]
    },
    {
        "num": "6",
        "nombre": "Inteligencia Artificial Clínica Local y Escáner de Recetas Médicas",
        "objetivo": "Facilitar la captura de tratamientos mediante visión por computadora y ofrecer asistencia informativa sobre medicamentos preservando la privacidad del paciente.",
        "historias": [
            {
                "id": "HU-16",
                "nombre": "Asistente Virtual 'Medi Companion' con Modelo Local Ollama",
                "como": "paciente con dudas cotidianas sobre sus medicamentos",
                "quiero": "consultar al asistente Medi sobre el propósito general de un fármaco o si debe ingerirse con alimentos",
                "para": "obtener orientación preliminar comprensible sin consultar fuentes no verificadas en internet",
                "criterios": "Procesamiento local mediante el modelo afinado 'medi-clinico' en Ollama, sin envío de datos al exterior.",
                "prioridad": "Should",
                "puntos": 8
            },
            {
                "id": "HU-17",
                "nombre": "Extracción de Prescripciones Médicas mediante Fotografía",
                "como": "paciente o familiar con una receta médica impresa o manuscrita",
                "quiero": "capturar una fotografía de la receta para que la IA reconozca el fármaco, la concentración y la frecuencia indicada",
                "para": "simplificar la captura de tratamientos extensos y reducir errores al teclear nombres complejos",
                "criterios": "Modelo multimodal que procesa la imagen y devuelve los datos estructurados en formato JSON.",
                "prioridad": "Must",
                "puntos": 8
            },
            {
                "id": "HU-18",
                "nombre": "Pantalla de Verificación y Corrección de Datos Escaneados",
                "como": "usuario precavido",
                "quiero": "revisar y editar la información detectada por la IA antes de confirmar el tratamiento",
                "para": "asegurar que los miligramos y horarios sean exactamente los indicados por el médico antes de programar las alarmas",
                "criterios": "Formulario precargado con campos totalmente editables previo a la confirmación de guardado.",
                "prioridad": "Must",
                "puntos": 5
            }
        ]
    },
    {
        "num": "7",
        "nombre": "Seguridad Farmacológica: Alergias e Interacciones Medicamentosas",
        "objetivo": "Validar que los medicamentos registrados no generen reacciones adversas conocidas ni choquen de forma perjudicial entre sí.",
        "historias": [
            {
                "id": "HU-19",
                "nombre": "Registro y Validación de Alergias Medicamentosas",
                "como": "paciente con alergias conocidas (ej. Penicilinas o AINEs)",
                "quiero": "registrar mis sustancias contraindicadas en mi perfil médico",
                "para": "que la aplicación me alerte inmediatamente si intento agregar un fármaco que contenga componentes alérgenos",
                "criterios": "Verificación cruzada al dar de alta medicamentos con mensaje de advertencia y bloqueo preventivo.",
                "prioridad": "Must",
                "puntos": 5
            },
            {
                "id": "HU-20",
                "nombre": "Detección de Contraindicaciones e Interacciones Cruzadas",
                "como": "paciente polimedicado",
                "quiero": "que el sistema revise si existen conflictos o efectos adversos conocidos entre los medicamentos activos",
                "para": "consultar oportunamente al médico tratante y prevenir intoxicaciones o pérdida de eficacia farmacológica",
                "criterios": "Evaluación con motor de lógica clínica y matrices de compatibilidad farmacológica implementadas en el backend.",
                "prioridad": "Must",
                "puntos": 8
            }
        ]
    },
    {
        "num": "8",
        "nombre": "Adherencia Terapéutica, Adaptación Gerontológica y Red de Apoyo",
        "objetivo": "Fomentar la constancia en el paciente respetando sus tiempos y mantener comunicada a la familia ante situaciones imprevistas.",
        "historias": [
            {
                "id": "HU-21",
                "nombre": "Métricas de Cumplimiento: Racha de Días y Reconocimiento",
                "como": "paciente que busca consolidar un hábito de salud",
                "quiero": "visualizar los días consecutivos con tomas cumplidas puntualmente",
                "para": "mantener la motivación y evaluar mi propio compromiso con el tratamiento",
                "criterios": "Incremento de racha diaria al completar el 100% de tomas y mensaje de felicitación por hitos.",
                "prioridad": "Could",
                "puntos": 3
            },
            {
                "id": "HU-22",
                "nombre": "Tolerancia Gerontológica y Flexibilidad de Posposición",
                "como": "adulto mayor con movilidad pausada",
                "quiero": "posponer la alarma hasta en dos ocasiones por 10 minutos sin recibir penalizaciones estrictas",
                "para": "preparar con calma el vaso con agua y el medicamento sin sentir presión apresurada del sistema",
                "criterios": "Ventana de tolerancia de 20 minutos con advertencias graduales antes de considerar la toma como omitida.",
                "prioridad": "Must",
                "puntos": 5
            },
            {
                "id": "HU-23",
                "nombre": "Alertas Automáticas al Cuidador ante Omisiones Relevantes",
                "como": "familiar o cuidador responsable",
                "quiero": "recibir una alerta si el paciente supera el límite de posposiciones en una dosis crítica",
                "para": "comunicarme de inmediato o asistir al paciente antes de que se presente una descompensación clínica",
                "criterios": "Registro del evento en el panel de cuidador con hora, medicamento y estado de omisión.",
                "prioridad": "Must",
                "puntos": 5
            },
            {
                "id": "HU-24",
                "nombre": "Acceso Directo a Contacto de Apoyo en Casos de Emergencia",
                "como": "paciente que experimenta malestar repentino",
                "quiero": "disponer de un botón de emergencia visible en la pantalla principal para contactar a mi familiar vía llamada o mensaje",
                "para": "solicitar apoyo rápidamente sin navegar por menús complejos del dispositivo",
                "criterios": "Enlace directo mediante Intent nativo de llamada o WhatsApp hacia el contacto de apoyo asignado.",
                "prioridad": "Must",
                "puntos": 3
            }
        ]
    },
    {
        "num": "9",
        "nombre": "Diseño Visual Accesible y Rendimiento a 60 FPS",
        "objetivo": "Ofrecer una interfaz con contraste adecuado, tipografía legible para personas con debilidad visual y una navegación fluida sin retrasos.",
        "historias": [
            {
                "id": "HU-25",
                "nombre": "Paleta Visual Clínica y Ergonomía Visual (Clinical Teal y Soft Mint)",
                "como": "usuario adulto mayor o persona con cansancio visual",
                "quiero": "fondos contrastantes y claros, botones con dimensiones amplias y texto de buen tamaño",
                "para": "leer la información cómodamente tanto en condiciones de iluminación diurna como nocturna",
                "criterios": "Implementación de la paleta médica oficial (#0E8074 y #1B365D), botones mínimos de 48dp y texto legible.",
                "prioridad": "Should",
                "puntos": 3
            },
            {
                "id": "HU-26",
                "nombre": "Optimización de Consultas y Navegación Fluida a 60 FPS",
                "como": "usuario con un dispositivo Android de gama estándar",
                "quiero": "que la pantalla principal cargue ágilmente y las transiciones sean suaves",
                "para": "tener una experiencia de uso ágil y confiable sin sobrecalentar el equipo ni agotar la batería",
                "criterios": "Carga unificada del cronograma en una sola llamada de red y renderizado fluido en Jetpack Compose.",
                "prioridad": "Should",
                "puntos": 5
            }
        ]
    },
    {
        "num": "10",
        "nombre": "Roadmap Tecnológico y Proyección a Futuro (Versión 2.0)",
        "objetivo": "Documentar las líneas de desarrollo previstas para la versión 2.0 y próximas iteraciones del proyecto.",
        "historias": [
            {
                "id": "HU-27",
                "nombre": "Generación de Reporte Clínico en PDF para Consulta Médica",
                "como": "paciente que asiste a consulta periódica en el sector salud (IMSS, ISSSTE o ISSEMYM)",
                "quiero": "exportar un resumen mensual en PDF con mis porcentajes de adherencia y registros de tomas",
                "para": "proporcionar al médico de cabecera información objetiva sobre la constancia de mi tratamiento",
                "criterios": "Generación de documento estructurado con gráficos de adherencia listo para imprimir o compartir.",
                "prioridad": "Must",
                "puntos": 5
            },
            {
                "id": "HU-28",
                "nombre": "Integración con Pastillero Físico Automatizado (IoT con ESP32)",
                "como": "familiar de un paciente con deterioro cognitivo significativo",
                "quiero": "enlazar la app mediante Bluetooth con un dispensador físico que ilumine y libere únicamente el compartimento correspondiente",
                "para": "eliminar el riesgo de confusiones mecánicas entre distintos frascos de medicamento",
                "criterios": "Comunicación BLE entre la aplicación móvil y microcontrolador ESP32 con sensores de apertura.",
                "prioridad": "Should",
                "puntos": 8
            },
            {
                "id": "HU-29",
                "nombre": "Confirmación Asistida por Voz ('Medi Voice')",
                "como": "paciente con dificultades motrices o artritis",
                "quiero": "confirmar mis tomas pronunciando comandos de voz simples hacia el asistente",
                "para": "registrar el cumplimiento sin depender de la interacción táctil fina en la pantalla",
                "criterios": "Reconocimiento de comandos de voz locales en español y confirmación de la toma registrada.",
                "prioridad": "Should",
                "puntos": 8
            },
            {
                "id": "HU-30",
                "nombre": "Notificaciones Push Remotas en la Nube (Multi-dispositivo)",
                "como": "cuidador que reside o labora en una ubicación distante",
                "quiero": "recibir avisos críticos directamente en mi celular a través de notificaciones push en tiempo real",
                "para": "mantener la supervisión del paciente aun cuando no nos encontremos en la misma vivienda",
                "criterios": "Integración con Firebase Cloud Messaging para entrega confiable de avisos de omisión.",
                "prioridad": "Must",
                "puntos": 5
            }
        ]
    }
]

# --- XML Helpers con protección total contra cortes de tabla ---
def set_cell_background(cell, hex_color):
    tcPr = cell._tc.get_or_add_tcPr()
    shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{hex_color}"/>')
    tcPr.append(shd)

def set_cell_margins(cell, top=100, bottom=100, left=120, right=120):
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = parse_xml(f'<w:tcMar {nsdecls("w")}>'
                      f'<w:top w:w="{top}" w:type="dxa"/>'
                      f'<w:bottom w:w="{bottom}" w:type="dxa"/>'
                      f'<w:left w:w="{left}" w:type="dxa"/>'
                      f'<w:right w:w="{right}" w:type="dxa"/>'
                      f'</w:tcMar>')
    tcPr.append(tcMar)

def set_cell_borders(cell, top=None, bottom=None, left=None, right=None):
    tcPr = cell._tc.get_or_add_tcPr()
    tcBorders = parse_xml(f'<w:tcBorders {nsdecls("w")}/>')
    borders = {'top': top, 'bottom': bottom, 'left': left, 'right': right}
    for side, border in borders.items():
        if border:
            val, sz, space, color = border
            b_elm = parse_xml(f'<w:{side} {nsdecls("w")} w:val="{val}" w:sz="{sz}" w:space="{space}" w:color="{color}"/>')
            tcBorders.append(b_elm)
        else:
            b_elm = parse_xml(f'<w:{side} {nsdecls("w")} w:val="none"/>')
            tcBorders.append(b_elm)
    tcPr.append(tcBorders)

def add_heading_1(doc, title):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(14)
    p.paragraph_format.space_after = Pt(5)
    p.paragraph_format.keep_with_next = True
    r = p.add_run(title)
    r.font.name = "Arial"
    r.font.size = Pt(12)
    r.font.bold = True
    r.font.color.rgb = C_NAVY
    return p

def add_heading_2(doc, title):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(10)
    p.paragraph_format.space_after = Pt(3)
    p.paragraph_format.keep_with_next = True
    r = p.add_run(title)
    r.font.name = "Arial"
    r.font.size = Pt(10.5)
    r.font.bold = True
    r.font.color.rgb = C_TEAL
    return p

def add_p(doc, text, bold_prefix="", space_after=4, italic=False):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(1)
    p.paragraph_format.space_after = Pt(space_after)
    p.paragraph_format.line_spacing = 1.15
    if bold_prefix:
        r_pre = p.add_run(bold_prefix)
        r_pre.font.name = "Arial"
        r_pre.font.size = Pt(9.5)
        r_pre.font.bold = True
        r_pre.font.color.rgb = C_NAVY
    r = p.add_run(text)
    r.font.name = "Arial"
    r.font.size = Pt(9.5)
    r.font.italic = italic
    r.font.color.rgb = C_TEXT
    return p

def add_bullet(doc, bold_prefix, text):
    p = doc.add_paragraph()
    p.paragraph_format.left_indent = Inches(0.2)
    p.paragraph_format.space_before = Pt(1)
    p.paragraph_format.space_after = Pt(2.5)
    p.paragraph_format.line_spacing = 1.15
    r_b = p.add_run("• ")
    r_b.font.name = "Arial"
    r_b.font.size = Pt(9.5)
    r_b.font.bold = True
    r_b.font.color.rgb = C_TEAL
    if bold_prefix:
        r_pre = p.add_run(bold_prefix)
        r_pre.font.name = "Arial"
        r_pre.font.size = Pt(9.5)
        r_pre.font.bold = True
        r_pre.font.color.rgb = C_NAVY
    r = p.add_run(text)
    r.font.name = "Arial"
    r.font.size = Pt(9.5)
    r.font.color.rgb = C_TEXT
    return p

def add_callout(doc, title, text, border_color=HEX_TEAL, bg_color=HEX_LIGHT_BG):
    tbl = doc.add_table(rows=1, cols=1)
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    tbl.autofit = False
    
    trPr = tbl.rows[0]._tr.get_or_add_trPr()
    trPr.append(parse_xml(f'<w:cantSplit {nsdecls("w")}/>'))
    
    c = tbl.cell(0, 0)
    c.width = Inches(6.8)
    set_cell_background(c, bg_color)
    set_cell_margins(c, top=80, bottom=80, left=120, right=120)
    set_cell_borders(c, left=("single", "24", "0", border_color),
                        top=("single", "4", "0", HEX_BORDER),
                        bottom=("single", "4", "0", HEX_BORDER),
                        right=("single", "4", "0", HEX_BORDER))
    p = c.paragraphs[0]
    p.paragraph_format.space_after = Pt(2)
    p.paragraph_format.line_spacing = 1.15
    if title:
        rt = p.add_run(title + "\n")
        rt.font.name = "Arial"
        rt.font.size = Pt(9.5)
        rt.font.bold = True
        rt.font.color.rgb = C_NAVY
    r = p.add_run(text)
    r.font.name = "Arial"
    r.font.size = Pt(9)
    r.font.color.rgb = C_TEXT
    doc.add_paragraph().paragraph_format.space_after = Pt(2)

def add_backlog_table(doc, stories):
    """Genera la tabla con cantSplit en cada fila y tblHeader en el encabezado."""
    tbl = doc.add_table(rows=len(stories) + 1, cols=6)
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    tbl.autofit = False
    
    col_w = [Inches(0.65), Inches(1.4), Inches(2.2), Inches(1.5), Inches(0.55), Inches(0.5)]
    hdrs = ["ID", "Historia de Usuario", "Estructura Canónica (Como / Quiero / Para)", "Criterios de Aceptación", "Prior.", "Pts."]
    
    r0 = tbl.rows[0]
    trPr0 = r0._tr.get_or_add_trPr()
    trPr0.append(parse_xml(f'<w:cantSplit {nsdecls("w")}/>'))
    trPr0.append(parse_xml(f'<w:tblHeader {nsdecls("w")}/>'))
    
    for i, h in enumerate(hdrs):
        c = r0.cells[i]
        c.width = col_w[i]
        set_cell_background(c, HEX_NAVY)
        set_cell_margins(c, top=70, bottom=70, left=60, right=60)
        p = c.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER if i in [0, 4, 5] else WD_ALIGN_PARAGRAPH.LEFT
        r = p.add_run(h)
        r.font.name = "Arial"
        r.font.size = Pt(8)
        r.font.bold = True
        r.font.color.rgb = C_WHITE
        
    for row_idx, st in enumerate(stories, start=1):
        row = tbl.rows[row_idx]
        trPr = row._tr.get_or_add_trPr()
        trPr.append(parse_xml(f'<w:cantSplit {nsdecls("w")}/>'))
        
        bg = HEX_LIGHT_BG if row_idx % 2 == 0 else "FFFFFF"
        for col_idx in range(6):
            c = row.cells[col_idx]
            c.width = col_w[col_idx]
            set_cell_background(c, bg)
            set_cell_margins(c, top=60, bottom=60, left=60, right=60)
            set_cell_borders(c, top=("single", "4", "0", HEX_BORDER),
                                bottom=("single", "4", "0", HEX_BORDER),
                                left=("single", "4", "0", HEX_BORDER),
                                right=("single", "4", "0", HEX_BORDER))
            p = c.paragraphs[0]
            p.paragraph_format.line_spacing = 1.15
            p.paragraph_format.space_after = Pt(1)
            
            if col_idx == 0:
                p.alignment = WD_ALIGN_PARAGRAPH.CENTER
                r = p.add_run(st["id"])
                r.font.name = "Arial"
                r.font.size = Pt(8)
                r.font.bold = True
                r.font.color.rgb = C_NAVY
            elif col_idx == 1:
                r = p.add_run(st["nombre"])
                r.font.name = "Arial"
                r.font.size = Pt(8)
                r.font.bold = True
                r.font.color.rgb = C_TEXT
            elif col_idx == 2:
                r1 = p.add_run("Como ")
                r1.font.bold = True
                r1.font.size = Pt(7.5)
                r1.font.color.rgb = C_TEAL
                r2 = p.add_run(st["como"] + ", ")
                r2.font.size = Pt(7.5)
                r3 = p.add_run("quiero ")
                r3.font.bold = True
                r3.font.size = Pt(7.5)
                r3.font.color.rgb = C_NAVY
                r4 = p.add_run(st["quiero"] + ", ")
                r4.font.size = Pt(7.5)
                r5 = p.add_run("para ")
                r5.font.bold = True
                r5.font.size = Pt(7.5)
                r5.font.color.rgb = C_GREEN
                r6 = p.add_run(st["para"] + ".")
                r6.font.size = Pt(7.5)
            elif col_idx == 3:
                r = p.add_run(st["criterios"])
                r.font.name = "Arial"
                r.font.size = Pt(7.5)
                r.font.color.rgb = C_TEXT
            elif col_idx == 4:
                p.alignment = WD_ALIGN_PARAGRAPH.CENTER
                r = p.add_run(st["prioridad"])
                r.font.name = "Arial"
                r.font.size = Pt(7.5)
                r.font.bold = True
                r.font.color.rgb = C_TEAL if st["prioridad"] in ["Must", "Crítica"] else C_MUTED
            elif col_idx == 5:
                p.alignment = WD_ALIGN_PARAGRAPH.CENTER
                r = p.add_run(str(st["puntos"]))
                r.font.name = "Arial"
                r.font.size = Pt(8)
                r.font.bold = True
                r.font.color.rgb = C_NAVY
                
    doc.add_paragraph().paragraph_format.space_after = Pt(3)

def build_docx():
    print(f"Cargando plantilla de portada UTVT: {PORTADA_SRC}")
    doc = docx.Document(PORTADA_SRC)
    
    # 1. Carátula oficial UTVT ajustada con datos correctos
    p6 = doc.paragraphs[6]
    p6.text = "INGENIERÍA EN TECNOLOGÍAS DE LA INFORMACIÓN E INNOVACIÓN DIGITAL"
    p6.alignment = WD_ALIGN_PARAGRAPH.CENTER
    for r in p6.runs:
        r.font.name = "Calibri"
        r.font.size = Pt(10.5)
        r.font.bold = True
        r.font.color.rgb = C_NAVY

    p9 = doc.paragraphs[9]
    p9.text = "PRODUCT BACKLOG INTEGRAL Y HISTORIAL DE DESARROLLO\nProyecto: MedReminder AI (Recordatorio y Gestión de Medicamentos)"
    p9.alignment = WD_ALIGN_PARAGRAPH.CENTER
    for r in p9.runs:
        r.font.name = "Calibri"
        r.font.size = Pt(12)
        r.font.bold = True
        r.font.color.rgb = C_NAVY

    p11 = doc.paragraphs[11]
    p11.text = "Formulación de Proyectos de Tecnología"
    p11.alignment = WD_ALIGN_PARAGRAPH.CENTER
    for r in p11.runs:
        r.font.name = "Calibri"
        r.font.size = Pt(11)
        r.font.bold = True
        r.font.color.rgb = C_TEAL

    p13 = doc.paragraphs[13]
    p13.text = "I.C. Héctor Pérez Paulín"
    p13.alignment = WD_ALIGN_PARAGRAPH.CENTER
    for r in p13.runs:
        r.font.name = "Calibri"
        r.font.size = Pt(11)
        r.font.bold = True
        r.font.color.rgb = C_NAVY

    # P17: Nombres de los integrantes con acentos correctos
    p17 = doc.paragraphs[17]
    p17.text = (
        "222410897   –   Gutiérrez Ugalde Samuel\n"
        "222410935   –   Nava García Rodrigo\n"
        "222411182   –   Castillo Ramírez Nahúm Yabet\n"
        "222410915   –   Ramírez Romero Pablo\n"
        "222410899   –   Peña Hernández Alexander"
    )
    p17.alignment = WD_ALIGN_PARAGRAPH.LEFT
    for r in p17.runs:
        r.font.name = "Calibri"
        r.font.size = Pt(10)
        r.font.color.rgb = C_TEXT

    # P19: Grupo ITIID - 73 sin número de equipo
    p19 = doc.paragraphs[19]
    p19.text = "GRUPO: ITIID - 73"
    p19.alignment = WD_ALIGN_PARAGRAPH.CENTER
    for r in p19.runs:
        r.font.name = "Calibri"
        r.font.size = Pt(10.5)
        r.font.bold = True
        r.font.color.rgb = C_NAVY

    p24 = doc.paragraphs[24]
    p24.text = "SANTA MARÍA ATARASQUILLO, LERMA ESTADO DE MÉXICO. NOVIEMBRE 2026"
    p24.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    for r in p24.runs:
        r.font.name = "Calibri"
        r.font.size = Pt(9.5)
        r.font.color.rgb = C_MUTED

    doc.add_page_break()

    # =========================================================================
    # SECCIÓN 1: INTRODUCCIÓN Y PROBLEMÁTICA
    # =========================================================================
    add_heading_1(doc, "1. Introducción al Proyecto: Propósito y Problemática Atendida")
    
    add_p(doc, "El proyecto atiende una situación recurrente en el entorno familiar: la dificultad que experimentan los adultos mayores y pacientes con tratamientos prolongados (tales como hipertensión o diabetes) para mantener el control estricto de sus medicamentos. Con frecuencia surgen omisiones involuntarias o tomas duplicadas por falta de certeza sobre si la dosis ya fue ingerida, lo que representa un riesgo para la estabilidad de la salud.", bold_prefix="Problemática identificada: ")

    add_bullet(doc, "Desorganización en el botiquín doméstico: ", "En muchos hogares coexisten varios tratamientos simultáneos sobre la mesa. La similitud entre cajas y frascos incrementa la probabilidad de confusiones en horarios y dosis.")
    add_bullet(doc, "Limitaciones de aplicaciones existentes: ", "Tras analizar alternativas disponibles en tiendas móviles, se detectaron barreras importantes: saturación de publicidad invasiva que desorienta a personas mayores, modelos de cobro periódico en moneda extranjera y falta de fiabilidad en alarmas cuando el móvil entra en reposo o carece de conexión a internet.")
    add_bullet(doc, "Incertidumbre en el núcleo familiar: ", "Los familiares a cargo experimentan inquietud constante por verificar si el paciente tomó su medicamento oportunamente, lo que suele derivar en llamadas reiteradas y pérdida de autonomía del paciente.")

    add_callout(doc, "Objetivo del Proyecto MedReminder AI",
                "Desarrollar una solución móvil accesible, privada y altamente confiable que asegure la activación puntual de alarmas visuales y acústicas aun con el dispositivo bloqueado o sin conexión a internet, incorpore asistencia de Inteligencia Artificial local para interpretar recetas mediante fotografía sin costos recurrentes, descuente existencias del botiquín y emita alertas automáticas al cuidador ante retrasos significativos.",
                border_color=HEX_NAVY, bg_color=HEX_CARD_BG)

    # =========================================================================
    # SECCIÓN 2: METODOLOGÍA DEL BACKLOG
    # =========================================================================
    add_heading_1(doc, "2. Metodología de Trabajo y Organización del Backlog")
    add_p(doc, "Con el objetivo de coordinar el desarrollo de manera estructurada y eficiente, el equipo implementó principios de metodologías ágiles basadas en Scrum:")

    add_bullet(doc, "El Backlog como herramienta viva: ", "La pila de trabajo no permaneció estática; se refinó y ajustó periódicamente tras validar cada incremento en dispositivos físicos reales, incorporando mejoras detectadas durante las pruebas.")
    add_bullet(doc, "Rol del Product Owner: ", "El compañero Rodrigo Nava García asumió la responsabilidad de Product Owner, priorizando las necesidades clínicas y de accesibilidad del paciente sobre requerimientos secundarios o meramente visuales.")
    add_bullet(doc, "Estructura canónica de Historias de Usuario: ", "Cada funcionalidad fue descrita bajo el formato estándar de Mike Cohn: 'Como [rol], quiero [función], para [beneficio tangible]', asegurando que cada tarea aporte valor verificable al usuario.")
    add_bullet(doc, "Criterios de Aceptación (Definition of Done): ", "Ninguna historia se dio por concluida hasta verificar su funcionamiento en un dispositivo Android real, comprobar la persistencia de datos y asegurar su operatividad fuera de línea.")
    add_bullet(doc, "Priorización MoSCoW y Estimación: ", "Las historias se clasificaron en Must (indispensables), Should (importantes), Could (deseables) y Won't (proyectadas a futuro), asignando puntos de esfuerzo relativo en escala Fibonacci simplificada (1 a 8 puntos).")

    # =========================================================================
    # SECCIÓN 3: EL PRODUCT BACKLOG COMPLETO
    # =========================================================================
    add_heading_1(doc, "3. Product Backlog Completo de MedReminder AI")
    add_p(doc, "A continuación se presentan las 10 Épicas y las 30 Historias de Usuario estructuradas que componen el proyecto, acompañadas de sus criterios de aceptación y estimación de esfuerzo:")

    for ep in EPICAS_DATA:
        add_heading_2(doc, f"Épica {ep['num']}: {ep['nombre']}")
        add_p(doc, ep["objetivo"], bold_prefix="Objetivo técnico de la épica: ", italic=True, space_after=3)
        add_backlog_table(doc, ep["historias"])

    # =========================================================================
    # SECCIÓN 4: RETOS TÉCNICOS Y SOLUCIONES IMPLEMENTADAS
    # =========================================================================
    add_heading_1(doc, "4. Retos Técnicos y Soluciones Implementadas durante el Desarrollo")
    add_p(doc, "Durante las pruebas de integración en dispositivos físicos se presentaron diversos retos técnicos que motivaron ajustes directos en el backlog. A continuación se documentan los cuatro casos más significativos:")

    add_heading_2(doc, "Caso 1: Ejecución precisa de alarmas en modo de reposo (Doze Mode)")
    add_p(doc, "Inicialmente se utilizaron notificaciones locales estándar de Android. Aunque operaban correctamente durante el uso activo del teléfono, al dejar el dispositivo en reposo nocturno el sistema operativo retrasaba la notificación hasta 25 minutos con el fin de ahorrar batería.")
    add_callout(doc, "Solución técnica en el Backlog:",
                "Se incorporó la historia HU-13 con prioridad 'Crítica'. Se sustituyeron las notificaciones convencionales por AlarmManager nativo con setExactAndAllowWhileIdle() y una Activity con Full-Screen Intent. Con esto se garantizó que la pantalla se active puntualmente a la hora programada aun con el teléfono en reposo profundo.",
                border_color=HEX_NAVY)

    add_heading_2(doc, "Caso 2: Resolución dinámica de red local en laboratorios escolares")
    add_p(doc, "En las instalaciones de la UTVT, la infraestructura de red asigna direcciones IP variables al alternar entre redes académicas, talleres o puntos de acceso móviles. Esto interrumpía la comunicación entre la app y el servidor local en la computadora portátil.")
    add_callout(doc, "Solución técnica en el Backlog:",
                "Se formuló la historia HU-03 para dotar a la aplicación de un módulo de detección dinámica de subred. La app ejecuta un sondeo ágil con timeout de 400 ms entre direcciones IP predefinidas y establece conexión automática sin requerir ajustes manuales en el código.",
                border_color=HEX_TEAL)

    add_heading_2(doc, "Caso 3: Integración de Inteligencia Artificial local preservando costos y privacidad")
    add_p(doc, "Para la lectura de recetas médicas y la orientación clínica se evaluó el uso de servicios comerciales en la nube. No obstante, esto implicaba costos periódicos no viables y riesgos en la confidencialidad de datos personales de salud.")
    add_callout(doc, "Solución técnica en el Backlog:",
                "Se desarrollaron las historias HU-16 y HU-17 integrando Ollama de manera local con el modelo afinado 'medi-clinico'. De este modo, el procesamiento de imágenes y consultas se realiza directamente en la infraestructura del equipo sin costos de API y garantizando que los datos no abandonen el entorno privado.",
                border_color=HEX_GREEN)

    add_heading_2(doc, "Caso 4: Accesibilidad visual y ergonomía para adultos mayores")
    add_p(doc, "El prototipo inicial empleaba contrastes intensos y colores fluorescentes. Durante las pruebas con personas adultas mayores se observó que dicha interfaz producía fatiga visual y dificultaba la lectura de textos pequeños.")
    add_callout(doc, "Solución técnica en el Backlog:",
                "A través de la historia HU-25 se estandarizó una paleta visual basada en Clinical Teal (#0E8074) y Soft Mint, estableciendo botones táctiles con altura mínima de 48dp y tipografía de al menos 16sp para favorecer la interacción en personas con debilidad visual o movilidad reducida.",
                border_color=HEX_NAVY)

    # =========================================================================
    # SECCIÓN 5: MÉTRICAS Y BALANCE DEL PROYECTO
    # =========================================================================
    add_heading_1(doc, "5. Balance de Métricas y Estado Actual del Proyecto")
    add_p(doc, "El avance global del proyecto respecto al esfuerzo estimado en el backlog se resume en los siguientes indicadores cuantitativos:")

    tbl_met = doc.add_table(rows=7, cols=3)
    tbl_met.alignment = WD_TABLE_ALIGNMENT.CENTER
    tbl_met.autofit = False
    
    col_w_m = [Inches(2.5), Inches(1.8), Inches(2.5)]
    hdrs_m = ["Métrica del Backlog", "Resultado", "Interpretación Práctica"]
    
    r0 = tbl_met.rows[0]
    trPr0 = r0._tr.get_or_add_trPr()
    trPr0.append(parse_xml(f'<w:cantSplit {nsdecls("w")}/>'))
    trPr0.append(parse_xml(f'<w:tblHeader {nsdecls("w")}/>'))
    
    for i, h in enumerate(hdrs_m):
        c = r0.cells[i]
        c.width = col_w_m[i]
        set_cell_background(c, HEX_NAVY)
        set_cell_margins(c, top=70, bottom=70, left=80, right=80)
        p = c.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER if i == 1 else WD_ALIGN_PARAGRAPH.LEFT
        r = p.add_run(h)
        r.font.name = "Arial"
        r.font.size = Pt(8.5)
        r.font.bold = True
        r.font.color.rgb = C_WHITE

    met_data = [
        ("Total de Épicas Estructuradas", "10 Épicas", "Cobertura completa del ciclo de vida del sistema."),
        ("Total de Historias de Usuario", "30 Historias", "Formuladas con roles, funciones y criterios claros."),
        ("Historias Completadas y Validadas (Done)", "26 Historias (86.7%)", "Funcionales y comprobadas en dispositivos Android."),
        ("Historias Proyectadas a Futuro", "4 Historias (13.3%)", "Roadmap definido para la versión 2.0."),
        ("Puntos de Historia Estimados", "154 Puntos", "Volumen global de esfuerzo calculado por el equipo."),
        ("Puntos Concluidos con Éxito", "128 Puntos (83.1%)", "Capacidad efectiva de desarrollo alcanzada en el periodo.")
    ]

    for idx, (m_nom, m_val, m_desc) in enumerate(met_data, start=1):
        row = tbl_met.rows[idx]
        trPr = row._tr.get_or_add_trPr()
        trPr.append(parse_xml(f'<w:cantSplit {nsdecls("w")}/>'))
        
        bg = HEX_LIGHT_BG if idx % 2 == 0 else "FFFFFF"
        for col_idx, val in enumerate([m_nom, m_val, m_desc]):
            c = row.cells[col_idx]
            c.width = col_w_m[col_idx]
            set_cell_background(c, bg)
            set_cell_margins(c, top=60, bottom=60, left=80, right=80)
            set_cell_borders(c, top=("single", "4", "0", HEX_BORDER),
                                bottom=("single", "4", "0", HEX_BORDER),
                                left=("single", "4", "0", HEX_BORDER),
                                right=("single", "4", "0", HEX_BORDER))
            p = c.paragraphs[0]
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER if col_idx == 1 else WD_ALIGN_PARAGRAPH.LEFT
            r = p.add_run(val)
            r.font.name = "Arial"
            r.font.size = Pt(8)
            if col_idx == 1:
                r.font.bold = True
                r.font.color.rgb = C_TEAL
            else:
                r.font.color.rgb = C_TEXT

    doc.add_paragraph().paragraph_format.space_after = Pt(4)

    # =========================================================================
    # SECCIÓN 6: ROADMAP Y FUTURAS LÍNEAS DE DESARROLLO
    # =========================================================================
    add_heading_1(doc, "6. Roadmap Tecnológico: Proyección para Versión 2.0")
    add_p(doc, "Como parte de una formulación tecnológica integral, se establecieron las siguientes líneas de desarrollo futuro para su implementación en etapas subsecuentes:")

    add_bullet(doc, "Dispensador Físico Inteligente (IoT con ESP32): ", "Diseño de un pastillero automatizado con microcontrolador ESP32 conectado por Bluetooth, el cual ilumina y libera mecánicamente únicamente la cavidad del medicamento programado.")
    add_bullet(doc, "Confirmación por Comandos de Voz ('Medi Voice'): ", "Módulo de interacción por voz que permita a pacientes con movilidad reducida o temblor en manos registrar tomas mediante frases naturales.")
    add_bullet(doc, "Exportación de Reportes Clínicos en PDF: ", "Generación de resúmenes mensuales estructurados con porcentajes de cumplimiento para facilitar el seguimiento médico en consultas periódicas.")
    add_bullet(doc, "Notificaciones Push Remotas Multi-dispositivo: ", "Integración de servicios en la nube para mantener informados en tiempo real a familiares que residen en ubicaciones lejanas.")

    # =========================================================================
    # SECCIÓN 7: CONCLUSIONES DEL EQUIPO
    # =========================================================================
    add_heading_1(doc, "7. Conclusiones y Aprendizajes del Equipo")
    add_p(doc, "El desarrollo de MedReminder AI en el marco de la asignatura de Formulación de Proyectos de Tecnología aportó aprendizajes formativos sustanciales:")

    add_bullet(doc, "La formulación previa previene retrabajo técnico: ", "Contar con un backlog claro y criterios de aceptación definidos permitió que cada integrante comprendiera el alcance de sus tareas, reduciendo discrepancias y optimizando el tiempo de desarrollo.")
    add_bullet(doc, "Diseño enfocado en las necesidades reales del usuario: ", "En aplicaciones orientadas a la salud, la prioridad técnica radica en la confiabilidad de las alarmas y la sencillez operativa, adaptando la tecnología a las capacidades del paciente.")
    add_bullet(doc, "Cumplimiento de objetivos del proyecto: ", "Se alcanzó un 86.7% de historias completadas y validadas en dispositivos reales, consolidando una base técnica funcional con un plan claro de crecimiento para futuras etapas.")

    print(f"Guardando documento Word en: {DOCX_OUT}")
    doc.save(DOCX_OUT)
    print("Documento DOCX generado exitosamente.")

def build_html_and_pdf():
    print("Generando versión HTML con diseño equilibrado y protección contra cortes...")
    
    html_content = f"""<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<title>Product Backlog Oficial - MedReminder AI | UTVT</title>
<style>
  @page {{
    size: letter;
    margin: 1.4cm 1.4cm 1.4cm 1.4cm;
  }}
  body {{
    font-family: Arial, Helvetica, sans-serif;
    font-size: 9.5pt;
    line-height: 1.35;
    color: #282C34;
    background-color: #FFFFFF;
    margin: 0;
    padding: 0;
  }}
  
  /* --- PORTADA INSTITUCIONAL UTVT --- */
  .cover-page {{
    min-height: 880px;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    text-align: center;
    page-break-after: always;
    padding: 10px 0;
  }}
  .cover-logos {{
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 25px;
  }}
  .cover-logos img.utvt {{
    height: 65px;
    width: auto;
  }}
  .cover-logos img.edomex {{
    height: 52px;
    width: auto;
  }}
  .cover-institution {{
    font-size: 13pt;
    font-weight: bold;
    color: #1B365D;
    line-height: 1.3;
  }}
  .cover-direction {{
    font-size: 10pt;
    font-weight: bold;
    color: #0E8074;
    margin-top: 6px;
    line-height: 1.3;
  }}
  .cover-program {{
    font-size: 9pt;
    font-weight: bold;
    color: #475569;
    margin-top: 10px;
  }}
  .cover-program-name {{
    font-size: 10.5pt;
    font-weight: bold;
    color: #1B365D;
    margin-top: 3px;
  }}
  .cover-section-title {{
    margin-top: 35px;
  }}
  .cover-label {{
    font-size: 9.5pt;
    font-weight: bold;
    color: #64748B;
    letter-spacing: 0.5px;
  }}
  .cover-job-title {{
    font-size: 13.5pt;
    font-weight: bold;
    color: #1B365D;
    margin-top: 6px;
    line-height: 1.3;
  }}
  .cover-job-sub {{
    font-size: 10.5pt;
    color: #0E8074;
    font-weight: bold;
    margin-top: 4px;
  }}
  .cover-meta {{
    margin-top: 25px;
  }}
  .cover-meta-item {{
    margin-bottom: 12px;
  }}
  .cover-meta-val {{
    font-size: 10.5pt;
    color: #1E293B;
  }}
  .cover-team {{
    margin-top: 18px;
    text-align: left;
    display: inline-block;
    font-size: 9.5pt;
    line-height: 1.5;
  }}
  .cover-team-line {{
    font-family: monospace;
    font-size: 9pt;
  }}
  .cover-footer {{
    margin-top: 25px;
    font-size: 9pt;
    font-weight: bold;
    color: #64748B;
    text-align: center;
  }}

  /* --- PÁGINAS Y CONTENEDORES --- */
  .page {{
    page-break-after: always;
  }}
  .page-last {{
    page-break-after: avoid;
  }}
  h1 {{
    font-size: 12.5pt;
    font-weight: bold;
    color: #1B365D;
    border-bottom: 2px solid #0E8074;
    padding-bottom: 4px;
    margin: 18px 0 10px 0;
    page-break-after: avoid;
    break-after: avoid;
  }}
  h2 {{
    font-size: 10.5pt;
    font-weight: bold;
    color: #0E8074;
    margin: 12px 0 4px 0;
    page-break-after: avoid;
    break-after: avoid;
  }}
  p {{
    margin: 0 0 8px 0;
    text-align: justify;
  }}
  ul {{
    margin: 0 0 8px 0;
    padding-left: 18px;
  }}
  li {{
    margin-bottom: 4px;
    text-align: justify;
  }}

  /* Contenedor de Épica que NUNCA se corta */
  .epic-card {{
    page-break-inside: avoid !important;
    break-inside: avoid !important;
    margin-bottom: 16px;
    border: 1px solid #CBD5E1;
    border-radius: 6px;
    padding: 10px 12px;
    background-color: #FFFFFF;
  }}
  .epic-card h2 {{
    margin-top: 0;
    font-size: 10.5pt;
    color: #1B365D;
    border-bottom: 1.5px solid #0E8074;
    padding-bottom: 3px;
  }}

  /* Tablas de Backlog protegidas */
  table.clean-table {{
    width: 100%;
    border-collapse: collapse;
    margin: 6px 0 2px 0;
    font-size: 8pt;
  }}
  table.clean-table thead {{
    display: table-header-group;
  }}
  table.clean-table tr {{
    page-break-inside: avoid !important;
    break-inside: avoid !important;
  }}
  table.clean-table th {{
    background-color: #1B365D;
    color: #ffffff;
    font-weight: bold;
    padding: 6px 8px;
    text-align: left;
    border: 1px solid #1B365D;
  }}
  table.clean-table td {{
    padding: 6px 8px;
    border: 1px solid #CBD5E1;
    vertical-align: top;
    line-height: 1.2;
  }}
  table.clean-table tr:nth-child(even) {{
    background-color: #F8FAFC;
  }}
  .badge-must {{
    background-color: #DCFCE7;
    color: #166534;
    font-weight: bold;
    padding: 2px 5px;
    border-radius: 3px;
    display: inline-block;
  }}
  .badge-should {{
    background-color: #E0F2FE;
    color: #0369A1;
    font-weight: bold;
    padding: 2px 5px;
    border-radius: 3px;
    display: inline-block;
  }}
  .badge-could {{
    background-color: #FEF3C7;
    color: #B45309;
    font-weight: bold;
    padding: 2px 5px;
    border-radius: 3px;
    display: inline-block;
  }}

  /* Cajas de llamada */
  .callout {{
    background-color: #F8FAFC;
    border: 1px solid #CBD5E1;
    border-left: 5px solid #1B365D;
    border-radius: 4px;
    padding: 9px 12px;
    margin: 10px 0;
    font-size: 9pt;
    page-break-inside: avoid;
    break-inside: avoid;
  }}
  .callout-teal {{
    background-color: #F0FDF4;
    border: 1px solid #BBF7D0;
    border-left: 5px solid #0E8074;
    border-radius: 4px;
    padding: 9px 12px;
    margin: 10px 0;
    font-size: 9pt;
    page-break-inside: avoid;
    break-inside: avoid;
  }}
  .callout-title {{
    font-weight: bold;
    font-size: 9.5pt;
    color: #1B365D;
    margin-bottom: 4px;
  }}
</style>
</head>
<body>

<!-- ========================================== -->
<!-- PORTADA OFICIAL UTVT                       -->
<!-- ========================================== -->
<div class="cover-page">
  <div class="cover-logos">
    <img src="file://{LOGO_UTVT}" class="utvt" alt="UTVT">
    <img src="file://{LOGO_EDOMEX}" class="edomex" alt="EDOMEX">
  </div>

  <div>
    <div class="cover-institution">UNIVERSIDAD TECNOLÓGICA DEL VALLE DE TOLUCA</div>
    <div class="cover-direction">DIRECCIÓN DE CARRERA DE TECNOLOGÍAS DE LA INFORMACIÓN Y COMUNICACIÓN</div>
    <div class="cover-program">PROGRAMA EDUCATIVO</div>
    <div class="cover-program-name">INGENIERÍA EN TECNOLOGÍAS DE LA INFORMACIÓN E INNOVACIÓN DIGITAL</div>
  </div>

  <div class="cover-section-title">
    <div class="cover-label">NOMBRE DEL TRABAJO:</div>
    <div class="cover-job-title">PRODUCT BACKLOG INTEGRAL Y HISTORIAL DE DESARROLLO</div>
    <div class="cover-job-sub">Proyecto: MedReminder AI (Recordatorio y Gestión de Medicamentos)</div>
  </div>

  <div class="cover-meta">
    <div class="cover-meta-item">
      <div class="cover-label">ASIGNATURA:</div>
      <div class="cover-meta-val" style="font-weight:bold; color:#0E8074;">Formulación de Proyectos de Tecnología</div>
    </div>
    <div class="cover-meta-item">
      <div class="cover-label">NOMBRE DEL DOCENTE:</div>
      <div class="cover-meta-val" style="font-weight:bold; color:#1B365D;">I.C. Héctor Pérez Paulín</div>
    </div>
  </div>

  <div>
    <div class="cover-label" style="text-align: center; margin-bottom: 6px;">PRESENTA:</div>
    <div style="text-align: center;">
      <div class="cover-team">
        <div class="cover-team-line">222410897 &nbsp;–&nbsp; Gutiérrez Ugalde Samuel</div>
        <div class="cover-team-line">222410935 &nbsp;–&nbsp; Nava García Rodrigo</div>
        <div class="cover-team-line">222411182 &nbsp;–&nbsp; Castillo Ramírez Nahúm Yabet</div>
        <div class="cover-team-line">222410915 &nbsp;–&nbsp; Ramírez Romero Pablo</div>
        <div class="cover-team-line">222410899 &nbsp;–&nbsp; Peña Hernández Alexander</div>
      </div>
    </div>
    <div style="margin-top: 14px; font-weight: bold; color: #1B365D; font-size: 10.5pt;">
      GRUPO: ITIID - 73
    </div>
  </div>

  <div class="cover-footer">
    SANTA MARÍA ATARASQUILLO, LERMA ESTADO DE MÉXICO. NOVIEMBRE 2026
  </div>
</div>

<!-- ========================================== -->
<!-- SECCIÓN 1: INTRODUCCIÓN EQUILIBRADA        -->
<!-- ========================================== -->
<div class="page">
  <h1>1. Introducción al Proyecto: Propósito y Problemática Atendida</h1>
  
  <p><b>Problemática identificada:</b> El proyecto atiende una situación recurrente en el entorno familiar: la dificultad que experimentan los adultos mayores y pacientes con tratamientos prolongados (tales como hipertensión arterial o diabetes) para mantener el control estricto de sus medicamentos. Con frecuencia surgen omisiones involuntarias o tomas duplicadas por falta de certeza sobre si la dosis ya fue ingerida, lo que representa un riesgo para la estabilidad de la salud.</p>

  <ul>
    <li><b>Desorganización en el botiquín doméstico:</b> En muchos hogares coexisten varios tratamientos simultáneos sobre la mesa. La similitud entre cajas y frascos incrementa la probabilidad de confusiones en horarios y dosis.</li>
    <li><b>Limitaciones de aplicaciones existentes:</b> Tras analizar alternativas disponibles en tiendas móviles, se detectaron barreras importantes: saturación de publicidad invasiva que desorienta a personas mayores, modelos de cobro periódico en moneda extranjera y falta de fiabilidad en alarmas cuando el móvil entra en reposo o carece de conexión a internet.</li>
    <li><b>Incertidumbre en el núcleo familiar:</b> Los familiares a cargo experimentan inquietud constante por verificar si el paciente tomó su medicamento oportunamente, lo que suele derivar en llamadas reiteradas y pérdida de autonomía del paciente.</li>
  </ul>

  <div class="callout-teal">
    <div class="callout-title">Objetivo del Proyecto MedReminder AI</div>
    Desarrollar una solución móvil accesible, privada y altamente confiable que asegure la activación puntual de alarmas visuales y acústicas aun con el dispositivo bloqueado o sin conexión a internet, incorpore asistencia de Inteligencia Artificial local para interpretar recetas mediante fotografía sin costos recurrentes, descuente existencias del botiquín y emita alertas automáticas al cuidador ante retrasos significativos.
  </div>

  <h1>2. Metodología de Trabajo y Organización del Backlog</h1>
  <p>Con el objetivo de coordinar el desarrollo de manera estructurada y eficiente, el equipo implementó principios de metodologías ágiles basadas en Scrum:</p>
  <ul>
    <li><b>El Backlog como herramienta viva:</b> La pila de trabajo no permaneció estática; se refinó y ajustó periódicamente tras validar cada incremento en dispositivos físicos reales, incorporando mejoras detectadas durante las pruebas.</li>
    <li><b>Rol del Product Owner:</b> El compañero Rodrigo Nava García asumió la responsabilidad de Product Owner, priorizando las necesidades clínicas y de accesibilidad del paciente sobre requerimientos secundarios o meramente visuales.</li>
    <li><b>Estructura canónica de Historias de Usuario:</b> Cada funcionalidad fue descrita bajo el formato estándar de Mike Cohn: <i>'Como [rol], quiero [función], para [beneficio tangible]'</i>, asegurando que cada tarea aporte valor verificable al usuario.</li>
    <li><b>Criterios de Aceptación (Definition of Done):</b> Ninguna historia se dio por concluida hasta verificar su funcionamiento en un dispositivo Android real, comprobar la persistencia de datos y asegurar su operatividad fuera de línea.</li>
    <li><b>Priorización MoSCoW y Estimación:</b> Las historias se clasificaron en Must (indispensables), Should (importantes), Could (deseables) y Won't (proyectadas a futuro), asignando puntos de esfuerzo relativo en escala Fibonacci simplificada (1 a 8 puntos).</li>
  </ul>
</div>

<!-- ========================================== -->
<!-- SECCIÓN 3: EL PRODUCT BACKLOG COMPLETO    -->
<!-- ========================================== -->
<div>
  <h1 style="margin: 20px 0 10px 0;">3. Product Backlog Completo de MedReminder AI</h1>
  <p style="margin-bottom: 14px;">A continuación se presentan las 10 Épicas y las 30 Historias de Usuario estructuradas que componen el proyecto, acompañadas de sus criterios de aceptación y estimación de esfuerzo:</p>
"""

    for ep in EPICAS_DATA:
        html_content += f"""
  <div class="epic-card">
    <h2>Épica {ep['num']}: {ep['nombre']}</h2>
    <p style="font-size: 8.5pt; color: #475569; margin: 2px 0 6px 0;"><b>Objetivo técnico de la épica:</b> {ep['objetivo']}</p>
    <table class="clean-table">
      <thead>
        <tr>
          <th style="width: 8%; text-align: center;">ID</th>
          <th style="width: 22%;">Historia de Usuario</th>
          <th style="width: 36%;">Estructura Canónica (Como / Quiero / Para)</th>
          <th style="width: 20%;">Criterios de Aceptación</th>
          <th style="width: 7%; text-align: center;">Prior.</th>
          <th style="width: 7%; text-align: center;">Pts.</th>
        </tr>
      </thead>
      <tbody>
"""
        for st in ep["historias"]:
            badge_class = "badge-must" if st["prioridad"] in ["Must", "Crítica"] else ("badge-should" if st["prioridad"] == "Should" else "badge-could")
            html_content += f"""
        <tr>
          <td style="text-align: center; font-weight: bold; color: #1B365D;">{st['id']}</td>
          <td><b>{st['nombre']}</b></td>
          <td>
            <span style="color:#0E8074; font-weight:bold;">Como</span> {st['como']},<br>
            <span style="color:#1B365D; font-weight:bold;">quiero</span> {st['quiero']},<br>
            <span style="color:#16A34A; font-weight:bold;">para</span> {st['para']}.
          </td>
          <td>{st['criterios']}</td>
          <td style="text-align: center;"><span class="{badge_class}">{st['prioridad']}</span></td>
          <td style="text-align: center; font-weight: bold; color: #1B365D;">{st['puntos']}</td>
        </tr>
"""
        html_content += """
      </tbody>
    </table>
  </div>
"""

    html_content += f"""
</div>

<!-- ========================================== -->
<!-- SECCIÓN 4: RETOS TÉCNICOS Y SOLUCIONES     -->
<!-- ========================================== -->
<div class="page" style="page-break-before: always;">
  <h1>4. Retos Técnicos y Soluciones Implementadas durante el Desarrollo</h1>
  <p>Durante las pruebas de integración en dispositivos físicos se presentaron diversos retos técnicos que motivaron ajustes directos en el backlog. A continuación se documentan los cuatro casos más significativos:</p>

  <h2>Caso 1: Ejecución precisa de alarmas en modo de reposo (Doze Mode)</h2>
  <p>Inicialmente se utilizaron notificaciones locales estándar de Android. Aunque operaban correctamente durante el uso activo del teléfono, al dejar el dispositivo en reposo nocturno el sistema operativo retrasaba la notificación hasta 25 minutos con el fin de ahorrar batería.<br>
  <b>Solución técnica en el Backlog:</b> Se incorporó la historia <b>HU-13</b> con prioridad 'Crítica'. Se sustituyeron las notificaciones convencionales por <code>AlarmManager</code> nativo con <code>setExactAndAllowWhileIdle()</code> y una Activity con Full-Screen Intent. Con esto se garantizó que la pantalla se active puntualmente a la hora programada aun con el teléfono en reposo profundo.</p>

  <h2>Caso 2: Resolución dinámica de red local en laboratorios escolares</h2>
  <p>En las instalaciones de la UTVT, la infraestructura de red asigna direcciones IP variables al alternar entre redes académicas, talleres o puntos de acceso móviles. Esto interrumpía la comunicación entre la app y el servidor local en la computadora portátil.<br>
  <b>Solución técnica en el Backlog:</b> Se formuló la historia <b>HU-03</b> para dotar a la aplicación de un módulo de detección dinámica de subred. La app ejecuta un sondeo ágil con timeout de 400 ms entre direcciones IP predefinidas y establece conexión automática sin requerir ajustes manuales en el código.</p>

  <h2>Caso 3: Integración de Inteligencia Artificial local preservando costos y privacidad</h2>
  <p>Para la lectura de recetas médicas y la orientación clínica se evaluó el uso de servicios comerciales en la nube. No obstante, esto implicaba costos periódicos no viables y riesgos en la confidencialidad de datos personales de salud.<br>
  <b>Solución técnica en el Backlog:</b> Se desarrollaron las historias <b>HU-16</b> y <b>HU-17</b> integrando <b>Ollama</b> de manera local con el modelo afinado <code>medi-clinico</code>. De este modo, el procesamiento de imágenes y consultas se realiza directamente en la infraestructura del equipo sin costos de API y garantizando que los datos no abandonen el entorno privado.</p>

  <h2>Caso 4: Accesibilidad visual y ergonomía para adultos mayores</h2>
  <p>El prototipo inicial empleaba contrastes intensos y colores fluorescentes. Durante las pruebas con personas adultas mayores se observó que dicha interfaz producía fatiga visual y dificultaba la lectura de textos pequeños.<br>
  <b>Solución técnica en el Backlog:</b> A través de la historia <b>HU-25</b> se estandarizó una paleta visual basada en Clinical Teal (<code>#0E8074</code>) y Soft Mint, estableciendo botones táctiles con altura mínima de 48dp y tipografía de al menos 16sp para favorecer la interacción en personas con debilidad visual o movilidad reducida.</p>
</div>

<!-- ========================================== -->
<!-- SECCIÓN 5: MÉTRICAS Y CONCLUSIONES        -->
<!-- ========================================== -->
<div class="page-last" style="page-break-before: always;">
  <h1>5. Balance de Métricas y Estado Actual del Proyecto</h1>
  <p>El avance global del proyecto respecto al esfuerzo estimado en el backlog se resume en los siguientes indicadores cuantitativos:</p>
  
  <table class="clean-table" style="font-size: 8.5pt; margin-bottom: 16px;">
    <thead>
      <tr>
        <th style="width: 35%;">Métrica del Backlog</th>
        <th style="width: 25%; text-align: center;">Resultado</th>
        <th style="width: 40%;">Interpretación Práctica</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td><b>Total de Épicas Estructuradas</b></td>
        <td style="text-align: center; font-weight: bold; color: #0E8074;">10 Épicas</td>
        <td>Cobertura completa del ciclo de vida del sistema.</td>
      </tr>
      <tr>
        <td><b>Total de Historias de Usuario</b></td>
        <td style="text-align: center; font-weight: bold; color: #1B365D;">30 Historias</td>
        <td>Formuladas con roles, funciones y criterios claros.</td>
      </tr>
      <tr>
        <td><b>Historias Completadas y Validadas (Done)</b></td>
        <td style="text-align: center; font-weight: bold; color: #16A34A;">26 Historias (86.7%)</td>
        <td>Funcionales y comprobadas en dispositivos Android.</td>
      </tr>
      <tr>
        <td><b>Historias Proyectadas a Futuro</b></td>
        <td style="text-align: center; font-weight: bold; color: #B45309;">4 Historias (13.3%)</td>
        <td>Roadmap definido para la versión 2.0.</td>
      </tr>
      <tr>
        <td><b>Puntos de Historia Estimados</b></td>
        <td style="text-align: center; font-weight: bold; color: #1B365D;">154 Puntos</td>
        <td>Volumen global de esfuerzo calculado por el equipo.</td>
      </tr>
      <tr>
        <td><b>Puntos Concluidos con Éxito</b></td>
        <td style="text-align: center; font-weight: bold; color: #16A34A;">128 Puntos (83.1%)</td>
        <td>Capacidad efectiva de desarrollo alcanzada en el periodo.</td>
      </tr>
    </tbody>
  </table>

  <h1>6. Roadmap Tecnológico: Proyección para Versión 2.0</h1>
  <ul>
    <li><b>Dispensador Físico Inteligente (IoT con ESP32):</b> Diseño de un pastillero automatizado con microcontrolador ESP32 conectado por Bluetooth, el cual ilumina y libera mecánicamente únicamente la cavidad del medicamento programado.</li>
    <li><b>Confirmación por Comandos de Voz ('Medi Voice'):</b> Módulo de interacción por voz que permita a pacientes con movilidad reducida o temblor en manos registrar tomas mediante frases naturales.</li>
    <li><b>Exportación de Reportes Clínicos en PDF:</b> Generación de resúmenes mensuales estructurados con porcentajes de cumplimiento para facilitar el seguimiento médico en consultas periódicas.</li>
    <li><b>Notificaciones Push Remotas Multi-dispositivo:</b> Integración de servicios en la nube para mantener informados en tiempo real a familiares que residen en ubicaciones lejanas.</li>
  </ul>

  <h1>7. Conclusiones y Aprendizajes del Equipo</h1>
  <p>El desarrollo de MedReminder AI en el marco de la asignatura de Formulación de Proyectos de Tecnología aportó aprendizajes formativos sustanciales:</p>
  <ul>
    <li><b>La formulación previa previene retrabajo técnico:</b> Contar con un backlog claro y criterios de aceptación definidos permitió que cada integrante comprendiera el alcance de sus tareas, reduciendo discrepancias y optimizando el tiempo de desarrollo.</li>
    <li><b>Diseño enfocado en las necesidades reales del usuario:</b> En aplicaciones orientadas a la salud, la prioridad técnica radica en la confiabilidad de las alarmas y la sencillez operativa, adaptando la tecnología a las capacidades del paciente.</li>
    <li><b>Cumplimiento de objetivos del proyecto:</b> Se alcanzó un 86.7% de historias completadas y validadas en dispositivos reales, consolidando una base técnica funcional con un plan claro de crecimiento para futuras etapas.</li>
  </ul>
</div>

</body>
</html>
"""

    with open(HTML_OUT, "w", encoding="utf-8") as f:
        f.write(html_content)
    print(f"Archivo HTML guardado en: {HTML_OUT}")

    chrome_cmd = [
        "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
        "--headless",
        "--disable-gpu",
        "--no-sandbox",
        f"--print-to-pdf={PDF_OUT}",
        HTML_OUT
    ]
    try:
        subprocess.run(chrome_cmd, check=True)
        print(f"Documento PDF generado exitosamente en: {PDF_OUT}")
    except Exception as e:
        print(f"Aviso al compilar PDF con Chrome ({e})")

if __name__ == "__main__":
    build_docx()
    build_html_and_pdf()
    print("\n¡Documentos generados en el punto medio perfecto entre formal y natural!")
