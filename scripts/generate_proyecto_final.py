#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Generador Maestro del Documento Oficial de Proyecto Final:
Base de Datos y Arquitectura de Software - MedReminder AI

Genera:
1. docs/Proyecto_Final_Base_de_Datos_y_Arquitectura_MedReminderAI.docx
2. docs/Proyecto_Final_Base_de_Datos_y_Arquitectura_MedReminderAI.html
3. docs/Proyecto_Final_Base_de_Datos_y_Arquitectura_MedReminderAI.pdf
"""

import os
import subprocess
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn

from data_proyecto_final import (
    SEC_1_NOMBRE, SEC_1_NOMBRE_DESC,
    SEC_1_DESC, SEC_1_DESC_TEXT,
    SEC_1_PROBLEMA, SEC_1_PROBLEMA_TEXT,
    SEC_1_MODELO_REL, SEC_1_MODELO_REL_TEXT,
    RELACIONES_TABLA_DATA, DICCIONARIOS,
    SEC_2_NECESIDADES, SEC_2_NECESIDADES_TEXT,
    SEC_2_UBICACION, SEC_2_UBICACION_TEXT,
    SEC_2_AUTOMATIZACION, SEC_2_AUTOMATIZACION_TEXT,
    SEC_2_IMPORT_EXPORT, SEC_2_IMPORT_EXPORT_TEXT,
    SEC_2_SEGURIDAD, SEC_2_SEGURIDAD_TEXT,
    SEC_3_REQUERIMIENTOS, REQUERIMIENTOS_FUNCIONALES, REQUERIMIENTOS_NO_FUNCIONALES,
    SEC_3_JUSTIFICACION, SEC_3_JUSTIFICACION_TEXT,
    SEC_3_DIAGRAMA_ARQ, SEC_3_DIAGRAMA_ARQ_TEXT,
    COMPONENTES_DATA,
    SEC_3_DIAGRAMAS_SECUENCIA, SEC_3_DIAGRAMAS_SECUENCIA_TEXT,
    SEC_4_ESTRUCTURA, SEC_4_ESTRUCTURA_TEXT, JSON_EJEMPLO_BSON,
    SEC_4_CRUD, SEC_4_CRUD_TEXT, CRUD_OPERACIONES,
    SEC_4_SEGURIDAD_MONGODB, SEC_4_SEGURIDAD_MONGODB_TEXT, CODIGO_MONGODB_RBAC,
    SEC_4_CONFIG_SEGURIDAD, SEC_4_CONFIG_SEGURIDAD_PUNTOS,
    SEC_5_METODOS_CONEXION,
    SEC_5_PASOS_CONEXION, PASOS_CONEXION_DETALLE,
    SEC_5_CONSUMO_DATOS, SEC_5_CONSUMO_DATOS_PUNTOS,
    ENDPOINTS_REST_DATA, SEC_5_PROTECCION_DATOS, SEC_5_CONSUMO_ANDROID
)

DOCS_DIR = "/Users/4strob0y/Developer/MedReminderAI/docs"
PORTADA_SRC = os.path.join(DOCS_DIR, "Portada.docx")
DOCX_OUT = os.path.join(DOCS_DIR, "Proyecto_Final_Base_de_Datos_y_Arquitectura_MedReminderAI.docx")
HTML_OUT = os.path.join(DOCS_DIR, "Proyecto_Final_Base_de_Datos_y_Arquitectura_MedReminderAI.html")
PDF_OUT = os.path.join(DOCS_DIR, "Proyecto_Final_Base_de_Datos_y_Arquitectura_MedReminderAI.pdf")

SCREENSHOTS_DIR = os.path.join(DOCS_DIR, "screenshots")

# Palette - MedReminder Design System
C_NAVY = RGBColor(27, 54, 93)       # #1B365D - Primario Institucional
C_TEAL = RGBColor(14, 128, 116)     # #0E8074 - Secundario Clínico
C_ACCENT = RGBColor(217, 83, 79)    # #D9534F - Alertas / Crítico
C_TEXT = RGBColor(40, 44, 52)       # #282C34 - Texto Principal
C_MUTED = RGBColor(100, 116, 139)   # #64748B - Subtítulos / Notas
C_WHITE = RGBColor(255, 255, 255)
C_CODE = RGBColor(30, 41, 59)

HEX_NAVY = "1B365D"
HEX_TEAL = "0E8074"
HEX_ACCENT = "D9534F"
HEX_LIGHT_BG = "F8FAFC"
HEX_CARD_BG = "F0FDF4"
HEX_ALERT_BG = "FEF2F2"
HEX_CODE_BG = "F1F5F9"
HEX_BORDER = "CBD5E1"

def set_cell_background(cell, hex_color):
    tcPr = cell._tc.get_or_add_tcPr()
    shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{hex_color}"/>')
    tcPr.append(shd)

def set_cell_margins(cell, top=120, bottom=120, left=160, right=160):
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

def add_sec_title(doc, title):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(18)
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
    p.paragraph_format.space_before = Pt(12)
    p.paragraph_format.space_after = Pt(4)
    p.paragraph_format.keep_with_next = True
    r = p.add_run(title)
    r.font.name = "Arial"
    r.font.size = Pt(11)
    r.font.bold = True
    r.font.color.rgb = C_TEAL
    return p

def add_subsub_title(doc, title):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(8)
    p.paragraph_format.space_after = Pt(3)
    p.paragraph_format.keep_with_next = True
    r = p.add_run(title)
    r.font.name = "Arial"
    r.font.size = Pt(10)
    r.font.bold = True
    r.font.color.rgb = C_NAVY
    return p

def add_body_p(doc, bold_prefix, text, space_after=6):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(2)
    p.paragraph_format.space_after = Pt(space_after)
    p.paragraph_format.line_spacing = 1.18
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

def add_bullet_p(doc, bold_prefix, text, space_after=4):
    p = doc.add_paragraph(style='List Bullet')
    p.paragraph_format.space_before = Pt(1)
    p.paragraph_format.space_after = Pt(space_after)
    p.paragraph_format.line_spacing = 1.15
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
    set_cell_margins(c, top=130, bottom=130, left=170, right=150)
    set_cell_borders(c, left=("single", "24", "0", border_color),
                        top=("single", "4", "0", HEX_BORDER),
                        bottom=("single", "4", "0", HEX_BORDER),
                        right=("single", "4", "0", HEX_BORDER))
    p = c.paragraphs[0]
    p.paragraph_format.space_after = Pt(2)
    p.paragraph_format.line_spacing = 1.2
    if title:
        rt = p.add_run(title + "\n")
        rt.font.name = "Arial"
        rt.font.size = Pt(10.5)
        rt.font.bold = True
        rt.font.color.rgb = C_NAVY
    for txt, bld, itl, clr in runs:
        r = p.add_run(txt)
        r.font.name = "Arial"
        r.font.size = Pt(9.5)
        r.font.bold = bld
        r.font.italic = itl
        r.font.color.rgb = clr if clr else C_TEXT
    doc.add_paragraph().paragraph_format.space_after = Pt(4)

def add_code_box(doc, title, code_text):
    tbl = doc.add_table(rows=1, cols=1)
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    tbl.autofit = False
    c = tbl.cell(0, 0)
    c.width = Inches(6.8)
    set_cell_background(c, HEX_CODE_BG)
    set_cell_margins(c, top=100, bottom=100, left=140, right=140)
    set_cell_borders(c, left=("single", "20", "0", HEX_TEAL),
                        top=("single", "4", "0", HEX_BORDER),
                        bottom=("single", "4", "0", HEX_BORDER),
                        right=("single", "4", "0", HEX_BORDER))
    p = c.paragraphs[0]
    p.paragraph_format.space_after = Pt(2)
    p.paragraph_format.line_spacing = 1.1
    if title:
        rt = p.add_run(title + "\n")
        rt.font.name = "Arial"
        rt.font.size = Pt(9.5)
        rt.font.bold = True
        rt.font.color.rgb = C_NAVY
    r = p.add_run(code_text)
    r.font.name = "Consolas"
    r.font.size = Pt(8.5)
    r.font.color.rgb = C_CODE
    doc.add_paragraph().paragraph_format.space_after = Pt(4)

def add_styled_table(doc, headers, data, col_widths, alignments=None):
    rows_cnt = len(data) + 1
    cols_cnt = len(headers)
    tbl = doc.add_table(rows=rows_cnt, cols=cols_cnt)
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    tbl.autofit = False

    # Header Row
    hdr_row = tbl.rows[0]
    for i, h in enumerate(headers):
        c = hdr_row.cells[i]
        c.width = col_widths[i]
        set_cell_background(c, HEX_NAVY)
        set_cell_margins(c, top=90, bottom=90, left=110, right=110)
        set_cell_borders(c, top=("single", "6", "0", HEX_NAVY),
                            bottom=("single", "12", "0", HEX_TEAL),
                            left=("none", "0", "0", "auto"),
                            right=("none", "0", "0", "auto"))
        p = c.paragraphs[0]
        p.paragraph_format.space_after = Pt(0)
        if alignments and i < len(alignments):
            p.alignment = alignments[i]
        else:
            p.alignment = WD_ALIGN_PARAGRAPH.LEFT
        r = p.add_run(h)
        r.font.name = "Arial"
        r.font.size = Pt(9)
        r.font.bold = True
        r.font.color.rgb = C_WHITE

    # Data Rows
    for r_idx, row_data in enumerate(data):
        row = tbl.rows[r_idx + 1]
        bg_col = HEX_LIGHT_BG if (r_idx % 2 == 1) else "FFFFFF"
        for c_idx, val in enumerate(row_data):
            c = row.cells[c_idx]
            c.width = col_widths[c_idx]
            set_cell_background(c, bg_col)
            set_cell_margins(c, top=70, bottom=70, left=100, right=100)
            set_cell_borders(c, top=("single", "4", "0", HEX_BORDER),
                                bottom=("single", "4", "0", HEX_BORDER),
                                left=("none", "0", "0", "auto"),
                                right=("none", "0", "0", "auto"))
            p = c.paragraphs[0]
            p.paragraph_format.space_after = Pt(0)
            p.paragraph_format.line_spacing = 1.15
            if alignments and c_idx < len(alignments):
                p.alignment = alignments[c_idx]
            else:
                p.alignment = WD_ALIGN_PARAGRAPH.LEFT
            r = p.add_run(str(val))
            r.font.name = "Arial"
            r.font.size = Pt(8.5)
            r.font.color.rgb = C_TEXT

    doc.add_paragraph().paragraph_format.space_after = Pt(6)

def add_image_box(doc, img_path, caption, width=Inches(3.2)):
    if not os.path.exists(img_path):
        return
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_before = Pt(6)
    p.paragraph_format.space_after = Pt(2)
    p.add_run().add_picture(img_path, width=width)
    
    p_cap = doc.add_paragraph()
    p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_cap.paragraph_format.space_after = Pt(6)
    r = p_cap.add_run(caption)
    r.font.name = "Arial"
    r.font.size = Pt(8.5)
    r.font.italic = True
    r.font.color.rgb = C_MUTED

# ==============================================================================
# CONSTRUCCIÓN DEL DOCUMENTO DOCX A PARTIR DE PORTADA.DOCX
# ==============================================================================

print("Cargando plantilla de portada oficial...")
doc = docx.Document(PORTADA_SRC)

# Actualizar título del trabajo en P9
p9 = doc.paragraphs[9]
p9.text = "PROYECTO FINAL: MODELO DE BASE DE DATOS Y ARQUITECTURA DE SOFTWARE\nMedReminder AI: Sistema Inteligente de Gestión, Supervisión Clínica y Recordatorio Farmacológico"
for r in p9.runs:
    r.font.bold = True
    r.font.size = Pt(13)
    r.font.color.rgb = C_NAVY

# Actualizar fecha en P24
p24 = doc.paragraphs[24]
p24.text = "SANTA MARÍA ATARASQUILLO, LERMA ESTADO DE MÉXICO. NOVIEMBRE 2026"

# Salto de página para iniciar el contenido formal
doc.add_page_break()

# Introducción / Resumen Ejecutivo
add_sec_title(doc, "RESUMEN EJECUTIVO DEL PROYECTO")
add_clean_box(doc, "MedReminder AI — Salud Digital y Adherencia Farmacológica", [
    ("El presente documento técnico integra la especificación formal del modelo de datos relacional y no relacional, "
     "los requerimientos de ingeniería de software, la justificación de la arquitectura distribuida multicapa y las "
     "estrategias de seguridad, conexión y consumo en la nube para el sistema ", False, False, C_TEXT),
    ("MedReminder AI", True, False, C_NAVY),
    (". Diseñado bajo una filosofía de accesibilidad extrema para adultos mayores y supervisión reactiva para cuidadores familiares, "
     "el sistema articula aplicaciones nativas Android, microservicios en FastAPI, persistencia políglota (MySQL + MongoDB) e inteligencia "
     "artificial clínica local.", False, False, C_TEXT)
], border_color=HEX_NAVY, bg_color=HEX_CARD_BG)

# ==============================================================================
# PUNTOS 1.0 A 1.4
# ==============================================================================
add_sec_title(doc, "1.0 NOMBRE DEL PROYECTO")
add_body_p(doc, "Nombre Oficial: ", SEC_1_NOMBRE_DESC)

add_sec_title(doc, "1.1 DESCRIPCIÓN DEL PROYECTO")
for p_text in SEC_1_DESC_TEXT.split("\n\n"):
    add_body_p(doc, "", p_text)

add_sec_title(doc, "1.2 PLANTEAMIENTO DEL PROBLEMA")
for p_text in SEC_1_PROBLEMA_TEXT.split("\n\n"):
    add_body_p(doc, "", p_text)

add_sec_title(doc, "1.3 MODELO RELACIONAL")
for p_text in SEC_1_MODELO_REL_TEXT.split("\n\n"):
    add_body_p(doc, "", p_text)

add_sub_title(doc, "Tabla de Relaciones, Cardinalidades e Integridad Referencial")
hdrs_rel = ["Entidades Vinculadas", "Cardinalidad", "Descripción del Vínculo", "Regla de Cascada"]
widths_rel = [Inches(1.8), Inches(1.3), Inches(2.5), Inches(1.2)]
add_styled_table(doc, hdrs_rel, RELACIONES_TABLA_DATA, widths_rel)

add_sub_title(doc, "Estructura Esquemática del Modelo Relacional")
diagrama_ascii = (
    "+-----------------------+\n"
    "|        usuario        |\n"
    "+-----------------------+\n"
    "| PK  id_usuario        |<-------+\n"
    "|     nombre_completo   |        |\n"
    "|     correo (UQ)       |        |\n"
    "|     password_hash     |        |\n"
    "|     fecha_nacimiento  |        |\n"
    "|     rol               |        |\n"
    "+-----------------------+        |\n"
    "       | 1             1 |       |\n"
    "       | N             N |       |\n"
    "+-------------------+  +--------------------+  +---------------------+\n"
    "|  contacto_apoyo   |  |   alergia_usuario  |  |   alerta_cuidador   |\n"
    "+-------------------+  +--------------------+  +---------------------+\n"
    "| PK id_contacto    |  | PK id_alergia      |  | PK id_alerta        |\n"
    "| FK id_usuario     |  | FK id_usuario      |  | FK id_usuario       |\n"
    "|    nombre_completo|  |    sustancia       |  |    tipo_alerta      |\n"
    "|    telefono       |  |    severidad       |  |    mensaje          |\n"
    "+-------------------+  +--------------------+  +---------------------+\n"
    "       |\n"
    "       | (usuario 1:N medicamento)\n"
    "       v\n"
    "+-----------------------+\n"
    "|      medicamento      |\n"
    "+-----------------------+\n"
    "| PK  id_medicamento    |<-------------------+\n"
    "| FK  id_usuario        |                    |\n"
    "|     nombre            |                    |\n"
    "|     dosis             |                    |\n"
    "|     cantidad_stock    |                    |\n"
    "|     es_critico        |                    |\n"
    "+-----------------------+                    |\n"
    "       | 1                                   |\n"
    "       | N                                   |\n"
    "       v                                     |\n"
    "+-----------------------+                    |\n"
    "|      tratamiento      |                    |\n"
    "+-----------------------+                    |\n"
    "| PK  id_tratamiento    |                    |\n"
    "| FK  id_medicamento    |                    |\n"
    "|     frecuencia_horas  |                    |\n"
    "|     fecha_inicio      |                    |\n"
    "+-----------------------+                    |\n"
    "       | 1                                   |\n"
    "       | N                                   |\n"
    "       v                                     |\n"
    "+-----------------------+                    |\n"
    "|      recordatorio     |                    |\n"
    "+-----------------------+                    |\n"
    "| PK  id_recordatorio   |<----+              |\n"
    "| FK  id_tratamiento    |     |              |\n"
    "|     hora_programada   |     |              |\n"
    "|     estado            |     |              |\n"
    "+-----------------------+     |              |\n"
    "       | 1                    |              |\n"
    "       | N                    |              |\n"
    "       v                      |              |\n"
    "+-----------------------+     |              |\n"
    "|     historial_toma    |     |              |\n"
    "+-----------------------+     |              |\n"
    "| PK  id_historial      |     |              |\n"
    "| FK  id_recordatorio   |-----+              |\n"
    "|     fecha_accion      |                    |\n"
    "|     estado_final      |                    |\n"
    "+-----------------------+                    +\n"
)
add_code_box(doc, "Diagrama Entidad-Relación (Modelo Lógico-Físico MySQL)", diagrama_ascii)

add_sec_title(doc, "1.4 DICCIONARIO DE DATOS")
add_body_p(doc, "", "A continuación se presentan las especificaciones técnicas completas de las 8 tablas de la base de datos relacional de MedReminder AI:")

col_w_dic = [Inches(1.3), Inches(0.8), Inches(1.1), Inches(0.5), Inches(0.4), Inches(0.9), Inches(1.8)]
hdrs_dic = ["Campo", "Tipo", "Longitud", "Clave", "Nulo", "Default", "Descripción"]

for tbl_name, campos in DICCIONARIOS.items():
    add_sub_title(doc, f"Tabla: {tbl_name.upper()}")
    add_styled_table(doc, hdrs_dic, campos, col_w_dic)

# ==============================================================================
# PUNTOS 2.0 A 2.4
# ==============================================================================
doc.add_page_break()
add_sec_title(doc, "2.0 DEFINICIÓN DE LAS NECESIDADES DE INFORMACIÓN")
for p_text in SEC_2_NECESIDADES_TEXT.split("\n\n"):
    add_body_p(doc, "", p_text)

add_sec_title(doc, "2.1 DESCRIPCIÓN DE LA UBICACIÓN Y CARACTERÍSTICAS DE LOS DATOS")
for p_text in SEC_2_UBICACION_TEXT.split("\n\n"):
    add_body_p(doc, "", p_text)

add_sec_title(doc, "2.2 DESCRIPCIÓN DE LAS TAREAS Y SUS TÉCNICAS DE AUTOMATIZACIÓN")
for p_text in SEC_2_AUTOMATIZACION_TEXT.split("\n\n"):
    add_body_p(doc, "", p_text)

add_sec_title(doc, "2.3 DESCRIPCIÓN DEL MÉTODO DE IMPORTACIÓN Y EXPORTACIÓN")
for p_text in SEC_2_IMPORT_EXPORT_TEXT.split("\n\n"):
    add_body_p(doc, "", p_text)

add_sec_title(doc, "2.4 LINEAMIENTOS DE SEGURIDAD QUE SE APLICARÁN EN LA BASE DE DATOS")
for p_text in SEC_2_SEGURIDAD_TEXT.split("\n\n"):
    add_body_p(doc, "", p_text)

# ==============================================================================
# PUNTOS 3.0 A 3.4
# ==============================================================================
doc.add_page_break()
add_sec_title(doc, "3.0 REQUERIMIENTOS FUNCIONALES Y NO FUNCIONALES DE DESARROLLO DE SOFTWARE")

add_sub_title(doc, "Requerimientos Funcionales (RF)")
hdrs_rf = ["Código", "Nombre de la Funcionalidad", "Descripción y Reglas de Negocio"]
widths_rf = [Inches(1.0), Inches(2.2), Inches(3.6)]
add_styled_table(doc, hdrs_rf, REQUERIMIENTOS_FUNCIONALES, widths_rf)

add_sub_title(doc, "Requerimientos No Funcionales (RNF)")
hdrs_rnf = ["Código", "Criterio de Calidad", "Métrica de Aceptación / Restricción"]
widths_rnf = [Inches(1.0), Inches(2.2), Inches(3.6)]
add_styled_table(doc, hdrs_rnf, REQUERIMIENTOS_NO_FUNCIONALES, widths_rnf)

add_sec_title(doc, "3.1 JUSTIFICACIÓN DE LA ARQUITECTURA SELECCIONADA")
for p_text in SEC_3_JUSTIFICACION_TEXT.split("\n\n"):
    add_body_p(doc, "", p_text)

add_sec_title(doc, "3.2 DIAGRAMA DE ARQUITECTURA DE SOFTWARE")
add_body_p(doc, "", SEC_3_DIAGRAMA_ARQ_TEXT)

diagrama_arq_ascii = (
    "+=============================================================================+\n"
    "|                  1. CAPA DE PRESENTACIÓN / CLIENTE MÓVIL                    |\n"
    "|  - Dispositivo Android (Smartphones pacientes y cuidadores)                 |\n"
    "|  - UI Reactiva: Jetpack Compose (Kotlin) con Arquitectura MVVM              |\n"
    "|  - Persistencia Local Offline: Room SQLite Cache & DataStore                |\n"
    "|  - Planificador Determinista: Android Native AlarmManager (Exact Alarms)    |\n"
    "+=============================================================================+\n"
    "                                      | HTTPS / TLS 1.3 (JSON Payloads)\n"
    "                                      v\n"
    "+=============================================================================+\n"
    "|               2. CAPA DE SEGURIDAD PERIMETRAL Y API GATEWAY                 |\n"
    "|  - Reverse Proxy Nginx / SSL Termination (Túnel Cifrado Seguro)             |\n"
    "|  - OAuth2 Password Bearer / Tokens JWT con expiración estricta              |\n"
    "|  - Middleware de Seguridad: CORS estricto, Rate Limiting y Sanitización     |\n"
    "+=============================================================================+\n"
    "                                      |\n"
    "                                      v\n"
    "+=============================================================================+\n"
    "|            3. CAPA DE LÓGICA DE NEGOCIO Y SERVICIOS (FASTAPI)               |\n"
    "|  - Router de Autenticación (`/auth`) y Gestión de Pacientes                 |\n"
    "|  - Router de Botiquín y Farmacovigilancia (`/medicamentos`)                 |\n"
    "|  - Motor de Generación y Validación de Tomas (`/recordatorios`)             |\n"
    "|  - Sistema de Alertas y Supervisión de Cuidadores (`/alertas`)              |\n"
    "|  - Esquemas de Validación y Serialización Estricta con Pydantic             |\n"
    "+=============================================================================+\n"
    "               |                                            |\n"
    "               v (Llamadas asíncronas HTTP)                 v (Pool de hilos)\n"
    "+-----------------------------+            +----------------------------------+\n"
    "| 4. CAPA DE IA CLÍNICA LOCAL |            | 5. CAPA DE PERSISTENCIA POLÍGLOTA|\n"
    "|  - Contenedor Ollama Runner |            |                                  |\n"
    "|  - Modelo: `medi-clinico`   |            |  [MySQL 8.4 Server - ACID]       |\n"
    "|  - Visión Multimodal OCR    |            |  - Usuarios, Medicamentos, Tomas |\n"
    "|  - Asistente Clínico Local  |            |  - Integridad Referencial 3NF    |\n"
    "+-----------------------------+            |                                  |\n"
    "                                           |  [MongoDB 7.0 - NoSQL BSON]      |\n"
    "                                           |  - `eventos_clinicos` (Inmutable)|\n"
    "                                           |  - Auditoría de Accesos & BI     |\n"
    "+=============================================================================+\n"
)
add_code_box(doc, "Topología y Capas de la Arquitectura de Software", diagrama_arq_ascii)

add_sec_title(doc, "3.3 CARACTERÍSTICAS Y FUNCIONES DE LOS COMPONENTES")
hdrs_comp = ["Componente del Sistema", "Tecnología / Framework", "Responsabilidad Funcional en la Arquitectura"]
widths_comp = [Inches(1.8), Inches(1.8), Inches(3.2)]
add_styled_table(doc, hdrs_comp, COMPONENTES_DATA, widths_comp)

add_sec_title(doc, "3.4 DIAGRAMAS NECESARIOS DE ACUERDO A LA ARQUITECTURA SELECCIONADA")
add_body_p(doc, "", SEC_3_DIAGRAMAS_SECUENCIA_TEXT)

add_sub_title(doc, "A. Diagrama de Secuencia: Flujo de Toma de Medicamento Crítico y Alerta Reactiva")
secuencia_ascii = (
    "Paciente (App Android)     Backend (FastAPI)     MySQL 8.4      MongoDB 7.0     Cuidador (Familiar)\n"
    "      |                          |                  |               |                    |\n"
    "      |--- 1. Alarma Sonora ---->|                  |               |                    |\n"
    "      |    (AlarmManager local)  |                  |               |                    |\n"
    "      |                          |                  |               |                    |\n"
    "      |--- 2. Toca 'Posponer' -->|                  |               |                    |\n"
    "      |    (POST /accion)        |                  |               |                    |\n"
    "      |                          |-- 3. Verifica -->|               |                    |\n"
    "      |                          |      criticidad  |               |                    |\n"
    "      |                          |<- es_critico=TRUE|               |                    |\n"
    "      |                          |                  |               |                    |\n"
    "      |                          |-- 4. Registra -->|               |                    |\n"
    "      |                          |      en historial|               |                    |\n"
    "      |                          |                  |               |                    |\n"
    "      |                          |-- 5. Inserta alerta ------------>|                    |\n"
    "      |                          |      en tabla alerta_cuidador    |                    |\n"
    "      |                          |                  |               |                    |\n"
    "      |                          |-- 6. Despacha evento asíncrono ->|                    |\n"
    "      |                          |      a colección eventos_clinicos|                    |\n"
    "      |                          |                  |               |                    |\n"
    "      |                          |-- 7. Dispara Notificación Push ---------------------->|\n"
    "      |                          |      ¡ALERTA: Fármaco crítico pospuesto!              |\n"
    "      |<- 8. 200 OK (Reprograma)-|                  |               |                    |\n"
)
add_code_box(doc, "Secuencia de Comunicación entre Componentes", secuencia_ascii)

add_sub_title(doc, "B. Diagrama de Despliegue en Contenedores Docker (Docker Compose)")
despliegue_ascii = (
    "+-----------------------------------------------------------------------------+\n"
    "|                          HOST DOCKER (Servidor / VPS)                       |\n"
    "|                                                                             |\n"
    "|  +-----------------------------------------------------------------------+  |\n"
    "|  |                      RED BRIDGE (medreminder-net)                     |  |\n"
    "|  |                                                                       |  |\n"
    "|  |  +------------------------+             +--------------------------+  |  |\n"
    "|  |  | Contenedor: api        |             | Contenedor: mysql        |  |  |\n"
    "|  |  | Image: python:3.12-slim|             | Image: mysql:8.4         |  |  |\n"
    "|  |  | Port: 8000:8000        |<----------->| Port: 3306 (red interna) |  |  |\n"
    "|  |  | FastAPI ASGI Server    |             | Vol: mysql_data          |  |  |\n"
    "|  |  +------------------------+             +--------------------------+  |  |\n"
    "|  |              |                                        |               |  |\n"
    "|  |              |                          +--------------------------+  |  |\n"
    "|  |              |                          | Contenedor: mongo        |  |  |\n"
    "|  |              +------------------------->| Image: mongo:7.0         |  |  |\n"
    "|  |              |                          | Port: 27017 (red interna)|  |  |\n"
    "|  |              v                          | Vol: mongo_data          |  |  |\n"
    "|  |  +------------------------+             +--------------------------+  |  |\n"
    "|  |  | Contenedor: ollama     |                                           |  |\n"
    "|  |  | Image: ollama/ollama   |                                           |  |\n"
    "|  |  | Modelo: medi-clinico   |                                           |  |\n"
    "|  |  +------------------------+                                           |  |\n"
    "|  +-----------------------------------------------------------------------+  |\n"
    "+-----------------------------------------------------------------------------+\n"
)
add_code_box(doc, "Topología de Despliegue Contenerizado Docker Compose", despliegue_ascii)

add_sub_title(doc, "C. Evidencia Visual de Componentes en la Aplicación Android")
add_body_p(doc, "", "A continuación se presentan capturas de pantalla reales del cliente móvil en funcionamiento:")

img_hoy = os.path.join(SCREENSHOTS_DIR, "02_hoy.png")
img_botiquin = os.path.join(SCREENSHOTS_DIR, "04_botiquin.png")
img_apoyo = os.path.join(SCREENSHOTS_DIR, "07_salud_apoyo.png")
img_companion = os.path.join(SCREENSHOTS_DIR, "06_medi_companion.png")

if os.path.exists(img_hoy):
    add_image_box(doc, img_hoy, "Figura 1: Pantalla Principal 'Hoy' — Agenda de tomas programadas, color de comprimido y racha de adherencia.", width=Inches(2.5))
if os.path.exists(img_botiquin):
    add_image_box(doc, img_botiquin, "Figura 2: Módulo 'Botiquín' — Inventario de medicamentos, stock disponible y etiquetas de criticidad.", width=Inches(2.5))
if os.path.exists(img_apoyo):
    add_image_box(doc, img_apoyo, "Figura 3: Módulo 'Salud y Apoyo' — Directorio de cuidadores y panel reactivo de alertas de emergencia.", width=Inches(2.5))
if os.path.exists(img_companion):
    add_image_box(doc, img_companion, "Figura 4: Asistente Clínico IA 'Medi Companion' — Interacción médica contextualizada con Ollama.", width=Inches(2.5))

# ==============================================================================
# PUNTOS 4.0 A 4.3 (MONGODB NO RELACIONAL)
# ==============================================================================
doc.add_page_break()
add_sec_title(doc, "4.0 ESTRUCTURA DE ALMACENAMIENTO MEDIANTE ELEMENTOS NO RELACIONALES")
for p_text in SEC_4_ESTRUCTURA_TEXT.split("\n\n"):
    add_body_p(doc, "", p_text)

add_sub_title(doc, "Ejemplo Real de un Documento BSON en MedReminder AI (`eventos_clinicos`)")
add_code_box(doc, "Documento BSON: Evento Clínico de Alerta por Medicamento Crítico", JSON_EJEMPLO_BSON)

add_sec_title(doc, "4.1 MÉTODOS DE MANIPULACIÓN DE DATOS (CRUD) EN MONGODB")
add_body_p(doc, "", SEC_4_CRUD_TEXT)

for op in CRUD_OPERACIONES:
    add_sub_title(doc, f"{op['letra']}. {op['titulo']}")
    add_body_p(doc, "Descripción del Método: ", op['explicacion'])
    add_code_box(doc, f"Sintaxis Oficial mongosh ({op['letra']})", op['mongosh'])
    add_code_box(doc, f"Implementación en Python con PyMongo ({op['letra']})", op['pymongo'])

add_sec_title(doc, "4.2 MÉTODOS O SINTAXIS RELACIONADOS CON LA SEGURIDAD Y NIVELES DE ACCESO EN MONGODB EN LA NUBE")
for p_text in SEC_4_SEGURIDAD_MONGODB_TEXT.split("\n\n"):
    add_body_p(doc, "", p_text)

add_code_box(doc, "Script de Creación de Usuarios y Asignación de Roles (mongosh)", CODIGO_MONGODB_RBAC)

add_sec_title(doc, "4.3 CONFIGURACIÓN DE SEGURIDAD EN MONGODB DE ACUERDO AL PROYECTO")
add_body_p(doc, "", "En concordancia con los requerimientos específicos de la plataforma, se documenta la configuración aplicada a cada uno de los puntos clave:")

hdrs_seg_puntos = ["Punto de Seguridad", "Estrategia e Implementación Técnica en MedReminder AI"]
widths_seg_puntos = [Inches(2.2), Inches(4.6)]
add_styled_table(doc, hdrs_seg_puntos, SEC_4_CONFIG_SEGURIDAD_PUNTOS, widths_seg_puntos)

# ==============================================================================
# PUNTOS 5.0 A 5.2
# ==============================================================================
doc.add_page_break()
add_sec_title(doc, "5.0 MÉTODOS DE CONEXIÓN DE BASE DE DATOS EN LA NUBE Y LAS APLICACIONES")

add_sec_title(doc, "5.1 DESCRIBE LOS PASOS PARA ESTABLECER LA CONEXIÓN DE LA BASE DE DATOS CON LA APLICACIÓN")
hdrs_pasos = ["Paso / Fase", "Acción Técnica Detallada e Implementación en el Backend"]
widths_pasos = [Inches(2.0), Inches(4.8)]
add_styled_table(doc, hdrs_pasos, PASOS_CONEXION_DETALLE, widths_pasos)

add_sub_title(doc, "Código Fuente Real de Conexión y Pooling en FastAPI (`app/core/mongo.py`)")
codigo_fastapi_mongo = (
    "from concurrent.futures import ThreadPoolExecutor\n"
    "from datetime import datetime, timezone\n"
    "from typing import Any\n"
    "from pymongo import MongoClient\n"
    "from app.core.config import settings\n\n"
    "_mongo_client: MongoClient | None = None\n"
    "_mongo_executor = ThreadPoolExecutor(max_workers=2, thread_name_prefix=\"mongo-event\")\n\n"
    "def get_mongo_client() -> MongoClient:\n"
    "    \"\"\"Devuelve una instancia compartida (pooled) de MongoClient con timeouts seguros.\"\"\"\n"
    "    global _mongo_client\n"
    "    if _mongo_client is None:\n"
    "        _mongo_client = MongoClient(\n"
    "            settings.mongo_url,\n"
    "            serverSelectionTimeoutMS=1200,\n"
    "            connectTimeoutMS=1200,\n"
    "            socketTimeoutMS=1500,\n"
    "            maxPoolSize=16,\n"
    "        )\n"
    "    return _mongo_client\n\n"
    "def registrar_evento_mongo(evento: str, id_usuario: int | None = None, detalle: dict | None = None) -> bool:\n"
    "    \"\"\"Despacha de forma no bloqueante (0 ms de latencia en la API) el evento clínico.\"\"\"\n"
    "    documento = {\n"
    "        \"evento\": evento,\n"
    "        \"id_usuario\": id_usuario,\n"
    "        \"detalle\": detalle or {},\n"
    "        \"timestamp\": datetime.now(timezone.utc),\n"
    "    }\n"
    "    _mongo_executor.submit(_insert_mongo_doc, documento)\n"
    "    return True\n"
)
add_code_box(doc, "Implementación de Connection Pooling y Despacho Asíncrono en FastAPI", codigo_fastapi_mongo)

add_sec_title(doc, "5.2 MÉTODOS DE CONSUMO DE DATOS EN LA NUBE")

for sec_c in SEC_5_CONSUMO_DATOS_PUNTOS:
    add_sub_title(doc, sec_c["subtitulo"])
    for p_t in sec_c["contenido"].split("\n\n"):
        add_body_p(doc, "", p_t)

add_sub_title(doc, "Catálogo de Servicios Web Desarrollados (Endpoints REST)")
hdrs_ep = ["Método", "Ruta del Endpoint", "Seguridad", "Descripción del Intercambio de Información"]
widths_ep = [Inches(0.9), Inches(2.2), Inches(1.1), Inches(2.6)]
add_styled_table(doc, hdrs_ep, ENDPOINTS_REST_DATA, widths_ep)

add_sub_title(doc, "Importancia de Proteger la Información Almacenada en Servicios de Nube")
for p_t in SEC_5_PROTECCION_DATOS.split("\n\n"):
    add_body_p(doc, "", p_t)

add_sub_title(doc, "Consumo de Datos Mediante Servicios Web en la Aplicación Móvil Android")
for p_t in SEC_5_CONSUMO_ANDROID.split("\n\n"):
    add_body_p(doc, "", p_t)

# Conclusión
add_sec_title(doc, "CONCLUSIÓN Y LECCIONES APRENDIDAS")
add_clean_box(doc, "Síntesis del Proyecto Integrador", [
    ("La consolidación arquitectónica de MedReminder AI demuestra que la integración de una base de datos relacional "
     "normalizada (MySQL) y una base de datos no relacional orientada a documentos (MongoDB) resuelve de manera elegante y "
     "eficiente las exigencias contradictorias de un sistema de salud moderno: por un lado, la ", False, False, C_TEXT),
    ("necesidad innegociable de consistencia transaccional y reglas de negocio estrictas ", True, False, C_NAVY),
    ("en las recetas de los pacientes, y por el otro, la ", False, False, C_TEXT),
    ("velocidad, flexibilidad y tolerancia a fallos ", True, False, C_TEAL),
    ("para la telemetría masiva y la auditoría clínica inmutable. Combinado con una aplicación móvil nativa con alarmas deterministas "
     "y un modelo de IA médica local, el proyecto entrega una solución de alto impacto humano que devuelve la tranquilidad al adulto mayor "
     "y a sus seres queridos.", False, False, C_TEXT)
], border_color=HEX_TEAL, bg_color=HEX_LIGHT_BG)

print(f"Guardando documento DOCX en: {DOCX_OUT}")
doc.save(DOCX_OUT)
print("¡Documento DOCX generado con éxito!")

# ==============================================================================
# GENERACIÓN DE HTML Y COMPILACIÓN A PDF VÍA HEADLESS CHROME
# ==============================================================================
print("Construyendo versión HTML y compilando a PDF...")

html_content = f"""<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<title>Proyecto Final: Base de Datos y Arquitectura de Software - MedReminder AI</title>
<style>
  @page {{
    size: letter portrait;
    margin: 1.8cm 1.6cm 1.8cm 1.6cm;
    @bottom-center {{
      content: counter(page);
      font-family: Arial, sans-serif;
      font-size: 9pt;
      color: #64748B;
    }}
  }}
  body {{
    font-family: Arial, -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
    color: #282C34;
    line-height: 1.45;
    font-size: 10pt;
    margin: 0;
    padding: 0;
  }}
  .portada {{
    page-break-after: always;
    text-align: center;
    padding-top: 2cm;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    height: 90vh;
  }}
  .portada-logos {{
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 2cm;
  }}
  .portada-logos img {{
    height: 60px;
  }}
  .portada h2 {{
    color: #1B365D;
    font-size: 15pt;
    margin: 4px 0;
    text-transform: uppercase;
    font-weight: 700;
  }}
  .portada h3 {{
    color: #0E8074;
    font-size: 12pt;
    margin: 4px 0 1.5cm 0;
    font-weight: 600;
  }}
  .portada-box {{
    background: #F8FAFC;
    border-left: 5px solid #1B365D;
    padding: 16px;
    margin: 1cm auto;
    max-width: 85%;
    text-align: center;
    border-radius: 4px;
    box-shadow: 0 1px 3px rgba(0,0,0,0.05);
  }}
  .portada-box h1 {{
    color: #1B365D;
    font-size: 14pt;
    margin: 0 0 8px 0;
    text-transform: uppercase;
  }}
  .portada-box p {{
    color: #0E8074;
    font-size: 11pt;
    font-weight: bold;
    margin: 0;
  }}
  .portada-info {{
    font-size: 9.5pt;
    color: #334155;
    margin-top: 1cm;
    line-height: 1.6;
  }}
  .portada-footer {{
    font-size: 9pt;
    color: #64748B;
    margin-top: auto;
    font-weight: bold;
  }}
  h1.sec-title {{
    color: #1B365D;
    font-size: 13pt;
    border-bottom: 2px solid #0E8074;
    padding-bottom: 4px;
    margin-top: 24px;
    margin-bottom: 12px;
    page-break-after: avoid;
    text-transform: uppercase;
  }}
  h2.sub-title {{
    color: #0E8074;
    font-size: 11pt;
    margin-top: 18px;
    margin-bottom: 8px;
    page-break-after: avoid;
  }}
  p {{
    margin: 0 0 10px 0;
    text-align: justify;
  }}
  .callout {{
    background: #F0FDF4;
    border-left: 4px solid #0E8074;
    border-radius: 4px;
    padding: 12px 16px;
    margin: 14px 0;
    box-shadow: 0 1px 3px rgba(0,0,0,0.03);
  }}
  .callout h4 {{
    margin: 0 0 6px 0;
    color: #1B365D;
    font-size: 10.5pt;
  }}
  table {{
    width: 100%;
    border-collapse: collapse;
    margin: 14px 0 18px 0;
    font-size: 8.5pt;
    page-break-inside: avoid;
  }}
  th {{
    background-color: #1B365D;
    color: #FFFFFF;
    font-weight: bold;
    text-align: left;
    padding: 7px 9px;
    border: 1px solid #1B365D;
  }}
  td {{
    padding: 6px 8px;
    border: 1px solid #E2E8F0;
    vertical-align: top;
  }}
  tr:nth-child(even) td {{
    background-color: #F8FAFC;
  }}
  pre {{
    background-color: #F1F5F9;
    border-left: 4px solid #0E8074;
    padding: 10px 14px;
    font-family: "Consolas", "Courier New", monospace;
    font-size: 8pt;
    color: #1E293B;
    overflow-x: auto;
    white-space: pre-wrap;
    border-radius: 3px;
    margin: 12px 0 16px 0;
  }}
  .img-container {{
    text-align: center;
    margin: 16px 0;
    page-break-inside: avoid;
  }}
  .img-container img {{
    max-width: 48%;
    border: 1px solid #CBD5E1;
    border-radius: 6px;
    box-shadow: 0 2px 4px rgba(0,0,0,0.08);
  }}
  .img-caption {{
    font-size: 8pt;
    color: #64748B;
    font-style: italic;
    margin-top: 6px;
  }}
  .page-break {{
    page-break-after: always;
  }}
