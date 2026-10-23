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
        "Acceso Inmediato: Ingrese su correo electrónico y su contraseña registrada. Si aún no cuenta con un perfil personal, pulse 'Regístrate' al pie de la pantalla para crearlo en 30 segundos.",
        "Protección Táctil Inteligente: Al presionar 'Iniciar Sesión', el botón se desactiva al instante durante la conexión para evitar peticiones duplicadas o errores causados por temblores en las manos o pulsaciones involuntarias.",
        "Recuperación Rápida: Si olvidó sus credenciales, solicite el restablecimiento seguro directamente en la pantalla de bienvenida con verificación en un solo paso."
    ]
    add_step_card(
        doc,
        step_label="Paso 1 (30 seg)",
        title="Acceso y Perfil del Paciente",
        bullets=p1_bullets,
        img_path="docs/screenshots/01_login.png",
        caption="Inicio seguro y protegido",
        img_width=0.9
    )
    
    add_page_break(doc)
    
    # ==========================================================================
    # PÁGINA 2: PASOS 2 Y 3 + TARJETA DE REFERENCIA RÁPIDA DE BOTONES DE ALARMA
    # ==========================================================================
    p2_bullets = [
        "Forma Farmacéutica: Ingrese a la pestaña «Nuevo» y seleccione el formato del medicamento: Comprimidos, Jarabe o Inyectable.",
        "Dosis Rápida: Pulse un botón sugerido (500 mg, 1 comp., 10 ml) para evitar teclear y elija el intervalo de tomas de medicamentos (ej: cada 8 horas).",
        "Control de Existencias: Capture las piezas físicas disponibles en casa para que el botiquín calcule de inmediato los días de cobertura.",
    ]
    add_step_card(
        doc,
        step_label="Paso 2 (1 min)",
        title="Registro de Medicamento y Horario",
        bullets=p2_bullets,
        img_path="docs/screenshots/03_nuevo_medicamento.png",
        caption="Alta ágil de tratamientos",
        img_width=0.9
    )
    
    p3_bullets = [
        "Disparo de Alarma: Al cumplirse la hora exacta, sonará la alarma prioritaria con vibración y pantalla flotante Heads-Up.",
        "Asistente Medi: Medi anunciará por voz la dosis exacta requerida para sus tomas de medicamentos sin necesidad de leer la pantalla.",
        "Confirmación Inmediata: En la pantalla principal «Hoy», pulse un solo botón táctil de 56 dp para registrar la toma de medicamentos con timestamp UTC y descontar 1 unidad del botiquín.",
    ]
    add_step_card(
        doc,
        step_label="Paso 3 (Acción)",
        title="Notificación y Registro de Tomas de Medicamentos",
        bullets=p3_bullets,
        img_path="docs/screenshots/02_hoy.png",
        caption="Confirmación en un toque",
        img_width=0.9
    )
    
    add_section_heading(doc, "2. TARJETA DE REFERENCIA RÁPIDA DE BOTONES DE ALARMA", level=1)
    
    btn_headers = ["Botón de Acción", "Propósito y Situación Clínica", "Efecto en Tomas de Medicamentos e Inventario"]
    btn_rows = [
        ["🟢 Tomar Ahora", "Pulsar al momento exacto de ingerir el medicamento prescrito.", "Registra la toma de medicamentos con timestamp legal y descuenta 1 unidad del stock."],
        ["🟡 Posponer (+10 min)", "Aplazar la alarma si está comiendo, manejando o temporalmente ocupado.", "Reprograma la alarma exactamente 10 minutos (máximo 2 posposiciones consecutivas)."],
        ["⚪ Omitir", "Utilizar únicamente si el médico suspendió la dosis o por indicación clínica.", "Registra la omisión justificada con notas clínicas sin descontar unidades del stock."],
        ["🔵 Deshacer tomas de medicamentos", "Pulsación accidental involuntaria sobre el botón 'Tomar Ahora'.", "Disponible por 5 segundos en la barra inferior para anular el registro y restaurar el stock."]
    ]
    add_truth_table(doc, btn_headers, btn_rows, "Tabla 1: Funcionalidad de los botones en recordatorios de tomas de medicamentos", [1.8, 2.3, 2.4])
    
    add_page_break(doc)
    
    # ==========================================================================
    # PÁGINA 3: SEMÁFORO DE INVENTARIO, REGLA DE ORO Y FAQ DE EMERGENCIA
    # ==========================================================================
    add_section_heading(doc, "3. SEMÁFORO VISUAL DE INVENTARIO («MI BOTIQUÍN»)", level=1)
    add_body_p(
        doc,
        "La pestaña «Mi Botiquín» clasifica en tiempo real sus existencias de medicamentos según los días de cobertura restantes:"
    )
    
    sem_headers = ["Nivel del Semáforo", "Cobertura Restante", "Estado y Acción Preventiva Requerida"]
    sem_rows = [
        ["🟢 Verde (Suficiente)", "Más de 5 días de tratamiento", "Existencias óptimas en el hogar. Todas las tomas de medicamentos están garantizadas."],
        ["🟡 Amarillo (Por agotarse)", "3 días o menos de tratamiento", "Advertencia temprana: acuda oportunamente a la farmacia para reabastecer las cajas."],
        ["🔴 Rojo (Crítico)", "Stock agotado (0 comprimidos)", "Alerta crítica: riesgo inminente de interrupción en las tomas de medicamentos. Reponer ya."]
    ]
    add_truth_table(doc, sem_headers, sem_rows, "Tabla 2: Semáforo visual para prevención de desabastecimiento de medicamentos", [1.8, 2.0, 2.7])
    
    add_callout(
        doc,
        "Por estrictos criterios de seguridad clínica y farmacológica, el sistema solo permite posponer una dosis un MÁXIMO "
        "DE 2 VECES consecutivas (+10 minutos cada una). Al sonar la tercera alarma, el botón de posponer se bloquea "
        "y el sistema exige confirmar la ingesta mediante 'Tomar Ahora' o justificar la omisión con 'Omitir'. "
        "Esta restricción formal previene intoxicaciones o sobredosis por acumulación horaria y salvaguarda la salud del paciente.",
        callout_type="warn",
        title="REGLA DE ORO MÉDICA: MÁXIMO 2 POSPOSICIONES DE TOMAS DE MEDICAMENTOS"
    )
    
    add_section_heading(doc, "4. FAQ DE EMERGENCIA Y RESOLUCIÓN RÁPIDA", level=1)
    
    faq_headers = ["Pregunta Frecuente", "Diagnóstico Técnico Rápido", "Solución Inmediata en Pantalla"]
    faq_rows = [
        ["¿No suena la alarma con el teléfono bloqueado?", "Ahorro de batería agresivo de Android en segundo plano.", "Vaya a Ajustes > Apps > MedReminder AI > Batería y elija 'Sin restricciones'. Verifique volumen de alarmas."],
        ["¿Olvidé registrar una toma de medicamentos a tiempo?", "La dosis se tomó en hora pero no se confirmó en la app.", "Abra la pantalla «Hoy», pulse sobre la tarjeta atrasada y confirme la toma de medicamentos con su hora real."],
        ["¿Cómo edito una dosis o suspendo un tratamiento?", "Cambio de prescripción médica o ajuste de dosis.", "En «Mi Botiquín», pulse sobre el fármaco y seleccione 'Editar Pauta' o pulse 'Pausar Tratamiento'."]
    ]
    add_truth_table(doc, faq_headers, faq_rows, "Tabla 3: Solución inmediata a las 3 incidencias más comunes", [2.0, 2.0, 2.5])
    
    add_callout(
        doc,
        "MedReminder AI — Sistema Inteligente de Gestión y Recordatorio Farmacológico\n"
        "Dirección de TIC • Asignatura: Fundamentos de Inteligencia Artificial • Docente: Ing. Hector Velazquez Estrada\n"
        "Equipo: Gutierrez Ugalde Samuel • Nava Garcia Rodrigo • Castillo Ramirez Nahum Yabet • Ramirez Romero Pablo • Peña Hernandez Alexander (ITIID - D73)",
        callout_type="tip",
        title="CENTRO DE ASISTENCIA Y CONTACTO INSTITUCIONAL UTVT"
    )
    
    # Guardar documento en docs/
    out_path = "docs/Guia_de_Uso_Rapido_MedReminderAI.docx"
    doc.save(out_path)
    print(f"✅ Guía de Uso Rápido generada exitosamente en: {out_path}")
    return out_path

if __name__ == "__main__":
    build_guia_rapida()
