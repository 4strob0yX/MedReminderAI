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
DOCX_OUT = os.path.join(DOCS_DIR, "Practica_Product_Backlog_MedReminderAI.docx")
HTML_OUT = os.path.join(DOCS_DIR, "Practica_Product_Backlog_MedReminderAI.html")
PDF_OUT = os.path.join(DOCS_DIR, "Practica_Product_Backlog_MedReminderAI.pdf")

LOGO_UTVT = os.path.join(DOCS_DIR, "logo_utvt.png")
LOGO_EDOMEX = os.path.join(DOCS_DIR, "logo_edomex.png")

# Palette
C_NAVY = RGBColor(27, 54, 93)      # #1B365D
C_TEAL = RGBColor(14, 128, 116)    # #0E8074
C_TEXT = RGBColor(40, 44, 52)      # #282C34
C_MUTED = RGBColor(100, 116, 139)  # #64748B
C_WHITE = RGBColor(255, 255, 255)

HEX_NAVY = "1B365D"
HEX_TEAL = "0E8074"
HEX_LIGHT_BG = "F8FAFC"
HEX_CARD_BG = "F0FDF4"
HEX_BORDER = "CBD5E1"

def set_cell_background(cell, hex_color):
    tcPr = cell._tc.get_or_add_tcPr()
    shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{hex_color}"/>')
    tcPr.append(shd)

def set_cell_margins(cell, top=140, bottom=140, left=180, right=180):
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

# Start with Portada.docx
doc = docx.Document(PORTADA_SRC)

# Update the cover page title in paragraph 8/9
# P8: NOMBRE DEL TRABAJO:
# P9: PRÁCTICA: INVESTIGACIÓN Y ESTRUCTURACIÓN DEL PRODUCT BACKLOG
p9 = doc.paragraphs[9]
p9.text = "PRÁCTICA: INVESTIGACIÓN Y ESTRUCTURACIÓN DEL PRODUCT BACKLOG\nProyecto Integrador: MedReminder AI"
for r in p9.runs:
    r.font.bold = True
    r.font.size = Pt(13)
    r.font.color.rgb = C_NAVY

# P24: update date if desired
p24 = doc.paragraphs[24]
p24.text = "SANTA MARÍA ATARASQUILLO, LERMA ESTADO DE MÉXICO. NOVIEMBRE 2026"

# Add Page Break to start Section 1 on Page 2
doc.add_page_break()

# Function to add clean section headings
def add_sec_title(doc, title):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(14)
    p.paragraph_format.space_after = Pt(8)
    p.paragraph_format.keep_with_next = True
    r = p.add_run(title)
    r.font.name = "Arial"
    r.font.size = Pt(13)
    r.font.bold = True
    r.font.color.rgb = C_NAVY
    return p

def add_sub_title(doc, title):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(10)
    p.paragraph_format.space_after = Pt(4)
    p.paragraph_format.keep_with_next = True
    r = p.add_run(title)
    r.font.name = "Arial"
    r.font.size = Pt(11)
    r.font.bold = True
    r.font.color.rgb = C_TEAL
    return p

def add_body_p(doc, bold_prefix, text, space_after=6):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(2)
    p.paragraph_format.space_after = Pt(space_after)
    p.paragraph_format.line_spacing = 1.2
    if bold_prefix:
        r_pre = p.add_run(bold_prefix)
        r_pre.font.name = "Arial"
        r_pre.font.size = Pt(10)
        r_pre.font.bold = True
        r_pre.font.color.rgb = C_NAVY
    r = p.add_run(text)
    r.font.name = "Arial"
    r.font.size = Pt(10)
    r.font.color.rgb = C_TEXT
    return p

def add_clean_box(doc, title, runs, border_color=HEX_TEAL, bg_color=HEX_LIGHT_BG):
    tbl = doc.add_table(rows=1, cols=1)
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    tbl.autofit = False
    c = tbl.cell(0, 0)
    c.width = Inches(6.8)
    set_cell_background(c, bg_color)
    set_cell_margins(c, top=140, bottom=140, left=180, right=160)
    set_cell_borders(c, left=("single", "24", "0", border_color),
                        top=("single", "4", "0", HEX_BORDER),
                        bottom=("single", "4", "0", HEX_BORDER),
                        right=("single", "4", "0", HEX_BORDER))
    p = c.paragraphs[0]
    p.paragraph_format.space_after = Pt(2)
    p.paragraph_format.line_spacing = 1.25
    if title:
        rt = p.add_run(title + "\n")
        rt.font.name = "Arial"
        rt.font.size = Pt(10.5)
        rt.font.bold = True
        rt.font.color.rgb = C_NAVY
    for txt, bld, itl, clr in runs:
        r = p.add_run(txt)
        r.font.name = "Arial"
        r.font.size = Pt(10)
        r.font.bold = bld
        r.font.italic = itl
        r.font.color.rgb = clr if clr else C_TEXT
    doc.add_paragraph().paragraph_format.space_after = Pt(4)

