"""
doc_utils.py - Utilidades compartidas para la generación de manuales oficiales de MedReminder AI.
Garantiza carátula institucional de la UTVT, índice nativo de Word, tablas de verdad con 'V' y 'F',
marco PEAS, diccionario de variables, estandarización tipográfica al 100% (Calibri/Consolas),
espaciado e interlineado óptimos, y control estricto de saltos de página con w:cantSplit y w:tblHeader.
"""

import os
from pathlib import Path
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import parse_xml, OxmlElement
from docx.oxml.ns import nsdecls, qn

# ==============================================================================
# PALETA INSTITUCIONAL Y CLÍNICA (UTVT + MedReminder AI)
# ==============================================================================
HEX_NAVY       = "1B365D"  # Azul Institucional UTVT
HEX_TEAL       = "0D9488"  # Clinical Teal MedReminder AI
HEX_DARK       = "1E293B"  # Slate 800 (Cuerpo)
HEX_MUTED      = "64748B"  # Slate 500 (Subtítulos y notas)
HEX_BORDER     = "CBD5E1"  # Slate 300 (Bordes tenues)
HEX_BG_ALT     = "F8FAFC"  # Slate 50 (Fondo alterno de tablas)
HEX_TRUE_BG    = "DCFCE7"  # Verde pastel ('V')
HEX_TRUE_TXT   = "166534"  # Verde oscuro ('V')
HEX_FALSE_BG   = "FEE2E2"  # Rojo pastel ('F')
HEX_FALSE_TXT  = "991B1B"  # Rojo oscuro ('F')
HEX_CALLOUT_BG = "F0FDFA"  # Teal muy claro (Callout clínico)
HEX_WARN_BG    = "FEF3C7"  # Amarillo pastel (Advertencia)
HEX_CODE_BG    = "F1F5F9"  # Fondo gris para bloques de código

RGB_NAVY  = RGBColor(27, 54, 93)
RGB_TEAL  = RGBColor(13, 148, 136)
RGB_DARK  = RGBColor(30, 41, 59)
RGB_MUTED = RGBColor(100, 116, 139)
RGB_WHITE = RGBColor(255, 255, 255)

FONT_FAMILY = "Calibri"
FONT_MONO   = "Consolas"

# ==============================================================================
# CONFIGURACIÓN BASE DEL DOCUMENTO
# ==============================================================================
def create_base_document() -> docx.Document:
    """Crea y configura un documento Word estándar con márgenes, fuentes y estilos base.
    Precarga la carátula institucional oficial desde docs/Portada.docx si está disponible.
    """
    base_assets_dir = Path(__file__).resolve().parent.parent / "docs"
    portada_path = base_assets_dir / "Portada.docx"
    if not portada_path.exists():
        portada_path = Path("/Users/4strob0y/Developer/MedReminderAI/docs/Portada.docx")
        
    if portada_path.exists():
        doc = docx.Document(str(portada_path))
    else:
        doc = docx.Document()
    
    # Habilitar actualización automática de campos (TOC / Índice) en Word al abrir
    doc.settings.element.append(parse_xml(r'<w:updateFields %s w:val="true"/>' % nsdecls('w')))
    
    # Configuración de secciones:
    if len(doc.sections) > 1:
        # Sección 0: Portada oficial de Portada.docx (preservar márgenes y dimensiones exactas)
        s0 = doc.sections[0]
        s0.different_first_page_header_footer = False
        
        # Garantizar explícitamente tipo nextPage en la portada para compatibilidad universal
        if s0._sectPr.find(qn('w:type')) is None:
            s0._sectPr.insert(0, parse_xml(r'<w:type %s w:val="nextPage"/>' % nsdecls('w')))
        
        # Sección 1: Cuerpo del documento (márgenes estándar de 2.5 cm / 0.984 in)
        s1 = doc.sections[1]
        s1.top_margin = Inches(0.984)
        s1.bottom_margin = Inches(0.984)
        s1.left_margin = Inches(0.984)
        s1.right_margin = Inches(0.984)
        s1.different_first_page_header_footer = False
        s1.header.is_linked_to_previous = False
        s1.footer.is_linked_to_previous = False
    else:
        for section in doc.sections:
            section.top_margin = Inches(0.984)
            section.bottom_margin = Inches(0.984)
            section.left_margin = Inches(0.984)
            section.right_margin = Inches(0.984)
            section.different_first_page_header_footer = True

    # 1. Configurar <w:docDefaults> a nivel de estilos para garantizar 100% Calibri y es-MX en cualquier visor
    try:
        styles_elm = doc.styles.element
        doc_defaults = styles_elm.find(qn('w:docDefaults'))
        if doc_defaults is not None:
            rPrDef = doc_defaults.find(qn('w:rPrDefault'))
            if rPrDef is not None:
                rPr = rPrDef.find(qn('w:rPr'))
                if rPr is not None:
                    for ch in list(rPr):
                        if ch.tag.endswith('rFonts') or ch.tag.endswith('lang'):
                            rPr.remove(ch)
                    rPr.append(parse_xml(r'<w:rFonts %s w:ascii="%s" w:hAnsi="%s" w:cs="%s" w:eastAsia="%s"/>' % (nsdecls('w'), FONT_FAMILY, FONT_FAMILY, FONT_FAMILY, FONT_FAMILY)))
                    rPr.append(parse_xml(r'<w:lang %s w:val="es-MX" w:eastAsia="es-MX" w:bidi="ar-SA"/>' % nsdecls('w')))
    except Exception:
        pass

    # 2. Configurar estilos estándar de párrafo y tablas
    styles_to_configure = [
        ('Normal', Pt(11), RGB_DARK, False, 1.15, Pt(0), Pt(5)),
        ('Header', Pt(8.5), RGB_MUTED, False, 1.0, Pt(0), Pt(0)),
        ('Footer', Pt(8.5), RGB_MUTED, False, 1.0, Pt(0), Pt(0)),
        ('Caption', Pt(9.0), RGB_MUTED, False, 1.0, Pt(2), Pt(6)),
        ('List Paragraph', Pt(11), RGB_DARK, False, 1.15, Pt(0), Pt(4)),
    ]
    for s_name, s_size, s_color, s_bold, s_line, s_before, s_after in styles_to_configure:
        try:
            st = doc.styles[s_name]
            st.font.name = FONT_FAMILY
            st.font.size = s_size
            st.font.color.rgb = s_color
            st.font.bold = s_bold
            st.paragraph_format.line_spacing = s_line
            st.paragraph_format.space_before = s_before
            st.paragraph_format.space_after = s_after
            rPr = st.element.get_or_add_rPr()
            for rf in list(rPr.findall(qn('w:rFonts'))):
                rPr.remove(rf)
            rPr.append(parse_xml(r'<w:rFonts %s w:ascii="%s" w:hAnsi="%s" w:cs="%s"/>' % (nsdecls('w'), FONT_FAMILY, FONT_FAMILY, FONT_FAMILY)))
        except Exception:
            pass

    # 3. Configurar estilos de encabezados estándar
    heading_configs = [
        ('Heading 1', Pt(15), RGB_NAVY, Pt(14), Pt(4)),
        ('Heading 2', Pt(12.5), RGB_TEAL, Pt(10), Pt(3)),
        ('Heading 3', Pt(11), RGB_DARK, Pt(8), Pt(2)),
    ]
    for h_name, h_size, h_color, h_before, h_after in heading_configs:
        try:
            h_style = doc.styles[h_name]
            h_style.font.name = FONT_FAMILY
            h_style.font.size = h_size
            h_style.font.bold = True
            h_style.font.color.rgb = h_color
            h_style.paragraph_format.space_before = h_before
            h_style.paragraph_format.space_after = h_after
            h_style.paragraph_format.keep_with_next = True
            rPr_h = h_style.element.get_or_add_rPr()
            for rf in list(rPr_h.findall(qn('w:rFonts'))):
                rPr_h.remove(rf)
            rPr_h.append(parse_xml(r'<w:rFonts %s w:ascii="%s" w:hAnsi="%s" w:cs="%s"/>' % (nsdecls('w'), FONT_FAMILY, FONT_FAMILY, FONT_FAMILY)))
        except Exception:
            pass

    return doc

def setup_header_footer(doc: docx.Document, doc_title: str):
    """Configura encabezado y pie de página institucional en páginas subsecuentes del cuerpo."""
    if len(doc.sections) > 1:
        # Sección 0 es la portada: garantizar que quede 100% limpia sin referencias ni folios (0 pt overhead)
        s0 = doc.sections[0]
        for hr in list(s0._sectPr.findall(qn('w:headerReference'))):
            s0._sectPr.remove(hr)
        for fr in list(s0._sectPr.findall(qn('w:footerReference'))):
            s0._sectPr.remove(fr)
            
        # Sección 1 es el cuerpo del documento
        section = doc.sections[1]
        section.header.is_linked_to_previous = False
        section.footer.is_linked_to_previous = False
        section.different_first_page_header_footer = False
    else:
        section = doc.sections[0]
        section.different_first_page_header_footer = True
    
    # Encabezado (páginas del cuerpo)
    header = section.header
    p_hdr = header.paragraphs[0]
    p_hdr.text = ""
    p_hdr.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    p_hdr.paragraph_format.space_before = Pt(0)
    p_hdr.paragraph_format.space_after = Pt(0)
    r_hdr = p_hdr.add_run(f"UTVT • {doc_title} | MedReminder AI")
    r_hdr.font.name = FONT_FAMILY
    r_hdr.font.size = Pt(8.5)
    r_hdr.font.color.rgb = RGB_MUTED
    
    # Pie de página (páginas del cuerpo)
    footer = section.footer
    p_ftr = footer.paragraphs[0]
    p_ftr.text = ""
    p_ftr.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p_ftr.paragraph_format.space_before = Pt(0)
    p_ftr.paragraph_format.space_after = Pt(0)
    
    r_ftr_l = p_ftr.add_run("Dirección de TIC • Fundamentos de Inteligencia Artificial\t\tPágina ")
    r_ftr_l.font.name = FONT_FAMILY
    r_ftr_l.font.size = Pt(8.5)
    r_ftr_l.font.color.rgb = RGB_MUTED
    
    # Campo nativo de número de página
    fldSimple = OxmlElement('w:fldSimple')
    fldSimple.set(qn('w:instr'), 'PAGE')
    r_pg_num = OxmlElement('w:r')
    rPr = OxmlElement('w:rPr')
    rPr.append(parse_xml(r'<w:rFonts %s w:ascii="%s" w:hAnsi="%s" w:cs="%s"/>' % (nsdecls('w'), FONT_FAMILY, FONT_FAMILY, FONT_FAMILY)))
    r_pg_num.append(rPr)
    fldSimple.append(r_pg_num)
    p_ftr._p.append(fldSimple)

