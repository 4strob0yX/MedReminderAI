import os
import subprocess
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn

DOCS_DIR = "/Users/4strob0y/Developer/MedReminderAI/docs"
DOCX_PATH = os.path.join(DOCS_DIR, "Practica_Product_Backlog_MedReminderAI.docx")
HTML_PATH = os.path.join(DOCS_DIR, "Practica_Product_Backlog_MedReminderAI.html")
PDF_PATH = os.path.join(DOCS_DIR, "Practica_Product_Backlog_MedReminderAI.pdf")

LOGO_UTVT = os.path.join(DOCS_DIR, "logo_utvt.png")
LOGO_EDOMEX = os.path.join(DOCS_DIR, "logo_edomex.png")

# Colors
C_PRIMARY = RGBColor(27, 54, 93)     # #1B365D Deep Navy
C_SECONDARY = RGBColor(14, 128, 116) # #0E8074 Teal Clínico
C_TEXT = RGBColor(33, 37, 41)        # #212529 Dark Charcoal
C_MUTED = RGBColor(108, 117, 125)    # #6C757D Gray
C_WHITE = RGBColor(255, 255, 255)
HEX_PRIMARY = "1B365D"
HEX_SECONDARY = "0E8074"
HEX_LIGHT_BG = "F4F6F9"
HEX_BORDER = "D1D5DB"
HEX_ACCENT_BG = "E6F4F1"

def set_cell_background(cell, hex_color):
    tcPr = cell._tc.get_or_add_tcPr()
    shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{hex_color}"/>')
    tcPr.append(shd)

def set_cell_margins(cell, top=100, bottom=100, left=140, right=140):
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

def create_styled_paragraph(doc, text="", style=None, space_before=0, space_after=4, line_spacing=1.15, align=WD_ALIGN_PARAGRAPH.LEFT):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(space_before)
    p.paragraph_format.space_after = Pt(space_after)
    p.paragraph_format.line_spacing = line_spacing
    p.alignment = align
    if text:
        r = p.add_run(text)
        r.font.name = "Arial"
        r.font.size = Pt(10)
        r.font.color.rgb = C_TEXT
    return p

def add_heading_1(doc, text):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(12)
    p.paragraph_format.space_after = Pt(4)
    p.paragraph_format.keep_with_next = True
    r = p.add_run(text)
    r.font.name = "Arial"
    r.font.size = Pt(12.5)
    r.font.bold = True
    r.font.color.rgb = C_PRIMARY
    return p

def add_heading_2(doc, text):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(8)
    p.paragraph_format.space_after = Pt(3)
    p.paragraph_format.keep_with_next = True
    r = p.add_run(text)
    r.font.name = "Arial"
    r.font.size = Pt(11)
    r.font.bold = True
    r.font.color.rgb = C_SECONDARY
    return p

def add_callout(doc, title, runs, border_color=HEX_SECONDARY, bg_color=HEX_LIGHT_BG):
    table = doc.add_table(rows=1, cols=1)
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    table.autofit = False
    cell = table.cell(0, 0)
    cell.width = Inches(6.8)
    set_cell_background(cell, bg_color)
    set_cell_margins(cell, top=120, bottom=120, left=180, right=160)
    set_cell_borders(cell, left=("single", "24", "0", border_color),
                           top=("single", "4", "0", "E2E8F0"),
                           bottom=("single", "4", "0", "E2E8F0"),
                           right=("single", "4", "0", "E2E8F0"))
    
    p = cell.paragraphs[0]
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after = Pt(2)
    p.paragraph_format.line_spacing = 1.15
    
    if title:
        rt = p.add_run(title + "\n")
        rt.font.name = "Arial"
        rt.font.size = Pt(10)
        rt.font.bold = True
        rt.font.color.rgb = C_PRIMARY
        
    for text, bold, italic, color in runs:
        r = p.add_run(text)
        r.font.name = "Arial"
        r.font.size = Pt(9.5)
        r.font.bold = bold
        r.font.italic = italic
        r.font.color.rgb = color if color else C_TEXT
    doc.add_paragraph().paragraph_format.space_after = Pt(3)

print("Starting DOCX generation...")
doc = docx.Document()

# Page Margins: 0.75 in (around 1.9 cm)
for section in doc.sections:
    section.top_margin = Inches(0.7)
    section.bottom_margin = Inches(0.7)
    section.left_margin = Inches(0.75)
    section.right_margin = Inches(0.75)
    
    # Header
    header = section.header
    hp = header.paragraphs[0]
    hp.paragraph_format.space_after = Pt(0)
    hrun = hp.add_run("UTVT | TSU Desarrollo de Software Multiplataforma | Metodologías Ágiles de Desarrollo")
    hrun.font.name = "Arial"
    hrun.font.size = Pt(8)
    hrun.font.color.rgb = C_MUTED
    
    # Footer
    footer = section.footer
    fp = footer.paragraphs[0]
    fp.paragraph_format.space_after = Pt(0)
    frun = fp.add_run("Proyecto MedReminder AI — Práctica: Investigación y Estructuración del Product Backlog")
    frun.font.name = "Arial"
    frun.font.size = Pt(8)
    frun.font.color.rgb = C_MUTED

# --- 1. Institutional Header Table with Logos ---
table_hdr = doc.add_table(rows=1, cols=3)
table_hdr.alignment = WD_TABLE_ALIGNMENT.CENTER
table_hdr.autofit = False

# Cell 0: Logo UTVT
c0 = table_hdr.cell(0, 0)
c0.width = Inches(1.5)
c0.vertical_alignment = WD_ALIGN_VERTICAL.CENTER
p0 = c0.paragraphs[0]
p0.paragraph_format.space_after = Pt(0)
p0.alignment = WD_ALIGN_PARAGRAPH.LEFT
if os.path.exists(LOGO_UTVT):
    p0.add_run().add_picture(LOGO_UTVT, width=Inches(1.2))

# Cell 1: Institutional text
c1 = table_hdr.cell(0, 1)
c1.width = Inches(3.8)
c1.vertical_alignment = WD_ALIGN_VERTICAL.CENTER
p1 = c1.paragraphs[0]
p1.alignment = WD_ALIGN_PARAGRAPH.CENTER
p1.paragraph_format.space_after = Pt(0)
p1.paragraph_format.line_spacing = 1.05

r_univ = p1.add_run("UNIVERSIDAD TECNOLÓGICA DEL VALLE DE TOLUCA\n")
r_univ.font.name = "Arial"
r_univ.font.size = Pt(9.5)
r_univ.font.bold = True
r_univ.font.color.rgb = C_PRIMARY

r_dir = p1.add_run("DIRECCIÓN DE CARRERA DE TIC | TSU EN DESARROLLO DE SOFTWARE MULTIPLATAFORMA\n")
r_dir.font.name = "Arial"
r_dir.font.size = Pt(8)
r_dir.font.bold = True
r_dir.font.color.rgb = C_SECONDARY

r_sub = p1.add_run("PRÁCTICA ACADÉMICA: INVESTIGACIÓN Y ESTRUCTURACIÓN DEL PRODUCT BACKLOG")
r_sub.font.name = "Arial"
r_sub.font.size = Pt(8.5)
r_sub.font.bold = True
r_sub.font.color.rgb = C_PRIMARY

# Cell 2: Logo Edomex
c2 = table_hdr.cell(0, 2)
c2.width = Inches(1.5)
c2.vertical_alignment = WD_ALIGN_VERTICAL.CENTER
p2 = c2.paragraphs[0]
p2.paragraph_format.space_after = Pt(0)
p2.alignment = WD_ALIGN_PARAGRAPH.RIGHT
if os.path.exists(LOGO_EDOMEX):
    p2.add_run().add_picture(LOGO_EDOMEX, width=Inches(1.3))