# ==============================================================================
# PÁGINA 2: SECCIÓN 1: ¿QUÉ ES EL PRODUCT BACKLOG Y QUIÉN LO MANDA?
# ==============================================================================
add_sec_title(doc, "SECCIÓN 1: ¿Qué es el Product Backlog y quién lo manda?")

add_sub_title(doc, "Investigación:")
add_body_p(doc, "1. ¿Qué es un Product Backlog en Scrum y por qué se dice que es un documento «vivo» que nunca se termina?\n",
           "El Product Backlog es la lista ordenada de todo lo que el equipo planea construir o mejorar en la aplicación: "
           "nuevas funcionalidades, corrección de errores y cambios técnicos. En lugar de ser un documento rígido que se congela al inicio del proyecto, "
           "aquí los elementos se ordenan y ajustan de manera constante según el valor que le aportan al usuario y al negocio.\n\n"
           "Se dice que es un documento «vivo» que nunca se termina porque mientras la aplicación tenga usuarios activos, el proyecto nunca está "
           "completamente cerrado. Siempre surgen sugerencias de los médicos, actualizaciones del sistema operativo (como Android), ideas de los familiares "
           "o fallas que corregir. El Backlog se refina y actualiza en cada sprint; únicamente se da por terminado cuando el producto se retira formalmente del mercado.")

add_body_p(doc, "2. ¿Quién es el Product Owner (Dueño del Producto) y cuál es su única responsabilidad frente al equipo de desarrollo?\n",
           "El Product Owner es el integrante del equipo que representa la voz del cliente y de los usuarios finales (pacientes, familiares y personal médico). "
           "No actúa como un jefe tradicional que reparte órdenes o vigila horarios.\n\n"
           "Su única responsabilidad fundamental frente al equipo de desarrollo es maximizar el valor del producto que construimos. "
           "Esto significa que él tiene la última palabra para decidir qué funcionalidades van primero en el Backlog y explicar con total claridad el porqué. "
           "En resumen: el Product Owner decide el «qué» y el «para qué», mientras que el equipo de desarrollo decide con total autonomía el «cómo» técnico.")

add_sub_title(doc, "Aplicación en Nuestro Proyecto (MedReminder AI):")
add_body_p(doc, "1. Product Owner del Equipo: ",
           "Elegimos a Rodrigo Nava García como Product Owner de MedReminder AI. Su función es asegurar que cada funcionalidad resuelva "
           "un problema real de adherencia médica y accesibilidad para adultos mayores, antes de pasar a detalles secundarios.")

add_body_p(doc, "2. Top 3 de Funcionalidades Críticas de Nuestro Backlog:\n",
           "Estas son las tres funcionalidades más importantes que encabezan nuestra pila de trabajo para garantizar la utilidad de la app:")

# Table Top 3
t_top3 = doc.add_table(rows=4, cols=3)
t_top3.alignment = WD_TABLE_ALIGNMENT.CENTER
t_top3.autofit = False

col_w = [Inches(1.0), Inches(2.5), Inches(3.3)]
hdrs = ["Prioridad", "Funcionalidad", "Justificación Práctica de Negocio / Clínica"]

row_h = t_top3.rows[0]
for i, h in enumerate(hdrs):
    c = row_h.cells[i]
    c.width = col_w[i]
    set_cell_background(c, HEX_NAVY)
    set_cell_margins(c, top=100, bottom=100, left=120, right=120)
    p = c.paragraphs[0]
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER if i == 0 else WD_ALIGN_PARAGRAPH.LEFT
    r = p.add_run(h)
    r.font.name = "Arial"
    r.font.size = Pt(9.5)
    r.font.bold = True
    r.font.color.rgb = C_WHITE

top3_items = [
    ("#1 (Crítica)", "Motor de Alarmas Heads-Up Locales en Android", 
     "Hace que la alarma suene en el segundo exacto a pantalla completa, aun con celular bloqueado, sin internet o en ahorro de batería. Si falla, el paciente olvida el medicamento."),
    ("#2 (Alta)", "Confirmación de Toma y Descuento en Botiquín", 
     "Un botón directo para confirmar que ya se ingirió la pastilla, descontando el stock local para evitar confusiones de «¿ya me la tomé?» y prevenir sobredosis."),
    ("#3 (Alta)", "Avisos Automáticos al Cuidador ante Omisiones", 
     "Si el paciente pospone la alarma más del límite permitido (20 min) o no se toma una dosis crítica, el sistema notifica de inmediato al familiar responsable.")
]