# ==============================================================================
# CARÁTULA INSTITUCIONAL UTVT COMPLETA (3 MANUALES FORMALES)
# ==============================================================================
def add_utvt_cover(doc: docx.Document, title: str, subtitle: str, doc_code: str = "DOC-UTVT-2026"):
    """
    Personaliza la carátula formal oficial de la UTVT proveniente de Portada.docx
    (o inserta la carátula programática si Portada.docx no estuvo disponible).
    Ajusta la denominación del trabajo, asignatura, docente evaluador, equipo de 5 integrantes,
    grupo y fecha de emisión.
    """
    # Si el documento proviene de Portada.docx, tiene los elementos institucionales y párrafos precargados
    if len(doc.paragraphs) >= 24 and any("UNIVERSIDAD TECNOLÓGICA" in p.text for p in doc.paragraphs[:5]):
        # Configurar espaciados verticales óptimos en encabezados institucionales para garantizar 1 sola página
        p2 = doc.paragraphs[2]
        p2.paragraph_format.space_before = Pt(6)
        p2.paragraph_format.space_after = Pt(2)
        
        p3 = doc.paragraphs[3]
        p3.paragraph_format.space_before = Pt(0)
        p3.paragraph_format.space_after = Pt(0)
        
        p4 = doc.paragraphs[4]
        p4.paragraph_format.space_before = Pt(0)
        p4.paragraph_format.space_after = Pt(2)
        
        p5 = doc.paragraphs[5]
        p5.paragraph_format.space_before = Pt(0)
        p5.paragraph_format.space_after = Pt(0)
        
        p6 = doc.paragraphs[6]
        p6.paragraph_format.space_before = Pt(0)
        p6.paragraph_format.space_after = Pt(4)
        
        p8 = doc.paragraphs[8]
        p8.paragraph_format.space_before = Pt(2)
        p8.paragraph_format.space_after = Pt(1)
        
        p10 = doc.paragraphs[10]
        p10.paragraph_format.space_before = Pt(2)
        p10.paragraph_format.space_after = Pt(1)
        
        p12 = doc.paragraphs[12]
        p12.paragraph_format.space_before = Pt(2)
        p12.paragraph_format.space_after = Pt(1)
        
        p15 = doc.paragraphs[15]
        p15.paragraph_format.space_before = Pt(2)
        p15.paragraph_format.space_after = Pt(1)

        # 1. Título del Trabajo / Denominación del Documento (P9)
        p9 = doc.paragraphs[9]
        p9.text = ""
        p9.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p9.paragraph_format.space_before = Pt(2)
        p9.paragraph_format.space_after = Pt(4)
        p9.paragraph_format.line_spacing = 1.1
        
        r_t = p9.add_run(f"{title.upper()}\n")
        r_t.font.name = FONT_FAMILY
        r_t.font.size = Pt(13)
        r_t.font.bold = True
        r_t.font.color.rgb = RGB_NAVY
        
        if subtitle:
            r_st = p9.add_run(f"{subtitle}\n")
            r_st.font.name = FONT_FAMILY
            r_st.font.size = Pt(9.5)
            r_st.font.italic = True
            r_st.font.color.rgb = RGB_DARK
            
        r_pr = p9.add_run("PROYECTO: MedReminder AI — Sistema Inteligente de Gestión y Recordatorio Farmacológico")
        r_pr.font.name = FONT_FAMILY
        r_pr.font.size = Pt(9.0)
        r_pr.font.bold = True
        r_pr.font.color.rgb = RGB_TEAL
        
        # 2. Asignatura (P11)
        p11 = doc.paragraphs[11]
        p11.text = ""
        p11.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p11.paragraph_format.space_before = Pt(1)
        p11.paragraph_format.space_after = Pt(2)
        r_asig = p11.add_run("Fundamentos de Inteligencia Artificial")
        r_asig.font.name = FONT_FAMILY
        r_asig.font.size = Pt(11.5)
        r_asig.font.bold = True
        r_asig.font.color.rgb = RGB_NAVY
        
        # 3. Docente Evaluador (P13)
        p13 = doc.paragraphs[13]
        p13.text = ""
        p13.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p13.paragraph_format.space_before = Pt(1)
        p13.paragraph_format.space_after = Pt(2)
        r_doc = p13.add_run("Ing. Hector Velazquez Estrada")
        r_doc.font.name = FONT_FAMILY
        r_doc.font.size = Pt(11.5)
        r_doc.font.bold = True
        r_doc.font.color.rgb = RGB_DARK
        
        # 4. Integrantes del Equipo (P17)
        p17 = doc.paragraphs[17]
        p17.text = ""
        p17.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p17.paragraph_format.space_before = Pt(1)
        p17.paragraph_format.space_after = Pt(2)
        p17.paragraph_format.line_spacing = 1.05
        
        alumnos = [
            ("222410897", "Gutierrez Ugalde Samuel"),
            ("222410935", "Nava Garcia Rodrigo"),
            ("222411182", "Castillo Ramirez Nahum Yabet"),
            ("222410915", "Ramirez Romero Pablo"),
            ("222410899", "Peña Hernandez Alexander")
        ]
        for i, (mat, nom) in enumerate(alumnos):
            r_al = p17.add_run(f"{mat}\t-\t{nom}" + ("\n" if i < len(alumnos) - 1 else ""))
            r_al.font.name = FONT_FAMILY
            r_al.font.size = Pt(10)
            r_al.font.bold = True
            r_al.font.color.rgb = RGB_DARK
            
        # 5. Grupo y Equipo (P19)
        p19 = doc.paragraphs[19]
        p19.text = ""
        p19.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p19.paragraph_format.space_before = Pt(2)
        p19.paragraph_format.space_after = Pt(2)
        r_grp = p19.add_run("GRUPO: DSM - 53                             NO. DE EQUIPO: 5 (MedReminder AI)")
        r_grp.font.name = FONT_FAMILY
        r_grp.font.size = Pt(10)
        r_grp.font.bold = True
        r_grp.font.color.rgb = RGB_DARK
        
        # 6. Eliminar espaciadores redundantes P21, P22, P23 para equilibrar el alto vertical y mantener exactamente 1 página
        for idx in [23, 22, 21]:
            if idx < len(doc.paragraphs):
                p_rem = doc.paragraphs[idx]
                if not p_rem.text.strip():
                    p_rem._p.getparent().remove(p_rem._p)
                    
        # 7. Localizar el párrafo con sectPr (final de la portada) y actualizar fecha y código
        p_last = None
        for p in doc.paragraphs:
            if p._p.xpath('./w:pPr/w:sectPr'):
                p_last = p
                break
                
        if p_last is not None:
            # Asegurar tipo nextPage explícito y sin referencias de encabezado en la portada
            pPr = p_last._p.pPr
            if pPr is not None:
                sectPr_p = pPr.find(qn('w:sectPr'))
                if sectPr_p is not None:
                    for hr in list(sectPr_p.findall(qn('w:headerReference'))):
                        sectPr_p.remove(hr)
                    for fr in list(sectPr_p.findall(qn('w:footerReference'))):
                        sectPr_p.remove(fr)
                    if sectPr_p.find(qn('w:type')) is None:
                        sectPr_p.insert(0, parse_xml(r'<w:type %s w:val="nextPage"/>' % nsdecls('w')))
            
            for r in list(p_last.runs):
                p_last._p.remove(r._r)
            if pPr is not None:
                rPr = pPr.find(qn('w:rPr'))
                if rPr is not None:
                    for c in list(rPr):
                        if c.tag.endswith('rFonts'):
                            rPr.remove(c)
                    rPr.append(parse_xml(r'<w:rFonts %s w:ascii="Calibri" w:hAnsi="Calibri" w:cs="Calibri"/>' % nsdecls('w')))
            p_last.alignment = WD_ALIGN_PARAGRAPH.RIGHT
            p_last.paragraph_format.space_before = Pt(0)
            p_last.paragraph_format.space_after = Pt(0)
            r_loc = p_last.add_run(f"SANTA MARÍA ATARASQUILLO, LERMA ESTADO DE MÉXICO. 12 ENERO 2026\nCódigo Documental: {doc_code}")
            r_loc.font.name = FONT_FAMILY
            r_loc.font.size = Pt(8.0)
            r_loc.font.color.rgb = RGB_MUTED
            
        # 8. Remover el párrafo inicial vacío de la Sección 1 si existe
        if len(doc.paragraphs) > 0:
            p_after = doc.paragraphs[-1]
            if p_after != p_last and not p_after.text.strip():
                p_after._p.getparent().remove(p_after._p)
        return

    # Fallback si Portada.docx no estuviera disponible: carátula programática
    # 1. Tabla de logotipos (Gobierno Edomex a la izquierda, UTVT a la derecha)
    tbl_logos = doc.add_table(rows=1, cols=2)
    format_table_structure(tbl_logos, col_widths=[3.25, 3.25], repeat_header=False)
    set_table_borders(tbl_logos, top=False, bottom=False, left=False, right=False, insideH=False, insideV=False)
    
    base_assets_dir = Path(__file__).resolve().parent.parent / "docs"
    logo_edomex = base_assets_dir / "logo_edomex.png"
    logo_utvt = base_assets_dir / "logo_utvt.png"
    
    # Logo Izquierdo (Edomex)
    p_l = tbl_logos.rows[0].cells[0].paragraphs[0]
    p_l.alignment = WD_ALIGN_PARAGRAPH.LEFT
    p_l.paragraph_format.space_before = Pt(0)
    p_l.paragraph_format.space_after = Pt(0)
    r_l = p_l.add_run()
    r_l.font.name = FONT_FAMILY
    if logo_edomex.exists():
        r_l.add_picture(str(logo_edomex), width=Inches(1.85))
    elif os.path.exists("docs/logo_edomex.png"):
        r_l.add_picture("docs/logo_edomex.png", width=Inches(1.85))
    
    # Logo Derecho (UTVT)
    p_r = tbl_logos.rows[0].cells[1].paragraphs[0]
    p_r.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    p_r.paragraph_format.space_before = Pt(0)
    p_r.paragraph_format.space_after = Pt(0)
    r_r = p_r.add_run()
    r_r.font.name = FONT_FAMILY
    if logo_utvt.exists():
        r_r.add_picture(str(logo_utvt), width=Inches(1.85))
    elif os.path.exists("docs/logo_utvt.png"):
        r_r.add_picture("docs/logo_utvt.png", width=Inches(1.85))
        
    # 2. Encabezados Institucionales
    p_inst = doc.add_paragraph()
    p_inst.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_inst.paragraph_format.line_spacing = 1.15
    p_inst.paragraph_format.space_before = Pt(14)
    p_inst.paragraph_format.space_after = Pt(6)
    
    r_u1 = p_inst.add_run("UNIVERSIDAD TECNOLÓGICA DEL VALLE DE TOLUCA\n")
    r_u1.font.name = FONT_FAMILY
    r_u1.font.size = Pt(16)
    r_u1.font.bold = True
    r_u1.font.color.rgb = RGB_NAVY
    
    r_u2 = p_inst.add_run("DIRECCIÓN DE CARRERA DE TECNOLOGÍAS DE LA INFORMACIÓN Y COMUNICACIÓN\n")
    r_u2.font.name = FONT_FAMILY
    r_u2.font.size = Pt(11.5)
    r_u2.font.bold = True
    r_u2.font.color.rgb = RGB_DARK
    
    r_u3 = p_inst.add_run("PROGRAMA EDUCATIVO\nTÉCNICO SUPERIOR UNIVERSITARIO EN DESARROLLO DE SOFTWARE MULTIPLATAFORMA")
    r_u3.font.name = FONT_FAMILY
    r_u3.font.size = Pt(10)
    r_u3.font.bold = True
    r_u3.font.color.rgb = RGB_MUTED
    
    # 3. Datos de Asignatura y Docente
    p_mat = doc.add_paragraph()
    p_mat.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_mat.paragraph_format.line_spacing = 1.15
    p_mat.paragraph_format.space_before = Pt(10)
    p_mat.paragraph_format.space_after = Pt(12)
    
    r_m1 = p_mat.add_run("ASIGNATURA:\n")
    r_m1.font.name = FONT_FAMILY
    r_m1.font.size = Pt(10)
    r_m1.font.bold = True
    r_m1.font.color.rgb = RGB_MUTED
    
    r_m2 = p_mat.add_run("Fundamentos de Inteligencia Artificial\n")
    r_m2.font.name = FONT_FAMILY
    r_m2.font.size = Pt(13)
    r_m2.font.bold = True
    r_m2.font.color.rgb = RGB_NAVY
    
    r_d1 = p_mat.add_run("DOCENTE EVALUADOR:\n")
    r_d1.font.name = FONT_FAMILY
    r_d1.font.size = Pt(10)
    r_d1.font.bold = True
    r_d1.font.color.rgb = RGB_MUTED
    
    r_d2 = p_mat.add_run("Ing. Hector Velazquez Estrada")
    r_d2.font.name = FONT_FAMILY
    r_d2.font.size = Pt(12)
    r_d2.font.bold = True
    r_d2.font.color.rgb = RGB_DARK
    
    # 4. Título del Documento y Proyecto
    tbl_title = doc.add_table(rows=1, cols=1)
    format_table_structure(tbl_title, col_widths=[6.5], repeat_header=False)
    cell_t = tbl_title.rows[0].cells[0]
    set_cell_shading(cell_t, "F0F4F8")
    set_cell_border(cell_t, top="1B365D", bottom="1B365D", left="1B365D", right="1B365D", sz="16")
    set_cell_margins(cell_t, top=100, bottom=100, left=140, right=140)
    
    p_t = cell_t.paragraphs[0]
    p_t.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_t.paragraph_format.space_before = Pt(0)
    p_t.paragraph_format.space_after = Pt(0)
    p_t.paragraph_format.line_spacing = 1.05
    
    r_tt = p_t.add_run(f"{title.upper()}\n")
    r_tt.font.name = FONT_FAMILY
    r_tt.font.size = Pt(19)
    r_tt.font.bold = True
    r_tt.font.color.rgb = RGB_NAVY
    
    r_st = p_t.add_run(f"{subtitle}\n")
    r_st.font.name = FONT_FAMILY
    r_st.font.size = Pt(11)
    r_st.font.italic = True
    r_st.font.color.rgb = RGB_DARK
    
    r_proj = p_t.add_run("PROYECTO: MedReminder AI — Sistema Inteligente de Gestión y Recordatorio Farmacológico")
    r_proj.font.name = FONT_FAMILY
    r_proj.font.size = Pt(10)
    r_proj.font.bold = True
    r_proj.font.color.rgb = RGB_TEAL
    
    # 5. Integrantes del Equipo
    p_pres = doc.add_paragraph()
    p_pres.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_pres.paragraph_format.line_spacing = 1.15
    p_pres.paragraph_format.space_before = Pt(14)
    p_pres.paragraph_format.space_after = Pt(8)
    
    r_p1 = p_pres.add_run("PRESENTA EL EQUIPO DE INGENIERÍA:\n")
    r_p1.font.name = FONT_FAMILY
    r_p1.font.size = Pt(10)
    r_p1.font.bold = True
    r_p1.font.color.rgb = RGB_MUTED
    
    alumnos = [
        ("222410897", "Gutierrez Ugalde Samuel"),
        ("222410935", "Nava Garcia Rodrigo"),
        ("222411182", "Castillo Ramirez Nahum Yabet"),
        ("222410915", "Ramirez Romero Pablo"),
        ("222410899", "Peña Hernandez Alexander")
    ]
    for matricula, nombre in alumnos:
        r_al = p_pres.add_run(f"• {matricula} — {nombre}\n")
        r_al.font.name = FONT_FAMILY
        r_al.font.size = Pt(10)
        r_al.font.color.rgb = RGB_DARK
        
    # 6. Datos de Grupo, Generación y Localidad
    p_pie = doc.add_paragraph()
    p_pie.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_pie.paragraph_format.line_spacing = 1.1
    p_pie.paragraph_format.space_before = Pt(10)
    p_pie.paragraph_format.space_after = Pt(0)
    
    r_g1 = p_pie.add_run("GRUPO: DSM - 53   |   NO. DE EQUIPO: 5 (MedReminder AI)\n")
    r_g1.font.name = FONT_FAMILY
    r_g1.font.size = Pt(9.5)
    r_g1.font.bold = True
    r_g1.font.color.rgb = RGB_DARK
    
    r_g2 = p_pie.add_run("SANTA MARÍA ATARASQUILLO, LERMA ESTADO DE MÉXICO. 12 ENERO 2026\n")
    r_g2.font.name = FONT_FAMILY
    r_g2.font.size = Pt(9)
    r_g2.font.italic = True
    r_g2.font.color.rgb = RGB_MUTED
    
    r_g3 = p_pie.add_run(f"Código Documental: {doc_code} • Clasificación: Documentación Académica Oficial")
    r_g3.font.name = FONT_FAMILY
    r_g3.font.size = Pt(8)
    r_g3.font.color.rgb = RGB_MUTED
    
    # Salto de página adjunto a la carátula sin generar párrafo vacío extra
    r_br = p_pie.add_run()
    r_br.font.name = FONT_FAMILY
    r_br.add_break(docx.enum.text.WD_BREAK.PAGE)