for row in table_hdr.rows:
    for cell in row.cells:
        set_cell_borders(cell)

doc.add_paragraph().paragraph_format.space_after = Pt(2)

# --- Metadata Card ---
meta_table = doc.add_table(rows=1, cols=1)
meta_table.alignment = WD_TABLE_ALIGNMENT.CENTER
meta_cell = meta_table.cell(0, 0)
meta_cell.width = Inches(6.8)
set_cell_background(meta_cell, "F8FAFC")
set_cell_margins(meta_cell, top=100, bottom=100, left=140, right=140)
set_cell_borders(meta_cell, left=("single", "16", "0", HEX_PRIMARY),
                            top=("single", "4", "0", "CBD5E1"),
                            bottom=("single", "4", "0", "CBD5E1"),
                            right=("single", "4", "0", "CBD5E1"))

mp = meta_cell.paragraphs[0]
mp.paragraph_format.space_after = Pt(0)
mp.paragraph_format.line_spacing = 1.15

def add_meta_line(p, label, val):
    rl = p.add_run(f"• {label}: ")
    rl.font.name = "Arial"
    rl.font.size = Pt(8.5)
    rl.font.bold = True
    rl.font.color.rgb = C_PRIMARY
    
    rv = p.add_run(f"{val}   ")
    rv.font.name = "Arial"
    rv.font.size = Pt(8.5)
    rv.font.color.rgb = C_TEXT

add_meta_line(mp, "Proyecto Integrador", "MedReminder AI (Sistema de Gestión y Recordatorio Farmacológico)")
add_meta_line(mp, "Grupo", "DSM-53 | Equipo 5")
mp.add_run("\n")
add_meta_line(mp, "Docente", "Ing. Hector Velazquez Estrada")
add_meta_line(mp, "Fecha", "Ciclo Escolar 2026")
mp.add_run("\n")
add_meta_line(mp, "Integrantes", "Gutierrez Ugalde Samuel | Nava Garcia Rodrigo | Castillo Ramirez Nahum Yabet | Ramirez Romero Pablo | Peña Hernandez Alexander")

doc.add_paragraph().paragraph_format.space_after = Pt(4)

# ==============================================================================
# SECCIÓN 1: ¿QUÉ ES EL PRODUCT BACKLOG Y QUIÉN LO MANDA?
# ==============================================================================
add_heading_1(doc, "SECCIÓN 1: ¿Qué es el Product Backlog y quién lo manda?")

# --- 1. Investigación ---
add_heading_2(doc, "1. Fase de Investigación Conceptual")

p = create_styled_paragraph(doc)
r = p.add_run("1. ¿Qué es un Product Backlog en Scrum y por qué se dice que es un documento «vivo» que nunca se termina?\n")
r.font.bold = True
r.font.color.rgb = C_PRIMARY
p.add_run(
    "El Product Backlog (o Pila de Producto) es el inventario ordenado y centralizado que contiene absolutamente todo lo que podría "
    "necesitar el producto: nuevas características funcionales, mejoras técnicas, requerimientos no funcionales y corrección de incidentes. "
    "A diferencia del enfoque tradicional en cascada —donde los requerimientos se redactaban al inicio en un documento rígido de especificaciones "
    "y se congelaban durante meses—, en Scrum el Backlog es un documento dinámico y flexible que evoluciona a la par del software.\n\n"
    "Se le llama documento «vivo» que nunca se termina porque mientras un sistema exista en producción, el entorno nunca es estático. "
    "Las necesidades de los usuarios cambian, los médicos sugieren ajustes clínicos, surgen nuevas regulaciones y el aprendizaje obtenido al "
    "liberar incrementos reales revela oportunidades que nadie anticipó en la fase de planeación. El Backlog se refina, reprioriza, desglosa o "
    "depura continuamente en cada Sprint (Backlog Refinement). Un Product Backlog solo se da por finalizado cuando el producto se retira formalmente "
    "del mercado (decommissioning); mientras esté activo, permanece en constante evolución."
)

p2 = create_styled_paragraph(doc, space_before=4)
r2 = p2.add_run("2. ¿Quién es el Product Owner (Dueño del Producto) y cuál es su única responsabilidad frente al equipo de desarrollo?\n")
r2.font.bold = True
r2.font.color.rgb = C_PRIMARY
p2.add_run(
    "El Product Owner (PO) es el rol de Scrum responsable de ser la voz del cliente, de los usuarios finales y del negocio dentro del equipo. "
    "No actúa como un jefe jerárquico tradicional ni como un asignador de tareas diarias, sino como el estratega que define el rumbo del producto.\n\n"
    "Frente al equipo de desarrollo, su única responsabilidad fundamental e innegociable es "
)
r_bold_resp = p2.add_run("maximizar el valor del producto resultante del trabajo del Developers Team.")
r_bold_resp.font.bold = True
p2.add_run(
    " Esto lo logra asumiendo la autoría exclusiva de la gestión del Product Backlog: decide con claridad qué funcionalidades construir primero, "
    "establece el orden de prioridad según impacto de negocio y rentabilidad clínica, y transmite con total claridad el propósito de cada ítem. "
    "El Product Owner manda sobre el «qué» y el «para qué», pero respeta de manera absoluta la autonomía técnica del equipo de desarrollo sobre el «cómo»."
)

# --- 2. Aplicación en MedReminder AI ---
add_heading_2(doc, "2. Aplicación en Nuestro Proyecto Integrador (MedReminder AI)")

p_app1 = create_styled_paragraph(doc)
r_po_title = p_app1.add_run("1. Definición del Product Owner en el Equipo:\n")
r_po_title.font.bold = True
r_po_title.font.color.rgb = C_PRIMARY
p_app1.add_run(
    "En nuestro equipo, el compañero "
)
r_po_name = p_app1.add_run("Rodrigo Nava García")
r_po_name.font.bold = True
p_app1.add_run(
    " asume formalmente el rol de Product Owner. Su función principal es representar las necesidades reales de los adultos mayores "
    "(pacientes polimedicados con problemas de visión o destreza motriz), de sus familiares cuidadores y de los médicos tratantes. Rodrigo "
    "determina las prioridades del backlog asegurando que cada incremento resuelva primero los dolores críticos de adherencia terapéutica, "
    "mientras que Samuel Gutiérrez coordina la arquitectura técnica y el resto del equipo se enfoca en la implementación móvil y de servicios."
)

p_app2 = create_styled_paragraph(doc, space_before=4)
r_top3_title = p_app2.add_run("2. Lista Inicial de las 3 Funcionalidades Críticas (Top del Product Backlog):\n")
r_top3_title.font.bold = True
r_top3_title.font.color.rgb = C_PRIMARY
p_app2.add_run(
    "Para garantizar que MedReminder AI cumpla con su propósito clínico básico desde los primeros sprints, establecimos el siguiente orden "
    "estricto de prioridad hasta arriba del Backlog:"
)

# Backlog Table
t_backlog = doc.add_table(rows=4, cols=4)
t_backlog.alignment = WD_TABLE_ALIGNMENT.CENTER
t_backlog.autofit = False

col_widths = [Inches(0.8), Inches(2.0), Inches(1.4), Inches(2.6)]
headers = ["Pila", "Funcionalidad (Ítem de Backlog)", "Componente", "Justificación y Valor de Negocio / Clínico"]

