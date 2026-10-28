"""
generate_guia_rapida.py - Generador de la Guía de Uso Rápido Oficial de MedReminder AI.
Documento ejecutivo con carátula oficial UTVT (Portada.docx) y cuerpo de alta agilidad para el usuario final.
Incluye carátula institucional oficial de Portada.docx, resumen de contenido (TOC),
flujo de inicio en 3 pasos visuales con tarjetas de 2 columnas (texto + mockup),
tarjeta de botones de alarma, semáforo de inventario, regla de oro médica,
FAQ de emergencia y uso estricto del término "tomas de medicamentos".
"""

import os
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(BASE_DIR / "scripts"))

import docx
from doc_utils import (
    create_base_document, setup_header_footer, add_utvt_cover, add_compact_toc,
    add_section_heading, add_body_p, add_truth_table, add_callout, add_step_card, add_page_break
)

def build_guia_rapida():
    doc = create_base_document()
    doc_title = "Guía de Uso Rápido"
    setup_header_footer(doc, doc_title)
    
    # ==========================================================================
    # PÁGINA 1: CARÁTULA INSTITUCIONAL OFICIAL UTVT (PORTADA.DOCX)
    # ==========================================================================
    add_utvt_cover(
        doc,
        title="GUÍA DE USO RÁPIDO",
        subtitle="Referencia Ejecutiva de Inicio y Control Diario de Tomas de Medicamentos",
        doc_code="GUIA-RAP-MEDREMINDER-2026-V2"
    )
    
    # ==========================================================================
    # PÁGINA 2: ÍNDICE RÁPIDO Y PASO 1 (ACCESO Y PERFIL)
    # ==========================================================================
    add_compact_toc(doc, [
        "1. Flujo de Inicio en 3 Pasos Visuales (Pág. 2-3)",
        "2. Tarjeta de Botones de Alarma (Pág. 3)",
        "3. Semáforo de Inventario (Pág. 4)",
        "4. FAQ y Resolución Rápida (Pág. 4)"
    ])
    
    add_body_p(
        doc,
        "Esta guía provee las instrucciones esenciales para comenzar a utilizar MedReminder AI en menos de 2 minutos. "
        "Siga este flujo simplificado para asegurar el registro puntual de todas sus tomas de medicamentos "
        "y supervisar las existencias de su botiquín familiar con cero margen de error táctil."
    )
    
    add_section_heading(doc, "1. FLUJO DE INICIO EN 3 PASOS VISUALES", level=1)
    
    p1_bullets = [
        "Acceso y Edad Clínica: Ingrese su correo, contraseña y fecha de nacimiento en el registro. El sistema adapta la experiencia según su edad: gamificación con racha y honor para jóvenes/adultos (<60 años) o supervisión automática de cuidador para adultos mayores (≥60 años).",
        "Protección Táctil Inteligente: Al presionar 'Iniciar Sesión', el botón se desactiva al instante durante la conexión para evitar peticiones duplicadas o errores causados por temblores en las manos.",
        "Recuperación Rápida: Si olvidó sus credenciales, solicite el restablecimiento seguro directamente en la pantalla de bienvenida con verificación en un solo paso."
    ]
    add_step_card(
        doc,
        step_label="Paso 1 (30 seg)",
        title="Acceso y Perfil del Paciente",
        bullets=p1_bullets,
        img_path=str(BASE_DIR / "docs/screenshots/01_login.png"),
        caption="Inicio seguro y protegido",
        img_width=0.9
    )
    
    # ==========================================================================
    # PASOS 2 Y 3 + TARJETA DE REFERENCIA RÁPIDA DE BOTONES DE ALARMA
    # ==========================================================================
    p2_bullets = [
        "Autocompletado con IA y Escaneo de Recetas: En «Nuevo Medicamento», pulse 'Sugerencias IA' o escanee su receta médica con Ollama (medi-clinico) para autocompletar dosis, frecuencia de tomas de medicamentos e instrucciones.",
        "Dosis Rápida y Crítica: Seleccione el formato (Pastilla, Gotas o Inyección), el color distintivo y marque si es un medicamento crítico no posponible.",
        "Control de Existencias: Capture las piezas físicas disponibles en casa para que el botiquín calcule de inmediato los días de cobertura.",
    ]
    add_step_card(
        doc,
        step_label="Paso 2 (1 min)",
        title="Registro de Medicamento y Horario",
        bullets=p2_bullets,
        img_path=str(BASE_DIR / "docs/screenshots/03_nuevo_medicamento.png"),
        caption="Alta ágil con IA local",
        img_width=0.9
    )
    
    p3_bullets = [
        "Disparo de Alarma Nativa: Al cumplirse la hora exacta, saltará automáticamente la pantalla nativa de alarma con sonido, vibración y acciones directas aún con el teléfono bloqueado.",
        "Asistente Medi (Ollama): Medi anunciará por voz la dosis exacta requerida para sus tomas de medicamentos y resolverá dudas clínicas en tiempo real.",
        "Confirmación y Supervisión Senior: En «Hoy», pulse un solo botón de 56 dp para registrar la toma de medicamentos. En adultos mayores, omitir o posponer medicamentos críticos alerta automáticamente al cuidador.",
    ]
    add_step_card(
        doc,
        step_label="Paso 3 (Acción)",
        title="Notificación y Registro de Tomas de Medicamentos",
        bullets=p3_bullets,
        img_path=str(BASE_DIR / "docs/screenshots/02_hoy.png"),
        caption="Confirmación en un toque",
        img_width=0.9
    )
    
    add_section_heading(doc, "2. TARJETA DE REFERENCIA RÁPIDA DE BOTONES DE ALARMA", level=1, page_break_before=True)
    
    btn_headers = ["Botón de Acción", "Propósito y Situación Clínica", "Efecto en Tomas de Medicamentos e Inventario"]
    btn_rows = [
        ["[VERDE] Tomar Ahora", "Pulsar al momento exacto de ingerir el medicamento prescrito.", "Registra la toma de medicamentos con timestamp legal y descuenta 1 unidad del stock."],
        ["[ÁMBAR] Posponer (+30 min)", "Aplazar la alarma si está comiendo, manejando o temporalmente ocupado.", "Reprograma la alarma exactamente 30 minutos (máximo 2 posposiciones consecutivas)."],
        ["[GRIS] Omitir", "Utilizar únicamente si el médico suspendió la dosis o por indicación clínica.", "Registra la omisión justificada sin descontar stock (en adultos mayores notifica al cuidador)."],
        ["[AZUL] Deshacer tomas de medicamentos", "Pulsación accidental involuntaria sobre el botón 'Tomar Ahora'.", "Disponible por 5 segundos en la barra inferior para anular el registro y restaurar el stock."]
    ]
    add_truth_table(doc, btn_headers, btn_rows, "Tabla 1: Funcionalidad de los botones en recordatorios de tomas de medicamentos", [1.8, 2.3, 2.4])
    
    # ==========================================================================
    # SEMÁFORO DE INVENTARIO, REGLA DE ORO Y FAQ DE EMERGENCIA
    # ==========================================================================
    add_section_heading(doc, "3. SEMÁFORO VISUAL DE INVENTARIO («MI BOTIQUÍN»)", level=1, page_break_before=True)
    add_body_p(
        doc,
        "La pestaña «Mi Botiquín» clasifica en tiempo real sus existencias de medicamentos según los días de cobertura restantes:"
    )
    
    sem_headers = ["Nivel del Semáforo", "Cobertura Restante", "Estado y Acción Preventiva Requerida"]
    sem_rows = [
        ["[VERDE] Suficiente", "Más de 5 días de tratamiento", "Existencias óptimas en el hogar. Todas las tomas de medicamentos están garantizadas."],
        ["[AMARILLO] Por agotarse", "3 días o menos de tratamiento", "Advertencia temprana: acuda oportunamente a la farmacia para reabastecer las cajas."],
        ["[ROJO] Crítico", "Stock agotado (0 comprimidos)", "Alerta crítica: riesgo inminente de interrupción en las tomas de medicamentos. Reponer ya."]
    ]
    add_truth_table(doc, sem_headers, sem_rows, "Tabla 2: Semáforo visual para prevención de desabastecimiento de medicamentos", [1.8, 2.0, 2.7])
    
    add_callout(
        doc,
        "Por estrictos criterios de seguridad clínica y farmacológica, el sistema solo permite posponer una dosis un MÁXIMO "
        "DE 2 VECES consecutivas (+30 minutos cada una). Al sonar la tercera alarma, el botón de posponer se bloquea "
        "y el sistema exige confirmar la ingesta mediante 'Tomar Ahora' o justificar la omisión con 'Omitir'. "
        "En pacientes adultos mayores (≥60 años), omitir o posponer un medicamento crítico envía una alerta automática inmediata al Panel del Cuidador.",
        callout_type="warn",
        title="REGLA DE ORO MÉDICA: MÁXIMO 2 POSPOSICIONES DE TOMAS DE MEDICAMENTOS (+30 MIN)"
    )
    
    add_section_heading(doc, "4. FAQ DE EMERGENCIA Y RESOLUCIÓN RÁPIDA", level=1)
    
    faq_headers = ["Pregunta Frecuente", "Diagnóstico Técnico Rápido", "Solución Inmediata en Pantalla"]
    faq_rows = [
        ["¿No suena la alarma con el teléfono bloqueado?", "Ahorro de batería agresivo de Android en segundo plano.", "Vaya a Ajustes > Apps > MedReminder AI > Batería y elija 'Sin restricciones'. Verifique permisos de Alarmas Exactas."],
        ["¿Olvidé registrar una toma de medicamentos a tiempo?", "La dosis se tomó en hora pero no se confirmó en la app.", "Abra la pantalla «Hoy», pulse sobre la tarjeta atrasada y confirme la toma de medicamentos con su hora real."],
        ["¿Cómo vinculo o superviso a un adulto mayor como cuidador?", "Supervisión familiar de adherencia y alertas críticas.", "Desde la cabecera superior pulse 'Modo Cuidador' para abrir el Panel de Supervisión y vincular al paciente por correo."]
    ]
    add_truth_table(doc, faq_headers, faq_rows, "Tabla 3: Solución inmediata a las 3 incidencias más comunes", [2.0, 2.0, 2.5])
    
    add_callout(
        doc,
        "MedReminder AI — Sistema Inteligente de Gestión y Recordatorio Farmacológico\n"
        "Dirección de TIC • Asignatura: Fundamentos de Inteligencia Artificial • Docente: Ing. Hector Velazquez Estrada\n"
        "Equipo: Gutierrez Ugalde Samuel • Nava Garcia Rodrigo • Castillo Ramirez Nahum Yabet • Ramirez Romero Pablo • Peña Hernandez Alexander (DSM - 53)",
        callout_type="tip",
        title="CENTRO DE ASISTENCIA Y CONTACTO INSTITUCIONAL UTVT"
    )
    
    # Guardar documento en docs/
    out_path = str(BASE_DIR / "docs/Guia_de_Uso_Rapido_MedReminderAI.docx")
    doc.save(out_path)
    print(f"Guía de Uso Rápido generada exitosamente en: {out_path}")
    return out_path

if __name__ == "__main__":
    build_guia_rapida()