# ==============================================================================
# TABLA DE CONTROL DE VERSIONES
# ==============================================================================
def add_version_control_table(doc: docx.Document, versions: list, title: str = "CONTROL DE VERSIONES"):
    """
    Inserta la tabla formal de control de versiones requerida por la norma académica institucional.
    Columnas: Versión | Fecha | Autor / Responsable | Descripción de Cambios
    """
    p_title = doc.add_paragraph()
    p_title.paragraph_format.space_before = Pt(8)
    p_title.paragraph_format.space_after = Pt(4)
    p_title.paragraph_format.keep_with_next = True
    r_t = p_title.add_run(f"📋 {title}")
    r_t.font.name = FONT_FAMILY
    r_t.font.size = Pt(12)
    r_t.font.bold = True
    r_t.font.color.rgb = RGB_NAVY
    
    headers = ["Versión", "Fecha", "Autor / Responsable", "Descripción de Cambios"]
    col_widths = [0.9, 1.1, 1.8, 2.7]
    
    table = doc.add_table(rows=len(versions) + 1, cols=len(headers))
    format_table_structure(table, col_widths=col_widths, repeat_header=True)
    set_table_borders(table, color=HEX_BORDER, sz="6")
    
    # Cabecera
    hdr_cells = table.rows[0].cells
    for i, h_text in enumerate(headers):
        hdr_cells[i].text = h_text
        set_cell_shading(hdr_cells[i], HEX_NAVY)
        set_cell_margins(hdr_cells[i], top=90, bottom=90, left=100, right=100)
        p = hdr_cells[i].paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.paragraph_format.space_before = Pt(0)
        p.paragraph_format.space_after = Pt(0)
        p.paragraph_format.line_spacing = 1.0
        for run in p.runs:
            run.font.name = FONT_FAMILY
            run.font.size = Pt(9.5)
            run.font.bold = True
            run.font.color.rgb = RGB_WHITE
            
    for r_idx, v in enumerate(versions):
        cells = table.rows[r_idx + 1].cells
        row_bg = HEX_BG_ALT if (r_idx % 2 == 1) else "FFFFFF"
        for c_idx, key in enumerate(["version", "fecha", "autor", "descripcion"]):
            val = v.get(key, "")
            cells[c_idx].text = str(val)
            set_cell_shading(cells[c_idx], row_bg)
            set_cell_margins(cells[c_idx], top=60, bottom=60, left=90, right=90)
            p = cells[c_idx].paragraphs[0]
            p.paragraph_format.space_before = Pt(0)
            p.paragraph_format.space_after = Pt(0)
            p.paragraph_format.line_spacing = 1.0
            if c_idx in (0, 1):
                p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            else:
                set_paragraph_left_align(p)
            for run in p.runs:
                run.font.name = FONT_FAMILY
                run.font.size = Pt(9.5)
                if c_idx == 0:
                    run.font.bold = True
                    run.font.color.rgb = RGB_NAVY
                elif c_idx == 1:
                    run.font.color.rgb = RGB_TEAL
                else:
                    run.font.color.rgb = RGB_DARK
                    
    add_page_break(doc)
    return table

