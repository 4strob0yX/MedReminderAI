import os
import docx
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn

def set_cell_margins(cell, top=80, bottom=80, left=100, right=100):
    tc = cell._tc
    tcPr = tc.get_or_add_tcPr()
    tcMar = OxmlElement('w:tcMar')
    for m, val in [('top', top), ('bottom', bottom), ('left', left), ('right', right)]:
        node = OxmlElement(f'w:{m}')
        node.set(qn('w:w'), str(val))
        node.set(qn('w:type'), 'dxa')
        tcMar.append(node)
    tcPr.append(tcMar)

def set_cell_background(cell, hex_color):
    tcPr = cell._tc.get_or_add_tcPr()
    shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{hex_color}"/>')
    tcPr.append(shd)

def set_card_borders(cell, border_color="E2E8F0"):
    tcPr = cell._tc.get_or_add_tcPr()
    borders = parse_xml(f'''
        <w:tcBorders {nsdecls("w")}>
            <w:top w:val="single" w:sz="6" w:space="0" w:color="{border_color}"/>
            <w:left w:val="single" w:sz="18" w:space="0" w:color="0D9488"/>
            <w:bottom w:val="single" w:sz="6" w:space="0" w:color="{border_color}"/>
            <w:right w:val="single" w:sz="6" w:space="0" w:color="{border_color}"/>
        </w:tcBorders>
    ''')
    tcPr.append(borders)

def set_clean_table_borders(table, border_color="E2E8F0"):
    tblPr = table._tbl.tblPr
    borders = parse_xml(f'''
        <w:tblBorders {nsdecls("w")}>
            <w:top w:val="single" w:sz="6" w:space="0" w:color="0F766E"/>
            <w:bottom w:val="single" w:sz="8" w:space="0" w:color="CBD5E1"/>
            <w:insideH w:val="single" w:sz="4" w:space="0" w:color="{border_color}"/>
            <w:insideV w:val="none"/>
            <w:left w:val="none"/>
            <w:right w:val="none"/>
        </w:tblBorders>
    ''')
    tblPr.append(borders)

def set_page_setup(doc):
    for s in doc.sections:
        s.top_margin = Inches(0.6)
        s.bottom_margin = Inches(0.6)
        s.left_margin = Inches(0.65)
        s.right_margin = Inches(0.65)
        
        # Header
        header = s.header
        hp = header.paragraphs[0]
        hp.alignment = WD_ALIGN_PARAGRAPH.RIGHT
        hrun = hp.add_run("MedReminder AI • Guía de Uso Rápido")
        hrun.font.name = "Calibri"
        hrun.font.size = Pt(8.5)
        hrun.font.color.rgb = RGBColor(148, 163, 184)
        
        # Footer
        footer = s.footer
        fp = footer.paragraphs[0]
        fp.alignment = WD_ALIGN_PARAGRAPH.RIGHT
        frun1 = fp.add_run("Página ")
        frun1.font.name = "Calibri"
        frun1.font.size = Pt(8.5)
        frun1.font.color.rgb = RGBColor(100, 116, 139)
        
        fld_page = parse_xml(r'<w:fldSimple %s w:instr="PAGE"/>' % nsdecls('w'))
        fp._p.append(fld_page)
        
        frun2 = fp.add_run(" de ")
        frun2.font.name = "Calibri"
        frun2.font.size = Pt(8.5)
        frun2.font.color.rgb = RGBColor(100, 116, 139)
        
        fld_numpages = parse_xml(r'<w:fldSimple %s w:instr="NUMPAGES"/>' % nsdecls('w'))
        fp._p.append(fld_numpages)