# Header Row
hdr_row = t_backlog.rows[0]
for idx, title in enumerate(headers):
    cell = hdr_row.cells[idx]
    cell.width = col_widths[idx]
    set_cell_background(cell, HEX_PRIMARY)
    set_cell_margins(cell, top=100, bottom=100, left=100, right=100)
    set_cell_borders(cell, bottom=("single", "8", "0", HEX_SECONDARY))
    p = cell.paragraphs[0]
    p.paragraph_format.space_after = Pt(0)
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER if idx == 0 else WD_ALIGN_PARAGRAPH.LEFT
    r = p.add_run(title)
    r.font.name = "Arial"
    r.font.size = Pt(8.5)
    r.font.bold = True
    r.font.color.rgb = C_WHITE

backlog_data = [
    (
        "#1 (Máxima)",
        "Motor de Alarmas Heads-Up Locales y Deterministas",
        "Android Kotlin (AlarmManager & Service)",
        "Garantiza el disparo acústico y visual a pantalla completa en el segundo exacto, sin importar si no hay internet o si el celular está bloqueado en suspensión profunda (Doze Mode). Es el corazón del sistema; si falla, el paciente olvida el fármaco."
    ),
    (
        "#2 (Alta)",
        "Confirmación de Toma y Descuento Atómico de Inventario",
        "Android Room + SQLite + Backend FastAPI",
        "Permite al paciente registrar con un toque que ya ingirió la medicina, restando inmediatamente la unidad en 'Mi Botiquín' y evitando la sobredosis accidental por dudas de si ya se tomó la pastilla."
    ),
    (
        "#3 (Alta)",
        "Canal de Alertas Automáticas al Cuidador ante Omisiones",
        "Backend FastAPI + Servicio de Notificaciones",
        "Si un paciente omite una dosis crítica o la pospone más del límite seguro (20 min), el sistema notifica de inmediato al familiar o cuidador responsable para intervenir a tiempo."
    )
]

for row_idx, data in enumerate(backlog_data, start=1):
    row = t_backlog.rows[row_idx]
    bg = HEX_LIGHT_BG if row_idx % 2 == 1 else "FFFFFF"
    for col_idx in range(4):
        cell = row.cells[col_idx]
        cell.width = col_widths[col_idx]
        set_cell_background(cell, bg)
        set_cell_margins(cell, top=80, bottom=80, left=100, right=100)
        set_cell_borders(cell, bottom=("single", "4", "0", "E2E8F0"),
                               top=("single", "4", "0", "E2E8F0"))
        p = cell.paragraphs[0]
        p.paragraph_format.space_after = Pt(0)
        p.paragraph_format.line_spacing = 1.1
        if col_idx == 0:
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        
        r = p.add_run(data[col_idx])
        r.font.name = "Arial"
        r.font.size = Pt(8.5)
        if col_idx == 0:
            r.font.bold = True
            r.font.color.rgb = C_SECONDARY
        elif col_idx == 1:
            r.font.bold = True
            r.font.color.rgb = C_PRIMARY
        else:
            r.font.color.rgb = C_TEXT

doc.add_paragraph().paragraph_format.space_after = Pt(6)

# ==============================================================================
# SECCIÓN 2: ¿CÓMO SE ESCRIBE UNA HISTORIA DE USUARIO?
# ==============================================================================
add_heading_1(doc, "SECCIÓN 2: ¿Cómo se escribe una Historia de Usuario?")

# --- 1. Investigación ---
add_heading_2(doc, "1. Fase de Investigación Conceptual")

p_us = create_styled_paragraph(doc)
r_us_title = p_us.add_run("1. ¿Qué es una Historia de Usuario y cuál es la estructura canónica diseñada por Mike Cohn?\n")
r_us_title.font.bold = True
r_us_title.font.color.rgb = C_PRIMARY
p_us.add_run(
    "Una Historia de Usuario (User Story) es un instrumento ágil que describe de forma concisa, simple y en lenguaje natural una "
    "necesidad funcional desde la perspectiva de la persona que experimentará el valor de la solución (el usuario o cliente). "
    "Su propósito no es reemplazar un contrato legal ni detallar diagramas de base de datos, sino cambiar el foco: en lugar de redactar "
    "especificaciones técnicas frías y monolíticas, se busca propiciar conversaciones entre el negocio y los desarrolladores para resolver problemas humanos reales.\n\n"
    "Mike Cohn, referente global en Scrum y autor de 'User Stories Applied', diseñó la estructura canónica estándar más extendida en la industria:"
)

# Visual Callout for Cohn formula
add_callout(doc, "Fórmula Canónica de Mike Cohn:", [
    ("« Como ", True, False, C_PRIMARY),
    ("[ Rol del usuario ]", True, True, C_SECONDARY),
    (",  quiero ", True, False, C_PRIMARY),
    ("[ Funcionalidad específica o capacidad ]", True, True, C_SECONDARY),
    (",  para ", True, False, C_PRIMARY),
    ("[ Beneficio medible o valor de negocio esperado ]", True, True, C_SECONDARY),
    (" »", True, False, C_PRIMARY)
], border_color=HEX_PRIMARY, bg_color=HEX_ACCENT_BG)

p_breakdown = create_styled_paragraph(doc)
p_breakdown.add_run(
    "El valor de esta fórmula radica en la coherencia de sus tres partes esenciales:\n"
    "• «Como [Rol]»: Especifica con empatía quién se beneficia. No se usa un vago 'Como usuario', sino un arquetipo con contexto real (ej. paciente hipertenso, cuidador primario).\n"
    "• «Quiero [Qué]»: Expresa la acción o herramienta deseada en términos humanos, evitando forzar detalles técnicos de implementación prematuros.\n"
    "• «Para [Para qué]»: Es el componente más importante de la historia. Justifica el valor de negocio o beneficio en la vida del usuario. Si un ítem no aporta un beneficio claro, no merece ser desarrollado."
)

# --- 2. Aplicación en MedReminder AI ---
add_heading_2(doc, "2. Aplicación en Nuestro Proyecto Integrador (MedReminder AI)")

p_req_orig = create_styled_paragraph(doc)
r_req_lbl = p_req_orig.add_run("Requerimiento Tradicional de la Fase 1 (Tomado del Manual Técnico de MedReminder AI):\n")
r_req_lbl.font.bold = True
r_req_lbl.font.color.rgb = C_PRIMARY

p_quote = create_styled_paragraph(doc, space_before=2, space_after=4)
p_quote.paragraph_format.left_indent = Inches(0.25)
r_q = p_quote.add_run(
    "«RF-03: Alarmas Heads-Up Locales — El sistema debe disparar alarmas acústicas, visuales y hápticas en el segundo exacto "
    "mediante AlarmManager en Android, incluso en Doze mode, notificando al usuario sobre la toma de sus medicamentos programados.»"
)
r_q.font.italic = True
r_q.font.color.rgb = C_MUTED

p_trans_intro = create_styled_paragraph(doc)
p_trans_intro.add_run(
    "Al aplicar de forma obligatoria la fórmula canónica de Mike Cohn, transformamos este requisito técnico en una Historia de Usuario "
    "con empatía clínica y valor medible para el paciente:"
)

# Box with User Story Card
story_box = doc.add_table(rows=1, cols=1)
story_box.alignment = WD_TABLE_ALIGNMENT.CENTER
story_box.autofit = False
sb_cell = story_box.cell(0, 0)
sb_cell.width = Inches(6.8)
set_cell_background(sb_cell, "F0FDF4") # subtle soft green
set_cell_margins(sb_cell, top=140, bottom=140, left=180, right=160)
set_cell_borders(sb_cell, left=("single", "28", "0", "16A34A"),
                          top=("single", "4", "0", "BBF7D0"),
                          bottom=("single", "4", "0", "BBF7D0"),
                          right=("single", "4", "0", "BBF7D0"))

p_sb = sb_cell.paragraphs[0]
p_sb.paragraph_format.space_after = Pt(2)
p_sb.paragraph_format.line_spacing = 1.2