# ==============================================================================
# ENCABEZADO INSTITUCIONAL COMPACTO UTVT (GUÍA DE USO RÁPIDO)
# ==============================================================================
def add_compact_utvt_header(doc: docx.Document, title: str, subtitle: str, doc_code: str = "GUIA-RAP-MEDREMINDER-2026"):
    """
    Inserta un encabezado institucional compacto oficial de la UTVT al inicio de la Guía de Uso Rápido.
    Concentra en un banner elegante de alta densidad los logos, datos de universidad, carrera, materia,
    docente y los 5 integrantes del equipo evaluado, optimizando el espacio para permitir una guía ágil de 2-3 páginas.
    """
    base_assets_dir = Path(__file__).resolve().parent.parent / "docs"
    logo_edomex = base_assets_dir / "logo_edomex.png"
    logo_utvt = base_assets_dir / "logo_utvt.png"

    # Tabla principal de 3 filas con bordes limpios
    tbl = doc.add_table(rows=3, cols=3)
    format_table_structure(tbl, col_widths=[1.3, 3.9, 1.3], repeat_header=False)
    set_table_borders(tbl, top=True, bottom=True, left=True, right=True, insideH=True, insideV=False, color=HEX_NAVY, sz="12")
    
    # Fila 0: Logos y membrete universitario
    r0 = tbl.rows[0]
    # Logo izquierdo
    # Logo izquierdo
    c_l = r0.cells[0]
    set_cell_shading(c_l, "FFFFFF")
    set_cell_margins(c_l, top=40, bottom=40, left=60, right=60)
    p_l = c_l.paragraphs[0]
    p_l.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_l.paragraph_format.space_before = Pt(0)
    p_l.paragraph_format.space_after = Pt(0)
    r_l = p_l.add_run()
    r_l.font.name = FONT_FAMILY
    if logo_edomex.exists():
        r_l.add_picture(str(logo_edomex), width=Inches(1.15))
    elif os.path.exists("docs/logo_edomex.png"):
        r_l.add_picture("docs/logo_edomex.png", width=Inches(1.15))
        
    # Membrete central
    c_c = r0.cells[1]
    set_cell_shading(c_c, "FFFFFF")
    set_cell_margins(c_c, top=40, bottom=40, left=80, right=80)
    p_c = c_c.paragraphs[0]
    p_c.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_c.paragraph_format.space_before = Pt(0)
    p_c.paragraph_format.space_after = Pt(0)
    p_c.paragraph_format.line_spacing = 1.0
    
    r_u1 = p_c.add_run("UNIVERSIDAD TECNOLÓGICA DEL VALLE DE TOLUCA\n")
    r_u1.font.name = FONT_FAMILY
    r_u1.font.size = Pt(9.5)
    r_u1.font.bold = True
    r_u1.font.color.rgb = RGB_NAVY
    
    r_u2 = p_c.add_run("DIRECCIÓN DE CARRERA DE TIC • DSM   |   GRUPO: ITIID - D73\n")
    r_u2.font.name = FONT_FAMILY
    r_u2.font.size = Pt(8.0)
    r_u2.font.bold = True
    r_u2.font.color.rgb = RGB_DARK
    
    r_u3 = p_c.add_run("Asignatura: Fundamentos de Inteligencia Artificial | Docente: Ing. Hector Velazquez Estrada")
    r_u3.font.name = FONT_FAMILY
    r_u3.font.size = Pt(7.5)
    r_u3.font.color.rgb = RGB_MUTED

    # Logo derecho
    c_r = r0.cells[2]
    set_cell_shading(c_r, "FFFFFF")
    set_cell_margins(c_r, top=40, bottom=40, left=60, right=60)
    p_r = c_r.paragraphs[0]
    p_r.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_r.paragraph_format.space_before = Pt(0)
    p_r.paragraph_format.space_after = Pt(0)
    r_r = p_r.add_run()
    r_r.font.name = FONT_FAMILY
    if logo_utvt.exists():
        r_r.add_picture(str(logo_utvt), width=Inches(1.15))
    elif os.path.exists("docs/logo_utvt.png"):
        r_r.add_picture("docs/logo_utvt.png", width=Inches(1.15))

    # Fila 1: Integrantes del equipo (Celdas fusionadas)
    c_eq = tbl.rows[1].cells[0].merge(tbl.rows[1].cells[2])
    c_eq.width = Inches(6.5)
    set_cell_shading(c_eq, "F8FAFC")
    set_cell_margins(c_eq, top=30, bottom=30, left=80, right=80)
    p_eq = c_eq.paragraphs[0]
    p_eq.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_eq.paragraph_format.space_before = Pt(0)
    p_eq.paragraph_format.space_after = Pt(0)
    p_eq.paragraph_format.line_spacing = 1.0
    
    r_eq_lbl = p_eq.add_run("EQUIPO DE INGENIERÍA: ")
    r_eq_lbl.font.name = FONT_FAMILY
    r_eq_lbl.font.size = Pt(7.5)
    r_eq_lbl.font.bold = True
    r_eq_lbl.font.color.rgb = RGB_NAVY
    
    eq_text = (
        "222410897 Gutierrez Ugalde Samuel • 222410935 Nava Garcia Rodrigo • "
        "222411182 Castillo Ramirez Nahum Yabet • 222410915 Ramirez Romero Pablo • "
        "222410899 Peña Hernandez Alexander"
    )
    r_eq_val = p_eq.add_run(eq_text)
    r_eq_val.font.name = FONT_FAMILY
    r_eq_val.font.size = Pt(7.5)
    r_eq_val.font.color.rgb = RGB_DARK

    # Fila 2: Título Principal y Subtítulo (Celdas fusionadas)
    c_tit = tbl.rows[2].cells[0].merge(tbl.rows[2].cells[2])
    c_tit.width = Inches(6.5)
    set_cell_shading(c_tit, HEX_NAVY)
    set_cell_margins(c_tit, top=50, bottom=50, left=100, right=100)
    p_tit = c_tit.paragraphs[0]
    p_tit.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_tit.paragraph_format.space_before = Pt(0)
    p_tit.paragraph_format.space_after = Pt(0)
    p_tit.paragraph_format.line_spacing = 1.05
    
    r_tit = p_tit.add_run(f"{title.upper()}\n")
    r_tit.font.name = FONT_FAMILY
    r_tit.font.size = Pt(15.5)
    r_tit.font.bold = True
    r_tit.font.color.rgb = RGB_WHITE
    
    r_sub = p_tit.add_run(f"{subtitle}   |   Código: {doc_code}")
    r_sub.font.name = FONT_FAMILY
    r_sub.font.size = Pt(8.5)
    r_sub.font.italic = True
    r_sub.font.color.rgb = RGBColor(203, 213, 225) # Slate 300