def add_step_card(doc, step_num, title, img_path, bullets, tip=None):
    tbl = doc.add_table(rows=1, cols=2)
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    tbl.autofit = False
    
    col_img_width = Inches(1.85)
    col_txt_width = Inches(5.15)
    tbl.columns[0].width = col_img_width
    tbl.columns[1].width = col_txt_width
    
    cell_img = tbl.cell(0, 0)
    cell_txt = tbl.cell(0, 1)
    
    set_cell_background(cell_img, "F8FAFC")
    set_cell_background(cell_txt, "FFFFFF")
    
    set_card_borders(cell_img, "E2E8F0")
    set_card_borders(cell_txt, "E2E8F0")
    
    set_cell_margins(cell_img, top=100, bottom=100, left=80, right=80)
    set_cell_margins(cell_txt, top=100, bottom=100, left=140, right=140)
    
    # Imagen centrada en celda izquierda
    p_img = cell_img.paragraphs[0]
    p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_img.paragraph_format.space_before = Pt(2)
    p_img.paragraph_format.space_after = Pt(2)
    if os.path.exists(img_path):
        r_img = p_img.add_run()
        r_img.add_picture(img_path, width=Inches(1.65))
        
    # Texto en celda derecha
    p_title = cell_txt.paragraphs[0]
    p_title.paragraph_format.space_before = Pt(0)
    p_title.paragraph_format.space_after = Pt(6)
    
    r_badge = p_title.add_run(f"PASO {step_num}: ")
    r_badge.bold = True
    r_badge.font.name = "Calibri"
    r_badge.font.size = Pt(11.5)
    r_badge.font.color.rgb = RGBColor(13, 148, 136) # Teal-600
    
    r_head = p_title.add_run(title)
    r_head.bold = True
    r_head.font.name = "Calibri"
    r_head.font.size = Pt(11.5)
    r_head.font.color.rgb = RGBColor(15, 23, 42) # Slate-900
    
    for bold_prefix, text in bullets:
        pb = cell_txt.add_paragraph()
        pb.paragraph_format.space_before = Pt(0)
        pb.paragraph_format.space_after = Pt(3)
        pb.paragraph_format.line_spacing = 1.1
        
        rb_dot = pb.add_run("• ")
        rb_dot.bold = True
        rb_dot.font.color.rgb = RGBColor(13, 148, 136)
        
        if bold_prefix:
            rb_pre = pb.add_run(bold_prefix + ": ")
            rb_pre.bold = True
            rb_pre.font.size = Pt(9)
            rb_pre.font.color.rgb = RGBColor(30, 41, 59)
            
        rb_txt = pb.add_run(text)
        rb_txt.font.size = Pt(9)
        rb_txt.font.color.rgb = RGBColor(51, 65, 85)
        
    if tip:
        pt = cell_txt.add_paragraph()
        pt.paragraph_format.space_before = Pt(4)
        pt.paragraph_format.space_after = Pt(0)
        rt_lbl = pt.add_run("💡 Consejo clínico: ")
        rt_lbl.bold = True
        rt_lbl.font.size = Pt(8.5)
        rt_lbl.font.color.rgb = RGBColor(180, 83, 9)
        rt_txt = pt.add_run(tip)
        rt_txt.font.size = Pt(8.5)
        rt_txt.italic = True
        rt_txt.font.color.rgb = RGBColor(120, 53, 15)

    # Spacing between cards
    sp = doc.add_paragraph()
    sp.paragraph_format.space_before = Pt(0)
    sp.paragraph_format.space_after = Pt(6)