for idx, item in enumerate(top3_items, start=1):
    row = t_top3.rows[idx]
    bg = HEX_LIGHT_BG if idx % 2 == 1 else "FFFFFF"
    for col_i in range(3):
        c = row.cells[col_i]
        c.width = col_w[col_i]
        set_cell_background(c, bg)
        set_cell_margins(c, top=90, bottom=90, left=120, right=120)
        set_cell_borders(c, bottom=("single", "4", "0", HEX_BORDER), top=("single", "4", "0", HEX_BORDER))
        p = c.paragraphs[0]
        p.paragraph_format.line_spacing = 1.15
        if col_i == 0:
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r = p.add_run(item[col_i])
        r.font.name = "Arial"
        r.font.size = Pt(9)
        if col_i == 0:
            r.font.bold = True
            r.font.color.rgb = C_TEAL
        elif col_i == 1:
            r.font.bold = True
            r.font.color.rgb = C_NAVY
        else:
            r.font.color.rgb = C_TEXT

# Page Break for Section 2
doc.add_page_break()

# ==============================================================================
# PÁGINA 3: SECCIÓN 2: ¿CÓMO SE ESCRIBE UNA HISTORIA DE USUARIO?
# ==============================================================================
add_sec_title(doc, "SECCIÓN 2: ¿Cómo se escribe una Historia de Usuario?")

add_sub_title(doc, "Investigación:")
add_body_p(doc, "1. ¿Qué es una Historia de Usuario (User Story) y cuál es la estructura canónica diseñada por Mike Cohn?\n",
           "Una Historia de Usuario es una descripción breve y en lenguaje cotidiano sobre lo que necesita una persona al usar la aplicación. "
           "No se redacta como una especificación técnica aburrida, sino como una herramienta práctica para que los programadores entiendan "
           "el problema real del usuario y el valor que le vamos a entregar.\n\n"
           "Mike Cohn diseñó la estructura canónica más usada en desarrollo ágil:")

# Clean Box for Mike Cohn Formula
add_clean_box(doc, "Estructura Canónica de Mike Cohn:", [
    ("« Como ", True, False, C_NAVY),
    ("[ Rol del usuario ]", True, True, C_TEAL),
    (",  quiero ", True, False, C_NAVY),
    ("[ Funcionalidad específica ]", True, True, C_TEAL),
    (",  para ", True, False, C_NAVY),
    ("[ Beneficio de negocio / Valor ]", True, True, C_TEAL),
    (" »", True, False, C_NAVY)
], border_color=HEX_NAVY, bg_color="F1F5F9")

add_body_p(doc, "Explicación de cada parte:\n",
           "• «Como [Rol]»: Define con claridad quién es la persona (por ejemplo: paciente de la tercera edad, familiar cuidador).\n"
           "• «Quiero [Funcionalidad]»: Describe la acción que desea realizar en la app, sin meter términos de código o bases de datos de forma anticipada.\n"
           "• «Para [Beneficio]»: Explica la razón de ser de la funcionalidad. Esta parte es la más importante porque justifica si realmente vale la pena programarla.")

add_sub_title(doc, "Aplicación en Nuestro Proyecto (MedReminder AI):")
add_body_p(doc, "Requerimiento Tradicional de la Fase 1 (Manual Técnico):\n",
           "«RF-03: Alarmas Heads-Up Locales — El sistema debe disparar alarmas acústicas, visuales y hápticas en el segundo exacto mediante AlarmManager en Android, incluso en Doze mode, notificando al usuario sobre la toma de sus medicamentos programados.»")

add_body_p(doc, "Transformación Obligatoria a la Fórmula Canónica:\n",
           "Pasamos de una instrucción técnica sobre la API de Android a una historia centrada en la vida del paciente:")

# Card Box
add_clean_box(doc, "TARJETA DE HISTORIA DE USUARIO (HU-01: ALARMAS CLÍNICAS)", [
    ("« Como ", True, False, C_NAVY),
    ("adulto mayor con problemas de memoria que toma varios medicamentos al día,", True, False, C_TEXT),
    ("\n   quiero ", True, False, C_NAVY),
    ("recibir una alarma clara en pantalla completa a la hora exacta de mi dosis (aunque mi celular esté bloqueado o sin internet),", True, False, C_TEXT),
    ("\n   para ", True, False, C_NAVY),
    ("tomarme mis pastillas a tiempo por mí mismo, evitar descompensaciones de salud y no depender de que alguien me esté recordando a cada rato.", True, False, C_TEXT),
    (" »", True, False, C_NAVY)
], border_color="16A34A", bg_color=HEX_CARD_BG)

add_body_p(doc, "Diferencia Práctica: ",
           "El requerimiento tradicional solo le decía al programador «usa AlarmManager». La Historia de Usuario le recuerda al equipo que el objetivo "
           "es devolverle la autonomía y seguridad a un adulto mayor, asegurando que la interfaz sea fácil de ver y que no dependa de tener saldo o internet.")

# Page Break for Section 3
doc.add_page_break()

# ==============================================================================
# PÁGINA 4: SECCIÓN 3: LAS REGLAS DE ORO (LAS 3 C Y CRITERIOS DE ACEPTACIÓN)
# ==============================================================================
add_sec_title(doc, "SECCIÓN 3: Las reglas de oro (Las 3 C y Criterios de Aceptación)")