# ==============================================================================
# ÍNDICE NATIVO DE WORD COMPLETO (3 MANUALES)
# ==============================================================================
def add_native_toc(doc: docx.Document, initial_items: list = None):
    """
    Inserta un campo TOC nativo de Word con actualización automática,
    acompañado de una lista estructurada inicial para visualización inmediata en cualquier visor.
    NOTA TÉCNICA: El título NO se crea como Heading 1 para evitar que Word lo indexe recursivamente en el TOC.
    """
    p_title = doc.add_paragraph()
    p_title.alignment = WD_ALIGN_PARAGRAPH.LEFT
    p_title.paragraph_format.space_before = Pt(8)
    p_title.paragraph_format.space_after = Pt(10)
    p_title.paragraph_format.keep_with_next = True
    
    rh = p_title.add_run("ÍNDICE GENERAL DE CONTENIDO")
    rh.font.name = FONT_FAMILY
    rh.font.size = Pt(18)
    rh.font.bold = True
    rh.font.color.rgb = RGB_NAVY
    
    # Párrafo que contiene el campo de código Word TOC
    p_toc = doc.add_paragraph()
    p_toc.paragraph_format.space_before = Pt(0)
    p_toc.paragraph_format.space_after = Pt(4)
    
    # 1. fldChar begin
    r1 = p_toc.add_run()
    r1.font.name = FONT_FAMILY
    r1._r.append(parse_xml(r'<w:fldChar %s w:fldCharType="begin"/>' % nsdecls('w')))
    
    # 2. instrText
    r2 = p_toc.add_run()
    r2.font.name = FONT_FAMILY
    r2._r.append(parse_xml(r'<w:instrText %s xml:space="preserve"> TOC \o "1-3" \h \z \u </w:instrText>' % nsdecls('w')))
    
    # 3. fldChar separate
    r3 = p_toc.add_run()
    r3.font.name = FONT_FAMILY
    r3._r.append(parse_xml(r'<w:fldChar %s w:fldCharType="separate"/>' % nsdecls('w')))
    
    # Si se pasan items iniciales pre-calculados, agregarlos de forma visible
    if initial_items:
        for num, title, page in initial_items:
            p_item = doc.add_paragraph()
            p_item.paragraph_format.space_before = Pt(0)
            p_item.paragraph_format.space_after = Pt(2)
            p_item.paragraph_format.line_spacing = 1.15
            
            # Tab stops con dot leaders
            p_item_pr = p_item._p.get_or_add_pPr()
            tabs = parse_xml(r'<w:tabs %s><w:tab w:val="right" w:leader="dot" w:pos="9360"/></w:tabs>' % nsdecls('w'))
            p_item_pr.append(tabs)
            
            clean_num = str(num).strip()
            is_l1 = (clean_num.endswith('.') and clean_num[:-1].isdigit()) or clean_num.isdigit() or ('.' not in clean_num)
            
            r_num = p_item.add_run(f"{clean_num} {title}\t")
            r_num.font.name = FONT_FAMILY
            r_num.font.size = Pt(10)
            if is_l1:
                r_num.font.bold = True
                r_num.font.color.rgb = RGB_NAVY
            else:
                r_num.font.color.rgb = RGB_DARK
                
            r_pg = p_item.add_run(str(page))
            r_pg.font.name = FONT_FAMILY
            r_pg.font.size = Pt(10)
            r_pg.font.bold = is_l1
            r_pg.font.color.rgb = RGB_NAVY if is_l1 else RGB_MUTED
            
    # 4. fldChar end con salto de página en el mismo párrafo (sin líneas vacías residuales)
    p_end = doc.add_paragraph()
    p_end.paragraph_format.space_before = Pt(0)
    p_end.paragraph_format.space_after = Pt(0)
    r4 = p_end.add_run()
    r4.font.name = FONT_FAMILY
    r4._r.append(parse_xml(r'<w:fldChar %s w:fldCharType="end"/>' % nsdecls('w')))
    r_br = p_end.add_run()
    r_br.font.name = FONT_FAMILY
    r_br.add_break(docx.enum.text.WD_BREAK.PAGE)

# ==============================================================================
# ÍNDICE RÁPIDO COMPACTO (GUÍA DE USO RÁPIDO)
# ==============================================================================
def add_compact_toc(doc: docx.Document, items: list = None):
    """Inserta una tarjeta resumen de contenido de alta densidad con campo nativo TOC para Word."""
    tbl_toc = doc.add_table(rows=1, cols=1)
    format_table_structure(tbl_toc, col_widths=[6.5], repeat_header=False)
    cell = tbl_toc.rows[0].cells[0]
    set_cell_shading(cell, "F8FAFC")
    set_cell_margins(cell, top=40, bottom=40, left=80, right=80)
    set_cell_border(cell, left=HEX_TEAL, top=HEX_BORDER, bottom=HEX_BORDER, right=HEX_BORDER, sz="12")
    
    p = cell.paragraphs[0]
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after = Pt(0)
    p.paragraph_format.line_spacing = 1.0
    set_paragraph_left_align(p)
    
    r_hdr = p.add_run("RESUMEN DE CONTENIDO (ÍNDICE RÁPIDO): ")
    r_hdr.font.name = FONT_FAMILY
    r_hdr.font.size = Pt(8.5)
    r_hdr.font.bold = True
    r_hdr.font.color.rgb = RGB_TEAL
    
    # Campo TOC nativo para que Word mantenga sincronizado el documento
    r1 = p.add_run()
    r1.font.name = FONT_FAMILY
    r1._r.append(parse_xml(r'<w:fldChar %s w:fldCharType="begin"/>' % nsdecls('w')))
    r2 = p.add_run()
    r2.font.name = FONT_FAMILY
    r2._r.append(parse_xml(r'<w:instrText %s xml:space="preserve"> TOC \o "1-2" \h \z \u </w:instrText>' % nsdecls('w')))
    r3 = p.add_run()
    r3.font.name = FONT_FAMILY
    r3._r.append(parse_xml(r'<w:fldChar %s w:fldCharType="separate"/>' % nsdecls('w')))
    
    default_items = [
        "1. Flujo de Inicio en 3 Pasos Visuales (Pág. 1-2)",
        "2. Tarjeta de Botones de Alarma (Pág. 2)",
        "3. Semáforo de Inventario (Pág. 3)",
        "4. FAQ y Resolución Rápida (Pág. 3)"
    ]
    toc_list = items if items else default_items
    r_items = p.add_run("  •  ".join(toc_list))
    r_items.font.name = FONT_FAMILY
    r_items.font.size = Pt(8.0)
    r_items.font.color.rgb = RGB_DARK
    
    r4 = p.add_run()
    r4.font.name = FONT_FAMILY
    r4._r.append(parse_xml(r'<w:fldChar %s w:fldCharType="end"/>' % nsdecls('w')))

# ==============================================================================
# HELPERS DE MAQUETACIÓN Y ESTRUCTURA DE TABLAS (OpenXML)
# ==============================================================================
def format_table_structure(table, col_widths=None, repeat_header=True):
    """
    Configura alineación centrada, w:cantSplit en todas las filas para evitar roturas
    defectuosas entre saltos de página, w:tblHeader en la cabecera y anchos explícitos de columna.
    Normaliza anchos si superan el margen imprimible (6.5 pulgadas).
    """
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    if col_widths and len(col_widths) == len(table.rows[0].cells):
        total_w = sum(col_widths)
        if total_w > 6.53:
            scale = 6.5 / total_w
            col_widths = [round(w * scale, 2) for w in col_widths]
    for r_idx, row in enumerate(table.rows):
        trPr = row._tr.get_or_add_trPr()
        # Garantizar que ninguna fila se parta a mitad de página
        trPr.append(parse_xml(r'<w:cantSplit %s/>' % nsdecls('w')))
        if r_idx == 0 and repeat_header:
            trPr.append(parse_xml(r'<w:tblHeader %s/>' % nsdecls('w')))
        if col_widths and len(col_widths) == len(row.cells):
            for c_idx, w in enumerate(col_widths):
                row.cells[c_idx].width = Inches(w)

def add_step_card(doc: docx.Document, step_label: str, title: str, bullets: list, img_path: str, caption: str, img_width: float = 0.9):
    """
    Inserta una tarjeta visual de paso en 2 columnas:
    Columna izquierda: Instrucciones y viñetas clínicas claras.
    Columna derecha: Captura real de pantalla centrada con caption de 9pt.
    """
    tbl = doc.add_table(rows=1, cols=2)
    format_table_structure(tbl, col_widths=[4.9, 1.6], repeat_header=False)
    set_table_borders(tbl, top=True, bottom=True, left=True, right=True, insideH=True, insideV=True, color=HEX_BORDER, sz="6")
    
    # Celda izquierda (Texto y viñetas)
    c_txt = tbl.rows[0].cells[0]
    set_cell_shading(c_txt, "FFFFFF")
    set_cell_margins(c_txt, top=50, bottom=50, left=80, right=80)
    
    p_h = c_txt.paragraphs[0]
    p_h.paragraph_format.space_before = Pt(0)
    p_h.paragraph_format.space_after = Pt(0)
    p_h.paragraph_format.line_spacing = 1.0
    set_paragraph_left_align(p_h)
    
    r_badge = p_h.add_run(f"[{step_label}] ")
    r_badge.font.name = FONT_FAMILY
    r_badge.font.size = Pt(10)
    r_badge.font.bold = True
    r_badge.font.color.rgb = RGB_TEAL
    
    r_title = p_h.add_run(title)
    r_title.font.name = FONT_FAMILY
    r_title.font.size = Pt(11)
    r_title.font.bold = True
    r_title.font.color.rgb = RGB_NAVY
    
    for b in bullets:
        p_b = c_txt.add_paragraph()
        p_b.paragraph_format.space_before = Pt(0)
        p_b.paragraph_format.space_after = Pt(0)
        p_b.paragraph_format.line_spacing = 1.0
        set_paragraph_left_align(p_b)
        
        if ":" in b:
            part_bold, part_rest = b.split(":", 1)
            rb = p_b.add_run(f"• {part_bold}:")
            rb.font.name = FONT_FAMILY
            rb.font.size = Pt(9.5)
            rb.font.bold = True
            rb.font.color.rgb = RGB_DARK
            
            rr = p_b.add_run(part_rest)
            rr.font.name = FONT_FAMILY
            rr.font.size = Pt(9.5)
            rr.font.color.rgb = RGB_DARK
        else:
            rb = p_b.add_run(f"• {b}")
            rb.font.name = FONT_FAMILY
            rb.font.size = Pt(9.5)
            rb.font.color.rgb = RGB_DARK
            
    # Celda derecha (Captura de pantalla)
    c_img = tbl.rows[0].cells[1]
    set_cell_shading(c_img, HEX_BG_ALT)
    set_cell_margins(c_img, top=40, bottom=40, left=40, right=40)
    
    p_im = c_img.paragraphs[0]
    p_im.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_im.paragraph_format.space_before = Pt(0)
    p_im.paragraph_format.space_after = Pt(0)
    p_im.paragraph_format.line_spacing = 1.0
    
    if os.path.exists(img_path):
        r_im = p_im.add_run()
        r_im.font.name = FONT_FAMILY
        r_im.add_picture(img_path, width=Inches(img_width))
        
    p_cap = c_img.add_paragraph()
    p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_cap.paragraph_format.space_before = Pt(0)
    p_cap.paragraph_format.space_after = Pt(0)
    p_cap.paragraph_format.line_spacing = 1.0
    r_cp = p_cap.add_run(caption)
    r_cp.font.name = FONT_FAMILY
    r_cp.font.size = Pt(9.0)
    r_cp.font.italic = True
    r_cp.font.color.rgb = RGB_MUTED
    
    return tbl