</style>
</head>
<body>

<!-- PORTADA OFICIAL -->
<div class="portada">
  <div class="portada-logos">
    <img src="logo_utvt.png" alt="UTVT">
    <img src="logo_edomex.png" alt="Gobierno Estado de México">
  </div>
  <div>
    <h2>Universidad Tecnológica del Valle de Toluca</h2>
    <h3>Dirección de Tecnologías de la Información y Comunicación</h3>
    <p style="text-align:center; font-weight:bold; color:#1B365D;">TÉCNICO SUPERIOR UNIVERSITARIO EN DESARROLLO DE SOFTWARE MULTIPLATAFORMA</p>
    
    <div class="portada-box">
      <h1>PROYECTO FINAL: MODELO DE BASE DE DATOS Y ARQUITECTURA DE SOFTWARE</h1>
      <p>MedReminder AI: Sistema Inteligente de Gestión y Supervisión Farmacológica</p>
    </div>
    
    <div class="portada-info">
      <p style="text-align:center;"><strong>Docente:</strong> Ing. Hector Velazquez Estrada</p>
      <p style="text-align:center;"><strong>Grupo:</strong> DSM - 53 &nbsp;&nbsp;|&nbsp;&nbsp; <strong>Equipo:</strong> 5 (MedReminder AI)</p>
      <br>
      <p style="text-align:center;"><strong>Presentan:</strong></p>
      <p style="text-align:center;">
        222410897 – Gutierrez Ugalde Samuel<br>
        222410935 – Nava Garcia Rodrigo<br>
        222411182 – Castillo Ramirez Nahum Yabet<br>
        222410915 – Ramirez Romero Pablo<br>
        222410899 – Peña Hernandez Alexander
      </p>
    </div>
  </div>
  
  <div class="portada-footer">
    SANTA MARÍA ATARASQUILLO, LERMA ESTADO DE MÉXICO. NOVIEMBRE 2026
  </div>
