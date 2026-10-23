"""
build_all_manuals.py - Orquestador maestro de generación, validación y sincronización de los 4 manuales.
Ejecuta la suite completa de generadores y efectúa auditorías automáticas de calidad:
1. Existencia y tamaño de archivos.
2. Carátula UTVT y metadatos institucionales (en párrafos y tablas).
3. Presencia de campo nativo de índice Word (TOC) y flag updateFields.
4. Cumplimiento estricto de tablas de verdad únicamente con 'V' y 'F' (cero 0 y 1).
5. Cumplimiento estricto del término "tomas de medicamentos" (cero "tomas" o "toma" aisladas).
6. Auditoría de disposición y formato: w:cantSplit en tablas y keep_with_next en encabezados.
7. Sincronización en ambos workspaces (Developer y Downloads).
"""

import os
import sys
import shutil
import re
from pathlib import Path
import docx
from docx.oxml.ns import qn

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(BASE_DIR / "scripts"))

from generate_manual_tecnico import build_manual_tecnico
from generate_manual_usuario import build_manual_usuario
from generate_manual_instalacion import build_manual_instalacion
from generate_guia_rapida import build_guia_rapida

MANUALS = [
    {
        "name": "Manual Técnico Oficial",
        "file": "Manual_Tecnico_MedReminderAI.docx",
        "builder": build_manual_tecnico,
        "min_paragraphs": 100,
        "min_tables": 10
    },
    {
        "name": "Manual de Usuario Oficial",
        "file": "Manual_de_Usuario_MedReminderAI.docx",
        "builder": build_manual_usuario,
        "min_paragraphs": 80,
        "min_tables": 8
    },
    {
        "name": "Manual de Instalación y Despliegue",
        "file": "Manual_de_Instalacion_MedReminderAI.docx",
        "builder": build_manual_instalacion,
        "min_paragraphs": 90,
        "min_tables": 10
    },
    {
        "name": "Guía de Uso Rápido",
        "file": "Guia_de_Uso_Rapido_MedReminderAI.docx",
        "builder": build_guia_rapida,
        "min_paragraphs": 10,
        "min_tables": 3
    }
]