def set_cell_shading(cell, color_hex: str):
    """Aplica sombreado de fondo XML a una celda de tabla."""
    tcPr = cell._tc.get_or_add_tcPr()
    for child in list(tcPr):
        if child.tag.endswith('shd'):
            tcPr.remove(child)
    tcPr.append(parse_xml(r'<w:shd %s w:fill="%s"/>' % (nsdecls('w'), color_hex)))

def set_cell_margins(cell, top=70, bottom=70, left=100, right=100):
    """Establece padding interno en dxa (1 pt = 20 dxa)."""
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = parse_xml(r'<w:tcMar %s><w:top w:w="%d" w:type="dxa"/><w:bottom w:w="%d" w:type="dxa"/><w:left w:w="%d" w:type="dxa"/><w:right w:w="%d" w:type="dxa"/></w:tcMar>' % (nsdecls('w'), top, bottom, left, right))
    tcPr.append(tcMar)

def set_cell_border(cell, **kwargs):
    """
    Configura bordes específicos de una celda.
    Argumentos válidos: top, bottom, left, right.
    Valor: color hex o False. sz="4" (1/2 pt), "8" (1 pt), "12" (1.5 pt), "16" (2 pt).
    """
    tcPr = cell._tc.get_or_add_tcPr()
    tcBorders = parse_xml(r'<w:tcBorders %s/>' % nsdecls('w'))
    for border_name in ['top', 'left', 'bottom', 'right']:
        val = kwargs.get(border_name)
        if val:
            sz = kwargs.get('sz', '4')
            tcBorders.append(parse_xml(r'<w:%s %s w:val="single" w:sz="%s" w:space="0" w:color="%s"/>' % (border_name, nsdecls('w'), sz, val)))
        elif val is False:
            tcBorders.append(parse_xml(r'<w:%s %s w:val="none"/>' % (border_name, nsdecls('w'))))
    tcPr.append(tcBorders)

def set_table_borders(table, top=True, bottom=True, left=True, right=True, insideH=True, insideV=True, color=HEX_BORDER, sz="4"):
    """Configura bordes perimetrales e internos a nivel de tabla."""
    tblPr = table._tbl.tblPr
    borders_elm = parse_xml(r'<w:tblBorders %s/>' % nsdecls('w'))
    mapping = {
        'top': top, 'bottom': bottom, 'left': left, 'right': right,
        'insideH': insideH, 'insideV': insideV
    }
    for b_name, active in mapping.items():
        if active:
            borders_elm.append(parse_xml(r'<w:%s %s w:val="single" w:sz="%s" w:space="0" w:color="%s"/>' % (b_name, nsdecls('w'), sz, color)))
        else:
            borders_elm.append(parse_xml(r'<w:%s %s w:val="none"/>' % (b_name, nsdecls('w'))))
    tblPr.append(borders_elm)

def set_paragraph_left_align(p):
    """
    Configura estricta e incondicionalmente la alineación izquierda tanto a nivel de
    python-docx (WD_ALIGN_PARAGRAPH.LEFT) como en OpenXML (w:jc w:val="left").
    Elimina cualquier directiva w:jc previa (como justificado heredado del estilo Normal).
    """
    p.alignment = WD_ALIGN_PARAGRAPH.LEFT
    pPr = p._p.get_or_add_pPr()
    for jc in pPr.findall(qn('w:jc')):
        pPr.remove(jc)
    jc_elm = parse_xml(r'<w:jc %s w:val="left"/>' % nsdecls('w'))
    rPr = pPr.find(qn('w:rPr'))
    if rPr is not None:
        pPr.insert(pPr.index(rPr), jc_elm)
    else:
        pPr.append(jc_elm)

# ==============================================================================
# GENERADOR DE TABLAS DE VERDAD Y TABLAS FORMALES (SOLO 'V' Y 'F')
# ==============================================================================
def add_truth_table(doc: docx.Document, headers: list, rows: list, caption: str, col_widths: list = None):
    """
    Genera una tabla formal (o tabla de verdad) respetando estrictamente el uso de 'V' y 'F' (PROHIBIDO 0 y 1).
    Aplica sombreado inteligente, interlineado compacto (1.0), padding óptimo y OpenXML w:cantSplit / w:tblHeader.
    """
    if caption:
        p_cap = doc.add_paragraph()
        p_cap.paragraph_format.space_before = Pt(10)
        p_cap.paragraph_format.space_after = Pt(3)
        p_cap.paragraph_format.keep_with_next = True
        r_cap = p_cap.add_run(caption)
        r_cap.font.name = FONT_FAMILY
        r_cap.font.size = Pt(9.0)
        r_cap.font.bold = True
        r_cap.font.color.rgb = RGB_NAVY

    table = doc.add_table(rows=len(rows) + 1, cols=len(headers))
    # Calcular anchos automáticos equilibrados si no fueron provistos
    if not col_widths or len(col_widths) != len(headers):
        avg_w = round(6.5 / len(headers), 2)
        col_widths = [avg_w] * len(headers)
        
    format_table_structure(table, col_widths=col_widths, repeat_header=True)
    set_table_borders(table, color=HEX_BORDER, sz="6")
    
    # 1. Cabecera
    hdr_cells = table.rows[0].cells
    for i, h_text in enumerate(headers):
        hdr_cells[i].text = h_text
        set_cell_shading(hdr_cells[i], HEX_NAVY)
        set_cell_margins(hdr_cells[i], top=90, bottom=90, left=110, right=110)
        p = hdr_cells[i].paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.paragraph_format.space_before = Pt(0)
        p.paragraph_format.space_after = Pt(0)
        p.paragraph_format.line_spacing = 1.0
        for run in p.runs:
            run.font.name = FONT_FAMILY
            run.font.size = Pt(9.5)
            run.font.bold = True
            run.font.color.rgb = RGB_WHITE
            
    # 2. Filas de datos
    for r_idx, row_data in enumerate(rows):
        cells = table.rows[r_idx + 1].cells
        is_alt = (r_idx % 2 == 1)
        row_bg = HEX_BG_ALT if is_alt else "FFFFFF"
        
        for c_idx, val in enumerate(row_data):
            cells[c_idx].text = str(val)
            set_cell_margins(cells[c_idx], top=70, bottom=70, left=100, right=100)
            p = cells[c_idx].paragraphs[0]
            p.paragraph_format.space_before = Pt(0)
            p.paragraph_format.space_after = Pt(0)
            p.paragraph_format.line_spacing = 1.0
            
            text_val = str(val).strip()
            # Sombreado y color para valores de verdad formales
            if text_val == "V":
                set_cell_shading(cells[c_idx], HEX_TRUE_BG)
                p.alignment = WD_ALIGN_PARAGRAPH.CENTER
                for run in p.runs:
                    run.font.name = FONT_FAMILY
                    run.font.size = Pt(9.5)
                    run.font.bold = True
                    run.font.color.rgb = RGBColor(22, 101, 52)
            elif text_val == "F":
                set_cell_shading(cells[c_idx], HEX_FALSE_BG)
                p.alignment = WD_ALIGN_PARAGRAPH.CENTER
                for run in p.runs:
                    run.font.name = FONT_FAMILY
                    run.font.size = Pt(9.5)
                    run.font.bold = True
                    run.font.color.rgb = RGBColor(153, 27, 27)
            else:
                set_cell_shading(cells[c_idx], row_bg)
                # Alineación inteligente: centrado para códigos breves o estados cortos, izquierda para descripciones
                is_short = len(text_val) <= 15 and (" " not in text_val or len(text_val.split()) <= 2)
                if is_short and c_idx < 3:
                    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
                else:
                    set_paragraph_left_align(p)
                for run in p.runs:
                    run.font.name = FONT_FAMILY
                    run.font.size = Pt(9.5)
                    run.font.color.rgb = RGB_DARK
                    
    return table