</div>

<!-- CONTENIDO -->
<h1 class="sec-title">1.0 NOMBRE DEL PROYECTO</h1>
<p><strong>Nombre Oficial:</strong> {SEC_1_NOMBRE_DESC}</p>

<h1 class="sec-title">1.1 DESCRIPCIÓN DEL PROYECTO</h1>
<p>{SEC_1_DESC_TEXT.replace(chr(10)+chr(10), '</p><p>')}</p>

<h1 class="sec-title">1.2 PLANTEAMIENTO DEL PROBLEMA</h1>
<p>{SEC_1_PROBLEMA_TEXT.replace(chr(10)+chr(10), '</p><p>')}</p>

<h1 class="sec-title">1.3 MODELO RELACIONAL</h1>
<p>{SEC_1_MODELO_REL_TEXT.replace(chr(10)+chr(10), '</p><p>')}</p>

<h2 class="sub-title">Tabla de Relaciones, Cardinalidades e Integridad Referencial</h2>
<table>
  <tr>
    <th>Entidades Vinculadas</th><th>Cardinalidad</th><th>Descripción del Vínculo</th><th>Regla Cascada</th>
  </tr>
  {''.join(f'<tr><td><b>{r[0]}</b></td><td>{r[1]}</td><td>{r[2]}</td><td><code>{r[3]}</code></td></tr>' for r in RELACIONES_TABLA_DATA)}