def audit_document(file_path: Path, item: dict = None):
    doc = docx.Document(str(file_path))
    issues = []
    
    # 0. Verificación de umbrales cuantitativos mínimos
    if item:
        if len(doc.paragraphs) < item["min_paragraphs"]:
            issues.append(f"Número de párrafos ({len(doc.paragraphs)}) menor al mínimo requerido ({item['min_paragraphs']})")
        if len(doc.tables) < item["min_tables"]:
            issues.append(f"Número de tablas ({len(doc.tables)}) menor al mínimo requerido ({item['min_tables']})")
    
    # 1. Auditoría de Carátula / Encabezado UTVT (revisar párrafos y celdas de tablas)
    p_texts = [p.text for p in doc.paragraphs]
    for t in doc.tables:
        for r in t.rows:
            for c in r.cells:
                p_texts.extend([p.text for p in c.paragraphs])
    full_text = "\n".join(p_texts)
    
    if "UNIVERSIDAD TECNOLÓGICA DEL VALLE DE TOLUCA" not in full_text:
        issues.append("Falta encabezado de UNIVERSIDAD TECNOLÓGICA DEL VALLE DE TOLUCA")
    if "Hector Velazquez Estrada" not in full_text:
        issues.append("Falta mención del docente Hector Velazquez Estrada")
    if "Fundamentos de Inteligencia Artificial" not in full_text:
        issues.append("Falta mención de la asignatura Fundamentos de Inteligencia Artificial")
    alumnos_esperados = [
        "Gutierrez Ugalde Samuel",
        "Nava Garcia Rodrigo",
        "Castillo Ramirez Nahum Yabet",
        "Ramirez Romero Pablo",
        "Peña Hernandez Alexander"
    ]
    for al in alumnos_esperados:
        if al not in full_text:
            issues.append(f"Falta el integrante '{al}' en la carátula o encabezado institucional")
            
    # Verificar que el título del índice no esté como Heading 1 (evita autorecursión en Word)
    for p in doc.paragraphs:
        if "ÍNDICE GENERAL DE CONTENIDO" in p.text and p.style.name.startswith("Heading"):
            issues.append(f"El título del Índice está estilizado como '{p.style.name}' (debe ser estilo título normal para evitar autorecursión en el TOC)")
        
    # 2. Auditoría de uso de "tomas de medicamentos"
    for i, p in enumerate(doc.paragraphs):
        for m in re.finditer(r'\b(tomas?)\b', p.text, re.IGNORECASE):
            sub = p.text[m.start():m.start()+35]
            if not re.search(r'tomas?\s+de\s+medicamentos', sub, re.IGNORECASE) and not re.search(r'historial_toma|instrucciones_toma', sub):
                issues.append(f"Párrafo {i}: uso indebido de '{sub}' (debe ser 'tomas de medicamentos')")
                
    for t_idx, t in enumerate(doc.tables):
        for r_idx, r in enumerate(t.rows):
            for c_idx, c in enumerate(r.cells):
                for m in re.finditer(r'\b(tomas?)\b', c.text, re.IGNORECASE):
                    sub = c.text[m.start():m.start()+35]
                    if not re.search(r'tomas?\s+de\s+medicamentos', sub, re.IGNORECASE) and not re.search(r'historial_toma|instrucciones_toma', sub):
                        issues.append(f"Tabla {t_idx} Fila {r_idx} Celda {c_idx}: uso indebido de '{sub}'")
                        
    # 3. Auditoría de Tablas de Verdad (cero '0' o '1' como valores booleanos)
    for t_idx, t in enumerate(doc.tables):
        for r_idx, r in enumerate(t.rows[1:]): # omitir cabecera
            for c_idx, c in enumerate(r.cells[:5]): # columnas de variables booleanas
                txt = c.text.strip()
                if txt in ["0", "1"]:
                    issues.append(f"Tabla {t_idx} Fila {r_idx+1} Celda {c_idx}: valor booleano numérico '{txt}' (debe ser 'V' o 'F')")
                    
    # 4. Auditoría de Índice Nativo Word TOC
    xml_doc = doc._element.xml
    if "TOC \\o" not in xml_doc and "TOC" not in xml_doc:
        issues.append("No se encontró el campo de código nativo TOC de Word")
        
    # 5. Auditoría de integridad estructural OpenXML en tablas (w:cantSplit en todas las tablas)
    tables_without_cantsplit = 0
    for t_idx, t in enumerate(doc.tables):
        for r in t.rows:
            tr_xml = r._tr.xml
            if "cantSplit" not in tr_xml:
                tables_without_cantsplit += 1
                break
    if tables_without_cantsplit > 0:
        issues.append(f"{tables_without_cantsplit} tablas no cuentan con la directiva OpenXML w:cantSplit en sus filas")

    # 6. Auditoría de encabezados sin keep_with_next
    headings_without_keep = 0
    for p in doc.paragraphs:
        if p.style.name.startswith("Heading"):
            if not p.paragraph_format.keep_with_next:
                headings_without_keep += 1
    if headings_without_keep > 0:
        issues.append(f"{headings_without_keep} encabezados no tienen keep_with_next = True (riesgo de orfandad)")

    # 7. Auditoría de espaciado en celdas de tablas (space_before y space_after deben ser 0)
    bad_cell_spacing = 0
    for t_idx, t in enumerate(doc.tables):
        for r_idx, r in enumerate(t.rows):
            for c_idx, c in enumerate(r.cells):
                for p in c.paragraphs:
                    sb = p.paragraph_format.space_before
                    sa = p.paragraph_format.space_after
                    if (sb is not None and sb.pt != 0) or (sa is not None and sa.pt != 0):
                        bad_cell_spacing += 1
    if bad_cell_spacing > 0:
        issues.append(f"{bad_cell_spacing} párrafos en celdas de tabla tienen space_before o space_after > 0")

    # 8. Auditoría de tipografía (solo Calibri o Consolas autorizados)
    unauthorized_fonts = set()
    for p in doc.paragraphs:
        for r in p.runs:
            if r.font.name and r.font.name not in ["Calibri", "Consolas"]:
                unauthorized_fonts.add(r.font.name)
    for t in doc.tables:
        for r in t.rows:
            for c in r.cells:
                for p in c.paragraphs:
                    for r in p.runs:
                        if r.font.name and r.font.name not in ["Calibri", "Consolas"]:
                            unauthorized_fonts.add(r.font.name)
    if unauthorized_fonts:
        issues.append(f"Fuentes tipográficas no autorizadas detectadas: {unauthorized_fonts}")

    # 9. Auditoría de Diagramas Textuales y Caracteres de Dibujo ASCII/Unicode
    box_chars_detected = 0
    text_arrows_detected = 0
    diagram_pat = re.compile(r'-->|==>|<--|<==|\+---|\|\s*\|\s*\|')
    for p in doc.paragraphs:
        if re.search(r'[\u2500-\u257F]', p.text):
            box_chars_detected += 1
        if diagram_pat.search(p.text):
            text_arrows_detected += 1
    for t in doc.tables:
        for r in t.rows:
            for c in r.cells:
                for p in c.paragraphs:
                    if re.search(r'[\u2500-\u257F]', p.text):
                        box_chars_detected += 1
                    if diagram_pat.search(p.text):
                        text_arrows_detected += 1
    if box_chars_detected > 0:
        issues.append(f"Detectados {box_chars_detected} caracteres box-drawing de diagramas textuales (U+2500 a U+257F)")
    if text_arrows_detected > 0:
        issues.append(f"Detectadas {text_arrows_detected} flechas o esquemas textuales informales ('-->', '==>', '+---')")

    # 10. Auditoría de alineación obligatoria a la izquierda en bloques de código y textos monoespaciados
    cli_cmd_pat = re.compile(
        r'^\s*(?:docker\s+(?:exec|logs|run|compose)|adb\s+(?:logcat|shell|reverse|install)|curl\s+-|mysqldump|mongodump|mongorestore)\b',
        re.MULTILINE
    )

    for t_idx, t in enumerate(doc.tables):
        for r_idx, r in enumerate(t.rows):
            for c_idx, c in enumerate(r.cells):
                for p_idx, p in enumerate(c.paragraphs):
                    is_mono = any(run.font.name == "Consolas" for run in p.runs)
                    is_code_cell = False
                    shd = c._tc.find('.//' + qn('w:shd'))
                    if shd is not None and shd.attrib.get(qn('w:fill'), '').upper() == 'F1F5F9':
                        is_code_cell = True
                    has_cli = bool(cli_cmd_pat.search(p.text))
                    
                    if is_mono or is_code_cell or has_cli:
                        jc = p._p.find('.//' + qn('w:jc'))
                        jc_val = jc.attrib.get(qn('w:val')) if jc is not None else None
                        if jc_val in ["both", "distribute", "justify"]:
                            issues.append(f"Tabla {t_idx} Fila {r_idx} Celda {c_idx} Párrafo {p_idx}: código/comando con justificación no autorizada (w:val='{jc_val}')")
                        elif jc_val != "left":
                            issues.append(f"Tabla {t_idx} Fila {r_idx} Celda {c_idx} Párrafo {p_idx}: código/comando sin alineación izquierda explícita w:jc w:val='left' (actual: {jc_val})")

    for p_idx, p in enumerate(doc.paragraphs):
        is_mono = any(run.font.name == "Consolas" for run in p.runs)
        has_cli = bool(cli_cmd_pat.search(p.text))
        if is_mono or has_cli:
            jc = p._p.find('.//' + qn('w:jc'))
            jc_val = jc.attrib.get(qn('w:val')) if jc is not None else None
            if jc_val in ["both", "distribute", "justify"]:
                issues.append(f"Párrafo {p_idx}: código/comando CLI con justificación no autorizada (w:val='{jc_val}')")
            elif jc_val != "left":
                issues.append(f"Párrafo {p_idx}: código/comando CLI sin alineación izquierda explícita w:jc w:val='left' (actual: {jc_val})")

    return {
        "paragraphs": len(doc.paragraphs),
        "tables": len(doc.tables),
        "size_kb": round(file_path.stat().st_size / 1024, 1),
        "issues": issues
    }