def main():
    doc = Document()
    set_page_setup(doc)
    
    # Normal style
    style_normal = doc.styles['Normal']
    style_normal.font.name = 'Calibri'
    style_normal.font.size = Pt(9.5)
    style_normal.font.color.rgb = RGBColor(30, 41, 59)
    
    # ==========================================
    # PÁGINA 1: ENCABEZADO + PASO 1 Y PASO 2
    # ==========================================
    
    # Banner superior compacto
    tbl_top = doc.add_table(rows=1, cols=1)
    tbl_top.alignment = WD_TABLE_ALIGNMENT.CENTER
    tbl_top.autofit = False
    tbl_top.columns[0].width = Inches(7.0)
    cell_top = tbl_top.cell(0, 0)
    set_cell_background(cell_top, "0F766E") # Dark Teal
    set_cell_margins(cell_top, top=100, bottom=100, left=140, right=140)
    
    pt = cell_top.paragraphs[0]
    pt.paragraph_format.space_before = Pt(0)
    pt.paragraph_format.space_after = Pt(2)
    rt1 = pt.add_run("GUÍA DE USO RÁPIDO • MEDREMINDER AI")
    rt1.bold = True
    rt1.font.size = Pt(15)
    rt1.font.color.rgb = RGBColor(255, 255, 255)
    
    pt_sub = cell_top.add_paragraph()
    pt_sub.paragraph_format.space_before = Pt(0)
    pt_sub.paragraph_format.space_after = Pt(0)
    rt2 = pt_sub.add_run("Control estricto de medicamentos, tomas de medicamentos puntuales y adherencia en 4 pasos simples.")
    rt2.font.size = Pt(9.5)
    rt2.font.color.rgb = RGBColor(204, 251, 241) # Teal-100
    
    p_intro = doc.add_paragraph()
    p_intro.paragraph_format.space_before = Pt(8)
    p_intro.paragraph_format.space_after = Pt(8)
    p_intro.paragraph_format.line_spacing = 1.15
    r_in = p_intro.add_run("Esta guía resume el uso diario del paciente y cuidador. La interfaz está optimizada con botones extragrandes (≥ 56 dp) y protección contra pulsaciones involuntarias para máxima seguridad médica.")
    r_in.font.size = Pt(9.5)
    r_in.font.color.rgb = RGBColor(71, 85, 105)
    
    # Paso 1: Iniciar Sesión
    add_step_card(
        doc,
        step_num="1",
        title="Acceso al Sistema",
        img_path="docs/screenshots/01_login.png",
        bullets=[
            ("Credenciales", "Ingresa tu correo y contraseña asignada."),
            ("Protección táctil", "Al presionar «Iniciar Sesión», el botón se deshabilita para evitar dobles solicitudes."),
            ("Nuevo usuario", "Si aún no tienes cuenta, pulsa «Regístrate» al pie de la pantalla en segundos.")
        ],
        tip="Tus datos y contraseñas viajan cifrados bajo estándar seguro bcrypt y JWT."
    )
    
    # Paso 2: Registrar Medicamento
    add_step_card(
        doc,
        step_num="2",
        title="Alta de un Nuevo Medicamento",
        img_path="docs/screenshots/03_nuevo_medicamento.png",
        bullets=[
            ("Forma y Nombre", "Selecciona si es Comprimido, Gotas o Inyectable y escribe el fármaco."),
            ("Dosis rápida", "Escribe la dosis o pulsa las sugerencias (ej. 500 mg, 1 comp., 10 ml)."),
            ("Frecuencia y Stock", "Indica el horario (ej. cada 8 horas) y el número de piezas iniciales en casa.")
        ],
        tip="Al guardar, el backend calcula automáticamente todos los horarios del día en UTC."
    )
    
    doc.add_page_break()
    
    # ==========================================
    # PÁGINA 2: PASO 3 Y PASO 4 + REGLA DE ALARMAS
    # ==========================================
    
    p_p2_hdr = doc.add_paragraph()
    p_p2_hdr.paragraph_format.space_before = Pt(4)
    p_p2_hdr.paragraph_format.space_after = Pt(8)
    r_p2_t = p_p2_hdr.add_run("Gestión Diaria y Suministros")
    r_p2_t.bold = True
    r_p2_t.font.size = Pt(14)
    r_p2_t.font.color.rgb = RGBColor(15, 118, 110)
    
    # Paso 3: Pantalla Hoy y Tomas de Medicamentos
    add_step_card(
        doc,
        step_num="3",
        title="Plan Diario y Alarmas (Pantalla «Hoy»)",
        img_path="docs/screenshots/02_hoy.png",
        bullets=[
            ("Plan del Día", "Revisa en la tarjeta superior tus tomas de medicamentos programadas y el contador diario (ej. 0/3)."),
            ("Tomar Ahora", "Registra la toma de medicamentos con marca de tiempo precisa con validez médico-legal."),
            ("Posponer 30 min", "Mueve la alarma 30 minutos sin perder el seguimiento activo."),
            ("Omitir", "Se registra la justificación de omisión para el expediente del médico tratante.")
        ],
        tip="Las alarmas son 100% locales con AlarmManager: suenan con exactitud incluso sin conexión a internet."
    )
    
    # Paso 4: Mi Botiquín
    add_step_card(
        doc,
        step_num="4",
        title="Control de Existencias («Mi Botiquín»)",
        img_path="docs/screenshots/04_botiquin.png",
        bullets=[
            ("Inventario Activo", "Consulta el porcentaje de suministros asegurados y fecha de reposición."),
            ("Alerta preventiva", "La tarjeta avisa en amarillo cuando queden menos de 3 días de dosis."),
            ("Ajuste de Stock", "Suma unidades cuando compres una nueva caja para mantener el conteo al día.")
        ],
        tip="Evita interrupciones de tratamiento: surte la receta cuando la alerta llegue al 20% de stock."
    )
    
    # Mini tabla destacada: Regla estricta de posposición
    tbl_regla = doc.add_table(rows=1, cols=1)
    tbl_regla.alignment = WD_TABLE_ALIGNMENT.CENTER
    tbl_regla.columns[0].width = Inches(7.0)
    c_regla = tbl_regla.cell(0, 0)
    set_cell_background(c_regla, "FFFBEB") # Soft amber
    set_card_borders(c_regla, "F59E0B")
    set_cell_margins(c_regla, top=80, bottom=80, left=120, right=120)
    
    pr = c_regla.paragraphs[0]
    pr.paragraph_format.space_before = Pt(0)
    pr.paragraph_format.space_after = Pt(2)
    rr1 = pr.add_run("⚠️ REGLA DE ORO DE LAS POSPOSICIONES: ")
    rr1.bold = True
    rr1.font.size = Pt(9.5)
    rr1.font.color.rgb = RGBColor(180, 83, 9)
    rr2 = pr.add_run("Solo puedes posponer una dosis un máximo de 2 veces (30 min c/u). Si no confirmas en la tercera alerta, el sistema registrará automáticamente la toma de medicamentos como «Omitida» para auditar el olvido con precisión médica.")
    rr2.font.size = Pt(9)
    rr2.font.color.rgb = RGBColor(120, 53, 15)
    
    doc.add_page_break()
    
    # ==========================================
    # PÁGINA 3: CHEAT SHEET, TROUBLESHOOTING Y ANÁLISIS
    # ==========================================
    
    p_p3_hdr = doc.add_paragraph()
    p_p3_hdr.paragraph_format.space_before = Pt(4)
    p_p3_hdr.paragraph_format.space_after = Pt(6)
    r_p3_t = p_p3_hdr.add_run("Tarjeta de Referencia Rápida y Soporte")
    r_p3_t.bold = True
    r_p3_t.font.size = Pt(14)
    r_p3_t.font.color.rgb = RGBColor(15, 118, 110)
    
    # Tabla 1: Glosario de Estados
    p_sub1 = doc.add_paragraph()
    p_sub1.paragraph_format.space_before = Pt(4)
    p_sub1.paragraph_format.space_after = Pt(3)
    r_s1 = p_sub1.add_run("1. Estados de un Recordatorio")
    r_s1.bold = True
    r_s1.font.size = Pt(10)
    r_s1.font.color.rgb = RGBColor(30, 41, 59)
    
    tbl_estados = doc.add_table(rows=5, cols=3)
    tbl_estados.alignment = WD_TABLE_ALIGNMENT.CENTER
    tbl_estados.columns[0].width = Inches(1.5)
    tbl_estados.columns[1].width = Inches(3.2)
    tbl_estados.columns[2].width = Inches(2.3)
    set_clean_table_borders(tbl_estados)
    
    heads1 = ["Estado", "Significado Clínico", "Acción del Paciente"]
    for c_i, h_val in enumerate(heads1):
        cell = tbl_estados.cell(0, c_i)
        set_cell_background(cell, "0F766E")
        set_cell_margins(cell, top=80, bottom=80, left=80, right=80)
        p = cell.paragraphs[0]
        r = p.add_run(h_val)
        r.bold = True
        r.font.size = Pt(8.5)
        r.font.color.rgb = RGBColor(255, 255, 255)
        
    data_est = [
        ("Pendiente", "Hora programada futura o alarma sonando actualmente.", "Pulsar la notificación y abrir la app."),
        ("Tomado", "Medicamento ingerido; se descuenta 1 unidad del stock.", "Ninguna; dosis completada exitosamente."),
        ("Pospuesto", "Alarma retrasada 30 min (máx. 2 posposiciones).", "Esperar el nuevo aviso antes de que expire."),
        ("Omitido", "Dosis no administrada por decisión del paciente o timeout.", "Consultar al médico si requiere reposición.")
    ]
    for r_i, row in enumerate(data_est, start=1):
        bg = "F8FAFC" if r_i % 2 == 1 else "FFFFFF"
        for c_i, val in enumerate(row):
            cell = tbl_estados.cell(r_i, c_i)
            set_cell_background(cell, bg)
            set_cell_margins(cell, top=60, bottom=60, left=80, right=80)
            p = cell.paragraphs[0]
            r = p.add_run(val)
            r.font.size = Pt(8.5)
            if c_i == 0:
                r.bold = True
                
    # Tabla 2: Solución de Incidencias en 1 paso
    p_sub2 = doc.add_paragraph()
    p_sub2.paragraph_format.space_before = Pt(8)
    p_sub2.paragraph_format.space_after = Pt(3)
    r_s2 = p_sub2.add_run("2. Solución Rápida de Incidencias (Troubleshooting)")
    r_s2.bold = True
    r_s2.font.size = Pt(10)
    r_s2.font.color.rgb = RGBColor(30, 41, 59)
    
    tbl_faq = doc.add_table(rows=4, cols=3)
    tbl_faq.alignment = WD_TABLE_ALIGNMENT.CENTER
    tbl_faq.columns[0].width = Inches(2.1)
    tbl_faq.columns[1].width = Inches(2.2)
    tbl_faq.columns[2].width = Inches(2.7)
    set_clean_table_borders(tbl_faq)
    
    heads2 = ["Síntoma", "¿Por qué sucede?", "Solución Inmediata"]
    for c_i, h_val in enumerate(heads2):
        cell = tbl_faq.cell(0, c_i)
        set_cell_background(cell, "0F766E")
        set_cell_margins(cell, top=80, bottom=80, left=80, right=80)
        p = cell.paragraphs[0]
        r = p.add_run(h_val)
        r.bold = True
        r.font.size = Pt(8.5)
        r.font.color.rgb = RGBColor(255, 255, 255)
        
    data_faq = [
        ("La alarma no suena con pantalla apagada", "Ahorro de batería agresivo en Android.", "Ajustes > Apps > MedReminder AI > Batería: marcar «Sin restricciones»."),
        ("No aparece botón 'Posponer'", "Se consumieron los 2 intentos permitidos.", "Tomar la dosis inmediatamente o confirmar la omisión."),
        ("Sin conexión a internet", "Falta de datos móviles o señal Wi-Fi.", "Los recordatorios suenan igual. Al volver la red, el registro se sincroniza.")
    ]
    for r_i, row in enumerate(data_faq, start=1):
        bg = "F8FAFC" if r_i % 2 == 1 else "FFFFFF"
        for c_i, val in enumerate(row):
            cell = tbl_faq.cell(r_i, c_i)
            set_cell_background(cell, bg)
            set_cell_margins(cell, top=60, bottom=60, left=80, right=80)
            p = cell.paragraphs[0]
            r = p.add_run(val)
            r.font.size = Pt(8.5)
            if c_i == 0:
                r.bold = True

    # Cuadro final de contacto
    p_spacer_end = doc.add_paragraph()
    p_spacer_end.paragraph_format.space_before = Pt(8)
    p_spacer_end.paragraph_format.space_after = Pt(0)
    
    tbl_contact = doc.add_table(rows=1, cols=1)
    tbl_contact.alignment = WD_TABLE_ALIGNMENT.CENTER
    tbl_contact.columns[0].width = Inches(7.0)
    c_contact = tbl_contact.cell(0, 0)
    set_cell_background(c_contact, "F1F5F9")
    set_card_borders(c_contact, "94A3B8")
    set_cell_margins(c_contact, top=80, bottom=80, left=120, right=120)
    
    pc = c_contact.paragraphs[0]
    pc.paragraph_format.space_before = Pt(0)
    pc.paragraph_format.space_after = Pt(0)
    rc1 = pc.add_run("🏥 SOPORTE CLÍNICO Y TÉCNICO: ")
    rc1.bold = True
    rc1.font.size = Pt(8.5)
    rc1.font.color.rgb = RGBColor(51, 65, 85)
    rc2 = pc.add_run("Para dudas sobre interacciones de medicamentos, consulte de inmediato a su médico. Para asistencia sobre el funcionamiento de la app MedReminder AI, contacte al administrador de su clínica o al equipo de soporte local.")
    rc2.font.size = Pt(8.5)
    rc2.font.color.rgb = RGBColor(71, 85, 105)

    # Guardar
    output_path = "/Users/4strob0y/Downloads/MedReminderAI/docs/Guia_de_Uso_Rapido_MedReminderAI.docx"
    doc.save(output_path)
    print(f"Guía rápida compacta (exactamente 3 páginas) generada en: {output_path}")

if __name__ == "__main__":
    main()