</table>

<h2 class="sub-title">Diagrama Entidad-Relación Lógico-Físico</h2>
<pre>{diagrama_ascii}</pre>

<h1 class="sec-title">1.4 DICCIONARIO DE DATOS</h1>
<p>Especificaciones técnicas detalladas de las 8 tablas de la base de datos relacional MySQL 8.4:</p>
"""

for tbl, rows in DICCIONARIOS.items():
    html_content += f"""
<h2 class="sub-title">Tabla: {tbl.upper()}</h2>
<table>
  <tr>
    <th>Campo</th><th>Tipo</th><th>Longitud</th><th>Clave</th><th>Nulo</th><th>Default</th><th>Descripción</th>
  </tr>
  {''.join(f'<tr><td><b>{c[0]}</b></td><td>{c[1]}</td><td>{c[2]}</td><td>{c[3]}</td><td>{c[4]}</td><td>{c[5]}</td><td>{c[6]}</td></tr>' for c in rows)}
</table>
"""

html_content += f"""
<div class="page-break"></div>

<h1 class="sec-title">2.0 DEFINICIÓN DE LAS NECESIDADES DE INFORMACIÓN</h1>
<p>{SEC_2_NECESIDADES_TEXT.replace(chr(10)+chr(10), '</p><p>')}</p>