# ==============================================================================
# GENERADOR DE DICCIONARIO DE VARIABLES
# ==============================================================================
def add_variable_dictionary_table(doc: docx.Document, variables: list, title: str = "Diccionario Formal de Variables"):
    """
    Inserta una tabla formal de variables con:
    Variable | Tipo | Capa / Ámbito | Rango / Formato | Descripción y Semántica Clínica
    """
    headers = ["Variable", "Tipo", "Capa / Ámbito", "Rango / Formato", "Descripción y Semántica Clínica"]
    col_widths = [1.3, 0.9, 1.1, 1.2, 2.0]
    
    p_title = doc.add_paragraph()
    p_title.paragraph_format.space_before = Pt(10)
    p_title.paragraph_format.space_after = Pt(4)
    p_title.paragraph_format.keep_with_next = True
    r_t = p_title.add_run(f"📋 {title}")
    r_t.font.name = FONT_FAMILY
    r_t.font.size = Pt(10.5)
    r_t.font.bold = True
    r_t.font.color.rgb = RGB_NAVY
    
    table = doc.add_table(rows=len(variables) + 1, cols=len(headers))
    format_table_structure(table, col_widths=col_widths, repeat_header=True)
    set_table_borders(table, color=HEX_BORDER, sz="4")
    
    # Cabecera
    hdr_cells = table.rows[0].cells
    for i, h_text in enumerate(headers):
        hdr_cells[i].text = h_text
        set_cell_shading(hdr_cells[i], HEX_NAVY)
        set_cell_margins(hdr_cells[i], top=90, bottom=90, left=100, right=100)
        p = hdr_cells[i].paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.paragraph_format.space_before = Pt(0)
        p.paragraph_format.space_after = Pt(0)
        p.paragraph_format.line_spacing = 1.0
        for run in p.runs:
            run.font.name = FONT_FAMILY
            run.font.size = Pt(9.5)
            run.font.bold = True
            run.font.color.rgb = RGB_WHITE
            
    for r_idx, var in enumerate(variables):
        cells = table.rows[r_idx + 1].cells
        row_bg = HEX_BG_ALT if (r_idx % 2 == 1) else "FFFFFF"
        
        for c_idx, key in enumerate(["name", "type", "scope", "range", "desc"]):
            val = var.get(key, "")
            cells[c_idx].text = str(val)
            set_cell_shading(cells[c_idx], row_bg)
            set_cell_margins(cells[c_idx], top=60, bottom=60, left=90, right=90)
            p = cells[c_idx].paragraphs[0]
            p.paragraph_format.space_before = Pt(0)
            p.paragraph_format.space_after = Pt(0)
            p.paragraph_format.line_spacing = 1.0
            
            if c_idx in (1, 2):
                p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            else:
                set_paragraph_left_align(p)
            for run in p.runs:
                run.font.name = FONT_MONO if c_idx == 0 else FONT_FAMILY
                run.font.size = Pt(9.5)
                if c_idx == 0:
                    run.font.bold = True
                    run.font.color.rgb = RGB_NAVY
                elif c_idx == 1:
                    run.font.color.rgb = RGB_TEAL
                else:
                    run.font.color.rgb = RGB_DARK
                    
    return table

# ==============================================================================
# GENERADOR DE LISTA DE VERIFICACIÓN
# ==============================================================================
def add_checklist_table(doc: docx.Document, items: list, title: str = "LISTA DE VERIFICACIÓN ANTES DE ENTREGAR"):
    """
    Inserta una tabla formal de lista de verificación con:
    N° | Criterio de Verificación | Estado / Conformidad | Observaciones / Evidencia
    """
    p_title = doc.add_paragraph()
    p_title.paragraph_format.space_before = Pt(10)
    p_title.paragraph_format.space_after = Pt(4)
    p_title.paragraph_format.keep_with_next = True
    r_t = p_title.add_run(f"✅ {title}")
    r_t.font.name = FONT_FAMILY
    r_t.font.size = Pt(11)
    r_t.font.bold = True
    r_t.font.color.rgb = RGB_NAVY
    
    headers = ["N°", "Criterio de Verificación", "Estado / Conformidad", "Observaciones / Evidencia"]
    col_widths = [0.6, 2.6, 1.4, 1.9]
    
    table = doc.add_table(rows=len(items) + 1, cols=len(headers))
    format_table_structure(table, col_widths=col_widths, repeat_header=True)
    set_table_borders(table, color=HEX_BORDER, sz="6")
    
    # Cabecera
    hdr_cells = table.rows[0].cells
    for i, h_text in enumerate(headers):
        hdr_cells[i].text = h_text
        set_cell_shading(hdr_cells[i], HEX_NAVY)
        set_cell_margins(hdr_cells[i], top=90, bottom=90, left=100, right=100)
        p = hdr_cells[i].paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.paragraph_format.space_before = Pt(0)
        p.paragraph_format.space_after = Pt(0)
        p.paragraph_format.line_spacing = 1.0
        for run in p.runs:
            run.font.name = FONT_FAMILY
            run.font.size = Pt(9.5)
            run.font.bold = True
            run.font.color.rgb = RGB_WHITE
            
    for r_idx, item in enumerate(items):
        cells = table.rows[r_idx + 1].cells
        row_bg = HEX_BG_ALT if (r_idx % 2 == 1) else "FFFFFF"
        for c_idx, key in enumerate(["num", "criterio", "estado", "observaciones"]):
            val = item.get(key, "")
            cells[c_idx].text = str(val)
            set_cell_shading(cells[c_idx], row_bg)
            set_cell_margins(cells[c_idx], top=60, bottom=60, left=90, right=90)
            p = cells[c_idx].paragraphs[0]
            p.paragraph_format.space_before = Pt(0)
            p.paragraph_format.space_after = Pt(0)
            p.paragraph_format.line_spacing = 1.0
            if c_idx in (0, 2):
                p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            else:
                set_paragraph_left_align(p)
            for run in p.runs:
                run.font.name = FONT_FAMILY
                run.font.size = Pt(9.5)
                if c_idx == 0:
                    run.font.bold = True
                    run.font.color.rgb = RGB_NAVY
                elif c_idx == 2:
                    run.font.bold = True
                    run.font.color.rgb = RGB_TEAL
                else:
                    run.font.color.rgb = RGB_DARK
                    
    return table

# ==============================================================================
# GENERADOR DEL MARCO FORMAL PEAS
# ==============================================================================
def add_peas_section(doc: docx.Document, peas_data: dict, intro_text: str = None, caption: str = None):
    """
    Genera la sección y tabla estructurada del Marco de Agente Inteligente PEAS:
    - Performance Measures (Medidas de Rendimiento)
    - Environment (Entorno)
    - Actuators (Actuadores)
    - Sensors (Sensores)
    """
    if intro_text is None:
        p_intro = doc.add_paragraph()
        p_intro.paragraph_format.line_spacing = 1.15
        p_intro.paragraph_format.space_before = Pt(4)
        p_intro.paragraph_format.space_after = Pt(6)
        r_in = p_intro.add_run(
            "Bajo el paradigma de la Inteligencia Artificial determinista y la ingeniería de software clínica, "
            "MedReminder AI se modela formalmente como un Agente Inteligente Basado en Metas y Estados. "
            "A continuación se especifica la formalización bajo el marco PEAS (Performance, Environment, Actuators, Sensors):"
        )
        r_in.font.name = FONT_FAMILY
        r_in.font.size = Pt(11)
        r_in.font.color.rgb = RGB_DARK
    elif intro_text.strip():
        p_intro = doc.add_paragraph()
        p_intro.paragraph_format.line_spacing = 1.15
        p_intro.paragraph_format.space_before = Pt(4)
        p_intro.paragraph_format.space_after = Pt(6)
        r_in = p_intro.add_run(intro_text.strip())
        r_in.font.name = FONT_FAMILY
        r_in.font.size = Pt(11)
        r_in.font.color.rgb = RGB_DARK
    
    headers = ["Dimensión PEAS", "Especificación Técnica y Operativa en MedReminder AI", "Métricas y Parámetros Formales"]
    col_widths = [1.5, 3.2, 1.8]
    
    rows = [
        [
            "Rendimiento (P)\nPerformance",
            peas_data.get("performance", "Maximizar adherencia terapéutica y eliminar omisiones posológicas."),
            peas_data.get("performance_metrics", "• Adherencia ≥ 95%\n• Falsos positivos stock < 1%\n• Latencia UI ≤ 200 ms\n• Descuento estricto D ↔ T")
        ],
        [
            "Entorno (E)\nEnvironment",
            peas_data.get("environment", "Dispositivo móvil Android, servidor FastAPI local/nube y base MySQL/Mongo."),
            peas_data.get("environment_metrics", "• SO: Android 8.0+ (API 26-35)\n• Conectividad: Híbrida (offline/LAN)\n• Almacenamiento: MySQL 8 + Mongo 6")
        ],
        [
            "Actuadores (A)\nActuators",
            peas_data.get("actuators") or peas_data.get("actuadores", "AlarmManager de alta precisión, notificaciones Heads-Up, síntesis TTS y UI."),
            peas_data.get("actuators_metrics") or peas_data.get("actuadores_metrics", "• AlarmManager exacto\n• Snackbar reactivo\n• Mutaciones REST en backend\n• Síntesis de voz háptica")
        ],
        [
            "Sensores (S)\nSensors",
            peas_data.get("sensors") or peas_data.get("sensores", "Reloj RTC de tiempo real, pantalla táctil, receptor BOOT_COMPLETED y sockets."),
            peas_data.get("sensors_metrics") or peas_data.get("sensores_metrics", "• Timestamp UTC (reloj RTC)\n• Eventos touch (botones ≥ 56dp)\n• Detector de red (WiFi/Datos)\n• Telemetría de inventario")
        ]
    ]
    
    if caption:
        p_cap = doc.add_paragraph()
        p_cap.paragraph_format.space_before = Pt(10)
        p_cap.paragraph_format.space_after = Pt(3)
        p_cap.paragraph_format.keep_with_next = True
        r_cap = p_cap.add_run(caption)
        r_cap.font.name = FONT_FAMILY
        r_cap.font.size = Pt(9.0)
        r_cap.font.bold = True
        r_cap.font.color.rgb = RGB_NAVY

    table = doc.add_table(rows=len(rows) + 1, cols=len(headers))
    format_table_structure(table, col_widths=col_widths, repeat_header=True)
    set_table_borders(table, color=HEX_BORDER, sz="6")
    
    hdr_cells = table.rows[0].cells
    for i, h_text in enumerate(headers):
        hdr_cells[i].text = h_text
        set_cell_shading(hdr_cells[i], HEX_NAVY)
        set_cell_margins(hdr_cells[i], top=90, bottom=90, left=110, right=110)
        p = hdr_cells[i].paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.paragraph_format.space_before = Pt(0)
        p.paragraph_format.space_after = Pt(0)
        p.paragraph_format.line_spacing = 1.0
        for run in p.runs:
            run.font.name = FONT_FAMILY
            run.font.size = Pt(9.5)
            run.font.bold = True
            run.font.color.rgb = RGB_WHITE
            
    for r_idx, (dim, spec, met) in enumerate(rows):
        cells = table.rows[r_idx + 1].cells
        row_bg = HEX_BG_ALT if (r_idx % 2 == 1) else "FFFFFF"
        
        for c_idx, val in enumerate([dim, spec, met]):
            cells[c_idx].text = val
            set_cell_shading(cells[c_idx], row_bg)
            set_cell_margins(cells[c_idx], top=70, bottom=70, left=100, right=100)
            p = cells[c_idx].paragraphs[0]
            p.paragraph_format.space_before = Pt(0)
            p.paragraph_format.space_after = Pt(0)
            p.paragraph_format.line_spacing = 1.0
            if c_idx == 0:
                p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            else:
                set_paragraph_left_align(p)
            for run in p.runs:
                run.font.name = FONT_FAMILY
                run.font.size = Pt(9.5)
                if c_idx == 0:
                    run.font.bold = True
                    run.font.color.rgb = RGB_NAVY
                else:
                    run.font.color.rgb = RGB_DARK
                    
    return table