r_tag = p_sb.add_run("HISTORIA DE USUARIO CANÓNICA — HU-01 (MÓDULO DE ADHERENCIA MÉDICA)\n")
r_tag.font.name = "Arial"
r_tag.font.size = Pt(9)
r_tag.font.bold = True
r_tag.font.color.rgb = RGBColor(22, 101, 52)

runs_hu = [
    ("« Como ", True, False, C_PRIMARY),
    ("adulto mayor con tratamiento farmacológico diario y problemas frecuentes de memoria,", True, False, C_TEXT),
    ("\n   quiero ", True, False, C_PRIMARY),
    ("recibir una alarma sonora prioritaria y a pantalla completa en mi teléfono a la hora exacta de mi dosis (incluso si no tengo internet o el celular está bloqueado),", True, False, C_TEXT),
    ("\n   para ", True, False, C_PRIMARY),
    ("tomar mis medicamentos a tiempo por mi propia cuenta, evitar complicaciones de salud por olvido y conservar mi racha de tratamiento sin depender de que un familiar me esté cuidando todo el día.", True, False, C_TEXT),
    (" »", True, False, C_PRIMARY)
]
for text, bold, italic, color in runs_hu:
    r = p_sb.add_run(text)
    r.font.name = "Arial"
    r.font.size = Pt(10)
    r.font.bold = bold
    r.font.italic = italic
    r.font.color.rgb = color

doc.add_paragraph().paragraph_format.space_after = Pt(6)

# ==============================================================================
# SECCIÓN 3: LAS REGLAS DE ORO (LAS 3 C Y CRITERIOS DE ACEPTACIÓN)
# ==============================================================================
add_heading_1(doc, "SECCIÓN 3: Las reglas de oro (Las 3 C y Criterios de Aceptación)")

# --- 1. Investigación ---
add_heading_2(doc, "1. Fase de Investigación Conceptual")

p_3c = create_styled_paragraph(doc)
r_3c_title = p_3c.add_run("1. ¿En qué consiste el modelo de las 3 C propuesto por Ron Jeffries?\n")
r_3c_title.font.bold = True
r_3c_title.font.color.rgb = C_PRIMARY
p_3c.add_run(
    "En 2001, Ron Jeffries (uno de los padres de Extreme Programming y coautor del Manifiesto Ágil) propuso el modelo de las 3 C "
    "para recordar que una Historia de Usuario no es solo una frase escrita, sino un proceso colaborativo compuesto por tres dimensiones inseparables:\n\n"
    "• "
)
r_c1 = p_3c.add_run("1. Card (Tarjeta): ")
r_c1.font.bold = True
r_c1.font.color.rgb = C_SECONDARY
p_3c.add_run(
    "Es el soporte físico o digital breve (la ficha de cartulina clásica o la tarjeta en Jira/Trello). No pretende redactar toda la "
    "especificación exhaustiva de software, sino capturar la esencia de la necesidad (fórmula de Cohn) como una 'promesa de conversación' futura.\n"
    "• "
)
r_c2 = p_3c.add_run("2. Conversation (Conversación): ")
r_c2.font.bold = True
r_c2.font.color.rgb = C_SECONDARY
p_3c.add_run(
    "Es el diálogo continuo y presencial entre el Product Owner, los desarrolladores y los usuarios a lo largo del Sprint. "
    "En esta conversación se aclaran dudas, se descubren reglas de negocio no explícitas, se evalúan restricciones técnicas de Android/backend "
    "y se alinea el entendimiento compartido (shared understanding).\n"
    "• "
)
r_c3 = p_3c.add_run("3. Confirmation (Confirmación): ")
r_c3.font.bold = True
r_c3.font.color.rgb = C_SECONDARY
p_3c.add_run(
    "Es el acuerdo explícito sobre cómo se verificará que la historia funciona correctamente: representa los Criterios de Aceptación. "
    "La confirmación define la frontera exacta entre lo que está 'en proceso' y lo que está realmente 'Terminado' (Done)."
)

p_ca = create_styled_paragraph(doc, space_before=4)
r_ca_title = p_ca.add_run("2. ¿Qué son los Criterios de Aceptación y por qué una tarjeta no se puede programar si no los tiene?\n")
r_ca_title.font.bold = True
r_ca_title.font.color.rgb = C_PRIMARY
p_ca.add_run(
    "Los Criterios de Aceptación son las condiciones, restricciones operativas y reglas de negocio específicas, objetivas y medibles "
    "que el software debe cumplir rigurosamente para que el Product Owner dé por válida y aceptada la historia de usuario.\n\n"
    "Una tarjeta "
)
r_noprogram = p_ca.add_run("NO se puede programar si carece de criterios de aceptación")
r_noprogram.font.bold = True
p_ca.add_run(
    " por tres razones críticas en ingeniería de software:\n"
    "1. Ambigüedad y Suposiciones Peligrosas: Sin criterios claros, cada desarrollador programa basándose en su propia interpretación personal. En una app médica, asumir un comportamiento incorrecto (como que la alarma solo vibre en vez de sonar) pone en riesgo la vida del paciente.\n"
    "2. Imposibilidad de Pruebas Automatizadas y QA: El equipo de testing no puede diseñar casos de prueba si desconoce qué resultado se considera exitoso o fallido.\n"
    "3. Conflicto en la Sprint Review: Sin criterios acordados de antemano, el cierre de la historia se vuelve una discusión subjetiva entre el programador ('yo ya terminé la pantalla') y el Product Owner ('pero no descuenta el stock'). Los Criterios de Aceptación son el contrato de calidad que protege a ambas partes."
)

# --- 2. Aplicación en MedReminder AI ---
add_heading_2(doc, "2. Aplicación en Nuestro Proyecto Integrador (MedReminder AI)")

p_app3c = create_styled_paragraph(doc)
p_app3c.add_run(
    "Aplicando las 3 C a nuestra Historia de Usuario HU-01 (Alarmas Heads-Up para el paciente), formalizamos la Conversación y la Confirmación:"
)

# Conversacion: Dudas Técnicas
add_callout(doc, "1. CONVERSACIÓN: Dudas Técnicas Clave del Equipo hacia el Product Owner (Rodrigo Nava)", [
    ("• Duda Técnica 1 (Comportamiento en Silencio y Modo No Molestar de Android):\n", True, False, C_PRIMARY),
    ("  Pregunta del Equipo (Samuel / Nahum): ", True, True, C_SECONDARY),
    ("«Rodrigo, a partir de Android 12 y 13 las políticas de batería y permisos de 'Alarma Exacta' son muy estrictas. Si el abuelo tiene el teléfono en Modo No Molestar o en vibración, ¿la alarma debe romper el silencio y sonar con volumen máximo de emergencia, o debe respetar el volumen general del celular?»\n", False, False, C_TEXT),
    ("  Respuesta del Product Owner (Rodrigo): ", True, True, C_PRIMARY),
    ("«Tratándose de medicamentos críticos (como antihipertensivos o insulina), la alarma debe utilizar obligatoriamente el canal de audio de alarma del sistema (USAGE_ALARM). Esto garantiza que el tono suene con volumen audible aun cuando el móvil esté en silencio. Para medicamentos catalogados como suplementos o vitaminas, respetará el volumen multimedia común para no sobresaltar al paciente.»\n\n", False, False, C_TEXT),
    ("• Duda Técnica 2 (Políticas de Posposición y Alerta al Cuidador):\n", True, False, C_PRIMARY),
    ("  Pregunta del Equipo (Pablo / Alexander): ", True, True, C_SECONDARY),
    ("«¿Cuántas veces permitiremos que el paciente pulse el botón de 'Posponer' y de cuánto tiempo será cada intervalo? Si lo dejamos libre, el paciente podría posponer la medicina toda la tarde.»\n", False, False, C_TEXT),
    ("  Respuesta del Product Owner (Rodrigo): ", True, True, C_PRIMARY),
    ("«El límite máximo e improrrogable es de 2 posposiciones de exactamente 10 minutos (20 minutos de tolerancia total). Al llegar a la segunda posposición, el botón se bloquea. Si transcurren los últimos 10 minutos sin confirmación, la dosis se registrará automáticamente como 'Omitida' y el backend disparará la alerta de advertencia inmediata al celular del cuidador.»", False, False, C_TEXT)
], border_color=HEX_PRIMARY, bg_color="F8FAFC")