<h1 class="sec-title">2.1 DESCRIPCIÓN DE LA UBICACIÓN Y CARACTERÍSTICAS DE LOS DATOS</h1>
<p>{SEC_2_UBICACION_TEXT.replace(chr(10)+chr(10), '</p><p>')}</p>

<h1 class="sec-title">2.2 DESCRIPCIÓN DE LAS TAREAS Y SUS TÉCNICAS DE AUTOMATIZACIÓN</h1>
<p>{SEC_2_AUTOMATIZACION_TEXT.replace(chr(10)+chr(10), '</p><p>')}</p>

<h1 class="sec-title">2.3 DESCRIPCIÓN DEL MÉTODO DE IMPORTACIÓN Y EXPORTACIÓN</h1>
<p>{SEC_2_IMPORT_EXPORT_TEXT.replace(chr(10)+chr(10), '</p><p>')}</p>

<h1 class="sec-title">2.4 LINEAMIENTOS DE SEGURIDAD QUE SE APLICARÁN EN LA BASE DE DATOS</h1>
<p>{SEC_2_SEGURIDAD_TEXT.replace(chr(10)+chr(10), '</p><p>')}</p>

<div class="page-break"></div>

<h1 class="sec-title">3.0 REQUERIMIENTOS FUNCIONALES Y NO FUNCIONALES</h1>
<h2 class="sub-title">Requerimientos Funcionales (RF)</h2>
<table>
  <tr><th>Código</th><th>Nombre de la Funcionalidad</th><th>Descripción y Reglas de Negocio</th></tr>
  {''.join(f'<tr><td><b>{rf[0]}</b></td><td><b>{rf[1]}</b></td><td>{rf[2]}</td></tr>' for rf in REQUERIMIENTOS_FUNCIONALES)}