add_sub_title(doc, "Investigación:")
add_body_p(doc, "1. ¿En qué consiste el modelo de las 3 C de Ron Jeffries?\n",
           "Ron Jeffries explicó que una Historia de Usuario no es solo texto en un papel, sino tres pasos que deben cumplirse siempre:\n"
           "• 1. Card (Tarjeta): La ficha física o tarjeta digital donde se escribe la historia. Es breve a propósito porque solo representa una «promesa de conversación».\n"
           "• 2. Conversation (Conversación): La charla directa entre el Product Owner y los desarrolladores antes de programar para resolver dudas, revisar casos especiales y ponerse de acuerdo.\n"
           "• 3. Confirmation (Confirmación): Los criterios de aceptación con los que probaremos la función para confirmar que ya quedó bien hecha.")

add_body_p(doc, "2. ¿Qué son los Criterios de Aceptación y por qué una tarjeta no se puede programar si no los tiene?\n",
           "Son las reglas claras y medibles que nos dicen qué condiciones debe cumplir la función para darla por buena. "
           "Una tarjeta no se puede programar sin ellos porque el programador terminaría adivinando cómo debe funcionar la app, haría cosas de más "
           "o dejaría fuera detalles importantes. Además, en la revisión con el cliente no habría forma objetiva de saber si la tarea está realmente terminada.")

add_sub_title(doc, "Aplicación en Nuestro Proyecto (MedReminder AI):")

# Conversacion
add_clean_box(doc, "1. CONVERSACIÓN: Dudas Técnicas del Equipo al Product Owner (Rodrigo Nava)", [
    ("• Duda 1 (Teléfono en Silencio o Modo No Molestar):\n", True, False, C_NAVY),
    ("  Pregunta del Equipo: ", True, True, C_TEAL),
    ("«¿Qué pasa si el paciente tiene el celular en vibración o No Molestar? ¿La alarma debe sonar a la fuerza o se queda en silencio?»\n", False, False, C_TEXT),
    ("  Respuesta de Rodrigo (PO): ", True, True, C_NAVY),
    ("«Para medicinas críticas (presión o insulina) debe sonar a la fuerza usando el canal de alarma del sistema (USAGE_ALARM). Para vitaminas comunes puede respetar el modo silencio.»\n\n", False, False, C_TEXT),
    ("• Duda 2 (Límite de Posposición):\n", True, False, C_NAVY),
    ("  Pregunta del Equipo: ", True, True, C_TEAL),
    ("«¿Cuántas veces puede posponer la alarma el abuelo? Si no le ponemos límite, podría posponerla todo el día.»\n", False, False, C_TEXT),
    ("  Respuesta de Rodrigo (PO): ", True, True, C_NAVY),
    ("«Máximo 2 veces de 10 minutos cada una. Si a la segunda no confirma en los siguientes 10 minutos, se marca como Omitida y se le avisa al cuidador.»", False, False, C_TEXT)
], border_color=HEX_NAVY, bg_color="F8FAFC")

# Confirmacion Table
add_body_p(doc, "2. CONFIRMACIÓN: Criterios de Aceptación Medibles de la Función (Checklist):\n",
           "Para que la historia HU-01 se considere terminada (Done), debe pasar estas tres pruebas medibles:")

t_ca = doc.add_table(rows=4, cols=2)
t_ca.alignment = WD_TABLE_ALIGNMENT.CENTER
t_ca.autofit = False

col_w_ca = [Inches(2.2), Inches(4.6)]
hdrs_ca = ["Regla Verificable", "Criterio Medible y Prueba de Aceptación"]

row_h_ca = t_ca.rows[0]
for i, h in enumerate(hdrs_ca):
    c = row_h_ca.cells[i]
    c.width = col_w_ca[i]
    set_cell_background(c, HEX_NAVY)
    set_cell_margins(c, top=90, bottom=90, left=120, right=120)
    p = c.paragraphs[0]
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER if i == 0 else WD_ALIGN_PARAGRAPH.LEFT
    r = p.add_run(h)
    r.font.name = "Arial"
    r.font.size = Pt(9.5)
    r.font.bold = True
    r.font.color.rgb = C_WHITE

ca_items = [
    ("Criterio 1:\nPuntualidad y Despertar de Pantalla",
     "La alarma debe sonar a la hora exacta (tolerancia máxima de ±2 segundos) y encender la pantalla completa con sonido y vibración durante al menos 45 segundos, incluso con el teléfono bloqueado y sin internet."),
    ("Criterio 2:\nConfirmación y Descuento en Botiquín",
     "La pantalla solo muestra dos botones grandes («Tomar Ahora» y «Posponer 10 min»). Al tocar «Tomar Ahora», se descuenta 1 pastilla del stock local en menos de 1 segundo y se cierra la alarma."),
    ("Criterio 3:\nLímite de Posposición y Alerta al Cuidador",
     "El botón «Posponer» solo se puede usar 2 veces consecutivas. Si pasan 10 minutos tras la segunda posposición sin confirmación, la dosis se registra como Omitida y se envía la alerta al contacto de emergencia.")
]