# Confirmacion: Criterios de Aceptación
p_conf_title = create_styled_paragraph(doc, space_before=4)
r_conf_lbl = p_conf_title.add_run("2. CONFIRMACIÓN: Criterios de Aceptación Medibles de la Función (Checklist Verificable):\n")
r_conf_lbl.font.bold = True
r_conf_lbl.font.color.rgb = C_PRIMARY
p_conf_title.add_run(
    "Para considerar que la Historia de Usuario HU-01 está completada ('Done') y lista para liberarse en producción, el equipo de "
    "desarrollo y QA deben certificar el cumplimiento de las siguientes tres reglas medibles:"
)

# Table for Acceptance Criteria
t_ca = doc.add_table(rows=4, cols=3)
t_ca.alignment = WD_TABLE_ALIGNMENT.CENTER
t_ca.autofit = False

col_widths_ca = [Inches(1.5), Inches(2.3), Inches(3.0)]
headers_ca = ["Regla / Dimensión", "Criterio Medible (Condición)", "Método de Verificación y Prueba de Aceptación"]

hdr_row_ca = t_ca.rows[0]
for idx, title in enumerate(headers_ca):
    cell = hdr_row_ca.cells[idx]
    cell.width = col_widths_ca[idx]
    set_cell_background(cell, HEX_PRIMARY)
    set_cell_margins(cell, top=100, bottom=100, left=100, right=100)
    set_cell_borders(cell, bottom=("single", "8", "0", HEX_SECONDARY))
    p = cell.paragraphs[0]
    p.paragraph_format.space_after = Pt(0)
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER if idx == 0 else WD_ALIGN_PARAGRAPH.LEFT
    r = p.add_run(title)
    r.font.name = "Arial"
    r.font.size = Pt(8.5)
    r.font.bold = True
    r.font.color.rgb = C_WHITE

data_ca = [
    (
        "Criterio 1:\nPuntualidad y Despertar de Pantalla (Doze Mode)",
        "Disparo en el segundo exacto (tolerancia máxima de ±2 segundos) con pantalla activa completa.",
        "Prueba en dispositivo físico con pantalla apagada en reposo profundo (Doze Mode). Se verifica que la pantalla se encienda con el Activity Heads-Up, reproduciendo sonido y vibración durante mínimo 45 segundos sin requerir conexión a internet."
    ),
    (
        "Criterio 2:\nConfirmación Táctil y Descuento Atómico",
        "Disponibilidad exclusiva de dos botones gigantes ('Tomar Ahora' y 'Posponer 10 min') con impacto en base de datos en <300 ms.",
        "Al pulsar 'Tomar Ahora', se descuenta exactamente 1 unidad en la tabla SQLite local ('Mi Botiquín'), se guarda la hora exacta en la bitácora de cumplimiento y la alarma se cancela de forma inmediata."
    ),
    (
        "Criterio 3:\nLímite de Posposiciones y Respaldo Familiar",
        "Límite estricto de dos posposiciones (k=2) de 10 minutos cada una antes de escalar a omisión.",
        "Tras la segunda posposición consecutiva, el botón 'Posponer' se deshabilita visualmente. Si tras 10 minutos no se pulsa 'Tomar', la dosis se etiqueta como OMITIDA y se registra el evento de alerta para el módulo de supervisión del cuidador."
    )
]

for row_idx, data in enumerate(data_ca, start=1):
    row = t_ca.rows[row_idx]
    bg = HEX_LIGHT_BG if row_idx % 2 == 1 else "FFFFFF"
    for col_idx in range(3):
        cell = row.cells[col_idx]
        cell.width = col_widths_ca[col_idx]
        set_cell_background(cell, bg)
        set_cell_margins(cell, top=80, bottom=80, left=100, right=100)
        set_cell_borders(cell, bottom=("single", "4", "0", "E2E8F0"),
                               top=("single", "4", "0", "E2E8F0"))
        p = cell.paragraphs[0]
        p.paragraph_format.space_after = Pt(0)
        p.paragraph_format.line_spacing = 1.1
        
        r = p.add_run(data[col_idx])
        r.font.name = "Arial"
        r.font.size = Pt(8.5)
        if col_idx == 0:
            r.font.bold = True
            r.font.color.rgb = C_PRIMARY
        elif col_idx == 1:
            r.font.bold = True
            r.font.color.rgb = C_SECONDARY
        else:
            r.font.color.rgb = C_TEXT

# --- Conclusión y Firmas de Entrega ---
doc.add_paragraph().paragraph_format.space_after = Pt(4)
p_concl = create_styled_paragraph(doc)
r_c_lbl = p_concl.add_run("Conclusión del Equipo 5 (MedReminder AI):\n")
r_c_lbl.font.bold = True
r_c_lbl.font.color.rgb = C_PRIMARY
p_concl.add_run(
    "La realización de esta práctica nos permitió comprender en la práctica que Scrum no consiste en llenar formatos burocráticos, "
    "sino en orientar cada línea de código hacia el valor humano real. Pasar de un requerimiento técnico estático (RF-03) a una Historia "
    "de Usuario canónica bajo las 3 C de Ron Jeffries transformó radicalmente la perspectiva del equipo: ya no estamos 'programando un servicio "
    "en segundo plano con AlarmManager', sino construyendo una herramienta confiable que le devuelve la tranquilidad a un adulto mayor y a su "
    "familia. Los Criterios de Aceptación medibles aseguran que la calidad nunca sea negociable cuando la salud de las personas está de por medio."
)

# Save Document
doc.save(DOCX_PATH)
print(f"DOCX successfully generated at: {DOCX_PATH}")