</table>

<h2 class="sub-title">Requerimientos No Funcionales (RNF)</h2>
<table>
  <tr><th>Código</th><th>Criterio de Calidad</th><th>Métrica de Aceptación / Restricción</th></tr>
  {''.join(f'<tr><td><b>{rnf[0]}</b></td><td><b>{rnf[1]}</b></td><td>{rnf[2]}</td></tr>' for rnf in REQUERIMIENTOS_NO_FUNCIONALES)}
</table>

<h1 class="sec-title">3.1 JUSTIFICACIÓN DE LA ARQUITECTURA SELECCIONADA</h1>
<p>{SEC_3_JUSTIFICACION_TEXT.replace(chr(10)+chr(10), '</p><p>')}</p>

<h1 class="sec-title">3.2 DIAGRAMA DE ARQUITECTURA DE SOFTWARE</h1>
<p>{SEC_3_DIAGRAMA_ARQ_TEXT}</p>
<pre>{diagrama_arq_ascii}</pre>

<h1 class="sec-title">3.3 CARACTERÍSTICAS Y FUNCIONES DE LOS COMPONENTES</h1>
<table>
  <tr><th>Componente del Sistema</th><th>Tecnología / Framework</th><th>Responsabilidad Funcional en la Arquitectura</th></tr>
  {''.join(f'<tr><td><b>{cp[0]}</b></td><td><code>{cp[1]}</code></td><td>{cp[2]}</td></tr>' for cp in COMPONENTES_DATA)}
