"""
generate_manual_instalacion.py - Generador del Manual de Instalación y Despliegue Oficial de MedReminder AI.
Incluye carátula institucional UTVT, índice nativo de Word, marco PEAS, tablas de verdad con V y F,
diccionario de variables de entorno y despliegue, comandos reproducibles con curl, salidas de terminal
completas, comandos de ADB para Android 13/14/15, pruebas SQL y uso estricto de "tomas de medicamentos".
"""

import os
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(BASE_DIR / "scripts"))

import docx
from doc_utils import (
    create_base_document, setup_header_footer, add_utvt_cover, add_native_toc,
    add_section_heading, add_body_p, add_truth_table, add_variable_dictionary_table,
    add_peas_section, add_callout, add_code_block, add_figure_image, add_version_control_table
)

def build_manual_instalacion():
    doc = create_base_document()
    doc_title = "Manual de Instalación y Despliegue"
    setup_header_footer(doc, doc_title)
    
    # --------------------------------------------------------------------------
    # 0. CARÁTULA INSTITUCIONAL UTVT
    # --------------------------------------------------------------------------
    add_utvt_cover(
        doc,
        title="MANUAL DE INSTALACIÓN, DESPLIEGUE Y CONFIGURACIÓN",
        subtitle="Guía Quirúrgica de Despliegue de Microservicios con Docker Compose, Configuración de Bases de Datos MySQL/MongoDB, Compilación de Android y Pruebas de Humo",
        doc_code="MAN-INS-MEDREMINDER-2026-V1.3"
    )
    
    # --------------------------------------------------------------------------
    # CONTROL DE VERSIONES
    # --------------------------------------------------------------------------
    versiones = [
        {
            "version": "1.0",
            "fecha": "20/10/2026",
            "autor": "Equipo de Ingeniería UTVT",
            "descripcion": "Versión inicial: Guía de despliegue con Docker Compose, configuración de MySQL y MongoDB."
        },
        {
            "version": "1.1",
            "fecha": "21/10/2026",
            "autor": "Equipo de Ingeniería UTVT",
            "descripcion": "Estructuración formal con marco PEAS de infraestructura, tablas de verdad de verificación, compilación de Android y pruebas de humo."
        },
        {
            "version": "1.2",
            "fecha": "22/10/2026",
            "autor": "Equipo de Ingeniería UTVT",
            "descripcion": "Eliminación de tablas y diagramas textuales, sustitución por matrices institucionales limpias, y sincronización con marco PEAS arriba."
        },
        {
            "version": "1.3",
            "fecha": "22/10/2026",
            "autor": "Equipo de Infraestructura UTVT",
            "descripcion": "Verificación y ratificación de Tablas de Verdad de Despliegue con 'V' y 'F' en Sección 3 'hasta arriba' inmediatamente después del Marco PEAS."
        }
    ]
    add_version_control_table(doc, versiones, "CONTROL DE VERSIONES DEL MANUAL DE INSTALACIÓN")
    
    # --------------------------------------------------------------------------
    # ÍNDICE GENERAL NATIVO DE WORD
    # --------------------------------------------------------------------------
    toc_items = [
        ("1.", "OBJETIVOS DEL SISTEMA Y DEL MANUAL DE INSTALACIÓN", 3),
        ("1.1", "Objetivo General de Despliegue", 3),
        ("1.2", "Objetivos Específicos de Infraestructura, DevOps y Resiliencia", 3),
        ("2.", "MARCO PEAS DE INFRAESTRUCTURA Y DESPLIEGUE", 4),
        ("2.1", "El Entorno de Despliegue como Agente de Operaciones", 4),
        ("2.2", "Matriz Operativa PEAS de Infraestructura", 4),
        ("3.", "TABLAS DE VERDAD DE VERIFICACIÓN DE INSTALACIÓN Y DESPLIEGUE", 5),
        ("3.1", "Condiciones de Arranque de Microservicios Backend", 5),
        ("3.2", "Condiciones de Conectividad Móvil y Conmutación de IP", 6),
        ("3.3", "Requisitos de Activación de Alarmas Locales en Android", 7),
        ("3.4", "Integridad Referencial en la Inicialización de Persistencia Relacional", 8),
        ("4.", "DICCIONARIO DE VARIABLES DE CONFIGURACIÓN Y ENTORNO", 9),
        ("5.", "REQUISITOS PREVIOS DE HARDWARE Y SOFTWARE", 11),
        ("5.1", "Especificaciones Mínimas y Recomendadas de Hardware", 11),
        ("5.2", "Matriz de Software y Dependencias de Sistema", 12),
        ("5.3", "Verificación de Entorno en Host", 13),
        ("6.", "PROCEDIMIENTO PASO A PASO DE DESPLIEGUE DEL BACKEND (DOCKER)", 14),
        ("6.1", "Clonación y Verificación del Árbol de Trabajo", 14),
        ("6.2", "Configuración Quirúrgica del Archivo .env", 15),
        ("6.3", "Construcción de Imágenes con Docker Compose", 16),
        ("6.4", "Lanzamiento y Orquestación del Stack de Microservicios", 17),
        ("6.5", "Inspección del Estado de Contenedores y Sockets TCP", 18),
        ("6.6", "Inspección de Logs Unificados del Sistema", 19),
        ("6.7", "Verificación de Inicialización de Persistencia Relacional MySQL", 20),
        ("6.8", "Verificación de Persistencia Documental MongoDB", 21),
        ("6.9", "Verificación de Salud de la API y Swagger UI", 22),
        ("7.", "PROCEDIMIENTO PASO A PASO DE COMPILACIÓN E INSTALACIÓN DE ANDROID", 23),
        ("7.1", "Configuración del SDK de Android y local.properties", 23),
        ("7.2", "Configuración de Conectividad en NetworkModule.kt y Reverse Proxy con ADB", 24),
        ("7.3", "Configuración de Seguridad de Red (network_security_config.xml)", 25),
        ("7.4", "Compilación Determinista de APK Debug vía Gradle CLI", 26),
        ("7.5", "Instalación en Dispositivo Físico o Emulador vía ADB", 27),
        ("7.6", "Configuración Quirúrgica de Permisos Especiales en Android 13/14/15", 28),
        ("8.", "BATERÍA COMPLETA DE PRUEBAS DE HUMO (SMOKE TESTS) Y VALIDACIÓN INTEGRAL", 29),
        ("8.1", "Introducción y Preparación de Variables de Prueba", 29),
        ("8.2", "Prueba 1: Sonda de Salud del Backend y Conexión MySQL", 30),
        ("8.3", "Prueba 2: Registro de Usuario Paciente", 31),
        ("8.4", "Prueba 3: Autenticación OAuth2 y Emisión de Token JWT", 32),
        ("8.5", "Prueba 4: Alta de Medicamento con Control de Stock", 33),
        ("8.6", "Prueba 5: Programación de Tratamiento y Recordatorio de Tomas de Medicamentos", 34),
        ("8.7", "Prueba 6: Consulta de Agenda Diaria de Tomas de Medicamentos", 35),
        ("8.8", "Prueba 7: Confirmación Transaccional de Toma de Medicamentos", 36),
        ("8.9", "Prueba 8: Posposición de Toma de Medicamentos con Límite de 2 Snoozes", 37),
        ("8.10", "Prueba 9: Registro de Omisión Justificada de Toma de Medicamentos", 38),
        ("8.11", "Prueba 10: Auditoría Transaccional en Base de Datos MySQL", 39),
        ("8.12", "Prueba 11: Consulta de Métricas de Adherencia y Racha de Honor", 40),
        ("9.", "MATRIZ DE RESOLUCIÓN DE INCIDENCIAS (TROUBLESHOOTING DE DESPLIEGUE)", 41)
    ]
    add_native_toc(doc, toc_items)
    
    # --------------------------------------------------------------------------
    # 1. OBJETIVOS DEL SISTEMA Y DEL MANUAL DE INSTALACIÓN
    # --------------------------------------------------------------------------
    add_section_heading(doc, "1. OBJETIVOS DEL SISTEMA Y DEL MANUAL DE INSTALACIÓN", level=1)
    
    add_section_heading(doc, "1.1 Objetivo General de Despliegue", level=2)
    add_body_p(
        doc,
        "Proporcionar una guía técnica, quirúrgica, reproducible y estandarizada para la instalación, configuración, "
        "orquestación y verificación operativa de la totalidad de los componentes que integran el ecosistema MedReminder AI. "
        "El presente manual detalla el aprovisionamiento de la infraestructura multicontenedor mediante Docker Compose "
        "(FastAPI ASGI, motor relacional MySQL 8.0, base documental MongoDB 6.0, y herramientas visuales Adminer y Mongo-Express), "
        "la validación del esquema relacional DDL para el seguimiento riguroso de las tomas de medicamentos, y la compilación, "
        "firma e instalación del cliente móvil nativo Android con Jetpack Compose en emuladores oficiales o terminales físicos."
    )
    
    add_section_heading(doc, "1.2 Objetivos Específicos de Infraestructura, DevOps y Resiliencia", level=2)
    add_body_p(
        doc,
        "1. Orquestación Inmediata con Docker Compose: Configurar y levantar el stack completo de servicios garantizando el "
        "aislamiento de redes virtuales bridged, persistencia mediante volúmenes con nombre y resolución interna por nombre de servicio.\n\n"
        "2. Inicialización Controlada de Persistencia: Montar y ejecutar automáticamente el script 01_schema.sql al inicializar MySQL, "
        "validando que las tablas usuario, medicamento, tratamiento, recordatorio y la bitácora inmutable historial_toma se creen con sus "
        "claves foráneas, índices compuestos y restricciones de integridad referencial para el registro de tomas de medicamentos.\n\n"
        "3. Conmutación Dinámica de Red Móvil: Configurar el cliente Android en NetworkModule.kt para resolver la dirección IP candidata "
        "de la máquina anfitriona (ej: 192.168.0.228) con conmutador automático de fallback rápido ante pérdida de enlace en la LAN.\n\n"
        "4. Compilación Determinista de Android: Ejecutar el pipeline de construcción con Gradle Wrapper (./gradlew assembleDebug) sobre "
        "OpenJDK 17 y Android SDK 34/35, asegurando la generación íntegra del APK ejecutable.\n\n"
        "5. Concesión de Permisos Críticos del SO: Garantizar la configuración de permisos del sistema operativo Android para "
        "SCHEDULE_EXACT_ALARM y POST_NOTIFICATIONS, además de la exención de optimizaciones agresivas de batería (Doze mode) para "
        "asegurar que las tomas de medicamentos se notifiquen con exactitud cronométrica.\n\n"
        "6. Batería Exhaustiva de Pruebas de Humo: Proporcionar solicitudes curl reproducibles con payloads y respuestas JSON completas, "
        "verificando desde la sonda de salud hasta el ciclo transaccional de confirmación, posposición y omisión de tomas de medicamentos."
    )
    
    # --------------------------------------------------------------------------
    # 2. MARCO PEAS DE INFRAESTRUCTURA Y DESPLIEGUE
    # --------------------------------------------------------------------------
    add_section_heading(doc, "2. MARCO PEAS DE INFRAESTRUCTURA Y DESPLIEGUE", level=1, page_break_before=True)
    
    add_section_heading(doc, "2.1 El Entorno de Despliegue como Agente de Operaciones", level=2)
    add_body_p(
        doc,
        "La puesta en marcha, orquestación y mantenimiento del ecosistema MedReminder AI se conceptualiza formalmente como un "
        "Agente Inteligente de Infraestructura y Entrega Continua, cuyas responsabilidades operativas se estructuran bajo las "
        "cuatro dimensiones del marco PEAS (Performance, Environment, Actuators, Sensors):"
    )
    
    peas_deploy_data = {
        "performance": (
            "• Tiempo de Arranque de Contenedores: T_up < 45 segundos para el stack completo (FastAPI, MySQL, Mongo).\n"
            "• Disponibilidad del Backend: Uptime ≥ 99.9% en pruebas de carga local.\n"
            "• Latencia de Sincronización: T_resp ≤ 50 ms en endpoints de consulta de tomas de medicamentos.\n"
            "• Cero Errores DDL: 100% de tablas y restricciones aplicadas exitosamente en la primera inicialización.\n"
            "• Precisión de Notificaciones: Disparo de alarmas en Android con desviación ≤ 500 ms respecto a la hora programada."
        ),
        "performance_metrics": "T_up < 45 s\nUptime ≥ 99.9%\nLatencia < 50 ms\nDDL Success = 100%\nJitter ≤ 500 ms",
        "environment": (
            "• Estación de trabajo de desarrollo (macOS Sonoma/Sequoia en Apple Silicon o Intel, Linux Ubuntu 22.04+, Windows 11 WSL2).\n"
            "• Motor Docker Engine 24.0+ y Docker Compose v2.20+.\n"
            "• Red local Wi-Fi 802.11ac/ax o red virtual de emulador Android (puente 10.0.2.2).\n"
            "• Dispositivo físico Android (USB debugging habilitado) o Emulador Pixel 7 con Google APIs (API 34/35)."
        ),
        "environment_metrics": "Docker Engine 24+\nRed LAN / Emulador\nAndroid API 34-35\nOpenJDK 17 LTS",
        "actuadores": (
            "• Gestor Docker Compose ejecutando comandos de compilación de imágenes, arranque de contenedores y montaje de volúmenes.\n"
            "• Motor Gradle Wrapper (gradlew) para compilación de bytecode Kotlin, procesamiento de recursos y firma de APK debug.\n"
            "• Herramienta Android Debug Bridge (adb) para transferencia de APK, reversión de puertos TCP y concesión de permisos vía CLI.\n"
            "• Cliente MySQL CLI para inspección y validación de tablas y transacciones relacionales."
        ),
        "actuadores_metrics": "docker compose CLI\ngradlew assembleDebug\nadb install / pm grant\nmysql client CLI",
        "sensores": (
            "• Sondas de salud de Docker (Healthchecks HTTP en /health/db).\n"
            "• Socket listeners TCP en puertos 8000 (API), 3306 (MySQL), 27017 (Mongo), 8080 (Adminer).\n"
            "• Logs unificados de stdout y stderr capturados mediante docker compose logs -f.\n"
            "• Registros de compilación de Gradle y salida en tiempo real de Android Logcat."
        ),
        "sensores_metrics": "Healthchecks HTTP\nSockets TCP escuchando\nLogs Docker unificados\nAndroid Logcat"
    }
    add_peas_section(doc, peas_deploy_data, intro_text="", caption="Tabla 2.1: Matriz Operativa PEAS de Infraestructura y Despliegue")
    
    # --------------------------------------------------------------------------
    # 3. TABLAS DE VERDAD DE VERIFICACIÓN DE INSTALACIÓN Y DESPLIEGUE (SOLO 'V' Y 'F')
    # --------------------------------------------------------------------------
    add_section_heading(doc, "3. TABLAS DE VERDAD DE VERIFICACIÓN DE INSTALACIÓN Y DESPLIEGUE", level=1, page_break_before=True)
    
    add_callout(
        doc,
        "Las condiciones que determinan si el despliegue es completamente operativo y apto para registrar tomas de medicamentos "
        "se formalizan mediante tablas de verdad deductivas evaluadas exclusivamente con los valores booleanos 'V' (Verdadero) y 'F' (Falso).",
        callout_type="arch",
        title="VERIFICACIÓN DEDUCTIVA DEL DESPLIEGUE"
    )
    
    add_section_heading(doc, "3.1 Condiciones de Arranque de Microservicios Backend", level=2)
    add_body_p(
        doc,
        "El backend FastAPI solo puede considerarse en estado 'Listo' (Backend_Listo) si concurren simultáneamente las cuatro "
        "condiciones de infraestructura:\n\n"
        "• dk: El daemon de Docker se encuentra activo y respondiendo (docker info == 0).\n"
        "• my: El contenedor de MySQL superó el healthcheck inicial y acepta conexiones TCP en puerto 3306.\n"
        "• mo: El contenedor de MongoDB está inicializado y autenticado en puerto 27017.\n"
        "• pf: El puerto 8000 del host está libre de conflictos con otros procesos locales.\n\n"
        "Predicado formal: Backend_Listo ↔ (dk ∧ my ∧ mo ∧ pf)"
    )
    
    i1_headers = ["dk (Docker)", "my (MySQL)", "mo (Mongo)", "pf (Puerto)", "Backend_Listo", "Diagnóstico Operativo de Despliegue"]
    i1_rows = [
        ["V", "V", "V", "V", "V", "Despliegue Exitoso: Backend FastAPI operativo en http://localhost:8000/docs"],
        ["V", "V", "V", "F", "F", "Fallo de Puerto: Conflicto en puerto 8000; liberar puerto o cambiar API_PORT"],
        ["V", "V", "F", "V", "F", "Fallo de Mongo: Contenedor mongodb caído; revisar logs con docker compose logs mongo"],
        ["V", "F", "V", "V", "F", "Fallo de MySQL: Base relacional no lista; verificar inicialización de 01_schema.sql"],
        ["F", "V", "V", "V", "F", "Fallo de Docker: Daemon detenido; iniciar Docker Desktop o servicio dockerd"],
        ["F", "F", "F", "F", "F", "Fallo Crítico Total: Ningún servicio de infraestructura está activo"]
    ]
    add_truth_table(doc, i1_headers, i1_rows, "Tabla 3.1: Verificación de Arranque de Microservicios Backend (Tabla de Verdad 1)", [1.0, 1.0, 1.0, 1.0, 1.2, 2.3])
    
    add_section_heading(doc, "3.2 Condiciones de Conectividad Móvil y Conmutación de IP", level=2)
    add_body_p(
        doc,
        "La comunicación entre el dispositivo móvil Android y el backend FastAPI depende de tres variables proposicionales:\n\n"
        "• red: El smartphone cuenta con conexión activa a la misma subred Wi-Fi que el servidor host.\n"
        "• ip_ok: La dirección IP candidata configurada en NetworkModule.kt coincide con la IP real del servidor.\n"
        "• fw_ok: El firewall del sistema operativo anfitrión permite tráfico entrante en el puerto 8000.\n\n"
        "Predicado de conectividad: Conexión_Exitosa ↔ (red ∧ ip_ok ∧ fw_ok)"
    )
    
    i2_headers = ["red (Wi-Fi)", "ip_ok (IP Coincide)", "fw_ok (Firewall)", "Conexión_Exitosa", "Comportamiento del Aplicativo Android"]
    i2_rows = [
        ["V", "V", "V", "V", "Sincronización Total: Tomas de medicamentos se sincronizan en tiempo real con MySQL"],
        ["V", "V", "F", "F", "Bloqueo por Firewall: Timeout de conexión; habilitar regla en macOS/Windows Defender"],
        ["V", "F", "V", "F", "IP Errónea: Conmutador inteligente activa fallback rápido hacia emulador o snackbar"],
        ["F", "V", "V", "F", "Sin Red: App opera en modo offline; alarmas locales siguen sonando por RTC"],
        ["F", "F", "F", "F", "Desconexión Total: App aislada en caché local de tomas de medicamentos"]
    ]
    add_truth_table(doc, i2_headers, i2_rows, "Tabla 3.2: Conectividad Móvil y Conmutación de Red (Tabla de Verdad 2)", [1.1, 1.2, 1.2, 1.4, 2.6])
    
    add_section_heading(doc, "3.3 Requisitos de Activación de Alarmas Locales en Android", level=2)
    add_body_p(
        doc,
        "Para que las tomas de medicamentos suenen puntualmente en Android 12+ (API 31 a 35), el sistema operativo exige "
        "tres autorizaciones formales independientes:\n\n"
        "• p_exact: Permiso SCHEDULE_EXACT_ALARM otorgado en Ajustes del Sistema.\n"
        "• p_notif: Permiso POST_NOTIFICATIONS autorizado por el usuario en el diálogo inicial.\n"
        "• bat_ex: Optimización de batería configurada como 'Sin restricciones' para la aplicación.\n\n"
        "Predicado de confiabilidad: Alarma_Confiable ↔ (p_exact ∧ p_notif ∧ bat_ex)"
    )
    
    i3_headers = ["p_exact", "p_notif", "bat_ex", "Alarma_Confiable", "Riesgo Clínico y Efecto Operativo"]
    i3_rows = [
        ["V", "V", "V", "V", "Confiabilidad Máxima: La alarma suena y despierta el teléfono con precisión absoluta"],
        ["V", "V", "F", "F", "Riesgo Moderado: Doze mode puede diferir la alarma si el teléfono pasa horas inmóvil"],
        ["V", "F", "V", "F", "Fallo Visual: La alarma se programa pero la notificación Heads-Up queda bloqueada"],
        ["F", "V", "V", "F", "Fallo Crítico: Android degrada la alarma a inexacta (demora de hasta 15 minutos)"],
        ["F", "F", "F", "F", "Bloqueo Absoluto: Banner bloqueante fijo en pantalla exigiendo configuración"]
    ]
    add_truth_table(doc, i3_headers, i3_rows, "Tabla 3.3: Requisitos de Activación de Alarmas Locales en Android (Tabla de Verdad 3)", [1.0, 1.0, 1.0, 1.4, 3.1])
    
    add_section_heading(doc, "3.4 Integridad Referencial en la Inicialización de Persistencia Relacional", level=2)
    add_body_p(
        doc,
        "Durante el primer arranque del contenedor MySQL, el motor ejecuta los comandos del script 01_schema.sql. La integridad "
        "del modelo exige que las claves foráneas respeten la jerarquía de inserción relacional:\n\n"
        "• fk_u: La clave foránea usuario_id existe en las tablas medicamento y tratamiento.\n"
        "• fk_m: La clave foránea medicamento_id existe en tratamiento y recordatorio.\n"
        "• fk_t: La clave foránea tratamiento_id existe en la tabla recordatorio.\n"
        "• fk_r: La clave foránea recordatorio_id existe en la bitácora historial_toma.\n\n"
        "Predicado de esquema: DDL_Valido ↔ (fk_u ∧ fk_m ∧ fk_t ∧ fk_r)"
    )
    
    i4_headers = ["fk_u (Usuario)", "fk_m (Medicamento)", "fk_t (Tratamiento)", "fk_r (Recordatorio)", "DDL_Valido", "Estado del Esquema Relacional"]
    i4_rows = [
        ["V", "V", "V", "V", "V", "Esquema Íntegro: Todas las claves foráneas creadas; listo para tomas de medicamentos"],
        ["V", "V", "V", "F", "F", "Fallo en Bitácora: Tabla historial_toma no referenciada; riesgo de inconsistencia"],
        ["V", "V", "F", "V", "F", "Fallo en Recordatorios: Tabla recordatorio sin enlace a tratamiento"],
        ["V", "F", "V", "V", "F", "Fallo en Tratamientos: Tabla tratamiento sin enlace a medicamento"],
        ["F", "V", "V", "V", "F", "Fallo en Jerarquía Base: Tablas no pueden asociarse a ningún usuario"],
        ["F", "F", "F", "F", "F", "Esquema Corrupto: Fallo grave en inicialización; limpiar volumen db_data"]
    ]
    add_truth_table(doc, i4_headers, i4_rows, "Tabla 3.4: Integridad Referencial en la Inicialización de Persistencia Relacional (Tabla de Verdad 4)", [1.0, 1.0, 1.0, 1.0, 1.1, 2.4])
    
    # --------------------------------------------------------------------------
    # 4. DICCIONARIO DE VARIABLES DE CONFIGURACIÓN Y ENTORNO
    # --------------------------------------------------------------------------
    add_section_heading(doc, "4. DICCIONARIO DE VARIABLES DE CONFIGURACIÓN Y ENTORNO", level=1, page_break_before=True)
    
    add_body_p(
        doc,
        "La siguiente tabla documenta de manera exhaustiva todas las variables del archivo .env, directivas de Docker Compose, "
        "propiedades de Gradle y parámetros de red móvil que controlan la instalación y ejecución del sistema:"
    )
    
    deploy_vars = [
        {"name": "MYSQL_ROOT_PASSWORD", "type": "String Secreto", "scope": ".env / MySQL", "range": "Mínimo 8 caracteres", "desc": "Contraseña maestra para la cuenta de administración root del motor MySQL."},
        {"name": "MYSQL_DATABASE", "type": "String", "scope": ".env / MySQL", "range": "medreminder_db", "desc": "Nombre de la base de datos relacional creada automáticamente en la inicialización."},
        {"name": "MYSQL_USER", "type": "String", "scope": ".env / MySQL", "range": "meduser", "desc": "Usuario no-root con privilegios de lectura y escritura asignado al servicio backend FastAPI."},
        {"name": "MYSQL_PASSWORD", "type": "String Secreto", "scope": ".env / MySQL", "range": "Mínimo 8 caracteres", "desc": "Contraseña de autenticación para el usuario meduser de la base relacional."},
        {"name": "MYSQL_PORT", "type": "Entero (Puerto)", "scope": ".env / Docker", "range": "3306", "desc": "Puerto TCP expuesto en la máquina host para conexiones hacia la base MySQL."},
        {"name": "MYSQL_HOST", "type": "String (DNS)", "scope": ".env / FastAPI", "range": "mysql / localhost", "desc": "Nombre de host DNS interno en Docker ('mysql') o localhost para depuración fuera del contenedor."},
        {"name": "MONGO_PORT", "type": "Entero (Puerto)", "scope": ".env / Docker", "range": "27017", "desc": "Puerto TCP expuesto para el servicio MongoDB de logs de actividad no estructurada."},
        {"name": "MONGO_DATABASE", "type": "String", "scope": ".env / Mongo", "range": "medreminder_logs", "desc": "Nombre de la base de datos de MongoDB donde se persisten trazas de auditoría clínica."},
        {"name": "API_PORT", "type": "Entero (Puerto)", "scope": ".env / Docker", "range": "8000", "desc": "Puerto TCP en el host donde escucha el servidor ASGI Uvicorn con FastAPI."},
        {"name": "SECRET_KEY", "type": "String Criptográfico", "scope": ".env / FastAPI", "range": "256 bits aleatorios", "desc": "Clave simétrica secreta empleada para la firma y validación de tokens de sesión JWT."},
        {"name": "ALGORITHM", "type": "String", "scope": ".env / FastAPI", "range": "HS256", "desc": "Algoritmo de cifrado empleado para la emisión de tokens de autenticación de pacientes."},
        {"name": "ACCESS_TOKEN_EXPIRE_MINUTES", "type": "Entero", "scope": ".env / FastAPI", "range": "[60, 43200]", "desc": "Tiempo de validez de la sesión del paciente (43200 minutos = 30 días para evitar deslogueos)."},
        {"name": "ADMINER_PORT", "type": "Entero (Puerto)", "scope": ".env / Docker", "range": "8080", "desc": "Puerto TCP para la interfaz gráfica web Adminer de administración de MySQL."},
        {"name": "MONGO_EXPRESS_PORT", "type": "Entero (Puerto)", "scope": ".env / Docker", "range": "8081", "desc": "Puerto TCP para la interfaz gráfica web Mongo-Express de administración de MongoDB."},
        {"name": "CANDIDATE_IPS", "type": "Array de Strings", "scope": "NetworkModule.kt", "range": "192.168.0.x, 10.0.2.2", "desc": "Lista de direcciones IP candidatas exploradas por el conmutador dinámico de Android."},
        {"name": "CONNECT_TIMEOUT_MS", "type": "Entero (ms)", "scope": "NetworkModule.kt", "range": "1500 ms", "desc": "Tiempo máximo de espera antes de activar el fallback rápido de red en Android."},
        {"name": "compileSdk", "type": "Entero", "scope": "build.gradle.kts", "range": "35", "desc": "Versión del SDK de Android utilizada para compilar el código fuente de la app."},
        {"name": "minSdk", "type": "Entero", "scope": "build.gradle.kts", "range": "26", "desc": "Versión mínima de Android requerida para instalar la aplicación (Android 8.0 Oreo)."},
        {"name": "targetSdk", "type": "Entero", "scope": "build.gradle.kts", "range": "35", "desc": "Versión de la API de Android hacia la cual se optimiza el comportamiento del sistema."},
        {"name": "jvmTarget", "type": "String", "scope": "build.gradle.kts", "range": "17", "desc": "Versión de la máquina virtual Java compatible con el compilador de Kotlin."}
    ]
    add_variable_dictionary_table(doc, deploy_vars, "Diccionario de Configuración de Despliegue y Entorno")
    
    # --------------------------------------------------------------------------
    # 5. REQUISITOS PREVIOS DE HARDWARE Y SOFTWARE
    # --------------------------------------------------------------------------
    add_section_heading(doc, "5. REQUISITOS PREVIOS DE HARDWARE Y SOFTWARE", level=1, page_break_before=True)
    
    add_section_heading(doc, "5.1 Especificaciones Mínimas y Recomendadas de Hardware", level=2)
    hw_headers = ["Componente", "Requisito Mínimo", "Requisito Recomendado", "Propósito en MedReminder AI"]
    hw_rows = [
        ["Procesador (CPU)", "Intel Core i5 / Apple M1 (4 núcleos)", "Intel Core i7 / Apple Silicon M2/M3 (8 núcleos)", "Compilación de Gradle y virtualización Docker"],
        ["Memoria RAM", "8 GB DDR4", "16 GB o superior", "Ejecución simultánea de MySQL, Mongo, API y emulador"],
        ["Disco Duro (Almacenamiento)", "10 GB de espacio libre SSD", "25 GB de espacio libre NVMe SSD", "Imágenes Docker, volúmenes de datos y Android SDK"],
        ["Dispositivo Móvil", "Android 8.0 (API 26) con 2 GB RAM", "Android 13+ (API 33-35) con 4 GB RAM", "Ejecución de la app y prueba de tomas de medicamentos"],
        ["Conectividad de Red", "Tarjeta Wi-Fi 802.11n", "Wi-Fi 802.11ac/ax en la misma subred LAN", "Comunicación bidireccional entre Android y FastAPI"]
    ]
    add_truth_table(doc, hw_headers, hw_rows, "Tabla 5.1: Especificaciones Mínimas y Recomendadas de Hardware", [1.4, 1.6, 1.8, 2.7])
    
    add_section_heading(doc, "5.2 Matriz de Software y Dependencias de Sistema", level=2)
    sw_headers = ["Software / Herramienta", "Versión Mínima", "Versión Probada", "Función Operativa Principal"]
    sw_rows = [
        ["Docker Engine", "24.0.0", "27.2.0 (macOS/Linux)", "Motor de contenedores para microservicios"],
        ["Docker Compose", "v2.20.0", "v2.29.2", "Orquestación multicontenedor y redes bridged"],
        ["Git CLI", "2.30.0", "2.44.0", "Control de versiones y clonación de repositorio"],
        ["OpenJDK (Java JDK)", "17 LTS", "17.0.12 (Zulu/Temurin)", "Compilación de código Kotlin en Gradle"],
        ["Android Studio", "Ladybug (2024.2.1)", "Ladybug 2024.2.1 Patch 1", "IDE oficial para depuración y emuladores"],
        ["Android SDK Platform", "API 34 (UpsideDownCake)", "API 35 (VanillaIceCream)", "Compilación del framework Android y Jetpack"],
        ["Android SDK Build-Tools", "34.0.0", "35.0.0", "D8 dexer, aapt2 y firma de APK debug"],
        ["Android Debug Bridge (adb)", "34.0.4", "35.0.1", "Instalación de APK y configuración de permisos"],
        ["cURL & jq", "7.80.0 / 1.6", "8.7.1 / 1.7.1", "Ejecución e inspección de pruebas de humo"]
    ]
    add_truth_table(doc, sw_headers, sw_rows, "Tabla 5.2: Matriz de Software y Dependencias de Sistema", [1.6, 1.4, 1.6, 2.9])
    
    add_section_heading(doc, "5.3 Verificación de Entorno en Host", level=2)
    add_body_p(
        doc,
        "Antes de proceder con la clonación y levantamiento, compruebe que las herramientas fundamentales se encuentren "
        "en el PATH de su sistema ejecutando los siguientes comandos en la terminal:"
    )
    add_code_block(
        doc,
        """# 1. Comprobar Docker y Docker Compose
docker --version
# Salida esperada: Docker version 27.2.0, build 3eee6c1
docker compose version
# Salida esperada: Docker Compose version v2.29.2-desktop.2

# 2. Comprobar versión de Java JDK
java -version
# Salida esperada:
# openjdk version "17.0.12" 2024-07-16 LTS
# OpenJDK Runtime Environment Zulu17.52+17-CA (build 17.0.12+7-LTS)

# 3. Comprobar Android Debug Bridge (adb)
adb version
# Salida esperada: Android Debug Bridge version 1.0.41, Version 35.0.1-11580240""",
        caption="Comandos de verificación preliminar del entorno de la estación de trabajo"
    )
    
    # --------------------------------------------------------------------------
    # 6. PROCEDIMIENTO PASO A PASO DE DESPLIEGUE DEL BACKEND (DOCKER)
    # --------------------------------------------------------------------------
    add_section_heading(doc, "6. PROCEDIMIENTO PASO A PASO DE DESPLIEGUE DEL BACKEND (DOCKER)", level=1, page_break_before=True)
    
    add_section_heading(doc, "6.1 Clonación y Verificación del Árbol de Trabajo", level=2)
    add_body_p(
        doc,
        "Abra una terminal y clone el repositorio oficial o diríjase a su directorio de trabajo local. Verifique que los "
        "directorios estructurales se encuentren intactos:"
    )
    add_code_block(
        doc,
        """# Acceder al directorio raíz del proyecto
cd /Users/4strob0y/Developer/MedReminderAI

# Verificar estructura de carpetas
ls -la
# Salida esperada en terminal:
# drwxr-xr-x  14 usuario  staff   448 Oct 21 00:15 .
# drwxr-xr-x   9 usuario  staff   288 Oct 21 00:10 android/
# drwxr-xr-x   7 usuario  staff   224 Oct 21 00:10 backend/
# drwxr-xr-x   5 usuario  staff   160 Oct 21 00:10 db/
# drwxr-xr-x  12 usuario  staff   384 Oct 21 00:15 docs/
# -rw-r--r--   1 usuario  staff  1950 Oct 21 00:10 docker-compose.yml
# -rw-r--r--   1 usuario  staff   420 Oct 21 00:10 .env.example
# drwxr-xr-x   8 usuario  staff   256 Oct 21 00:10 scripts/""",
        caption="Verificación del listado de directorios del repositorio mediante comando ls -la"
    )
    
    add_section_heading(doc, "6.2 Configuración Quirúrgica del Archivo .env", level=2)
    add_body_p(
        doc,
        "Copie la plantilla .env.example para crear el archivo definitivo de entorno .env. Este archivo almacena las credenciales "
        "críticas para MySQL, MongoDB y la firma de tokens JWT:"
    )
    add_code_block(
        doc,
        """# Copiar la plantilla base de entorno
cp .env.example .env

# Contenido exhaustivo y verificado de .env:
# ------------------------------------------------------------------------------
# Configuración del Motor Relacional MySQL
# ------------------------------------------------------------------------------
MYSQL_ROOT_PASSWORD=medrootpwd
MYSQL_DATABASE=medreminder_db
MYSQL_USER=meduser
MYSQL_PASSWORD=medpassword
MYSQL_PORT=3306

# ------------------------------------------------------------------------------
# Configuración del Motor Documental MongoDB
# ------------------------------------------------------------------------------
MONGO_PORT=27017
MONGO_DATABASE=medreminder_logs

# ------------------------------------------------------------------------------
# Configuración de la API FastAPI y Seguridad Criptográfica
# ------------------------------------------------------------------------------
API_PORT=8000
SECRET_KEY=medreminder_ai_secret_jwt_key_2026_production_secure_entropy_key_512
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=43200

# ------------------------------------------------------------------------------
# Puertos para Herramientas Visuales de Base de Datos (Perfil tools)
# ------------------------------------------------------------------------------
ADMINER_PORT=8080
MONGO_EXPRESS_PORT=8081""",
        caption="Archivo .env completamente documentado y listo para ejecución"
    )
    
    add_section_heading(doc, "6.3 Construcción de Imágenes con Docker Compose", level=2)
    add_body_p(
        doc,
        "Compile las imágenes de microservicios sin caché previa para garantizar que se descarguen las dependencias "
        "actualizadas de Python y que la compilación sea limpia:"
    )
    add_code_block(
        doc,
        """# Construir la imagen del servicio backend FastAPI
docker compose build --no-cache

# Salida esperada en terminal:
# [+] Building 14.8s (12/12) FINISHED
#  => [internal] load build definition from Dockerfile
#  => => transferring dockerfile: 520B
#  => [internal] load .dockerignore
#  => [internal] load metadata for docker.io/library/python:3.11-slim
#  => [1/5] FROM docker.io/library/python:3.11-slim@sha256:4a38...
#  => [2/5] WORKDIR /app
#  => [3/5] COPY requirements.txt .
#  => [4/5] RUN pip install --no-cache-dir -r requirements.txt
#  => [5/5] COPY . .
#  => exporting to image
#  => => naming to docker.io/library/medreminderai-api:latest""",
        caption="Compilación sin caché de la imagen del backend con Docker Compose"
    )
    
    add_section_heading(doc, "6.4 Lanzamiento y Orquestación del Stack de Microservicios", level=2)
    add_body_p(
        doc,
        "Inicie los servicios en segundo plano. Docker Compose creará la red virtual bridged medreminderai_default, "
        "los volúmenes persistentes y levantará los contenedores en el orden estricto de dependencias:"
    )
    add_code_block(
        doc,
        """# Levantar stack multicontenedor en modo detached (-d)
docker compose up -d

# Salida esperada en terminal:
# [+] Running 4/4
#  [OK] Network medreminderai_default     Created
#  [OK] Volume "medreminderai_db_data"    Created
#  [OK] Volume "medreminderai_mongo_data" Created
#  [OK] Container medreminder-mysql       Started
#  [OK] Container medreminder-mongo       Started
#  [OK] Container medreminder-api         Started""",
        caption="Lanzamiento de los contenedores en segundo plano"
    )
    
    add_section_heading(doc, "6.5 Inspección del Estado de Contenedores y Sockets TCP", level=2)
    add_body_p(
        doc,
        "Verifique que todos los contenedores reporten un estado saludable ('Up' o 'healthy') y que los puertos TCP "
        "estén vinculados correctamente al host:"
    )
    add_code_block(
        doc,
        """# Consultar estado de los procesos orquestados
docker compose ps""",
        caption="Comando de inspección de estado de contenedores"
    )
    
    ps_headers = ["Contenedor", "Servicio", "Estado del Proceso", "Mapeo de Puerto TCP"]
    ps_rows = [
        ["medreminder-api", "api", "Up (healthy)", "0.0.0.0:8000 → 8000/tcp"],
        ["medreminder-mysql", "mysql", "Up (healthy)", "0.0.0.0:3306 → 3306/tcp, 33060/tcp"],
        ["medreminder-mongo", "mongo", "Up", "0.0.0.0:27017 → 27017/tcp"]
    ]
    add_truth_table(doc, ps_headers, ps_rows, "Tabla 6.1: Estado Operativo y Mapeo de Puertos de los Contenedores", [1.8, 1.2, 1.5, 2.0])
    
    add_section_heading(doc, "6.6 Inspección de Logs Unificados del Sistema", level=2)
    add_body_p(
        doc,
        "Examine los registros unificados para confirmar que el servidor ASGI Uvicorn y el motor MySQL inicializaron sin errores:"
    )
    add_code_block(
        doc,
        """# Monitorear logs de inicialización
docker compose logs -f api mysql

# Salida esperada en terminal:
# medreminder-mysql  | 2026-10-21 00:20:00 [Server] /usr/sbin/mysqld: ready for connections. Version: '8.0.36'
# medreminder-mysql  | 2026-10-21 00:20:01 [Entrypoint] Executing 01_schema.sql... Done.
# medreminder-api    | INFO:     Started server process [1]
# medreminder-api    | INFO:     Waiting for application startup.
# medreminder-api    | INFO:     Application startup complete.
# medreminder-api    | INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)""",
        caption="Logs unificados de inicio de MySQL y FastAPI Uvicorn"
    )
    
    add_section_heading(doc, "6.7 Verificación de Inicialización de Persistencia Relacional MySQL", level=2)
    add_body_p(
        doc,
        "Conéctese directamente al contenedor de MySQL mediante el cliente de línea de comandos para corroborar que "
        "el script 01_schema.sql haya generado todas las tablas requeridas para el ciclo de tomas de medicamentos:"
    )
    add_code_block(
        doc,
        """# Conectar a MySQL dentro del contenedor y listar tablas
docker compose exec mysql mysql -u meduser -pmedpassword medreminder_db -e "SHOW TABLES;"

# Describir la estructura de la tabla de recordatorios de tomas de medicamentos
docker compose exec mysql mysql -u meduser -pmedpassword medreminder_db -e "DESCRIBE recordatorio;" """,
        caption="Verificación por CLI del esquema relacional DDL en MySQL"
    )
    
    tbl_headers = ["Tabla Relacional", "Propósito en el Sistema Clínico", "Estado Esperado"]
    tbl_rows = [
        ["contacto_apoyo", "Gestión de red familiar y alertas de emergencia", "Creada (InnoDB)"],
        ["historial_toma", "Auditoría inmutable de tomas de medicamentos", "Creada (InnoDB)"],
        ["medicamento", "Catálogo maestro e inventario de botiquín", "Creada (InnoDB)"],
        ["recordatorio", "Planificación temporal de tomas de medicamentos", "Creada (InnoDB)"],
        ["tratamiento", "Prescripción médica y posología asociada", "Creada (InnoDB)"],
        ["usuario", "Cuentas de usuario y credenciales seguras", "Creada (InnoDB)"]
    ]
    add_truth_table(doc, tbl_headers, tbl_rows, "Tabla 6.2: Tablas Relacionales Verificadas en MySQL 8.0", [2.0, 3.2, 1.5])
    
    add_section_heading(doc, "6.8 Verificación de Persistencia Documental MongoDB", level=2)
    add_body_p(
        doc,
        "Si desea verificar la disponibilidad del motor NoSQL MongoDB o inspeccionar las bases de datos de forma visual, "
        "active el perfil tools para desplegar Adminer y Mongo-Express:"
    )
    add_code_block(
        doc,
        """# Levantar herramientas visuales de administración de base de datos
docker compose --profile tools up -d

# Puertos de acceso en navegador web:
# • Adminer (MySQL):        http://localhost:8080 (Servidor: mysql, Usuario: meduser, DB: medreminder_db)
# • Mongo-Express (Mongo):  http://localhost:8081""",
        caption="Despliegue de herramientas visuales de persistencia"
    )
    
    add_section_heading(doc, "6.9 Verificación de Salud de la API y Swagger UI", level=2)
    add_body_p(
        doc,
        "Compruebe que el endpoint de salud de la base de datos responda de manera óptima y examine la interfaz interactiva "
        "de OpenAPI ingresando desde su navegador web:\n\n"
        "• Healthcheck: http://localhost:8000/health/db : Responde {\"status\":\"ok\",\"database\":\"connected\"}.\n"
        "• Swagger UI: http://localhost:8000/docs : Interfaz gráfica interactiva de pruebas de endpoints.\n"
        "• ReDoc: http://localhost:8000/redoc : Especificación técnica formal OpenAPI 3.0."
    )
    
    # --------------------------------------------------------------------------
    # 7. PROCEDIMIENTO PASO A PASO DE COMPILACIÓN E INSTALACIÓN DE ANDROID
    # --------------------------------------------------------------------------
    add_section_heading(doc, "7. PROCEDIMIENTO PASO A PASO DE COMPILACIÓN E INSTALACIÓN DE ANDROID", level=1, page_break_before=True)
    
    add_section_heading(doc, "7.1 Configuración del SDK de Android y local.properties", level=2)
    add_body_p(
        doc,
        "Acceda al subdirectorio android y verifique la existencia del archivo local.properties con la ruta exacta hacia su "
        "Android SDK local. En macOS se localiza habitualmente en el directorio Library:"
    )
    add_code_block(
        doc,
        """# Acceder a la carpeta del proyecto Android
cd /Users/4strob0y/Developer/MedReminderAI/android

# Crear o verificar local.properties
cat << 'EOF' > local.properties
sdk.dir=/Users/4strob0y/Library/Android/sdk
EOF""",
        caption="Configuración de la ruta del SDK de Android en local.properties"
    )
    
    add_section_heading(doc, "7.2 Configuración de Conectividad en NetworkModule.kt y Reverse Proxy con ADB", level=2)
    add_body_p(
        doc,
        "El módulo de red en android/app/src/main/java/com/medreminder/ai/data/remote/NetworkModule.kt cuenta con una lista de "
        "IPs candidatas que se exploran en orden de prioridad. Para pruebas con cable USB físico, puede ejecutar un tunelado "
        "inverso con ADB para mapear el puerto 8000 del teléfono hacia la computadora anfitriona:"
    )
    add_code_block(
        doc,
        """# Obtener la IP local de la computadora anfitriona en red Wi-Fi (macOS):
ipconfig getifaddr en0
# Salida: 192.168.0.228

# Configuración recomendada en NetworkModule.kt:
# private const val PRIMARY_HOST = "192.168.0.228" // IP LAN Wi-Fi
# private const val EMULATOR_HOST = "10.0.2.2"     // Loopback para emuladores

# Alternativa mediante cable USB (Reverse Proxy de ADB):
adb reverse tcp:8000 tcp:8000
# Salida: 8000 (Permite al smartphone acceder al backend mediante http://localhost:8000)""",
        caption="Configuración de IP de red local y reverse proxy mediante ADB"
    )
    
    add_section_heading(doc, "7.3 Configuración de Seguridad de Red (network_security_config.xml)", level=2)
    add_body_p(
        doc,
        "Dado que el entorno de desarrollo y pruebas opera bajo protocolo HTTP en red local (sin certificado SSL formal), "
        "el archivo android/app/src/main/res/xml/network_security_config.xml habilita explícitamente el tráfico de texto claro "
        "para evitar la excepción CLEAN_TEXT_NOT_PERMITTED:"
    )
    add_code_block(
        doc,
        """<?xml version="1.0" encoding="utf-8"?>
<network-security-config>
    <domain-config cleartextTrafficPermitted="true">
        <domain includeSubdomains="true">192.168.0.228</domain>
        <domain includeSubdomains="true">10.0.2.2</domain>
        <domain includeSubdomains="true">localhost</domain>
        <domain includeSubdomains="true">127.0.0.1</domain>
    </domain-config>
</network-security-config>""",
        caption="Configuración de seguridad de red para permitir tráfico HTTP de desarrollo"
    )
    
    add_section_heading(doc, "7.4 Compilación Determinista de APK Debug vía Gradle CLI", level=2)
    add_body_p(
        doc,
        "Compile el ejecutable APK mediante Gradle Wrapper asegurando el uso de JDK 17:"
    )
    add_code_block(
        doc,
        """# Otorgar permisos de ejecución al wrapper de Gradle
chmod +x gradlew

# Compilar artefacto APK en modo debug con traza completa
./gradlew assembleDebug --stacktrace

# Salida esperada en terminal:
# > Task :app:compileDebugKotlin
# > Task :app:compileDebugJavaWithJavac
# > Task :app:mergeDebugNativeLibs
# > Task :app:packageDebug
# BUILD SUCCESSFUL in 34s
# 38 actionable tasks: 38 executed

# El archivo binario generado se ubica en:
# android/app/build/outputs/apk/debug/app-debug.apk""",
        caption="Compilación determinista del APK con Gradle Wrapper"
    )
    
    add_section_heading(doc, "7.5 Instalación en Dispositivo Físico o Emulador vía ADB", level=2)
    add_body_p(
        doc,
        "Conecte el dispositivo móvil mediante cable USB con la depuración habilitada o inicie el emulador en Android Studio. "
        "Luego transfiera e instale el paquete binario:"
    )
    add_code_block(
        doc,
        """# Listar dispositivos y emuladores detectados
adb devices
# Salida esperada:
# List of devices attached
# emulator-5554    device

# Instalar el paquete APK sobreescribiendo instalaciones anteriores (-r)
adb install -r app/build/outputs/apk/debug/app-debug.apk
# Salida esperada:
# Performing Streamed Install
# Success

# Iniciar la actividad principal de la aplicación en pantalla
adb shell am start -n com.medreminder.ai/.MainActivity
# Salida esperada:
# Starting: Intent { cmp=com.medreminder.ai/.MainActivity }""",
        caption="Instalación y lanzamiento automatizado del paquete APK mediante ADB"
    )
    if os.path.exists("docs/screenshots/01_login.png"):
        add_figure_image(doc, "docs/screenshots/01_login.png", "Figura 1: Pantalla inicial de bienvenida y login tras el primer lanzamiento de la app instalada", 3.0)
        
    add_section_heading(doc, "7.6 Configuración Quirúrgica de Permisos Especiales en Android 13/14/15", level=2)
    add_body_p(
        doc,
        "Para garantizar que el hardware del dispositivo despierte puntualmente y emita la notificación sonora en cada una de "
        "las tomas de medicamentos programadas, ejecute los siguientes comandos por ADB o actívelos en el menú de Ajustes:"
    )
    add_code_block(
        doc,
        """# 1. Otorgar permiso de notificaciones (Android 13+ / API 33+)
adb shell pm grant com.medreminder.ai android.permission.POST_NOTIFICATIONS

# 2. Habilitar permiso de Alarmas Exactas (Android 14+ / API 34+)
adb shell cmd appops set com.medreminder.ai SCHEDULE_EXACT_ALARM allow

# 3. Eximir a MedReminder AI del modo Doze y optimización de batería
adb shell dumpsys deviceidle whitelist +com.medreminder.ai
# Salida: Added: com.medreminder.ai

# 4. Comprobar que la app figura en la lista blanca de ahorro de energía
adb shell dumpsys deviceidle whitelist | grep medreminder
# Salida esperada: com.medreminder.ai""",
        caption="Concesión de permisos críticos de alarma y batería mediante ADB"
    )
    
    # --------------------------------------------------------------------------
    # 8. BATERÍA COMPLETA DE PRUEBAS DE HUMO (SMOKE TESTS) Y VALIDACIÓN INTEGRAL
    # --------------------------------------------------------------------------
    add_section_heading(doc, "8. BATERÍA COMPLETA DE PRUEBAS DE HUMO (SMOKE TESTS) Y VALIDACIÓN INTEGRAL", level=1, page_break_before=True)
    
    add_section_heading(doc, "8.1 Introducción y Preparación de Variables de Prueba", level=2)
    add_body_p(
        doc,
        "Las pruebas de humo permiten certificar que todos los microservicios backend, la base de datos relacional MySQL y el motor "
        "de lógica proposicional se encuentran en perfecto estado operativo. Cada prueba documenta la solicitud curl exacta "
        "y la respuesta JSON completa retornada por el servidor:"
    )
    
    # Prueba 1: Healthcheck
    add_section_heading(doc, "8.2 Prueba 1: Sonda de Salud del Backend y Conexión MySQL", level=2)
    add_body_p(
        doc,
        "Verifica que el servidor FastAPI Uvicorn mantenga una conexión activa y saludable contra la base de datos relacional MySQL:"
    )
    add_code_block(
        doc,
        """# Solicitud HTTP:
curl -s -X GET http://localhost:8000/health/db

# Respuesta JSON del servidor (Código HTTP 200 OK):
{
  "status": "ok",
  "database": "connected",
  "mysql_version": "8.0.36",
  "active_pool_connections": 2
}""",
        caption="Prueba de humo 1: Verificación de salud y conectividad de base de datos"
    )
    
    # Prueba 2: Registro
    add_section_heading(doc, "8.3 Prueba 2: Registro de Usuario Paciente", level=2)
    add_body_p(
        doc,
        "Registra un nuevo usuario en la base de datos relacional con hashing bcrypt de contraseña:"
    )
    add_code_block(
        doc,
        """# Solicitud HTTP:
curl -s -X POST http://localhost:8000/auth/register \\
  -H "Content-Type: application/json" \\
  -d '{
    "nombre_completo": "Samuel Gutierrez Ugalde",
    "correo": "samuel.gutierrez@utvt.edu.mx",
    "password": "Password123!"
  }'

# Respuesta JSON del servidor (Código HTTP 201 Created):
{
  "id": 1,
  "nombre_completo": "Samuel Gutierrez Ugalde",
  "correo": "samuel.gutierrez@utvt.edu.mx",
  "activo": true,
  "fecha_creacion": "2026-10-21T08:00:00Z"
}""",
        caption="Prueba de humo 2: Alta de nuevo paciente en el sistema"
    )
    
    # Prueba 3: Login
    add_section_heading(doc, "8.4 Prueba 3: Autenticación OAuth2 y Emisión de Token JWT", level=2)
    add_body_p(
        doc,
        "Autentica las credenciales del usuario y captura el token Bearer JWT para autorizar las solicitudes subsiguientes:"
    )
    add_code_block(
        doc,
        """# Solicitud HTTP:
curl -s -X POST http://localhost:8000/auth/login \\
  -H "Content-Type: application/x-www-form-urlencoded" \\
  -d "username=samuel.gutierrez@utvt.edu.mx&password=Password123!"

# Respuesta JSON del servidor (Código HTTP 200 OK):
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxIiwiaXNzIjoibWVkcmVtaW5kZXJhaSIsImV4cCI6MTc2Mzg5MjAwMH0.d9f8a3c...",
  "token_type": "bearer",
  "user_id": 1,
  "expires_in": 2592000
}

# Captura automatizada del token en variable de entorno de terminal:
TOKEN=$(curl -s -X POST http://localhost:8000/auth/login \\
  -d "username=samuel.gutierrez@utvt.edu.mx&password=Password123!" | grep -o '"access_token":"[^"]*' | cut -d'"' -f4)""",
        caption="Prueba de humo 3: Autenticación y captura de token de sesión JWT"
    )
    
    # Prueba 4: Alta Medicamento
    add_section_heading(doc, "8.5 Prueba 4: Alta de Medicamento con Control de Stock", level=2)
    add_body_p(
        doc,
        "Crea un medicamento en el botiquín del paciente con stock inicial, umbral de reserva y validación lógica:"
    )
    add_code_block(
        doc,
        """# Solicitud HTTP:
curl -s -X POST http://localhost:8000/medicamentos \\
  -H "Authorization: Bearer $TOKEN" \\
  -H "Content-Type: application/json" \\
  -d '{
    "nombre": "Losartán",
    "dosis": "50 mg",
    "cantidad_stock": 30,
    "stock_inicial": 30,
    "stock_minimo_alerta": 5,
    "forma_farmaceutica": "comprimidos",
    "es_critico": true,
    "permite_posponer": true
  }'

# Respuesta JSON del servidor (Código HTTP 201 Created):
{
  "id": 1,
  "usuario_id": 1,
  "nombre": "Losartán",
  "dosis": "50 mg",
  "cantidad_stock": 30,
  "stock_inicial": 30,
  "stock_minimo_alerta": 5,
  "forma_farmaceutica": "comprimidos",
  "es_critico": true,
  "permite_posponer": true,
  "fecha_creacion": "2026-10-21T08:05:00Z"
}""",
        caption="Prueba de humo 4: Registro de fármaco con stock inicial en el botiquín"
    )
    
    # Prueba 5: Programación Tratamiento
    add_section_heading(doc, "8.6 Prueba 5: Programación de Tratamiento y Recordatorio de Tomas de Medicamentos", level=2)
    add_body_p(
        doc,
        "Genera un tratamiento activo y su correspondiente recordatorio diario para el ciclo de tomas de medicamentos:"
    )
    add_code_block(
        doc,
        """# Solicitud HTTP:
curl -s -X POST http://localhost:8000/tratamientos \\
  -H "Authorization: Bearer $TOKEN" \\
  -H "Content-Type: application/json" \\
  -d '{
    "medicamento_id": 1,
    "frecuencia_horas": 24,
    "fecha_inicio": "2026-10-21T08:00:00Z",
    "fecha_fin": "2026-11-20T08:00:00Z",
    "instrucciones": "Tomar un comprimido en ayunas con 200 ml de agua",
    "hora_preferida": "08:00:00"
  }'

# Respuesta JSON del servidor (Código HTTP 201 Created):
{
  "id": 1,
  "usuario_id": 1,
  "medicamento_id": 1,
  "frecuencia_horas": 24,
  "fecha_inicio": "2026-10-21T08:00:00Z",
  "fecha_fin": "2026-11-20T08:00:00Z",
  "activo": true,
  "recordatorios_generados": 30
}""",
        caption="Prueba de humo 5: Creación de tratamiento y generación de recordatorios"
    )
    
    # Prueba 6: Consulta de Agenda
    add_section_heading(doc, "8.7 Prueba 6: Consulta de Agenda Diaria de Tomas de Medicamentos", level=2)
    add_body_p(
        doc,
        "Obtiene la lista de tomas de medicamentos programadas para el día en curso filtrando por la zona horaria del paciente:"
    )
    add_code_block(
        doc,
        """# Solicitud HTTP:
curl -s -X GET "http://localhost:8000/recordatorios?tz_offset_minutes=-360" \\
  -H "Authorization: Bearer $TOKEN"

# Respuesta JSON del servidor (Código HTTP 200 OK):
[
  {
    "id": 1,
    "medicamento_id": 1,
    "medicamento_nombre": "Losartán",
    "dosis": "50 mg",
    "fecha_hora_programada": "2026-10-21T08:00:00Z",
    "estado": "pendiente",
    "veces_pospuesto": 0,
    "es_critico": true,
    "permite_posponer": true,
    "instrucciones": "Tomar un comprimido en ayunas con 200 ml de agua"
  }
]""",
        caption="Prueba de humo 6: Consulta de la agenda diaria de tomas de medicamentos"
    )
    
    # Prueba 7: Confirmar Toma de Medicamentos
    add_section_heading(doc, "8.8 Prueba 7: Confirmación Transaccional de Toma de Medicamentos", level=2)
    add_body_p(
        doc,
        "Registra la confirmación de ingesta, efectúa el descuento atómico de 1 unidad de stock y genera la bitácora inmutable:"
    )
    add_code_block(
        doc,
        """# Solicitud HTTP:
curl -s -X POST http://localhost:8000/recordatorios/1/tomar \\
  -H "Authorization: Bearer $TOKEN" \\
  -H "Content-Type: application/json" \\
  -d '{
    "hora_real_ingesta": "2026-10-21T08:06:12Z"
  }'

# Respuesta JSON del servidor (Código HTTP 200 OK):
{
  "status": "success",
  "mensaje": "Toma de medicamentos confirmada exitosamente",
  "recordatorio_id": 1,
  "nuevo_estado": "tomado",
  "medicamento_id": 1,
  "cantidad_stock_restante": 29,
  "puntos_honor_ganados": 15,
  "racha_actual_dias": 1
}""",
        caption="Prueba de humo 7: Confirmación de toma de medicamentos y descuento de stock"
    )
    
    # Prueba 8: Posponer Toma de Medicamentos
    add_section_heading(doc, "8.9 Prueba 8: Posposición de Toma de Medicamentos con Límite de 2 Snoozes", level=2)
    add_body_p(
        doc,
        "Aplica la regla formal de posposición desplazando la alarma 30 minutos e incrementando el contador de veces pospuesto:"
    )
    add_code_block(
        doc,
        """# Solicitud HTTP (asumiendo recordatorio_id = 2):
curl -s -X POST http://localhost:8000/recordatorios/2/posponer \\
  -H "Authorization: Bearer $TOKEN" \\
  -H "Content-Type: application/json" \\
  -d '{
    "minutos_desplazamiento": 30
  }'

# Respuesta JSON del servidor (Código HTTP 200 OK):
{
  "status": "success",
  "mensaje": "Alarma de toma de medicamentos pospuesta 30 minutos",
  "recordatorio_id": 2,
  "nuevo_estado": "pospuesto",
  "veces_pospuesto": 1,
  "limite_alcanzado": false,
  "nueva_fecha_hora_programada": "2026-10-21T14:30:00Z"
}""",
        caption="Prueba de humo 8: Posposición de alarma con control de límite de 2 snoozes"
    )
    
    # Prueba 9: Omitir Toma de Medicamentos
    add_section_heading(doc, "8.10 Prueba 9: Registro de Omisión Justificada de Toma de Medicamentos", level=2)
    add_body_p(
        doc,
        "Registra la omisión médica de una dosis con motivo justificado sin penalizar injustamente la racha de honor:"
    )
    add_code_block(
        doc,
        """# Solicitud HTTP:
curl -s -X POST http://localhost:8000/recordatorios/2/omitir \\
  -H "Authorization: Bearer $TOKEN" \\
  -H "Content-Type: application/json" \\
  -d '{
    "motivo": "Presencia de malestar estomacal y náuseas intensas reportadas por el paciente"
  }'

# Respuesta JSON del servidor (Código HTTP 200 OK):
{
  "status": "success",
  "mensaje": "Omisión de toma de medicamentos registrada con justificación clínica",
  "recordatorio_id": 2,
  "nuevo_estado": "omitido",
  "motivo_registrado": "Presencia de malestar estomacal y náuseas intensas reportadas por el paciente",
  "penalizacion_honor": false
}""",
        caption="Prueba de humo 9: Omisión con justificación clínica"
    )
    
    # Prueba 10: Verificación SQL
    add_section_heading(doc, "8.11 Prueba 10: Auditoría Transaccional en Base de Datos MySQL", level=2)
    add_body_p(
        doc,
        "Inspeccione las filas físicas en MySQL para corroborar la inmutabilidad de la bitácora y la consistencia del stock:"
    )
    add_code_block(
        doc,
        """# 1. Consultar bitácora historial_toma
docker compose exec mysql mysql -u meduser -pmedpassword medreminder_db \\
  -e "SELECT id, recordatorio_id, hora_real, estado_final FROM historial_toma ORDER BY id DESC LIMIT 2;"

# 2. Consultar inventario restante en medicamento
docker compose exec mysql mysql -u meduser -pmedpassword medreminder_db \\
  -e "SELECT id, nombre, cantidad_stock FROM medicamento WHERE id = 1;" """,
        caption="Prueba de humo 10: Auditoría directa de persistencia e inventario en MySQL"
    )
    
    audit_sql_headers = ["Consulta / Entidad", "Campo / Registro", "Valor Físico en BD", "Verificación de Integridad"]
    audit_sql_rows = [
        ["historial_toma", "recordatorio_id = 1", "estado_final = 'tomado'", "Confirmación nominal de tomas de medicamentos registrada."],
        ["historial_toma", "hora_real", "Timestamp UTC de auditoría", "Trazabilidad legal inmutable con fecha y hora exactas."],
        ["medicamento", "id = 1 (Losartán)", "cantidad_stock = 29", "Descuento atómico de 1 unidad comprobado (30 inicial - 1)."]
    ]
    add_truth_table(doc, audit_sql_headers, audit_sql_rows, "Tabla 8.1: Resultados de Auditoría Transaccional en MySQL", [1.8, 1.8, 1.6, 2.0])
    
    # Prueba 11: Estadísticas
    add_section_heading(doc, "8.12 Prueba 11: Consulta de Métricas de Adherencia y Racha de Honor", level=2)
    add_body_p(
        doc,
        "Consulta el balance consolidado de adherencia farmacológica, nivel de honor y mapa de calor de tomas de medicamentos:"
    )
    add_code_block(
        doc,
        """# Solicitud HTTP:
curl -s -X GET "http://localhost:8000/recordatorios/estadisticas?tz_offset_minutes=-360" \\
  -H "Authorization: Bearer $TOKEN"

# Respuesta JSON del servidor (Código HTTP 200 OK):
{
  "total_tomas_programadas": 1,
  "tomas_completadas_a_tiempo": 1,
  "tomas_pospuestas": 0,
  "tomas_omitidas": 0,
  "porcentaje_adherencia": 100.0,
  "puntos_honor_totales": 15,
  "rango_honor": "Bronce",
  "racha_dias_consecutivos": 1,
  "modo_castigo_activo": false
}""",
        caption="Prueba de humo 11: Consulta de métricas consolidadas de adherencia y honor"
    )
    
    # --------------------------------------------------------------------------
    # 9. MATRIZ DE RESOLUCIÓN DE INCIDENCIAS (TROUBLESHOOTING DE DESPLIEGUE)
    # --------------------------------------------------------------------------
    add_section_heading(doc, "9. MATRIZ DE RESOLUCIÓN DE INCIDENCIAS (TROUBLESHOOTING DE DESPLIEGUE)", level=1, page_break_before=True)
    
    add_body_p(
        doc,
        "La siguiente matriz exhaustiva proporciona el diagnóstico causa-raíz y los comandos exactos de solución "
        "para las diez incidencias más frecuentes durante el despliegue del ecosistema MedReminder AI:"
    )
    
    deploy_faq_headers = ["Incidencia Detectada", "Causa Raíz de Infraestructura", "Acción Correctiva Inmediata en Terminal"]
    deploy_faq_rows = [
        ["Error 'port is already allocated: 8000'", "Otro proceso local (ej. FastAPI previo o Node) ocupa el puerto 8000.", "Ejecute 'lsof -i :8000' y termine el proceso con 'kill -9 <PID>', o cambie API_PORT en .env."],
        ["Error 'port is already allocated: 3306'", "Un servidor MySQL local en la máquina anfitriona compite por el puerto.", "Detenga el servicio local con 'brew services stop mysql' o asigne MYSQL_PORT=3307 en .env."],
        ["MySQL en bucle 'restarting' o fallo DDL", "Permisos de escritura en volumen o datos corruptos en db_data.", "Ejecute 'docker compose down -v' para limpiar volúmenes y relance con 'docker compose up -d'."],
        ["Fallo de autenticación 'Could not validate credentials'", "Desfase horario entre cliente y host o token JWT expirado.", "Vuelva a iniciar sesión en /auth/login para renovar el token Bearer."],
        ["Error 'CLEARTEXT_COMMUNICATION_NOT_PERMITTED' en Android", "Android 9+ bloquea tráfico HTTP no encriptado de forma predeterminada.", "Compruebe que network_security_config.xml declare la IP candidata y esté vinculado en el Manifest."],
        ["Fallo de conexión 'Failed to connect to /192.168.0.228:8000'", "El firewall anfitrión bloquea tráfico entrante o cambió la IP por DHCP.", "Verifique 'ipconfig getifaddr en0', actualice NetworkModule.kt o use 'adb reverse tcp:8000 tcp:8000'."],
        ["Gradle falla con 'Unsupported class file major version 65'", "Incompatibilidad: el sistema usa Java 21+ en lugar de OpenJDK 17.", "Exporte JAVA_HOME apuntando a JDK 17: 'export JAVA_HOME=$(/usr/libexec/java_home -v 17)'."],
        ["Banner 'Alarma Exacta Requerida' bloqueante en Android", "El usuario o el sistema no autorizó SCHEDULE_EXACT_ALARM.", "Ejecute 'adb shell cmd appops set com.medreminder.ai SCHEDULE_EXACT_ALARM allow'."],
        ["Las alarmas no suenan con el teléfono inactivo (Doze)", "El gestor de batería del SO suspende los procesos en segundo plano.", "Ejecute 'adb shell dumpsys deviceidle whitelist +com.medreminder.ai' para otorgar exención."],
        ["Error de Android SDK Build-Tools no encontrado", "Falta el componente build-tools 34.0.0 o 35.0.0 en el SDK.", "Instale las herramientas mediante '$ANDROID_HOME/cmdline-tools/latest/bin/sdkmanager \"build-tools;34.0.0\"'."]
    ]
    add_truth_table(doc, deploy_faq_headers, deploy_faq_rows, "Tabla 9.1: Guía técnica exhaustiva de diagnóstico y resolución de incidencias de despliegue", [2.0, 2.0, 2.7])
    
    # Guardar documento
    out_path = "docs/Manual_de_Instalacion_MedReminderAI.docx"
    doc.save(out_path)
    print(f"✅ Manual de Instalación generado exitosamente en: {out_path}")
    return out_path

if __name__ == "__main__":
    build_manual_instalacion()
