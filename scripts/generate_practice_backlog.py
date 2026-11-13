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

# --- XML Helper Functions for Word Styling ---
def set_cell_background(cell, hex_color):
    tcPr = cell._tc.get_or_add_tcPr()
    shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{hex_color}"/>')
    tcPr.append(shd)

def set_cell_margins(cell, top=100, bottom=100, left=150, right=150):
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

def add_callout(doc, text_runs, title=None, border_color="0E8074", bg_color="F4F7F9"):
    table = doc.add_table(rows=1, cols=1)
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    table.autofit = False
    
    cell = table.cell(0, 0)
    cell.width = Inches(6.8)
    set_cell_background(cell, bg_color)
    set_cell_margins(cell, top=140, bottom=140, left=200, right=180)
    set_cell_borders(cell, left=("single", "24", "0", border_color),
                           top=("single", "4", "0", "E2E8F0"),
                           bottom=("single", "4", "0", "E2E8F0"),
                           right=("single", "4", "0", "E2E8F0"))
    
    p = cell.paragraphs[0]
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after = Pt(3)
    p.paragraph_format.line_spacing = 1.15
    
    if title:
        run_title = p.add_run(title + "\n")
        run_title.font.name = "Arial"
        run_title.font.size = Pt(10.5)
        run_title.font.bold = True
        run_title.font.color.rgb = RGBColor(14, 128, 116)
        
    for r_text, r_bold, r_italic, r_color in text_runs:
        run = p.add_run(r_text)
        run.font.name = "Arial"
        run.font.size = Pt(10)
        run.font.bold = r_bold
        run.font.italic = r_italic
        if r_color:
            run.font.color.rgb = r_color
        else:
            run.font.color.rgb = RGBColor(34, 40, 49)
            
    doc.add_paragraph().paragraph_format.space_after = Pt(4)

print("Helper functions compiled successfully.")