</table>

<h1 class="sec-title">3.4 DIAGRAMAS DE LA ARQUITECTURA Y EVIDENCIA VISUAL</h1>
<h2 class="sub-title">A. Diagrama de Secuencia: Flujo de Toma de Medicamento Crítico y Alerta al Cuidador</h2>
<pre>{secuencia_ascii}</pre>

<h2 class="sub-title">B. Diagrama de Despliegue en Contenedores Docker Compose</h2>
<pre>{despliegue_ascii}</pre>

<h2 class="sub-title">C. Capturas de Pantalla de la Aplicación Móvil en Funcionamiento</h2>
<div class="img-container">
  <img src="screenshots/02_hoy.png" alt="Pantalla Hoy">
  <img src="screenshots/04_botiquin.png" alt="Botiquín">
  <p class="img-caption">Figura 1 y 2: Pantalla 'Hoy' con agenda de tomas y Módulo 'Botiquín' con inventario y criticidad.</p>
</div>
<div class="img-container">
  <img src="screenshots/07_salud_apoyo.png" alt="Salud y Apoyo">
  <img src="screenshots/06_medi_companion.png" alt="Medi Companion">
  <p class="img-caption">Figura 3 y 4: Módulo de Cuidadores y Alertas, y Asistente Clínico Inteligente Medi Companion.</p>