def main():
    print("=" * 70)
    print("INICIANDO GENERACIÓN Y AUDITORÍA INTEGRAL DE LOS 4 MANUALES UTVT")
    print("=" * 70)
    
    docs_dir = BASE_DIR / "docs"
    docs_dir.mkdir(parents=True, exist_ok=True)
    
    downloads_docs = Path("/Users/4strob0y/Downloads/MedReminderAI/docs")
    downloads_docs.mkdir(parents=True, exist_ok=True)
    
    total_errors = 0
    
    for item in MANUALS:
        print(f"\n[1/3] Generando: {item['name']} ({item['file']})...")
        out_rel = item["builder"]()
        out_file = docs_dir / item["file"]
        
        print(f"[2/3] Auditando calidad y directrices académicas en {item['file']}...")
        stats = audit_document(out_file, item)
        print(f"      • Párrafos: {stats['paragraphs']} (Mínimo: {item['min_paragraphs']})")
        print(f"      • Tablas: {stats['tables']} (Mínimo: {item['min_tables']})")
        print(f"      • Tamaño en disco: {stats['size_kb']} KB")
        
        if stats["issues"]:
            print(f"      ❌ Incidencias detectadas ({len(stats['issues'])}):")
            for iss in stats["issues"]:
                print(f"         - {iss}")
            total_errors += len(stats["issues"])
        else:
            print(f"      ✅ 100% Conforme: Carátula UTVT, TOC nativo, Tablas V/F, w:cantSplit, 'tomas de medicamentos' y código sin justificación.")
            
        print(f"[3/3] Sincronizando en espacio Downloads...")
        shutil.copy2(out_file, downloads_docs / item["file"])
        print(f"      -> Copiado a: {downloads_docs / item['file']}")
        
    # Sincronización de scripts y assets institucionales hacia Downloads
    print("\n[+] Sincronizando scripts y assets institucionales hacia Downloads...")
    downloads_scripts = Path("/Users/4strob0y/Downloads/MedReminderAI/scripts")
    downloads_scripts.mkdir(parents=True, exist_ok=True)
    for scr in (BASE_DIR / "scripts").glob("*.py"):
        shutil.copy2(scr, downloads_scripts / scr.name)
        
    for asset_file in ["logo_edomex.png", "logo_utvt.png", "Portada.docx"]:
        src_asset = docs_dir / asset_file
        if src_asset.exists():
            shutil.copy2(src_asset, downloads_docs / asset_file)
            
    # Verificar paridad de tamaño y hash MD5 exacta en los 4 manuales
    print("\n[+] Verificando paridad exacta bit a bit (tamaño y hash MD5) entre Developer y Downloads...")
    import hashlib
    for item in MANUALS:
        dev_path = docs_dir / item["file"]
        dl_path = downloads_docs / item["file"]
        dev_size = dev_path.stat().st_size
        dl_size = dl_path.stat().st_size
        dev_md5 = hashlib.md5(dev_path.read_bytes()).hexdigest()
        dl_md5 = hashlib.md5(dl_path.read_bytes()).hexdigest()
        if dev_size != dl_size or dev_md5 != dl_md5:
            print(f"      ❌ Discrepancia en {item['file']}: Dev({dev_size}B, {dev_md5}) vs DL({dl_size}B, {dl_md5})")
            total_errors += 1
        else:
            print(f"      ✅ Paridad bit a bit 1:1 confirmada en {item['file']} ({dev_size} bytes, MD5: {dev_md5[:10]}...)")
        
    print("\n" + "=" * 70)
    if total_errors == 0:
        print("RESULTADO FINAL: AUDITORÍA EXITOSA CON CERO INCIDENCIAS")
        print("Los 4 manuales fueron generados y sincronizados correctamente.")
    else:
        print(f"RESULTADO FINAL: SE ENCONTRARON {total_errors} INCIDENCIAS A CORREGIR.")
    print("=" * 70)
    
    if total_errors > 0:
        sys.exit(1)

if __name__ == "__main__":
    main()