# ==============================================================================
# ELEMENTOS VISUALES: CALLOUTS, CÓDIGO E IMÁGENES
# ==============================================================================
def add_callout(doc: docx.Document, text: str, callout_type: str = "tip", title: str = None):
    """
    Inserta una caja de llamada profesional con borde izquierdo acentuado.
    Tipos: 'tip' (clínico), 'warn' (advertencia/regla de oro), 'arch' (técnico/arquitectura).
    """
    colors = {
        "tip":  (HEX_CALLOUT_BG, HEX_TEAL, "💡 CONSEJO CLÍNICO Y OPERATIVO"),
        "warn": (HEX_WARN_BG, "D97706", "⚠️ REGLA DE ORO DEL SISTEMA"),
        "arch": ("EFF6FF", "2563EB", "🏛️ DECISIÓN DE ARQUITECTURA E INGENIERÍA")
    }
    bg_color, border_color, default_title = colors.get(callout_type, colors["tip"])
    header_title = title if title else default_title
    
    table = doc.add_table(rows=1, cols=1)
    format_table_structure(table, col_widths=[6.5], repeat_header=False)
    cell = table.rows[0].cells[0]
    
    set_cell_shading(cell, bg_color)
    set_cell_margins(cell, top=80, bottom=80, left=140, right=140)
    set_cell_border(cell, left=border_color, top=False, bottom=False, right=False, sz="24")
    
    p = cell.paragraphs[0]
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after = Pt(0)
    p.paragraph_format.line_spacing = 1.15
    set_paragraph_left_align(p)
    
    r_h = p.add_run(f"{header_title}\n")
    r_h.font.name = FONT_FAMILY
    r_h.font.size = Pt(9.5)
    r_h.font.bold = True
    r_h.font.color.rgb = RGBColor(
        int(border_color[0:2], 16),
        int(border_color[2:4], 16),
        int(border_color[4:6], 16)
    )
    
    r_b = p.add_run(text)
    r_b.font.name = FONT_FAMILY
    r_b.font.size = Pt(9.5)
    r_b.font.color.rgb = RGB_DARK
    return table

def add_code_block(doc: docx.Document, code_text: str, caption: str = None):
    """Inserta un bloque de código fuente formateado con fondo gris tenue y fuente monospace con alineación izquierda obligatoria."""
    if caption:
        p_c = doc.add_paragraph()
        p_c.paragraph_format.space_before = Pt(8)
        p_c.paragraph_format.space_after = Pt(3)
        p_c.paragraph_format.keep_with_next = True
        set_paragraph_left_align(p_c)
        r_c = p_c.add_run(f"💻 {caption}")
        r_c.font.name = FONT_FAMILY
        r_c.font.size = Pt(9.0)
        r_c.font.bold = True
        r_c.font.color.rgb = RGB_MUTED
        
    table = doc.add_table(rows=1, cols=1)
    format_table_structure(table, col_widths=[6.5], repeat_header=False)
    cell = table.rows[0].cells[0]
    set_cell_shading(cell, HEX_CODE_BG)
    set_cell_margins(cell, top=80, bottom=80, left=120, right=120)
    set_cell_border(cell, left=HEX_BORDER, top=HEX_BORDER, bottom=HEX_BORDER, right=HEX_BORDER, sz="6")
    
    p = cell.paragraphs[0]
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after = Pt(0)
    p.paragraph_format.line_spacing = 1.0
    set_paragraph_left_align(p)
    
    cleaned_code = code_text.replace("\r\n", "\n").strip()
    run = p.add_run(cleaned_code)
    run.font.name = FONT_MONO
    run.font.size = Pt(8.5)
    run.font.color.rgb = RGBColor(30, 41, 59)
    rPr = run._r.get_or_add_rPr()
    rPr.append(parse_xml(r'<w:rFonts %s w:ascii="%s" w:hAnsi="%s" w:cs="%s"/>' % (nsdecls('w'), FONT_MONO, FONT_MONO, FONT_MONO)))
    
    # Si el bloque de código contiene múltiples párrafos o líneas divididas, garantizar
    # que cada párrafo dentro de la celda de código tenga asignado estricta e incondicionalmente w:val="left"
    for p_cell in cell.paragraphs:
        p_cell.paragraph_format.space_before = Pt(0)
        p_cell.paragraph_format.space_after = Pt(0)
        p_cell.paragraph_format.line_spacing = 1.0
        set_paragraph_left_align(p_cell)
        for r in p_cell.runs:
            r.font.name = FONT_MONO
            r_rPr = r._r.get_or_add_rPr()
            if r_rPr.find(qn('w:rFonts')) is None:
                r_rPr.append(parse_xml(r'<w:rFonts %s w:ascii="%s" w:hAnsi="%s" w:cs="%s"/>' % (nsdecls('w'), FONT_MONO, FONT_MONO, FONT_MONO)))
        
    return table

def add_figure_image(doc: docx.Document, img_path: str, caption: str, width_in_inches: float = 4.5):
    """Inserta una imagen centrada con keep_with_next y pie de figura formal de 9pt."""
    if not os.path.exists(img_path):
        return
        
    p_img = doc.add_paragraph()
    p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_img.paragraph_format.space_before = Pt(8)
    p_img.paragraph_format.space_after = Pt(2)
    p_img.paragraph_format.keep_with_next = True
    
    r_img = p_img.add_run()
    r_img.font.name = FONT_FAMILY
    r_img.add_picture(img_path, width=Inches(width_in_inches))
    
    p_cap = doc.add_paragraph()
    p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_cap.paragraph_format.space_before = Pt(2)
    p_cap.paragraph_format.space_after = Pt(8)
    r_cap = p_cap.add_run(caption)
    r_cap.font.name = FONT_FAMILY
    r_cap.font.size = Pt(9.0)
    r_cap.font.italic = True
    r_cap.font.color.rgb = RGB_MUTED

# ==============================================================================
# ENCABEZADOS Y TEXTO DEL CUERPO
# ==============================================================================
def add_section_heading(doc: docx.Document, text: str, level: int = 1, page_break_before: bool = False):
    """Agrega un encabezado estructurado con jerarquía clara y keep_with_next para evitar huérfanos."""
    h = doc.add_heading(level=level)
    h.paragraph_format.keep_with_next = True
    if page_break_before:
        h.paragraph_format.page_break_before = True
    run = h.add_run(text)
    run.font.name = FONT_FAMILY
    run.font.bold = True
    
    if level == 1:
        run.font.size = Pt(15)
        run.font.color.rgb = RGB_NAVY
        h.paragraph_format.space_before = Pt(14)
        h.paragraph_format.space_after = Pt(4)
    elif level == 2:
        run.font.size = Pt(12.5)
        run.font.color.rgb = RGB_TEAL
        h.paragraph_format.space_before = Pt(10)
        h.paragraph_format.space_after = Pt(3)
    else:
        run.font.size = Pt(11)
        run.font.color.rgb = RGB_DARK
        h.paragraph_format.space_before = Pt(8)
        h.paragraph_format.space_after = Pt(2)
    return h

def add_body_p(doc: docx.Document, text: str) -> docx.text.paragraph.Paragraph:
    """
    Inserta párrafos de texto justificado con tipografía estándar de 11pt e interlineado 1.15.
    Si el texto contiene dobles saltos de línea (\\n\\n), los desglosa en párrafos nativos
    para garantizar espaciado homogéneo y evitar líneas vacías o cortes artificiales.
    """
    blocks = [b.strip() for b in text.split("\n\n") if b.strip()]
    if not blocks:
        blocks = [""]
        
    last_p = None
    for block in blocks:
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        p.paragraph_format.line_spacing = 1.15
        p.paragraph_format.space_before = Pt(0)
        p.paragraph_format.space_after = Pt(5)
        
        run = p.add_run(block)
        run.font.name = FONT_FAMILY
        run.font.size = Pt(11)
        run.font.color.rgb = RGB_DARK
        last_p = p
        
    return last_p

def add_page_break(doc: docx.Document) -> docx.text.paragraph.Paragraph:
    """Inserta un salto de página limpio con espaciado cero y fuente explícita para evitar fuentes residuales."""
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after = Pt(0)
    p.paragraph_format.line_spacing = 1.0
    r = p.add_run()
    r.font.name = FONT_FAMILY
    r.add_break(docx.enum.text.WD_BREAK.PAGE)
    return p