</div>

<div class="page-break"></div>

<h1 class="sec-title">4.0 ESTRUCTURA DE ALMACENAMIENTO MEDIANTE ELEMENTOS NO RELACIONALES</h1>
<p>{SEC_4_ESTRUCTURA_TEXT.replace(chr(10)+chr(10), '</p><p>')}</p>

<h2 class="sub-title">Ejemplo Real de un Documento BSON en MedReminder AI</h2>
<pre>{JSON_EJEMPLO_BSON}</pre>

<h1 class="sec-title">4.1 MÉTODOS DE MANIPULACIÓN DE DATOS (CRUD) EN MONGODB</h1>
<p>{SEC_4_CRUD_TEXT}</p>
"""

for op in CRUD_OPERACIONES:
    html_content += f"""
<h2 class="sub-title">{op['letra']}. {op['titulo']}</h2>
<p><strong>Descripción:</strong> {op['explicacion']}</p>
<pre><b>// Sintaxis mongosh:</b><br>{op['mongosh']}</pre>
<pre><b># Implementación PyMongo:</b><br>{op['pymongo']}</pre>
"""

html_content += f"""
<h1 class="sec-title">4.2 MÉTODOS O SINTAXIS RELACIONADOS CON LA SEGURIDAD Y NIVELES DE ACCESO EN MONGODB EN LA NUBE</h1>
<p>{SEC_4_SEGURIDAD_MONGODB_TEXT.replace(chr(10)+chr(10), '</p><p>')}</p>
<pre>{CODIGO_MONGODB_RBAC}</pre>

<h1 class="sec-title">4.3 CONFIGURACIÓN DE SEGURIDAD EN MONGODB DE ACUERDO AL PROYECTO</h1>
<table>
  <tr><th>Punto de Seguridad</th><th>Estrategia e Implementación Técnica en MedReminder AI</th></tr>
  {''.join(f'<tr><td><b>{pt[0]}</b></td><td>{pt[1]}</td></tr>' for pt in SEC_4_CONFIG_SEGURIDAD_PUNTOS)}
</table>

<div class="page-break"></div>

<h1 class="sec-title">5.0 MÉTODOS DE CONEXIÓN DE BASE DE DATOS EN LA NUBE Y LAS APLICACIONES</h1>

<h1 class="sec-title">5.1 PASOS PARA ESTABLECER LA CONEXIÓN DE LA BASE DE DATOS CON LA APLICACIÓN</h1>
<table>
  <tr><th>Paso / Fase</th><th>Acción Técnica Detallada e Implementación en el Backend</th></tr>
  {''.join(f'<tr><td><b>{ps[0]}</b></td><td>{ps[1]}</td></tr>' for ps in PASOS_CONEXION_DETALLE)}
</table>

<h2 class="sub-title">Implementación de Connection Pooling en FastAPI (`app/core/mongo.py`)</h2>
<pre>{codigo_fastapi_mongo}</pre>

<h1 class="sec-title">5.2 MÉTODOS DE CONSUMO DE DATOS EN LA NUBE</h1>
"""

for sec_c in SEC_5_CONSUMO_DATOS_PUNTOS:
    html_content += f"""
<h2 class="sub-title">{sec_c['subtitulo']}</h2>
<p>{sec_c['contenido'].replace(chr(10)+chr(10), '</p><p>')}</p>
"""

html_content += f"""
<h2 class="sub-title">Catálogo de Servicios Web Desarrollados (Endpoints REST)</h2>
<table>
  <tr><th>Método</th><th>Ruta del Endpoint</th><th>Seguridad</th><th>Descripción del Intercambio de Información</th></tr>
  {''.join(f'<tr><td><code><b>{ep[0]}</b></code></td><td><code>{ep[1]}</code></td><td>{ep[2]}</td><td>{ep[3]}</td></tr>' for ep in ENDPOINTS_REST_DATA)}
</table>

<h2 class="sub-title">Importancia de Proteger la Información Almacenada en Servicios de Nube</h2>
<p>{SEC_5_PROTECCION_DATOS.replace(chr(10)+chr(10), '</p><p>')}</p>

<h2 class="sub-title">Consumo de Datos Mediante Servicios Web en la Aplicación Móvil Android</h2>
<p>{SEC_5_CONSUMO_ANDROID.replace(chr(10)+chr(10), '</p><p>')}</p>

<div class="callout">
  <h4>Conclusión y Lecciones Aprendidas</h4>
  <p>La consolidación arquitectónica de MedReminder AI demuestra que la persistencia políglota (MySQL + MongoDB) satisface a la perfección tanto la integridad transaccional ACID requerida en prescripciones médicas como la alta velocidad no bloqueante requerida para la telemetría clínica. Este proyecto entrega una plataforma ergonómica, resiliente y de alto valor humano para la sociedad.</p>
</div>

</body>
</html>
"""

with open(HTML_OUT, "w", encoding="utf-8") as f:
    f.write(html_content)
print(f"Archivo HTML guardado en: {HTML_OUT}")

# Compilación a PDF con Chrome Headless
chrome_path = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
if os.path.exists(chrome_path):
    print("Compilando versión PDF con Google Chrome Headless...")
    cmd = [
        chrome_path,
        "--headless",
        "--disable-gpu",
        "--no-pdf-header-footer",
        f"--print-to-pdf={PDF_OUT}",
        HTML_OUT
    ]
    try:
        subprocess.run(cmd, check=True)
        print(f"¡PDF compilado exitosamente en: {PDF_OUT}!")
    except Exception as e:
        print(f"Aviso: No se pudo generar PDF con Chrome: {e}")
else:
    print("Aviso: Google Chrome no encontrado para compilar PDF.")

print("¡Proceso completado exitosamente!")