# Now build HTML representation and compile to PDF via headless Chrome
html_content = f"""<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<title>Práctica: Investigación y Estructuración del Product Backlog - MedReminder AI</title>
<style>
  @page {{
    size: letter;
    margin: 1.6cm 1.5cm 1.6cm 1.5cm;
    @bottom-center {{
      content: "Página " counter(page) " de " counter(pages);
      font-size: 8pt;
      color: #6C757D;
      font-family: Arial, sans-serif;
    }}
  }}
  body {{
    font-family: 'Segoe UI', Arial, Helvetica, sans-serif;
    font-size: 9.2pt;
    line-height: 1.25;
    color: #212529;
    margin: 0;
    padding: 0;
  }}
  .header-table {{
    width: 100%;
    border-collapse: collapse;
    margin-bottom: 8px;
  }}
  .header-table td {{
    vertical-align: middle;
    border: none;
    padding: 0;
  }}
  .logo-left {{
    width: 18%;
    text-align: left;
  }}
  .logo-left img {{
    height: 48px;
    width: auto;
  }}
  .logo-right {{
    width: 20%;
    text-align: right;
  }}
  .logo-right img {{
    height: 38px;
    width: auto;
  }}
  .header-center {{
    width: 62%;
    text-align: center;
  }}
  .univ-title {{
    font-size: 10.5pt;
    font-weight: bold;
    color: #1B365D;
    margin: 0;
  }}
  .dir-title {{
    font-size: 8pt;
    font-weight: bold;
    color: #0E8074;
    margin: 2px 0;
  }}
  .doc-title {{
    font-size: 9pt;
    font-weight: bold;
    color: #1B365D;
    letter-spacing: 0.5px;
    margin-top: 3px;
  }}
  .meta-card {{
    background-color: #F8FAFC;
    border: 1px solid #CBD5E1;
    border-left: 5px solid #1B365D;
    border-radius: 4px;
    padding: 6px 10px;
    margin-bottom: 12px;
    font-size: 8.2pt;
    line-height: 1.3;
  }}
  .meta-card span.label {{
    font-weight: bold;
    color: #1B365D;
  }}
  h1 {{
    font-size: 11.5pt;
    font-weight: bold;
    color: #1B365D;
    border-bottom: 1.5px solid #0E8074;
    padding-bottom: 3px;
    margin: 12px 0 6px 0;
    page-break-after: avoid;
  }}
  h2 {{
    font-size: 10pt;
    font-weight: bold;
    color: #0E8074;
    margin: 8px 0 4px 0;
    page-break-after: avoid;
  }}
  p {{
    margin: 0 0 6px 0;
    text-align: justify;
  }}
  .q-title {{
    font-weight: bold;
    color: #1B365D;
  }}
  .highlight-bold {{
    font-weight: bold;
  }}
  table.data-table {{
    width: 100%;
    border-collapse: collapse;
    margin: 8px 0 10px 0;
    font-size: 8.2pt;
  }}
  table.data-table th {{
    background-color: #1B365D;
    color: #ffffff;
    font-weight: bold;
    padding: 5px 8px;
    text-align: left;
    border: 1px solid #1B365D;
  }}
  table.data-table td {{
    padding: 5px 8px;
    border: 1px solid #CBD5E1;
    vertical-align: top;
  }}
  table.data-table tr:nth-child(even) {{
    background-color: #F8FAFC;
  }}
  .callout-box {{
    background-color: #F4F7F9;
    border: 1px solid #E2E8F0;
    border-left: 4px solid #0E8074;
    border-radius: 4px;
    padding: 7px 10px;
    margin: 6px 0;
  }}
  .story-card {{
    background-color: #F0FDF4;
    border: 1px solid #BBF7D0;
    border-left: 5px solid #16A34A;
    border-radius: 5px;
    padding: 8px 12px;
    margin: 8px 0;
  }}
  .badge {{
    display: inline-block;
    padding: 2px 6px;
    font-size: 7.5pt;
    font-weight: bold;
    border-radius: 3px;
    background-color: #0E8074;
    color: white;
  }}
  .page-break {{
    page-break-before: always;
  }}
  .footer-signatures {{
    margin-top: 10px;
    padding-top: 6px;
    border-top: 1px solid #E2E8F0;
    font-size: 7.8pt;
    color: #64748B;
    text-align: center;
  }}
</style>
</head>
<body>

<!-- Header con Logos Institucionales -->
<table class="header-table">
  <tr>
    <td class="logo-left"><img src="file://{LOGO_UTVT}" alt="UTVT"></td>
    <td class="header-center">
      <div class="univ-title">UNIVERSIDAD TECNOLÓGICA DEL VALLE DE TOLUCA</div>
      <div class="dir-title">DIRECCIÓN DE CARRERA DE TIC | TSU EN DESARROLLO DE SOFTWARE MULTIPLATAFORMA</div>
      <div class="doc-title">PRÁCTICA ACADÉMICA: INVESTIGACIÓN Y ESTRUCTURACIÓN DEL PRODUCT BACKLOG</div>
    </td>
    <td class="logo-right"><img src="file://{LOGO_EDOMEX}" alt="EDOMEX"></td>
  </tr>
</table>

<!-- Ficha de Datos Institucionales -->
<div class="meta-card">
  <div><span class="label">• Proyecto Integrador:</span> MedReminder AI (Gestión Farmacológica Inteligente) &nbsp;|&nbsp; <span class="label">Asignatura:</span> Metodologías Ágiles de Desarrollo &nbsp;|&nbsp; <span class="label">Grupo:</span> DSM-53 (Equipo 5)</div>
  <div><span class="label">• Docente:</span> Ing. Hector Velazquez Estrada &nbsp;|&nbsp; <span class="label">Ciclo Escolar:</span> 2026 &nbsp;|&nbsp; <span class="label">Ubicación:</span> Santa María Atarasquillo, Lerma, Edo. Méx.</div>
  <div><span class="label">• Integrantes:</span> Gutierrez Ugalde Samuel &nbsp;•&nbsp; Nava Garcia Rodrigo &nbsp;•&nbsp; Castillo Ramirez Nahum Yabet &nbsp;•&nbsp; Ramirez Romero Pablo &nbsp;•&nbsp; Peña Hernandez Alexander</div>
</div>

<!-- ========================================== -->
<!-- SECCIÓN 1 -->
<!-- ========================================== -->
<h1>SECCIÓN 1: ¿Qué es el Product Backlog y quién lo manda?</h1>

<h2>1. Fase de Investigación Conceptual</h2>
<p><span class="q-title">1. ¿Qué es un Product Backlog (Pila de Producto) en Scrum y por qué se dice que es un documento "vivo" que nunca se termina?</span><br>
El <b>Product Backlog</b> es la fuente única, centralizada y ordenada de todo el trabajo conocido que requiere un producto: nuevas funcionalidades, mejoras operativas, requisitos técnicos y corrección de bugs. En lugar de ser una lista estática de especificaciones congeladas en el tiempo (como ocurría en el modelo tradicional en cascada), en Scrum es un artefacto dinámico ordenado por valor e impacto de negocio.<br>
Se dice que es un <b>documento "vivo" que nunca se termina</b> porque un producto de software real jamás se mantiene estático mientras esté en producción. Los hábitos de los usuarios cambian, surgen regulaciones médicas imprevistas, se actualizan los sistemas operativos (como Android) y la retroalimentación de cada Sprint revela nuevas necesidades. El Backlog se refina, reordena y depura continuamente (<i>Product Backlog Refinement</i>). Solo deja de existir cuando el producto es retirado definitivamente del mercado (<i>decommissioning</i>); mientras siga en uso, el Backlog continuará evolucionando.</p>

<p><span class="q-title">2. ¿Quién es el Product Owner (Dueño del Producto) y cuál es su única responsabilidad frente al equipo de desarrollo?</span><br>
El <b>Product Owner (PO)</b> es el rol responsable de maximizar el valor del producto y representar la voz de los usuarios (adultos mayores, cuidadores y médicos) frente a la organización. No es un capataz que asigna tareas técnicas diarias ni un jefe jerárquico tradicional.<br>
Frente al equipo de desarrollo, su <b>única y máxima responsabilidad</b> es: <b>maximizar el valor del producto resultante del trabajo del Developers Team</b>. Esto se materializa a través de la gestión eficaz del Product Backlog: tiene la autoridad exclusiva para definir los ítems, ordenar las prioridades (qué va primero y por qué) y asegurar que el equipo comprenda la necesidad de negocio. El PO gobierna el <i>«qué»</i> y el <i>«para qué»</i>, respetando con total autonomía la decisión técnica del equipo sobre el <i>«cómo»</i> construirlo.</p>

<h2>2. Aplicación en Nuestro Proyecto Integrador (MedReminder AI)</h2>
<p><b>1. Definición del Product Owner:</b> En nuestro equipo, <b>Rodrigo Nava García</b> asume el rol de <b>Product Owner</b>. Su responsabilidad es velar por que cada incremento priorice la adherencia médica y la accesibilidad de los adultos mayores, dialogando con cuidadores y médicos, mientras que Samuel Gutiérrez lidera la arquitectura técnica y el equipo restante programa la solución.</p>

<p><b>2. Top 3 de Funcionalidades Críticas de Nuestro Backlog:</b> Para asegurar que MedReminder AI sea útil y confiable desde sus primeros despliegues, establecimos las siguientes tres prioridades absolutas en la cima de la pila:</p>

<table class="data-table">
  <thead>
    <tr>
      <th style="width: 14%; text-align: center;">Prioridad</th>
      <th style="width: 28%;">Funcionalidad (Ítem de Backlog)</th>
      <th style="width: 20%;">Módulo Técnico</th>
      <th style="width: 38%;">Justificación y Valor de Negocio / Clínico</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="text-align: center;"><span class="badge">#1 (Máxima)</span></td>
      <td><b>Motor de Alarmas Heads-Up Locales y Deterministas</b></td>
      <td>Android Kotlin (AlarmManager & Service)</td>
      <td>Garantiza que la alarma suene en el segundo exacto a pantalla completa, aun con celular bloqueado, en suspensión profunda (Doze Mode) o sin internet. Es la esencia de la app: si la alarma no suena, el paciente olvida el fármaco.</td>
    </tr>
    <tr>
      <td style="text-align: center;"><span class="badge" style="background-color: #1B365D;">#2 (Alta)</span></td>
      <td><b>Confirmación Atómica y Control de Stock en Botiquín</b></td>
      <td>Android Room + SQLite + FastAPI</td>
      <td>Permite confirmar la toma con un solo toque, descontando en tiempo real el inventario en "Mi Botiquín". Evita sobredosis accidentales (dudas de "¿ya me tomé la pastilla?") y advierte desabasto.</td>
    </tr>
    <tr>
      <td style="text-align: center;"><span class="badge" style="background-color: #2C3E50;">#3 (Alta)</span></td>
      <td><b>Canal de Alertas Automáticas al Cuidador ante Omisiones</b></td>
      <td>Backend FastAPI + Microservicio Push</td>
      <td>Si el paciente omite una toma crítica o la pospone más del límite seguro (20 min), el sistema avisa de inmediato al familiar o cuidador responsable para intervenir a tiempo.</td>
    </tr>
  </tbody>
</table>

<div class="page-break"></div>

<!-- ========================================== -->
<!-- SECCIÓN 2 -->
<!-- ========================================== -->
<h1>SECCIÓN 2: ¿Cómo se escribe una Historia de Usuario?</h1>

<h2>1. Fase de Investigación Conceptual</h2>
<p><span class="q-title">1. ¿Qué es una Historia de Usuario (User Story) y cuál es la estructura canónica diseñada por Mike Cohn?</span><br>
Una <b>Historia de Usuario</b> es un instrumento ágil que describe un requerimiento en lenguaje cotidiano desde la perspectiva de la persona que lo usará. Su meta no es generar especificaciones rígidas de software, sino servir de punto de partida para generar empatía y conversaciones continuas entre el equipo técnico y el negocio.<br>
<b>Mike Cohn</b> estandarizó la fórmula canónica más empleada a nivel mundial:</p>

<div class="callout-box" style="text-align: center; font-size: 9.5pt; font-weight: bold; color: #1B365D; background-color: #E6F4F1; border-color: #0E8074;">
  « Como <span style="color:#0E8074;">[ Rol del usuario ]</span>, quiero <span style="color:#0E8074;">[ Funcionalidad específica ]</span>, para <span style="color:#0E8074;">[ Beneficio de negocio / Valor ]</span> »
</div>

<p>Esta estructura se descompone en tres elementos esenciales:<br>
• <b>«Como [Rol]»:</b> Identifica a quién beneficia la función. Evita roles genéricos; sitúa al usuario con sus limitaciones y entorno real.<br>
• <b>«Quiero [Qué]»:</b> Describe la capacidad o comportamiento deseado en términos humanos, sin acoplarlo de forma anticipada a bases de datos o código.<br>
• <b>«Para [Para qué]»:</b> Es el núcleo de la historia. Expresa el valor real o retorno de inversión. Si una historia carece de un "para qué" convincente, carece de justificación técnica y no debe desarrollarse.</p>

<h2>2. Aplicación en Nuestro Proyecto Integrador (MedReminder AI)</h2>
<p><b>Requerimiento Tradicional de la Fase 1 (Tomado del Manual Técnico de MedReminder AI):</b><br>
<i>«RF-03: Alarmas Heads-Up Locales — El sistema debe disparar alarmas acústicas, visuales y hápticas en el segundo exacto mediante AlarmManager en Android, incluso en Doze mode, notificando al usuario sobre la toma de sus medicamentos programados.»</i></p>

<p><b>Transformación Obligatoria a la Fórmula Canónica de Mike Cohn:</b></p>

<div class="story-card">
  <div style="font-size: 8.5pt; font-weight: bold; color: #166534; margin-bottom: 4px;">TARJETA DE HISTORIA DE USUARIO CANÓNICA — HU-01 (MÓDULO DE ADHERENCIA MÉDICA)</div>
  <div style="font-size: 9.8pt; line-height: 1.35;">
    « <b>Como</b> <span style="color:#1B365D; font-weight: bold;">adulto mayor con tratamiento farmacológico diario y problemas frecuentes de memoria</span>,<br>
    &nbsp;&nbsp;<b>quiero</b> <span style="color:#0E8074; font-weight: bold;">recibir una alarma a pantalla completa con sonido prioritario y vibración a la hora exacta de mi dosis (aun si el celular está bloqueado o sin internet)</span>,<br>
    &nbsp;&nbsp;<b>para</b> <span style="color:#166534; font-weight: bold;">tomar mis pastillas a tiempo por mi propia cuenta, evitar crisis médicas por olvido y conservar mi racha de tratamiento sin depender de que un familiar me esté recordando a cada rato.</span> »
  </div>
</div>

<p style="margin-top: 6px;"><b>Diferencia Clave:</b> Mientras el requerimiento tradicional RF-03 se centraba fríamente en la API técnica de Android (<code>AlarmManager</code>), la Historia de Usuario visibiliza la necesidad humana: la autonomía del adulto mayor y la prevención de complicaciones clínicas severas.</p>

<!-- ========================================== -->
<!-- SECCIÓN 3 -->
<!-- ========================================== -->
<h1 style="margin-top: 14px;">SECCIÓN 3: Las reglas de oro (Las 3 C y Criterios de Aceptación)</h1>

<h2>1. Fase de Investigación Conceptual</h2>
<p><span class="q-title">1. ¿En qué consiste el modelo de las 3 C (Card, Conversation, Confirmation) propuesto por Ron Jeffries?</span><br>
En 2001, <b>Ron Jeffries</b> sintetizó que una Historia de Usuario no es un documento final, sino un proceso en tres fases complementarias:<br>
• <b>Card (Tarjeta):</b> El soporte físico o digital breve donde se escribe la historia (fórmula de Cohn). No contiene todo el detalle, sino una síntesis pensada para actuar como una "promesa de conversación".<br>
• <b>Conversation (Conversación):</b> El diálogo directo y continuo entre el Product Owner, los desarrolladores y los usuarios durante el refinamiento y el Sprint. Aquí se aclaran dudas, se definen escenarios límite y se construye un entendimiento compartido.<br>
• <b>Confirmation (Confirmación):</b> Los Criterios de Aceptación acordados que permiten comprobar de forma objetiva si la historia quedó bien construida y cumple su propósito.</p>

<p><span class="q-title">2. ¿Qué son los Criterios de Aceptación y por qué una tarjeta no se puede programar si no los tiene?</span><br>
Los <b>Criterios de Aceptación</b> son las reglas, condiciones y límites medibles que determinan cuándo una historia está lista para ser aceptada por el Product Owner. Indican la frontera exacta entre lo incompleto y lo terminado (<i>Done</i>).<br>
Una tarjeta <b>no se puede programar sin criterios de aceptación</b> porque:<br>
1. <b>Evita la programación a ciegas:</b> Sin ellos, el programador programa según sus propias suposiciones (pudiendo asumir que una alarma no debe sonar si el teléfono está en silencio).<br>
2. <b>Controla el desvío de alcance (Scope Creep):</b> Establece el límite exacto de lo que se debe y no se debe construir.<br>
3. <b>Permite certificar la calidad:</b> Sin pruebas objetivas medibles, la revisión del Sprint (Sprint Review) se convierte en una discusión subjetiva de opiniones en lugar de una demostración de software funcionando.</p>

<div class="page-break"></div>

<h2>2. Aplicación en Nuestro Proyecto Integrador (MedReminder AI)</h2>
<p>Tomando nuestra Historia de Usuario HU-01 (Alarmas Heads-Up para el paciente), desarrollamos las dos fases complementarias del modelo de Jeffries:</p>

<div class="callout-box" style="background-color: #F8FAFC; border-color: #1B365D;">
  <div style="font-weight: bold; color: #1B365D; margin-bottom: 4px; font-size: 8.8pt;">1. CONVERSACIÓN: Dudas Técnicas Clave del Equipo hacia el Product Owner (Rodrigo Nava)</div>
  <div style="margin-bottom: 6px; font-size: 8.4pt;">
    <b>• Duda Técnica 1 (Comportamiento en Silencio y Modo No Molestar de Android):</b><br>
    <i>Pregunta del Equipo (Samuel / Nahum):</i> «Rodrigo, a partir de Android 12 y 13 las restricciones de batería son muy estrictas. Si el abuelo tiene el teléfono en Modo No Molestar o en vibración, ¿la alarma debe romper el silencio y sonar con volumen máximo de emergencia, o debe respetar el volumen general del celular?»<br>
    <b>Respuesta del Product Owner (Rodrigo):</b> «Para medicamentos críticos (como antihipertensivos o insulina), la alarma debe utilizar obligatoriamente el canal de audio de alarma del sistema (<code>USAGE_ALARM</code>). Esto garantiza que el tono suene aun cuando el móvil esté en silencio. Para vitaminas o suplementos comunes, respetará el volumen multimedia convencional para no sobresaltar al paciente.»
  </div>
  <div style="font-size: 8.4pt;">
    <b>• Duda Técnica 2 (Políticas de Posposición y Alerta al Cuidador):</b><br>
    <i>Pregunta del Equipo (Pablo / Alexander):</i> «¿Cuántas veces permitiremos que el paciente pulse el botón de 'Posponer' y con qué intervalo? Si lo dejamos libre, el paciente podría posponer la medicina toda la tarde y falsear la adherencia.»<br>
    <b>Respuesta del Product Owner (Rodrigo):</b> «El límite estricto es de 2 posposiciones de exactamente 10 minutos (máximo 20 minutos de tolerancia total). Al llegar a la segunda posposición, el botón se bloquea. Si transcurren los últimos 10 minutos sin confirmación, la dosis se catalogará automáticamente como 'Omitida' y el backend disparará la notificación inmediata al teléfono del cuidador registrado.»
  </div>
</div>

<p style="margin-top: 8px;"><b>2. CONFIRMACIÓN: Criterios de Aceptación Medibles de la Función (Checklist de Aceptación):</b><br>
Para certificar que la Historia de Usuario HU-01 está completada (<i>Done</i>) y lista para producción, el equipo de desarrollo y pruebas debe validar las siguientes tres reglas medibles:</p>

<table class="data-table">
  <thead>
    <tr>
      <th style="width: 22%;">Regla / Dimensión</th>
      <th style="width: 38%;">Criterio Medible (Condición de Éxito)</th>
      <th style="width: 40%;">Método de Verificación y Prueba de Aceptación</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td><b>Criterio 1: Exactitud Temporal y Suspensión Doze</b></td>
      <td>La alarma debe activarse con una tolerancia máxima de ±2 segundos respecto a la hora programada, desplegando pantalla completa.</td>
      <td>Prueba en smartphone físico Android con pantalla bloqueada y en reposo profundo (Doze Mode). Se verifica que la pantalla despierte automáticamente mostrando el Activity Heads-Up con sonido y vibración durante mínimo 45 segundos, incluso sin conexión a internet.</td>
    </tr>
    <tr>
      <td><b>Criterio 2: Acciones Táctiles y Descuento Atómico</b></td>
      <td>La pantalla activa debe mostrar obligatoriamente solo dos botones grandes («Tomar Ahora» y «Posponer 10 min»), con respuesta en base de datos en menos de 300 ms.</td>
      <td>Al pulsar «Tomar Ahora», se debe restar exactamente 1 unidad en la tabla SQLite local (<code>Mi Botiquín</code>), guardar la marca temporal en la bitácora de cumplimiento y cerrar la alarma sin bloqueos de interfaz.</td>
    </tr>
    <tr>
      <td><b>Criterio 3: Límite de Posposición y Alerta Familiar</b></td>
      <td>El contador de posposiciones no debe exceder de 2 eventos (k = 2) de 10 minutos cada uno antes de marcar omisión.</td>
      <td>Tras la segunda posposición, el botón «Posponer» se deshabilita visualmente. Si tras 10 minutos no se confirma la toma, la dosis pasa a estado OMITIDA, no se descuenta la pastilla y se registra el evento en la cola de notificaciones para el cuidador.</td>
    </tr>
  </tbody>
</table>

<div class="callout-box" style="margin-top: 10px; background-color: #F8FAFC; border-color: #0E8074;">
  <div style="font-weight: bold; color: #1B365D; font-size: 8.5pt;">Conclusión del Equipo 5 (MedReminder AI):</div>
  <div style="font-size: 8.2pt; text-align: justify; margin-top: 2px;">
    Esta práctica nos demostró que Scrum no se trata de burocracia, sino de enfocar el código en las personas. Convertir un requisito técnico estático (RF-03) en una Historia de Usuario bajo las 3 C de Jeffries nos permitió anticipar escenarios clínicos que hubieran fallado en producción (como la optimización de batería en Android y la necesidad de alertar al cuidador). Los Criterios de Aceptación garantizan que nuestra aplicación sea médicamente confiable y cumpla su promesa de salvar vidas.
  </div>
</div>

<div class="footer-signatures">
  <b>UNIVERSIDAD TECNOLÓGICA DEL VALLE DE TOLUCA — GRUPO DSM-53 — EQUIPO 5 (MEDREMINDER AI)</b><br>
  Gutierrez Ugalde Samuel (222410897) &nbsp;|&nbsp; Nava Garcia Rodrigo (222410935) &nbsp;|&nbsp; Castillo Ramirez Nahum Yabet (222411182)<br>
  Ramirez Romero Pablo (222410915) &nbsp;|&nbsp; Peña Hernandez Alexander (222410899)
</div>

</body>
</html>
"""

with open(HTML_PATH, "w", encoding="utf-8") as f:
    f.write(html_content)
print(f"HTML successfully generated at: {HTML_PATH}")

# Compile HTML to PDF using Chrome Headless
chrome_cmd = [
    "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
    "--headless",
    "--disable-gpu",
    "--no-sandbox",
    f"--print-to-pdf={PDF_PATH}",
    HTML_PATH
]
subprocess.run(chrome_cmd, check=True)
print(f"PDF successfully generated at: {PDF_PATH}")