for idx, item in enumerate(ca_items, start=1):
    row = t_ca.rows[idx]
    bg = HEX_LIGHT_BG if idx % 2 == 1 else "FFFFFF"
    for col_i in range(2):
        c = row.cells[col_i]
        c.width = col_w_ca[col_i]
        set_cell_background(c, bg)
        set_cell_margins(c, top=80, bottom=80, left=120, right=120)
        set_cell_borders(c, bottom=("single", "4", "0", HEX_BORDER), top=("single", "4", "0", HEX_BORDER))
        p = c.paragraphs[0]
        p.paragraph_format.line_spacing = 1.15
        r = p.add_run(item[col_i])
        r.font.name = "Arial"
        r.font.size = Pt(9)
        if col_i == 0:
            r.font.bold = True
            r.font.color.rgb = C_TEAL
        else:
            r.font.color.rgb = C_TEXT

doc.save(DOCX_OUT)
print(f"Clean DOCX generated successfully at: {DOCX_OUT}")

# ==============================================================================
# HTML Generation for Chrome Headless PDF (Matching Official Cover + Clean Layout)
# ==============================================================================
html_clean = f"""<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<title>Práctica: Investigación y Estructuración del Product Backlog</title>
<style>
  @page {{
    size: letter;
    margin: 2cm 2cm 2cm 2cm;
  }}
  body {{
    font-family: Arial, Helvetica, sans-serif;
    font-size: 10pt;
    line-height: 1.35;
    color: #282C34;
    margin: 0;
    padding: 0;
  }}
  
  /* --- PORTADA OFICIAL (PAGE 1) --- */
  .cover-page {{
    height: 100%;
    min-height: 880px;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    text-align: center;
    page-break-after: always;
  }}
  .cover-logos {{
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 25px;
  }}
  .cover-logos img.utvt {{
    height: 60px;
    width: auto;
  }}
  .cover-logos img.edomex {{
    height: 48px;
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
    margin-top: 30px;
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
    margin-top: 20px;
    text-align: left;
    display: inline-block;
    font-size: 10pt;
    line-height: 1.5;
  }}
  .cover-team-line {{
    font-family: monospace;
    font-size: 9.5pt;
  }}
  .cover-footer {{
    margin-top: 30px;
    font-size: 9pt;
    font-weight: bold;
    color: #64748B;
    text-align: center;
  }}

  /* --- PÁGINAS DE CONTENIDO --- */
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
    margin: 0 0 14px 0;
  }}
  h2 {{
    font-size: 11pt;
    font-weight: bold;
    color: #0E8074;
    margin: 14px 0 6px 0;
  }}
  p {{
    margin: 0 0 10px 0;
    text-align: justify;
  }}
  .q-title {{
    font-weight: bold;
    color: #1B365D;
  }}
  
  /* Tablas limpias y con espacio */
  table.clean-table {{
    width: 100%;
    border-collapse: collapse;
    margin: 12px 0 14px 0;
    font-size: 9pt;
  }}
  table.clean-table th {{
    background-color: #1B365D;
    color: #ffffff;
    font-weight: bold;
    padding: 8px 10px;
    text-align: left;
    border: 1px solid #1B365D;
  }}
  table.clean-table td {{
    padding: 8px 10px;
    border: 1px solid #CBD5E1;
    vertical-align: top;
    line-height: 1.3;
  }}
  table.clean-table tr:nth-child(even) {{
    background-color: #F8FAFC;
  }}

  /* Cajas de llamada limpias */
  .callout {{
    background-color: #F8FAFC;
    border: 1px solid #CBD5E1;
    border-left: 5px solid #1B365D;
    border-radius: 4px;
    padding: 10px 14px;
    margin: 12px 0;
    font-size: 9.5pt;
  }}
  .callout-story {{
    background-color: #F0FDF4;
    border: 1px solid #BBF7D0;
    border-left: 5px solid #16A34A;
    border-radius: 4px;
    padding: 12px 14px;
    margin: 12px 0;
  }}
  .callout-title {{
    font-weight: bold;
    font-size: 10pt;
    color: #1B365D;
    margin-bottom: 6px;
  }}
</style>
</head>
<body>

<!-- ========================================== -->
<!-- PÁGINA 1: PORTADA OFICIAL                  -->
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
    <div class="cover-program-name">TÉCNICO SUPERIOR UNIVERSITARIO EN DESARROLLO DE SOFTWARE MULTIPLATAFORMA</div>
  </div>

  <div class="cover-section-title">
    <div class="cover-label">NOMBRE DEL TRABAJO:</div>
    <div class="cover-job-title">PRÁCTICA: INVESTIGACIÓN Y ESTRUCTURACIÓN DEL PRODUCT BACKLOG</div>
    <div class="cover-job-sub">Proyecto Integrador: MedReminder AI (Gestión y Recordatorio Farmacológico)</div>
  </div>

  <div class="cover-meta">
    <div class="cover-meta-item">
      <div class="cover-label">ASIGNATURA:</div>
      <div class="cover-meta-val" style="font-weight:bold;">Fundamentos de Inteligencia Artificial / Metodologías Ágiles</div>
    </div>
    <div class="cover-meta-item">
      <div class="cover-label">NOMBRE DEL DOCENTE:</div>
      <div class="cover-meta-val">Ing. Hector Velazquez Estrada</div>
    </div>
  </div>

  <div>
    <div class="cover-label" style="text-align: center; margin-bottom: 6px;">PRESENTA:</div>
    <div style="text-align: center;">
      <div class="cover-team">
        <div class="cover-team-line">222410897 &nbsp;–&nbsp; Gutierrez Ugalde Samuel</div>
        <div class="cover-team-line">222410935 &nbsp;–&nbsp; Nava Garcia Rodrigo</div>
        <div class="cover-team-line">222411182 &nbsp;–&nbsp; Castillo Ramirez Nahum Yabet</div>
        <div class="cover-team-line">222410915 &nbsp;–&nbsp; Ramirez Romero Pablo</div>
        <div class="cover-team-line">222410899 &nbsp;–&nbsp; Peña Hernandez Alexander</div>
      </div>
    </div>
    <div style="margin-top: 14px; font-weight: bold; color: #1B365D; font-size: 9.5pt;">
      GRUPO: DSM - 53 &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; NO. DE EQUIPO: 5 (MedReminder AI)
    </div>
  </div>

  <div class="cover-footer">
    SANTA MARÍA ATARASQUILLO, LERMA ESTADO DE MÉXICO. NOVIEMBRE 2026
  </div>
</div>

<!-- ========================================== -->
<!-- PÁGINA 2: SECCIÓN 1                        -->
<!-- ========================================== -->
<div class="page">
  <h1>SECCIÓN 1: ¿Qué es el Product Backlog y quién lo manda?</h1>

  <h2>Investigación:</h2>
  <p><span class="q-title">1. ¿Qué es un Product Backlog en Scrum y por qué se dice que es un documento "vivo" que nunca se termina?</span><br>
  El <b>Product Backlog</b> es la lista ordenada de todo lo que el equipo planea construir o mejorar en la aplicación: nuevas funciones, correcciones de errores y cambios técnicos. En lugar de ser un documento congelado como en cascada, aquí los elementos se priorizan continuamente según el valor que aportan al usuario y al negocio.<br><br>
  Se dice que es un documento <b>«vivo» que nunca se termina</b> porque mientras la aplicación tenga usuarios reales, el proyecto nunca está 100% cerrado. Siempre van a surgir nuevas ideas, sugerencias de los médicos, cambios en las versiones de Android o fallas imprevistas. El Backlog se refina y actualiza en cada sprint; solo se da por concluido cuando la aplicación se retira del mercado de manera definitiva.</p>

  <p><span class="q-title">2. ¿Quién es el Product Owner (Dueño del Producto) y cuál es su única responsabilidad frente al equipo de desarrollo?</span><br>
  El <b>Product Owner</b> es el integrante del equipo que representa la voz de los clientes y usuarios (en nuestro caso: pacientes de la tercera edad, familiares y médicos). No es un jefe que da órdenes ni supervisa horarios.<br><br>
  Su <b>única responsabilidad frente al equipo de desarrollo</b> es <b>maximizar el valor del producto que construimos</b>. Esto significa que él es el único con la autoridad para decidir qué cosas van primero en el Backlog y explicar claramente por qué se necesitan. En resumen: el Product Owner manda sobre el <i>«qué»</i> y el <i>«para qué»</i>, pero respeta totalmente que los desarrolladores decidan con autonomía el <i>«cómo»</i> resolverlo técnicamente.</p>

  <h2>Aplicación en Nuestro Proyecto (MedReminder AI):</h2>
  <p><b>1. Product Owner del Equipo:</b> Elegimos a <b>Rodrigo Nava García</b> como Product Owner de MedReminder AI. Su labor es asegurar que cada función resuelva un problema real de adherencia médica y accesibilidad para adultos mayores, antes de pasar a detalles secundarios.</p>

  <p><b>2. Top 3 de Funcionalidades Críticas de Nuestro Backlog:</b></p>
  <table class="clean-table">
    <thead>
      <tr>
        <th style="width: 15%; text-align: center;">Prioridad</th>
        <th style="width: 35%;">Funcionalidad</th>
        <th style="width: 50%;">Justificación Práctica de Negocio / Clínica</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td style="text-align: center; font-weight: bold; color: #0E8074;">#1 (Crítica)</td>
        <td><b>Motor de Alarmas Heads-Up Locales (Android)</b></td>
        <td>Hace que la alarma suene en el segundo exacto a pantalla completa, aun con el celular bloqueado, sin internet o en reposo (Doze Mode). Es la función vital: si no suena, el paciente olvida el fármaco.</td>
      </tr>
      <tr>
        <td style="text-align: center; font-weight: bold; color: #1B365D;">#2 (Alta)</td>
        <td><b>Confirmación de Toma y Descuento en Botiquín</b></td>
        <td>Un botón directo para confirmar que ya se ingirió la dosis, descontando el stock local para evitar confusiones de «¿ya me la tomé?» y prevenir sobredosis.</td>
      </tr>
      <tr>
        <td style="text-align: center; font-weight: bold; color: #1B365D;">#3 (Alta)</td>
        <td><b>Avisos Automáticos al Cuidador ante Omisiones</b></td>
        <td>Si el abuelo pospone la alarma más del límite seguro (20 min) o no se toma un fármaco crítico, el sistema avisa de inmediato al familiar responsable.</td>
      </tr>
    </tbody>
  </table>
</div>

<!-- ========================================== -->
<!-- PÁGINA 3: SECCIÓN 2                        -->
<!-- ========================================== -->
<div class="page">
  <h1>SECCIÓN 2: ¿Cómo se escribe una Historia de Usuario?</h1>

  <h2>Investigación:</h2>
  <p><span class="q-title">1. ¿Qué es una Historia de Usuario (User Story) y cuál es la estructura canónica diseñada por Mike Cohn?</span><br>
  Una <b>Historia de Usuario</b> es una descripción breve y en lenguaje cotidiano sobre lo que necesita una persona al usar la aplicación. No se redacta como un manual técnico aburrido, sino como una herramienta práctica para que los programadores entiendan el problema real del usuario y el beneficio que le vamos a entregar.<br><br>
  <b>Mike Cohn</b> diseñó la estructura canónica estándar más usada en desarrollo ágil:</p>

  <div class="callout" style="text-align: center; font-size: 10.5pt; font-weight: bold; color: #1B365D; background-color: #F1F5F9; border-color: #1B365D;">
    « Como <span style="color:#0E8074;">[ Rol del usuario ]</span>, quiero <span style="color:#0E8074;">[ Funcionalidad específica ]</span>, para <span style="color:#0E8074;">[ Beneficio de negocio / Valor ]</span> »
  </div>

  <p><b>Desglose de cada componente:</b><br>
  • <b>«Como [Rol]»:</b> Define con claridad quién es la persona (ej. adulto mayor con hipertensión, familiar cuidador).<br>
  • <b>«Quiero [Funcionalidad]»:</b> Describe la acción que desea realizar en la app, sin meter términos de código o bases de datos de forma anticipada.<br>
  • <b>«Para [Beneficio]»:</b> Explica la razón de ser de la funcionalidad. Esta parte es la más importante porque justifica si realmente vale la pena programarla.</p>

  <h2>Aplicación en Nuestro Proyecto (MedReminder AI):</h2>
  <p><b>Requerimiento Tradicional de la Fase 1 (Manual Técnico):</b><br>
  <i>«RF-03: Alarmas Heads-Up Locales — El sistema debe disparar alarmas acústicas, visuales y hápticas en el segundo exacto mediante AlarmManager en Android, incluso en Doze mode, notificando al usuario sobre la toma de sus medicamentos programados.»</i></p>

  <p><b>Transformación Obligatoria a la Fórmula Canónica:</b><br>
  Pasamos de una instrucción técnica sobre la API de Android a una historia centrada en la vida del paciente:</p>

  <div class="callout-story">
    <div style="font-size: 9pt; font-weight: bold; color: #166534; margin-bottom: 6px;">TARJETA DE HISTORIA DE USUARIO (HU-01: ALARMAS CLÍNICAS)</div>
    <div style="font-size: 10.5pt; line-height: 1.4;">
      « <b>Como</b> <span style="color:#1B365D; font-weight: bold;">adulto mayor con problemas de memoria que toma varios medicamentos al día</span>,<br>
      &nbsp;&nbsp;<b>quiero</b> <span style="color:#0E8074; font-weight: bold;">recibir una alarma clara en pantalla completa a la hora exacta de mi dosis (aunque mi celular esté bloqueado o sin internet)</span>,<br>
      &nbsp;&nbsp;<b>para</b> <span style="color:#166534; font-weight: bold;">tomarme mis pastillas a tiempo por mí mismo, evitar descompensaciones de salud y no depender de que alguien me esté recordando a cada rato.</span> »
    </div>
  </div>

  <p style="margin-top: 10px;"><b>Diferencia Práctica:</b> El requerimiento tradicional solo le decía al programador «usa AlarmManager». La Historia de Usuario le recuerda al equipo que el objetivo es devolverle la autonomía y seguridad a un adulto mayor, asegurando que la interfaz sea fácil de ver y que no dependa de tener saldo o internet.</p>
</div>

<!-- ========================================== -->
<!-- PÁGINA 4: SECCIÓN 3                        -->
<!-- ========================================== -->
<div class="page-last">
  <h1>SECCIÓN 3: Las reglas de oro (Las 3 C y Criterios de Aceptación)</h1>

  <h2>Investigación:</h2>
  <p><span class="q-title">1. ¿En qué consiste el modelo de las 3 C propuesto por Ron Jeffries?</span><br>
  Ron Jeffries explicó que una Historia de Usuario no es solo texto en un papel, sino tres pasos inseparables:<br>
  • <b>Card (Tarjeta):</b> La ficha física o digital donde se escribe la historia. Es breve a propósito porque solo representa una «promesa de conversación».<br>
  • <b>Conversation (Conversación):</b> La charla directa entre el Product Owner y los desarrolladores antes de programar para resolver dudas, revisar casos especiales y ponerse de acuerdo.<br>
  • <b>Confirmation (Confirmación):</b> Los criterios de aceptación con los que probaremos la función para confirmar que ya quedó bien hecha.</p>

  <p><span class="q-title">2. ¿Qué son los Criterios de Aceptación y por qué una tarjeta no se puede programar si no los tiene?</span><br>
  Son las reglas claras y medibles que nos dicen qué condiciones debe cumplir la función para darla por buena. Una tarjeta <b>no se puede programar sin ellos</b> porque el programador terminaría adivinando cómo debe funcionar la app, haría cosas de más o dejaría fuera detalles importantes. Además, en la entrega con el cliente no habría forma objetiva de saber si la tarea está realmente terminada.</p>

  <h2>Aplicación en Nuestro Proyecto (MedReminder AI):</h2>

  <div class="callout" style="background-color: #F8FAFC; border-color: #1B365D;">
    <div class="callout-title">1. CONVERSACIÓN: Dudas Técnicas del Equipo al Product Owner (Rodrigo Nava)</div>
    <div style="margin-bottom: 8px;">
      <b>• Duda 1 (Teléfono en Silencio o Modo No Molestar):</b><br>
      <i>Pregunta del Equipo:</i> «¿Qué pasa si el paciente tiene el celular en silencio o No Molestar? ¿La alarma debe sonar a la fuerza o se queda callada?»<br>
      <b>Respuesta de Rodrigo (PO):</b> «Para medicinas críticas (presión o insulina) debe sonar a la fuerza usando el canal de alarma del sistema (<code>USAGE_ALARM</code>). Para vitaminas comunes puede respetar el modo silencio.»
    </div>
    <div>
      <b>• Duda 2 (Límite de Posposición):</b><br>
      <i>Pregunta del Equipo:</i> «¿Cuántas veces puede posponer la alarma el abuelo? Si no le ponemos límite, podría posponerla todo el día.»<br>
      <b>Respuesta de Rodrigo (PO):</b> «Máximo 2 veces de 10 minutos cada una. Si a la segunda no confirma en los siguientes 10 minutos, se marca como Omitida y se le avisa al cuidador.»
    </div>
  </div>

  <p style="margin-top: 8px;"><b>2. CONFIRMACIÓN: Criterios de Aceptación Medibles de la Función (Checklist):</b></p>
  <table class="clean-table">
    <thead>
      <tr>
        <th style="width: 30%;">Regla Verificable</th>
        <th style="width: 70%;">Criterio Medible y Prueba de Aceptación</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td><b>Criterio 1:<br>Puntualidad y Despertar</b></td>
        <td>La alarma debe sonar a la hora exacta (tolerancia de ±2 segundos) y encender la pantalla completa con sonido y vibración durante al menos 45 segundos, incluso con el teléfono bloqueado y sin internet.</td>
      </tr>
      <tr>
        <td><b>Criterio 2:<br>Confirmación y Stock</b></td>
        <td>La pantalla solo muestra dos botones grandes («Tomar Ahora» y «Posponer 10 min»). Al tocar «Tomar Ahora», se descuenta 1 pastilla del stock local en menos de 1 segundo y se cierra la alarma.</td>
      </tr>
      <tr>
        <td><b>Criterio 3:<br>Límite y Alerta Familiar</b></td>
        <td>El botón «Posponer» solo se puede usar 2 veces consecutivas. Si pasan 10 minutos tras la segunda posposición sin confirmación, la dosis se registra como Omitida y se envía la alerta al cuidador.</td>
      </tr>
    </tbody>
  </table>
</div>

</body>
</html>
"""

with open(HTML_OUT, "w", encoding="utf-8") as f:
    f.write(html_clean)
print(f"Clean HTML written to: {HTML_OUT}")

# Compile HTML to PDF using Chrome Headless
chrome_cmd = [
    "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
    "--headless",
    "--disable-gpu",
    "--no-sandbox",
    f"--print-to-pdf={PDF_OUT}",
    HTML_OUT
]
subprocess.run(chrome_cmd, check=True)
print(f"Clean PDF generated successfully at: {PDF_OUT}")
