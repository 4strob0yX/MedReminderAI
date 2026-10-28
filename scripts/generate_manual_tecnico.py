"""
generate_manual_tecnico.py - Generador del Manual Técnico Oficial de MedReminder AI.
Estructurado formalmente en 13 secciones normativas según lineamientos docentes de la UTVT:
1. Introducción y glosario
2. Descripción general y requisitos funcionales y no funcionales
3. Arquitectura y tecnologías
4. Instalación solo de las paqueterías y de los elementos que indican en los requisitos funcionales, NO es todo el proceso de instalación.
5. Estructura del proyecto
6. Configuración
7. Modelo de datos
8. Módulos y API
9. Pruebas
10. Despliegue y mantenimiento
11. Seguridad
12. Solución de problemas
13. Limitaciones y trabajo futuro
Además incluye: Referencias, Anexos A-D y Lista de Verificación antes de entregar.
"""

import os
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(BASE_DIR / "scripts"))

import docx
from doc_utils import (
    create_base_document, setup_header_footer, add_utvt_cover, add_version_control_table,
    add_native_toc, add_section_heading, add_body_p, add_truth_table, add_variable_dictionary_table,
    add_peas_section, add_callout, add_code_block, add_figure_image, add_checklist_table
)

def build_manual_tecnico():
    doc = create_base_document()
    doc_title = "Manual Técnico Oficial"
    setup_header_footer(doc, doc_title)
    
    # --------------------------------------------------------------------------
    # 0. CARÁTULA INSTITUCIONAL UTVT
    # --------------------------------------------------------------------------
    add_utvt_cover(
        doc,
        title="MANUAL TÉCNICO OFICIAL: ARQUITECTURA, LÓGICA Y DESARROLLO",
        subtitle="Especificación Formal de Ingeniería de Software, Lógica Proposicional, Algoritmos de Búsqueda en IA y Microservicios",
        doc_code="MAN-TEC-MEDREMINDER-2026-V1.3"
    )
    
    # --------------------------------------------------------------------------
    # CONTROL DE VERSIONES
    # --------------------------------------------------------------------------
    versiones = [
        {
            "version": "1.0",
            "fecha": "20/10/2026",
            "autor": "Equipo de Ingeniería UTVT",
            "descripcion": "Versión inicial: Especificación de arquitectura, modelo PEAS, lógica proposicional y grafos."
        },
        {
            "version": "1.1",
            "fecha": "21/10/2026",
            "autor": "Equipo de Ingeniería UTVT",
            "descripcion": "Reestructuración formal en 13 secciones normativas según rúbrica docente, matriz de paqueterías por RF, pruebas, anexos A-D y lista de verificación."
        },
        {
            "version": "1.2",
            "fecha": "22/10/2026",
            "autor": "Equipo de Ingeniería UTVT",
            "descripcion": "Integración del Marco Formal PEAS en Sección 2 'hasta arriba', eliminación de diagramas textuales en Sección 3.6, 5.1 y 7.1, e incorporación de tablas institucionales de secuencia y estructura canónica."
        },
        {
            "version": "1.3",
            "fecha": "22/10/2026",
            "autor": "Equipo de Ingeniería UTVT",
            "descripcion": "Reubicación prioritaria del Motor Formal de Lógica Proposicional y Tablas de Verdad (V/F) en Sección 2.2 'hasta arriba' inmediatamente después del Marco PEAS, precediendo a los Requisitos Funcionales y No Funcionales."
        }
    ]
    add_version_control_table(doc, versiones, "CONTROL DE VERSIONES DEL MANUAL TÉCNICO")
    
    # --------------------------------------------------------------------------
    # ÍNDICE GENERAL NATIVO DE WORD
    # --------------------------------------------------------------------------
    toc_items = [
        ("1.", "INTRODUCCIÓN, OBJETIVOS DEL SISTEMA Y GLOSARIO", 3),
        ("1.1", "Objetivos Generales y Específicos del Sistema y de Ingeniería", 3),
        ("1.2", "Objetivo del Manual Técnico para el Mantenimiento del Sistema", 3),
        ("1.3", "Perfil del Desarrollador y Mantenedor del Sistema", 4),
        ("1.4", "Glosario Técnico de Términos de Mantenimiento y Arquitectura", 4),
        ("2.", "DESCRIPCIÓN GENERAL Y REQUISITOS FUNCIONALES Y NO FUNCIONALES", 5),
        ("2.1", "Marco Formal del Agente Inteligente (PEAS - Russell & Norvig)", 5),
        ("2.2", "Motor Formal de Lógica Proposicional y Tablas de Verdad", 6),
        ("2.3", "Matriz Formal de Requisitos Funcionales (RF-01 a RF-12)", 8),
        ("2.4", "Matriz Formal de Requisitos No Funcionales (RNF-01 a RNF-08)", 10),
        ("2.5", "Propiedades Formales del Entorno Operativo Clínico", 11),
        ("2.6", "Descripción Global y Propósito del Sistema MedReminder AI", 11),
        ("2.7", "Resumen de Metas Cuantitativas y Criterios de Aceptación", 12),
        ("3.", "ARQUITECTURA Y TECNOLOGÍAS", 13),
        ("3.1", "Patrón Arquitectónico Global y Desacoplamiento Hexagonal", 13),
        ("3.2", "Capa Móvil: Arquitectura MVVM con Jetpack Compose y Coroutines", 14),
        ("3.3", "Capa de Backend: Microservicios en FastAPI, Inyección de Dependencias y Pydantic", 15),
        ("3.4", "Doble Capa de Datos: MySQL Relacional 8.0 y Telemetría MongoDB 6.0", 15),
        ("3.5", "Stack Tecnológico Formal con Versiones Exactas", 16),
        ("3.6", "Especificación de Secuencia de Flujos Críticos Transaccionales", 17),
        ("4.", "INSTALACIÓN SOLO DE LAS PAQUETERÍAS Y DE LOS ELEMENTOS QUE INDICAN EN LOS REQUISITOS FUNCIONALES (NO ES TODO EL PROCESO DE INSTALACIÓN)", 18),
        ("4.1", "Alcance Delimitado: Paqueterías Estrictamente Vinculadas a los Requisitos Funcionales", 18),
        ("4.2", "Matriz de Paqueterías del Backend Python vs. Requisitos Funcionales", 18),
        ("4.3", "Matriz de Dependencias Gradle en Android vs. Requisitos Funcionales", 19),
        ("4.4", "Entorno de Ejecución Contenedorizado y SDKs Base", 20),
        ("5.", "ESTRUCTURA DEL PROYECTO", 21),
        ("5.1", "Estructura Modular y Organización de Directorios del Repositorio", 21),
        ("5.2", "Desglose Funcional de Directorios del Backend", 22),
        ("5.3", "Desglose Funcional de Módulos de la Aplicación Android", 23),
        ("5.4", "Módulos de Inteligencia Artificial, Grafos y Scripts de Soporte", 24),
        ("6.", "CONFIGURACIÓN", 25),
        ("6.1", "Variables de Entorno del Sistema (.env)", 25),
        ("6.2", "Parámetros de Conexión a Motores de Persistencia", 26),
        ("6.3", "Configuración de IPs Dinámicas y Conmutador de Red Móvil", 27),
        ("6.4", "Parámetros de Timeout, Políticas de Retry y Sesión Criptográfica", 28),
        ("7.", "MODELO DE DATOS", 29),
        ("7.1", "Modelo Entidad-Relación y Normalización en Tercera Forma Normal (3FN)", 29),
        ("7.2", "Especificación DDL SQL Completa de MySQL 8.0", 30),
        ("7.3", "Colecciones y Esquema de Telemetría en MongoDB 6.0", 33),
        ("7.4", "Diccionario Formal de Datos y Variables de Persistencia", 34),
        ("8.", "MÓDULOS Y API", 36),
        ("8.1", "Catálogo Exhaustivo de Endpoints REST de FastAPI", 36),
        ("8.2", "Especificación de Payloads JSON y Contratos REST por Módulo", 37),
        ("8.3", "Descripción de Servicios Internos del Backend", 40),
        ("8.4", "Códigos de Estado HTTP y Manejo Estandarizado de Errores", 41),
        ("9.", "PRUEBAS", 42),
        ("9.1", "Estrategia Integral de Aseguramiento de Calidad", 42),
        ("9.2", "Pruebas Unitarias del Backend con pytest", 42),
        ("9.3", "Pruebas de Integración de API y Validación Transaccional SQL", 44),
        ("9.4", "Pruebas UI e Instrumentadas en Android Compose", 45),
        ("9.5", "Matriz de Casos de Prueba Ejecutados con Resultados", 46),
        ("10.", "DESPLIEGUE Y MANTENIMIENTO", 47),
        ("10.1", "Topología de Despliegue con Docker Compose", 47),
        ("10.2", "Procedimientos de Respaldo y Restauración de Datos", 48),
        ("10.3", "Política de Rotación y Monitoreo de Logs", 49),
        ("10.4", "Protocolos de Mantenimiento Preventivo y Correctivo", 50),
        ("11.", "SEGURIDAD", 51),
        ("11.1", "Cifrado y Hashing Criptográfico (Argon2id y bcrypt)", 51),
        ("11.2", "Autenticación y Autorización basada en Tokens JWT Bearer", 52),
        ("11.3", "Gestión de Permisos Críticos en Android 13/14/15", 53),
        ("11.4", "Mitigación de Vulnerabilidades OWASP Top 10", 54),
        ("12.", "SOLUCIÓN DE PROBLEMAS", 55),
        ("12.1", "Matriz Técnica de Troubleshooting para Mantenedores", 55),
        ("12.2", "Diagnóstico de Logs en Backend FastAPI y Uvicorn", 56),
        ("12.3", "Diagnóstico en Cliente Android mediante Logcat y ADB", 57),
        ("12.4", "Resolución de Excepciones de Concurrencia y Red", 58),
        ("13.", "LIMITACIONES Y TRABAJO FUTURO", 59),
        ("13.1", "Limitaciones Técnicas Identificadas", 59),
        ("13.2", "Hoja de Ruta Evolutiva de Ingeniería", 59),
        ("REFERENCIAS", "REFERENCIAS BIBLIOGRÁFICAS", 60),
        ("ANEXO A", "FORMALIZACIÓN COMPLEMENTARIA DEL AGENTE PEAS Y ACCIÓN RACIONAL", 61),
        ("ANEXO B", "MOTOR FORMAL DE LÓGICA PROPOSICIONAL Y DEMOSTRACIONES POR RESOLUCIÓN", 63),
        ("ANEXO C", "MODELADO DE INTELIGENCIA ARTIFICIAL Y GRAFOS DE BÚSQUEDA", 70),
        ("ANEXO D", "DICCIONARIO FORMAL DE VARIABLES DEL SISTEMA CLÍNICO", 78),
        ("CHECKLIST", "LISTA DE VERIFICACIÓN ANTES DE ENTREGAR", 82)
    ]
    add_native_toc(doc, toc_items)
    
    # ==========================================================================
    # 1. INTRODUCCIÓN, OBJETIVOS DEL SISTEMA Y GLOSARIO
    # ==========================================================================
    add_section_heading(doc, "1. INTRODUCCIÓN, OBJETIVOS DEL SISTEMA Y GLOSARIO", level=1)
    
    add_section_heading(doc, "1.1 Objetivos Generales y Específicos del Sistema y de Ingeniería", level=2)
    add_body_p(
        doc,
        "Objetivo General del Sistema y de Ingeniería:\n"
        "Diseñar, formalizar, implementar y validar un sistema distribuido y determinista para la gestión, seguimiento y supervisión "
        "del cumplimiento terapéutico de medicamentos denominado MedReminder AI. El sistema integra un agente inteligente basado en reglas "
        "lógicas proposicionales, algoritmos formales de exploración de grafos de estados para el ciclo de vida de las tomas de medicamentos, "
        "un backend modular en FastAPI con doble capa de persistencia (MySQL relacional y MongoDB no relacional), y un aplicativo móvil nativo "
        "en Android con Jetpack Compose que garantiza cero tolerancia a fallos en el disparo de notificaciones locales y latencia sub-milisegundo.\n\n"
        "Objetivos Específicos del Proyecto:\n"
        "1. Formalización Lógica Rigurosa: Modelar mediante lógica de proposiciones, leyes de De Morgan y relaciones biunívocas las condiciones "
        "de validez en la captura de fármacos, el disparo de alertas de inventario crítico y la exclusión mutua en las transiciones de estado asociadas a las tomas de medicamentos.\n\n"
        "2. Implementación del Agente PEAS: Estructurar la arquitectura del sistema bajo el marco de agentes inteligentes PEAS (Performance, "
        "Environment, Actuators, Sensors), estableciendo métricas cuantificables de desempeño con meta de adherencia terapéutica superior o igual al 95 %.\n\n"
        "3. Persistencia Relacional y Auditoría Inmutable: Diseñar e implementar un modelo E-R estricto en Tercera Forma Normal (3FN) sobre MySQL 8.0, "
        "asegurando que cada evento vinculado con las tomas de medicamentos quede registrado de forma inmutable en una tabla de auditoría dedicada (historial_toma).\n\n"
        "4. Modelado y Optimización mediante Búsqueda en Grafos: Representar el ciclo de vida de los recordatorios de tomas de medicamentos como un "
        "grafo con ciclos potenciales causados por posposiciones reiteradas, aplicando Búsqueda en Profundidad (DFS) con detección de ciclos, Búsqueda "
        "en Anchura (BFS), Búsqueda Heurística y Búsqueda de Costo Uniforme (UCS) para encontrar rutas óptimas hacia la adherencia terapéutica.\n\n"
        "5. Confiabilidad Crítica en Notificaciones Locales: Desarrollar un subsistema de alarmas locales en Android nativo apoyado en AlarmManager.setExactAndAllowWhileIdle "
        "y receptores de arranque (BOOT_COMPLETED), eliminando la dependencia de servicios de mensajería en la nube para asegurar el sonido exacto de "
        "recordatorios de tomas de medicamentos aún en ausencia total de conexión a internet o bajo el modo Doze de Android.\n\n"
        "6. Experiencia de Usuario Adaptada y Accesible: Construir interfaces declarativas bajo Jetpack Compose con botones de altura mayor o igual "
        "a 56 dp, protección contra pulsaciones dobles involuntarias, paleta de colores clínicos y retroalimentación háptica y por voz (TTS)."
    )
    
    add_section_heading(doc, "1.2 Objetivo del Manual Técnico para el Mantenimiento del Sistema", level=2)
    add_body_p(
        doc,
        "El presente Manual Técnico constituye el documento maestro de ingeniería dirigido estrictamente al equipo de "
        "desarrollo, administradores de infraestructura (DevOps) y especialistas de soporte encargados de realizar labores "
        "de mantenimiento preventivo, correctivo, evolutivo y perfectivo sobre la plataforma MedReminder AI.\n\n"
        "Su propósito fundamental es exponer con absoluta transparencia el diseño formal, la arquitectura física y lógica, "
        "los contratos de interfaz, la formulación matemática de los algoritmos de Inteligencia Artificial simbólica y "
        "heurística, y las directrices de seguridad clínica que rigen la persistencia y notificación de tomas de medicamentos. "
        "A través de este documento, cualquier ingeniero capacitado podrá depurar componentes, desplegar réplicas en nuevos "
        "entornos, auditar transacciones en bases de datos y extender funcionalidades sin comprometer la integridad clínica del sistema."
    )
    
    add_section_heading(doc, "1.3 Perfil del Desarrollador y Mantenedor del Sistema", level=2)
    add_body_p(
        doc,
        "Para garantizar un mantenimiento seguro y riguroso de MedReminder AI, el perfil técnico mínimo del profesional asignado comprende:\n\n"
        "• Conocimientos Sólidos en Lenguajes de Programación: Dominio avanzado de Python 3.11+ (tipado estático con Mypy, programación asíncrona "
        "con asyncio) y Kotlin 2.0 (Coroutines, StateFlow, Android Jetpack Compose).\n\n"
        "• Arquitectura de Software y Patrones de Diseño: Comprensión profunda de arquitectura limpia (Clean Architecture), patrón hexagonal, "
        "inyección de dependencias y el patrón Modelo-Vista-VistaModelo (MVVM) en el ecosistema Android.\n\n"
        "• Gestión y Modelado de Persistencia de Datos: Experiencia en normalización relacional en Tercera Forma Normal (3FN), sentencias SQL DDL/DML "
        "en MySQL 8.0, control de transacciones ACID y colecciones documentales en MongoDB 6.0.\n\n"
        "• Inteligencia Artificial y Estructuras de Datos: Dominio de lógica de proposiciones, leyes de De Morgan, tablas de verdad, espacios de "
        "estados, y algoritmos de exploración en grafos (DFS con detección de ciclos, BFS, UCS y Algoritmo Heurístico A*).\n\n"
        "• Seguridad y Criptografía Aplicada: Hashing de credenciales con Argon2/bcrypt, manejo de tokens JWT Bearer (RFC 7519) y mitigación de OWASP Top 10."
    )
    
    add_section_heading(doc, "1.4 Glosario Técnico de Términos de Mantenimiento y Arquitectura", level=2)
    add_body_p(
        doc,
        "Para facilitar las labores de mantenimiento preventivo, correctivo y evolutivo por parte del equipo de ingeniería, "
        "a continuación se definen con rigor conceptual los estándares, términos arquitectónicos, patrones y tecnologías que "
        "gobiernan la plataforma MedReminder AI. Asimismo, el catálogo matemático de variables proposicionales y de persistencia "
        "se formaliza en el Anexo D al final de este documento:"
    )
    
    glosario_headers = ["Término Técnico", "Capa / Dominio", "Definición Formal y Rol en el Mantenimiento del Sistema"]
    glosario_rows = [
        ["ACID", "Persistencia / MySQL", "Acrónimo de Atomicidad, Consistencia, Aislamiento (Isolation) y Durabilidad. Conjunto de propiedades que garantizan que las transacciones de confirmación de tomas de medicamentos y descuento de botiquín se ejecuten sin inconsistencias."],
        ["Adherencia Terapéutica", "Clínico / Salud", "Métrica porcentual que evalúa el grado de cumplimiento del paciente con los horarios y dosis prescritos. La meta operativa en MedReminder AI es mantenerla mayor o igual al 95 %."],
        ["Agente Inteligente (PEAS)", "Inteligencia Artificial", "Marco formal compuesto por Rendimiento (Performance), Entorno (Environment), Actuadores (Actuators) y Sensores (Sensors), estructurando el comportamiento asistivo del sistema."],
        ["AlarmManager / Exact Alarms", "Móvil / Android OS", "Servicio del kernel Android que permite programar alarmas deterministas en tiempo real mediante setExactAndAllowWhileIdle, despertando al dispositivo aún en reposo profundo."],
        ["Algoritmo A* (A-Estrella)", "Inteligencia Artificial", "Algoritmo de exploración heurística que evalúa estados mediante f(n) = g(n) + h(n), combinando costo real con heurística admisible hacia la confirmación de tomas de medicamentos."],
        ["Argon2id / Bcrypt", "Seguridad / Criptografía", "Funciones de derivación de claves criptográficas y hashing irreversible con salt pseudoaleatorio, resistentes a ataques acelerados por GPU y tablas arcoíris."],
        ["Arquitectura Hexagonal", "Arquitectura de Software", "Patrón de puertos y adaptadores que desacopla la lógica clínica del transporte HTTP (FastAPI) y del motor de persistencia (MySQL/MongoDB), facilitando pruebas y reemplazos."],
        ["Búsqueda en Profundidad (DFS)", "Inteligencia Artificial", "Algoritmo basado en pila LIFO con detección de ciclos por conjunto activo (in_path) y límite k=2 para podar bucles derivados de posposiciones reiteradas."],
        ["Coroutines y StateFlow", "Móvil / Kotlin 2.0", "Mecanismos de concurrencia estructurada y reactividad en Kotlin que ejecutan tareas asíncronas de red y base de datos sin bloquear el hilo principal de renderizado."],
        ["Docker Compose", "Infraestructura / DevOps", "Orquestador de contenedores que despliega la topología íntegra de servicios (FastAPI, MySQL 8.0, MongoDB 6.0) dentro de una red virtual privada aislada."],
        ["Doze Mode (Android)", "Móvil / Android OS", "Mecanismo de ahorro de batería de Android que suspende tareas secundarias. Requiere exención de optimización para garantizar el disparo sonoro exacto de recordatorios."],
        ["FastAPI / ASGI (Uvicorn)", "Backend / Python 3.11+", "Framework web asíncrono de alto rendimiento basado en OpenAPI y Pydantic, ejecutado sobre Uvicorn para atender peticiones concurrentes con baja latencia."],
        ["Heads-Up Notification", "Móvil / Android OS", "Notificación emergente flotante con canal de alta importancia (IMPORTANCE_HIGH) que interrumpe la pantalla para advertir al paciente sobre una dosis médica inmediata."],
        ["JWT (JSON Web Token)", "Seguridad / RFC 7519", "Estándar de tokens compactos firmados criptográficamente mediante HMAC-SHA256 (HS256) para autenticar y autorizar sesiones de pacientes y cuidadores."],
        ["Jetpack Compose", "Móvil / UI Android", "Kit de herramientas moderno declarativo para construir interfaces nativas en Android, facilitando el diseño ergonómico accesible con botones de altura mayor o igual a 56 dp."],
        ["MVVM (Model-View-ViewModel)", "Arquitectura Móvil", "Patrón que desacopla la UI declarativa de la lógica de presentación y de los repositorios de datos, optimizando el mantenimiento y testing unitario."],
        ["Normalización 3FN", "Persistencia / Base de Datos", "Tercera Forma Normal en modelos relacionales SQL. Elimina dependencias transitivas y redundancias, asegurando integridad referencial en tablas de recetas y usuarios."],
        ["Pydantic v2", "Backend / Validación", "Motor de validación y tipado de datos con núcleo en Rust, encargado de verificar esquemas JSON en cada petición entrante al microservicio."],
        ["Room Persistence Library", "Móvil / Base de Datos Local", "Capa de persistencia sobre SQLite nativo en Android que mantiene en caché local los recordatorios y medicamentos para operación 100 % fuera de línea."],
        ["Tomas de Medicamentos", "Terminología Canónica", "Término formal y obligatorio que designa el acto de ingesta física, reprogramación o registro médico de una dosis prescrita en el sistema."]
    ]
    add_truth_table(doc, glosario_headers, glosario_rows, "Tabla 1.1: Glosario Técnico de Términos de Mantenimiento y Arquitectura", [1.8, 1.5, 3.2])
    
    # ==========================================================================
    # 2. DESCRIPCIÓN GENERAL Y REQUISITOS FUNCIONALES Y NO FUNCIONALES
    # ==========================================================================
    add_section_heading(doc, "2. DESCRIPCIÓN GENERAL Y REQUISITOS FUNCIONALES Y NO FUNCIONALES", level=1, page_break_before=True)
    
    add_section_heading(doc, "2.1 Marco Formal del Agente Inteligente (PEAS - Russell & Norvig)", level=2)
    add_body_p(
        doc,
        "En el marco de la Inteligencia Artificial clásica (Russell & Norvig, 2020), MedReminder AI se clasifica formalmente como un "
        "Agente Basado en Objetivos y Estados con Razonamiento Deductivo. Su meta primordial es maximizar la adherencia terapéutica, "
        "minimizando las omisiones de tomas de medicamentos y eliminando riesgos de intoxicación por acumulación o desfase horario.\n\n"
        "A continuación se especifica la formalización canónica bajo las cuatro dimensiones del marco PEAS (Performance, Environment, "
        "Actuators, Sensors), estableciendo la correlación estricta entre requisitos de ingeniería, métricas clínicas y parámetros formales:"
    )
    
    peas_tech_data = {
        "performance": (
            "• Adherencia Terapéutica General: Tasa de tomas de medicamentos confirmadas >= 95 %.\n"
            "• Precisión de Alerta: Cero omisiones por fallas de temporización en hardware móvil (0.000 % de error).\n"
            "• Seguridad de Stock: Prevención de desabastecimiento con advertencias oportunas (semáforo amarillo y rojo).\n"
            "• Latencia del Agente: Tiempo de inferencia de reglas lógicas y validación clínica < 5 ms."
        ),
        "performance_metrics": "Adherencia >= 95%\nError temporal = 0 ms\nFalsos positivos < 1%\nInferencia < 5 ms",
        "environment": (
            "• Entorno de Ejecución: Dispositivo Android personal, servidor local o nube híbrida.\n"
            "• Sujetos del Entorno: Adulto mayor, paciente con enfermedad crónica o cuidador familiar.\n"
            "• Condiciones de Red: Conectividad intermitente o modo offline prolongado (Single Source of Truth).\n"
            "• Entorno Clínico: Esquemas posológicos con múltiples tomas de medicamentos al día."
        ),
        "environment_metrics": "Android 8.0+ (API 26-35)\nCon o sin red celular\nRestricciones Doze\nMySQL 8 / Mongo 6",
        "actuators": (
            "• AlarmManager de Android: Despertador de hardware de alta precisión con setExactAndAllowWhileIdle.\n"
            "• Notificaciones Heads-Up: Banners visuales de alta prioridad con botones ergonómicos >= 56 dp.\n"
            "• Motor TTS de Audio: Lectura en voz alta del fármaco y dosis correspondiente para accesibilidad visual.\n"
            "• Descuento Atómico de Inventario: Mutación matemática del stock en base de datos (-1 unidad por dosis)."
        ),
        "actuadores": (
            "• AlarmManager de Android: Despertador de hardware de alta precisión con setExactAndAllowWhileIdle.\n"
            "• Notificaciones Heads-Up: Banners visuales de alta prioridad con botones ergonómicos >= 56 dp.\n"
            "• Motor TTS de Audio: Lectura en voz alta del fármaco y dosis correspondiente para accesibilidad visual.\n"
            "• Descuento Atómico de Inventario: Mutación matemática del stock en base de datos (-1 unidad por dosis)."
        ),
        "actuators_metrics": "AlarmManager exacto\nNotificación prioritaria\nSíntesis de voz háptica\nMutación transaccional",
        "actuadores_metrics": "AlarmManager exacto\nNotificación prioritaria\nSíntesis de voz háptica\nMutación transaccional",
        "sensors": (
            "• Reloj en Tiempo Real (RTC): Temporizador de hardware para precisión temporal absoluta.\n"
            "• Pantalla Táctil: Captura de eventos de confirmación de tomas de medicamentos, posposición u omisión.\n"
            "• Receptor BOOT_COMPLETED: Detección de arranque tras apagado del dispositivo móvil.\n"
            "• Detector de Conectividad: Detección de transiciones Wi-Fi, datos móviles y modo offline."
        ),
        "sensores": (
            "• Reloj en Tiempo Real (RTC): Temporizador de hardware para precisión temporal absoluta.\n"
            "• Pantalla Táctil: Captura de eventos de confirmación de tomas de medicamentos, posposición u omisión.\n"
            "• Receptor BOOT_COMPLETED: Detección de arranque tras apagado del dispositivo móvil.\n"
            "• Detector de Conectividad: Detección de transiciones Wi-Fi, datos móviles y modo offline."
        ),
        "sensors_metrics": "Reloj RTC de hardware\nEventos táctiles (Compose)\nBroadcast de reinicio\nNetworkCallback API",
        "sensores_metrics": "Reloj RTC de hardware\nEventos táctiles (Compose)\nBroadcast de reinicio\nNetworkCallback API"
    }
    add_peas_section(doc, peas_tech_data, intro_text="", caption="Tabla 2.1: Especificación Formal de Dimensiones del Agente Inteligente PEAS")
    
    add_section_heading(doc, "2.2 Motor Formal de Lógica Proposicional y Tablas de Verdad", level=2)
    add_body_p(
        doc,
        "En concordancia con el marco de razonamiento deductivo de agentes inteligentes (Russell & Norvig, 2020), "
        "MedReminder AI fundamenta la totalidad de sus decisiones operativas y clínicas sobre un Motor Formal de Lógica "
        "Proposicional. Cada evento del sistema —desde la validación del alta de un fármaco hasta el bloqueo de interacciones, "
        "la exclusión mutua de estados en el ciclo de vida de las tomas de medicamentos y la activación del Modo Castigo— "
        "se modela mediante fórmulas proposicionales rigurosas cuyas condiciones de verdad se evalúan estrictamente mediante "
        "los valores canónicos 'V' (Verdadero) y 'F' (Falso).\n\n"
        "A continuación se especifican las seis matrices deductivas que gobiernan la lógica clínica de la plataforma:"
    )
    
    add_section_heading(doc, "2.2.1 Validación Lógica de Entrada (CRUD de Medicamentos)", level=3)
    add_body_p(
        doc,
        "La validación para el alta y modificación de fármacos exige el cumplimiento simultáneo de cuatro predicados atómicos:\n\n"
        "• p: Nombre del fármaco no vacío (longitud >= 2 caracteres).\n"
        "• q: Dosis válida y positiva (cantidad > 0).\n"
        "• r: Frecuencia horaria admisible (frecuencia in {4, 6, 8, 12, 24} horas).\n"
        "• s: Stock inicial no negativo (stock >= 0 unidades).\n\n"
        "Fórmula Proposicional: V_alta = p ∧ q ∧ r ∧ s\n"
        "Por Leyes de De Morgan, la condición de rechazo es: ¬V_alta = ¬p ∨ ¬q ∨ ¬r ∨ ¬s"
    )
    t1_headers = ["p (Nombre)", "q (Dosis)", "r (Frecuencia)", "s (Stock)", "V_alta (Aprobado)", "Estado Clínico"]
    t1_rows = [
        ["V", "V", "V", "V", "V", "Registro válido de fármaco"],
        ["V", "V", "V", "F", "F", "Rechazado: stock negativo"],
        ["V", "V", "F", "V", "F", "Rechazado: frecuencia no admisible"],
        ["V", "F", "V", "V", "F", "Rechazado: dosis nula o negativa"],
        ["F", "V", "V", "V", "F", "Rechazado: nombre vacío"],
        ["F", "F", "F", "F", "F", "Rechazado: múltiples fallas"]
    ]
    add_truth_table(doc, t1_headers, t1_rows, "Tabla 2.2: Tabla de Verdad Formal de Validación Lógica de Fármacos", [1.0, 1.0, 1.1, 1.0, 1.1, 1.3])
    
    add_section_heading(doc, "2.2.2 Disparo de Alerta de Inventario Crítico", level=3)
    add_body_p(
        doc,
        "Predicados de inventario para advertencia de desabastecimiento en botiquín:\n\n"
        "• A: Stock actual menor o igual al umbral mínimo de seguridad (stock <= limite).\n"
        "• B: Tratamiento médico activo en curso con tomas de medicamentos programadas.\n\n"
        "Fórmula Proposicional: Alerta_Stock = A ∧ B"
    )
    t2_headers = ["A (Stock <= Umbral)", "B (Tratamiento Activo)", "Alerta_Stock", "Acción del Sistema"]
    t2_rows = [
        ["V", "V", "V", "Disparar notificación urgente de compra"],
        ["V", "F", "F", "Sin alerta: tratamiento concluido"],
        ["F", "V", "F", "Sin alerta: inventario suficiente"],
        ["F", "F", "F", "Sin alerta: inventario suficiente y tratamiento inactivo"]
    ]
    add_truth_table(doc, t2_headers, t2_rows, "Tabla 2.3: Tabla de Verdad de Inventario Crítico de Medicamentos", [1.4, 1.6, 1.2, 2.3])
    
    add_section_heading(doc, "2.2.3 Transición de Estados y Exclusión Mutua en Tomas de Medicamentos", level=3)
    add_body_p(
        doc,
        "Para salvaguardar la coherencia médico-legal, una toma de medicamentos en turno solo puede culminar en uno y solo uno "
        "de tres estados finales mutuamente excluyentes:\n\n"
        "• t: Dosis confirmada como tomada nominalmente.\n"
        "• p: Dosis pospuesta temporalmente.\n"
        "• o: Dosis omitida formalmente con justificación clínica.\n\n"
        "Fórmula Proposicional de Exclusión Mutua: Validez_Estado = (t ⊕ p ⊕ o) ∧ ¬(t ∧ p) ∧ ¬(t ∧ o) ∧ ¬(p ∧ o)"
    )
    t3_headers = ["t (Tomado)", "p (Pospuesto)", "o (Omitido)", "Validez_Estado", "Semántica Transaccional"]
    t3_rows = [
        ["V", "F", "F", "V", "Válido: confirmación nominal de tomas de medicamentos"],
        ["F", "V", "F", "V", "Válido: posposición transitoria de la alarma"],
        ["F", "F", "V", "V", "Válido: omisión con justificación clínica"],
        ["V", "V", "F", "F", "Inválido: no puede tomarse y posponerse a la vez"],
        ["V", "F", "V", "F", "Inválido: no puede tomarse y omitirse a la vez"],
        ["F", "V", "V", "F", "Inválido: no puede posponerse y omitirse a la vez"],
        ["V", "V", "V", "F", "Inválido: contradicción clínica total"],
        ["F", "F", "F", "F", "Inválido: recordatorio pendiente sin resolución"]
    ]
    add_truth_table(doc, t3_headers, t3_rows, "Tabla 2.4: Tabla de Verdad de Exclusión Mutua en Estados de Tomas de Medicamentos", [1.0, 1.1, 1.0, 1.2, 2.2])
    
    add_section_heading(doc, "2.2.4 Regla Formal de Límite de Posposiciones de Tomas de Medicamentos (k=2)", level=3)
    add_body_p(
        doc,
        "Predicados para posposición de tomas de medicamentos con el fin de evitar sobredosificación o desfase de horarios:\n\n"
        "• C: Solicitud activa de aplazamiento por parte del paciente.\n"
        "• D: Contador de posposiciones estrictamente menor a 2 (contador < 2).\n\n"
        "Fórmula Proposicional: Permitir_Posponer = C ∧ D"
    )
    t4_headers = ["C (Solicitud Posponer)", "D (Contador < 2)", "Permitir_Posponer", "Resolución del Agente"]
    t4_rows = [
        ["V", "V", "V", "Reprogramar alarma determinista +30 min"],
        ["V", "F", "F", "Bloquear botón: forzar toma de medicamentos u omisión de dosis"],
        ["F", "V", "F", "Sin acción de posposición"],
        ["F", "F", "F", "Sin acción de posposición"]
    ]
    add_truth_table(doc, t4_headers, t4_rows, "Tabla 2.5: Tabla de Verdad de Límite de Posposiciones (k=2)", [1.5, 1.4, 1.4, 2.2])
    
    add_section_heading(doc, "2.2.5 Matriz Lógica de Alergias y Contraindicaciones Críticas", level=3)
    add_body_p(
        doc,
        "Predicados de seguridad clínica para prevenir reacciones adversas:\n\n"
        "• X: Fármaco recetado contiene principio activo con alergia registrada en el perfil del paciente.\n"
        "• Y: Tratamiento concurrente con interacción medicamentosa grave reportada.\n\n"
        "Fórmula Proposicional de Bloqueo Preventivo: Bloqueo_Seguridad = X ∨ Y"
    )
    t5_headers = ["X (Alergia Detectada)", "Y (Interacción Grave)", "Bloqueo_Seguridad", "Protocolo Clínico"]
    t5_rows = [
        ["V", "V", "V", "Bloqueo crítico inmediato de prescripción"],
        ["V", "F", "V", "Bloqueo crítico por alergia del paciente"],
        ["F", "V", "V", "Bloqueo crítico por interacción farmacológica"],
        ["F", "F", "F", "Prescripción segura aprobada por el sistema"]
    ]
    add_truth_table(doc, t5_headers, t5_rows, "Tabla 2.6: Tabla de Verdad de Bloqueo por Alergias e Interacciones", [1.4, 1.5, 1.4, 2.2])
    
    add_section_heading(doc, "2.2.6 Regla Lógica Formal del Modo Castigo y Pérdida de Honor", level=3)
    add_body_p(
        doc,
        "Predicados de motivación y cumplimiento terapéutico:\n\n"
        "• M: Paciente acumula 2 o más omisiones no justificadas en una ventana de 72 horas.\n"
        "• N: Escudos protectores de lealtad agotados (escudos == 0).\n\n"
        "Fórmula Proposicional: Modo_Castigo = M ∧ N\n"
        "Consecuencia Operativa: Al activarse el Modo Castigo, la opción de posponer se bloquea en todas las tomas de medicamentos del día."
    )
    t6_headers = ["M (Omisiones >= 2)", "N (Escudos == 0)", "Modo_Castigo", "Impacto en Interfaz Móvil"]
    t6_rows = [
        ["V", "V", "V", "Activar Modo Castigo: bloqueo total de posposición"],
        ["V", "F", "F", "Consumir 1 escudo protector; preservar racha"],
        ["F", "V", "F", "Modo normal: paciente cumplido sin escudos"],
        ["F", "F", "F", "Modo normal: paciente cumplido con escudos activos"]
    ]
    add_truth_table(doc, t6_headers, t6_rows, "Tabla 2.7: Tabla de Verdad de Activación del Modo Castigo", [1.4, 1.4, 1.3, 2.4])
    
    add_section_heading(doc, "2.2.7 Implementación de Referencia en Python del Motor Lógico Proposicional", level=3)
    add_body_p(
        doc,
        "A continuación se presenta el código fuente en Python (backend/app/core/logic_engine.py) que evalúa formalmente "
        "estas reglas utilizando operadores booleanos deterministas y verificación con leyes de De Morgan:"
    )
    py_logic_sec2 = """# backend/app/core/logic_engine.py - Motor formal de evaluación proposicional
def validar_alta_farmaco(nombre: str, dosis: float, frecuencia: int, stock: int) -> bool:
    p = len(nombre.strip()) >= 2
    q = dosis > 0.0
    r = frecuencia in [4, 6, 8, 12, 24]
    s = stock >= 0
    # Fórmula: V = p and q and r and s
    # Ley de De Morgan: not V = not p or not q or not r or not s
    return p and q and r and s

def verificar_inventario_critico(stock_actual: int, stock_minimo: int, tratamiento_activo: bool) -> bool:
    a = stock_actual <= stock_minimo
    b = tratamiento_activo
    return a and b

def validar_exclusion_mutua_tomas_de_medicamentos(tomado: bool, pospuesto: bool, omitido: bool) -> bool:
    # Exactamente una variable debe ser Verdadera (True)
    valores = [bool(tomado), bool(pospuesto), bool(omitido)]
    return valores.count(True) == 1

def permitir_posponer_tomas_de_medicamentos(solicita_posponer: bool, contador_posposiciones: int) -> bool:
    c = bool(solicita_posponer)
    d = contador_posposiciones < 2
    return c and d

def evaluar_bloqueo_seguridad_alergias(alergia_detectada: bool, interaccion_grave: bool) -> bool:
    # Fórmula: Bloqueo_Seguridad = X or Y
    x = bool(alergia_detectada)
    y = bool(interaccion_grave)
    return x or y

def evaluar_modo_castigo(omisiones_acumuladas: int, escudos_disponibles: int) -> bool:
    # Fórmula: Modo_Castigo = M and N
    m = omisiones_acumuladas >= 2
    n = escudos_disponibles == 0
    return m and n"""
    add_code_block(doc, py_logic_sec2, "Implementación en Python del Motor Lógico Proposicional (logic_engine.py)")
    
    add_section_heading(doc, "2.3 Matriz Formal de Requisitos Funcionales (RF-01 a RF-12)", level=2)
    add_body_p(
        doc,
        "A continuación se presenta la matriz canónica de Requisitos Funcionales que rigen el comportamiento operativo de MedReminder AI. "
        "Cada requisito funcional define una capacidad obligatoria que el mantenedor debe preservar durante cualquier modificación del código fuente:"
    )
    
    rf_headers = ["ID", "Requisito Funcional", "Descripción y Comportamiento Clínico", "Prioridad", "Regla de Negocio Asociada"]
    rf_rows = [
        ["RF-01", "Alta y Edición de Fármacos", "El sistema debe permitir registrar y modificar fármacos especificando nombre comercial, principio activo, presentación, concentración, stock inicial y límite de advertencia.", "Alta", "Regla Lógica 1 (Validación sintáctica y biunívoca de campos)."],
        ["RF-02", "Cálculo de Tomas de Medicamentos", "Generar automáticamente la secuencia temporal de horarios de tomas de medicamentos según la frecuencia horaria (cada 4, 6, 8, 12, 24 h) a partir de la fecha de inicio.", "Crítica", "Cálculo de intervalos biológicos en UTC proyectados a zona horaria local."],
        ["RF-03", "Alarmas Heads-Up Locales", "Disparar alarmas acústicas, visuales y hápticas en el segundo exacto mediante AlarmManager en Android, incluso en Doze mode.", "Crítica", "Garantía de despertar en segundo plano sin dependencia de red remota."],
        ["RF-04", "Gestión de Stock en Mi Botiquín", "Monitorear el inventario físico disponible, calculando el semáforo cromático (verde, amarillo y rojo) y advirtiendo desabastecimiento.", "Alta", "Regla Lógica 2 (Alerta de stock crítico cuando existencias <= límite)."],
        ["RF-05", "Confirmación Atómica de Dosis", "Registrar la confirmación de tomas de medicamentos realizadas ('Tomar Ahora'), descontando -1 unidad del botiquín e insertando auditoría.", "Crítica", "Regla Lógica 3 (Exclusión mutua de estados: Tomado ⊕ Pospuesto ⊕ Omitido)."],
        ["RF-06", "Posposición Controlada (k=2)", "Permitir posponer la alarma de tomas de medicamentos en lapsos fijos deterministas (+10 min o +30 min), con límite estricto de dos posposiciones.", "Alta", "Regla Lógica 4 (Bloqueo de botón 'Posponer' tras alcanzar contador = 2)."],
        ["RF-07", "Omisión Justificada con Bitácora", "Permitir registrar la omisión de tomas de medicamentos con captura obligatoria de justificación médica, sin descontar stock físico.", "Media", "Preservación de concordancia matemática entre stock digital y frasco físico."],
        ["RF-08", "Reversión Segura «Deshacer»", "Proporcionar una ventana de reversión tras marcar una toma de medicamentos por error, restaurando el stock del botiquín (+1).", "Media", "Regla de Reversión Inmediata (restauración atómica del inventario)."],
        ["RF-09", "Asistente Virtual Interactivo Medi", "Permitir interacción por texto y síntesis de voz (TTS) con el acompañante Medi para consultas sobre posología, consejos y ánimos.", "Media", "Procesamiento determinista de intenciones clínicas y respuestas empáticas."],
        ["RF-10", "Red de Apoyo y Contactos Médicos", "Permitir gestionar contactos de emergencia con números telefónicos para emisión de alertas automáticas ante omisiones reiteradas.", "Alta", "Protocolo de escalamiento familiar ante riesgo de abandono terapéutico."],
        ["RF-11", "Visualización del Árbol de IA", "Visualizar en el cliente móvil el árbol de exploración DFS/BFS y el estado de poda de ciclos para seguimiento del tratamiento.", "Baja", "Transparencia algorítmica y valor educativo para el paciente y médico."],
        ["RF-12", "Gamificación y Racha de Honor", "Calcular la racha de días continuos de cumplimiento, otorgando rangos (Hierro a Diamante) y administrando el Modo Castigo.", "Media", "Regla Lógica 6 (Activación de Modo Castigo tras omisiones consecutivas)."]
    ]
    add_truth_table(doc, rf_headers, rf_rows, "Tabla 2.8: Matriz Canónica de Requisitos Funcionales (RF-01 a RF-12)", [0.8, 1.4, 2.3, 0.8, 1.2])
    
    add_section_heading(doc, "2.4 Matriz Formal de Requisitos No Funcionales (RNF-01 a RNF-08)", level=2)
    add_body_p(
        doc,
        "Los Requisitos No Funcionales establecen las restricciones cuantitativas de calidad, rendimiento, seguridad y confiabilidad "
        "que el mantenedor debe auditar periódicamente para certificar la estabilidad operativa del sistema:"
    )
    
    rnf_headers = ["ID", "Requisito No Funcional", "Parámetro Cuantitativo / Métrica", "Método de Verificación y Criterio de Aceptación"]
    rnf_rows = [
        ["RNF-01", "Rendimiento y Tiempo de Respuesta API", "Tiempo de respuesta sub-250 ms en el percentil 95 (P95) para endpoints transaccionales.", "Pruebas de carga con 100 peticiones concurrentes mediante pytest y httpx."],
        ["RNF-02", "Fluidez y Latencia de Interfaz Gráfica", "Tasa de refresco constante a 60 fps (latencia por frame < 16.6 ms) en Compose.", "Monitoreo con Android GPU Profiler sin eventos de congelamiento (jank)."],
        ["RNF-03", "Disponibilidad Local Determinista", "100 % de precisión en disparo de alarmas de tomas de medicamentos sin internet.", "Prueba de desconexión de red en dispositivo físico durante 72 horas continuas."],
        ["RNF-04", "Seguridad Criptográfica en Reposo", "Contraseñas protegidas mediante Argon2id o bcrypt con work factor = 12.", "Auditoría de volcado SQL verificando ausencia total de credenciales en claro."],
        ["RNF-05", "Inmutabilidad de Bitácora Médico-Legal", "Cero sentencias UPDATE o DELETE sobre la tabla relacional historial_toma.", "Auditoría de privilegios DML del usuario de base de datos de producción."],
        ["RNF-06", "Eficiencia Energética en Dispositivo", "Consumo de batería en segundo plano menor al 2 % diario atribuible a la app.", "Medición de consumo mAh mediante Android Battery Historian en reposo prolongado."],
        ["RNF-07", "Ergonomía y Accesibilidad Motriz", "Botones de interacción primaria con altura mayor o igual a 56 dp.", "Inspección de código fuente en Compose y pruebas táctiles con usuarios senior."],
        ["RNF-08", "Integridad Referencial en Persistencia", "Esquema relacional estricto en Tercera Forma Normal (3FN) con claves foráneas activas.", "Ejecución de script DDL de MySQL 8.0 con motor InnoDB y foreign keys habilitadas."]
    ]
    add_truth_table(doc, rnf_headers, rnf_rows, "Tabla 2.9: Matriz Formal de Requisitos No Funcionales (RNF-01 a RNF-08)", [0.8, 1.6, 1.8, 2.3])
    
    add_section_heading(doc, "2.5 Propiedades Formales del Entorno Operativo Clínico", level=2)
    add_body_p(
        doc,
        "Según la taxonomía formal de Russell y Norvig (2020), el entorno operativo de MedReminder AI se caracteriza por:\n\n"
        "• Parcialmente Observable: El sistema conoce el estado del teléfono y los registros clínicos en base de datos, "
        "pero desconoce si el paciente ingirió físicamente el fármaco o solo pulsó el botón en pantalla.\n\n"
        "• Estocástico: El comportamiento humano presenta incertidumbre (olvidos imprevistos, viajes, falta de compra en farmacia).\n\n"
        "• Secuencial: Cada decisión sobre las tomas de medicamentos afecta las probabilidades de éxito futuro, la adherencia acumulada y la racha de honor.\n\n"
        "• Dinámico: El paso continuo del tiempo modifica el estado de las tomas de medicamentos (de pendiente a retrasado) sin requerir interacción del paciente.\n\n"
        "• Continuo: El reloj de tiempo y las horas biológicas de dosificación transcurren de manera continua.\n\n"
        "• Multiagente Asistivo: Interactúan el paciente, los familiares de apoyo, el médico tratante y el asistente digital Medi."
    )
    
    add_section_heading(doc, "2.6 Descripción Global y Propósito del Sistema MedReminder AI", level=2)
    add_body_p(
        doc,
        "MedReminder AI es una solución sociotécnica integral concebida para mitigar la crisis de adherencia terapéutica en pacientes "
        "con tratamientos farmacológicos crónicos o complejos. A nivel mundial, la Organización Mundial de la Salud (OMS) estima que el 50 % "
        "de los pacientes con enfermedades crónicas no toman sus tratamientos según lo prescrito, provocando hospitalizaciones evitables, "
        "complicaciones clínicas graves y un enorme sobrecosto a los sistemas de salud pública.\n\n"
        "La plataforma ataca este problema combinando la confiabilidad determinista del hardware móvil local con el razonamiento automatizado "
        "de la Inteligencia Artificial. No depende de conexiones remotas continuas para salvar la vida del paciente: las alarmas de tomas de "
        "medicamentos se calculan y programan de forma autónoma en el reloj de hardware del teléfono inteligente. Simultáneamente, el backend "
        "centraliza la telemetría, mantiene una bitácora inmutable médico-legal de tomas de medicamentos confirmadas, gestiona el botiquín "
        "virtual familiar y ofrece una interfaz accesible con el asistente Medi."
    )
    
    add_section_heading(doc, "2.7 Resumen de Metas Cuantitativas y Criterios de Aceptación", level=2)
    add_body_p(
        doc,
        "El éxito de la plataforma MedReminder AI se mide a través del cumplimiento simultáneo de tres metas operativas primarias:\n\n"
        "1. Adherencia Farmacológica Superior al 95 %: La tasa de tomas de medicamentos cumplidas respecto al total programado debe "
        "mantenerse en o por encima del 95 % en pacientes que utilizan el sistema de forma activa.\n\n"
        "2. Cero Falsos Negativos en Recordatorios: La probabilidad de que una alarma de tomas de medicamentos programada no suene "
        "por congelamiento del sistema operativo debe ser estrictamente cero (0.000 %), gracias al uso de AlarmManager.setExactAndAllowWhileIdle.\n\n"
        "3. Trazabilidad Total en Farmacovigilancia: Todo evento de confirmación, posposición u omisión de tomas de medicamentos "
        "debe contar con estampa de tiempo UTC, identificador único de paciente y justificación médica archivada en MySQL."
    )
    
    # ==========================================================================
    # 3. ARQUITECTURA Y TECNOLOGÍAS
    # ==========================================================================
    add_section_heading(doc, "3. ARQUITECTURA Y TECNOLOGÍAS", level=1, page_break_before=True)
    
    add_section_heading(doc, "3.1 Patrón Arquitectónico Global y Desacoplamiento Hexagonal", level=2)
    add_body_p(
        doc,
        "MedReminder AI adopta una arquitectura desacoplada basada en el patrón Hexagonal (Puertos y Adaptadores) articulada "
        "con una topología cliente-servidor asíncrona. La lógica nuclear del negocio y los modelos matemáticos residen en capas "
        "puras de dominio, totalmente aisladas de los detalles de persistencia (SQLAlchemy/PyMongo), transporte (HTTP/FastAPI) o "
        "renderizado gráfico (Jetpack Compose).\n\n"
        "Esta separación permite que el mantenedor reemplace motores de almacenamiento o actualice librerías de interfaz sin alterar "
        "las reglas de negocio clínicas ni las tablas de verdad que gobiernan el ciclo de vida de las tomas de medicamentos."
    )
    
    add_callout(
        doc,
        "Principio de Inversión de Dependencias (DIP): Los módulos de alto nivel (casos de uso) nunca dependen de módulos de bajo "
        "nivel (controladores de base de datos). Ambos dependen de abstracciones (interfaces de repositorio), lo que permite "
        "sustituir el backend de MySQL por una base de datos distribuida en memoria durante la ejecución de pruebas unitarias sin tocar la lógica de negocio.",
        callout_type="arch",
        title="DIRECTRIZ DE ARQUITECTURA HEXAGONAL"
    )
    
    add_section_heading(doc, "3.2 Capa Móvil: Arquitectura MVVM con Jetpack Compose y Coroutines", level=2)
    add_body_p(
        doc,
        "El cliente Android está construido íntegramente bajo el patrón Modelo-Vista-VistaModelo (MVVM) utilizando el kit de herramientas "
        "moderno Jetpack Compose para interfaces declarativas reactivas:\n\n"
        "• Capa de Vista (UI Screens): Compuesta exclusivamente por funciones composables puras (@Composable) que observan el estado inmutable "
        "emitido por el ViewModel. No contienen lógica de negocio ni llamadas directas a base de datos.\n\n"
        "• Capa de VistaModelo (ViewModels): Exponen flujos StateFlow<UiState> inmutables y encapsulan el estado de la pantalla. Gestionan "
        "la concurrencia asíncrona mediante corrutinas de Kotlin (viewModelScope) despachadas en Dispatchers.IO para operaciones de red "
        "y Dispatchers.Main para mutaciones de interfaz.\n\n"
        "• Capa de Datos (Repository Pattern): Unifica el acceso a datos locales (Room Database / SharedPreferences cifradas) y remotos (Retrofit2), "
        "implementando una estrategia Single Source of Truth (SSOT)."
    )
    
    add_section_heading(doc, "3.3 Capa de Backend: Microservicios en FastAPI, Inyección de Dependencias y Pydantic", level=2)
    add_body_p(
        doc,
        "El backend está implementado en Python sobre el framework asíncrono FastAPI, seleccionado por su extraordinario rendimiento "
        "(comparable a NodeJS y Go), tipado estático nativo y autogeneración de contratos OpenAPI 3.0:\n\n"
        "• Inyección de Dependencias Nativa (Depends): FastAPI resuelve dinámicamente las sesiones de base de datos MySQL (get_db), los clientes "
        "de MongoDB y la autenticación de usuarios (get_current_user), garantizando el cierre de conexiones en bloques finally deterministas.\n\n"
        "• Validación Estricta con Pydantic v2: Cada solicitud entrante y respuesta saliente es validada contra esquemas fuertemente tipados. "
        "Si un cliente envía una dosis negativa o un horario inválido, el sistema intercepta el error con código HTTP 422 antes de tocar la base de datos."
    )
    
    add_section_heading(doc, "3.4 Doble Capa de Datos: MySQL Relacional 8.0 y Telemetría MongoDB 6.0", level=2)
    add_body_p(
        doc,
        "La persistencia en MedReminder AI sigue un modelo políglota equilibrado:\n\n"
        "1. MySQL 8.0 (Motor InnoDB): Destinado a la información clínica crítica que exige estricto cumplimiento ACID (Atomicidad, Consistencia, "
        "Aislamiento y Durabilidad). Administra usuarios, fármacos, pautas de dosificación, inventario de botiquín y la bitácora inmutable historial_toma.\n\n"
        "2. MongoDB 6.0: Empleado para la ingesta masiva de telemetría de dispositivos móviles, logs de interacción empática con el acompañante Medi, "
        "y registros analíticos de exploración de grafos de búsqueda en IA, aprovechando su esquema flexible libre de migraciones costosas."
    )
    
    add_section_heading(doc, "3.5 Stack Tecnológico Formal con Versiones Exactas", level=2)
    add_body_p(
        doc,
        "La siguiente tabla detalla la pila tecnológica completa, sus versiones de producción probadas y su función operativa:"
    )
    
    tech_headers = ["Componente / Biblioteca", "Versión", "Capa / Ámbito", "Función Operativa Principal"]
    tech_rows = [
        ["Kotlin", "2.0.0", "Cliente Móvil", "Lenguaje de programación nativo moderno, corrutinas y StateFlow."],
        ["Android Jetpack Compose", "BOM 2024.09.00", "Interfaz Móvil", "Desarrollo de UI declarativa reactiva con Material Design 3."],
        ["Retrofit 2", "2.11.0", "Red Móvil", "Cliente HTTP REST con convertidor Gson para serialización JSON."],
        ["AndroidX Room", "2.6.1", "Persistencia Móvil", "Capa de abstracción SQLite para caché local y tolerancia offline."],
        ["Python", "3.11 / 3.12", "Servidor Backend", "Lenguaje del backend con tipado estático y librerías científicas."],
        ["FastAPI", "0.110.0+", "Servidor Backend", "Framework web asíncrono de alto rendimiento con Pydantic v2."],
        ["SQLAlchemy", "2.0.28+", "ORM Backend", "Mapeador objeto-relacional para consultas estructuradas en MySQL."],
        ["PyMySQL", "1.1.0+", "Driver MySQL", "Driver de conexión nativo para MySQL 8.0."],
        ["PyMongo", "4.6.2+", "Driver MongoDB", "Driver oficial asíncrono para almacenamiento no relacional BSON."],
        ["Passlib (bcrypt)", "1.7.4", "Seguridad", "Hashing criptográfico con salt dinámico de 128 bits."],
        ["Python-Jose (cryptography)", "3.3.0", "Seguridad", "Generación, firma y validación de tokens JWT Bearer (HS256)."],
        ["MySQL Community Server", "8.0.36", "Base de Datos", "Persistencia relacional ACID en 3FN con motor InnoDB."],
        ["MongoDB Community Server", "6.0.14", "Telemetría", "Persistencia documental semiestructurada para logs de IA y Medi."],
        ["Docker Engine & Compose", "26.0+ / v2.26+", "Infraestructura", "Contenedorización integral de microservicios y persistencia."]
    ]
    add_truth_table(doc, tech_headers, tech_rows, "Tabla 3.1: Stack Tecnológico Formal con Versiones de Producción", [1.5, 1.0, 1.3, 2.7])
    
    add_section_heading(doc, "3.6 Especificación de Secuencia de Flujos Críticos Transaccionales", level=2)
    add_body_p(
        doc,
        "La interacción coordinada entre la interfaz de usuario móvil en Android, la capa de red con Retrofit, "
        "el microservicio en FastAPI y los motores de persistencia MySQL/MongoDB se formaliza a través de matrices de secuencia "
        "transaccional que aseguran la consistencia ACID de las tomas de medicamentos y eliminan cualquier ambigüedad en el mantenimiento:\n\n"
        "1. Flujo Transaccional 1: Confirmación de Toma de Medicamentos («Tomar Ahora») con Descuento Atómico de Stock:\n"
        "Este flujo modela el ciclo de vida crítico cuando el paciente ingiere su fármaco y confirma la operación en el dispositivo. "
        "La siguiente matriz especifica cada paso de la secuencia, los componentes intervinientes y su garantía de consistencia:"
    )
    
    seq1_headers = ["Paso", "Capa Emisora", "Capa Receptora", "Mensaje / Operación Transaccional", "Garantía de Consistencia y Concurrencia"]
    seq1_rows = [
        ["Paso 1", "UI Móvil (Compose)", "ViewModel (HoyViewModel)", "Pulsación del botón táctil «Tomar Ahora» en ReminderCard.kt", "Desactivación reactiva de botón en el frame actual (prevención de doble toque)."],
        ["Paso 2", "HoyViewModel", "ReminderRepository", "Despacho de corrutina en Dispatchers.IO: confirmarToma(id_recordatorio)", "Aislamiento estricto de hilo principal de renderizado (garantía RNF-02 a 60 fps)."],
        ["Paso 3", "Cliente Retrofit", "FastAPI (/recordatorios/{id}/confirmar)", "Petición HTTP POST asíncrona con encabezado Authorization: Bearer <JWT>", "Validación criptográfica de firma HMAC-SHA256 y expiración del token."],
        ["Paso 4", "FastAPI (Depends)", "MedicationService", "Invocación del servicio clínico con sesión SQLAlchemy inyectada", "Apertura determinista de sesión transaccional con cierre en bloque finally."],
        ["Paso 5", "MedicationService", "MySQL 8.0 (InnoDB)", "Ejecución de bloque SQL atómico en 3 sentencias:\n• UPDATE recordatorios SET estado='tomado', fecha_hora_toma=NOW() WHERE id=:id\n• UPDATE medicamentos SET stock_actual = stock_actual - 1 WHERE id=:med_id AND stock_actual > 0\n• INSERT INTO historial_toma (id_usuario, id_medicamento, id_recordatorio, accion, fecha_hora) VALUES (...)\n• COMMIT", "Aislamiento transaccional SERIALIZABLE/REPEATABLE READ con bloqueo de fila foráneo."],
        ["Paso 6", "MySQL 8.0", "FastAPI Service", "Confirmación de commit exitoso y lectura de stock_actual actualizado", "Garantía de no negatividad en stock y concordancia biunívoca con frasco."],
        ["Paso 7", "FastAPI Service", "Cliente Android Retrofit", "Serialización de respuesta JSON HTTP 200 OK: {status: 'success', stock: N}", "Contrato REST validado en Rust mediante esquemas Pydantic v2."],
        ["Paso 8", "ReminderRepository", "UI Móvil (StateFlow)", "Persistencia en base local Room y emisión de nuevo UiState inmutable", "Actualización reactiva de tarjeta, disparo de sonido de éxito y aviso Snackbar."]
    ]
    add_truth_table(doc, seq1_headers, seq1_rows, "Tabla 3.2: Matriz de Secuencia Transaccional de Confirmación de Toma de Medicamentos («Tomar Ahora»)", [0.9, 1.3, 1.3, 2.3, 1.8])
    
    add_body_p(
        doc,
        "2. Flujo Transaccional 2: Posposición Controlada de Tomas de Medicamentos con Límite Determinista (k = 2):\n"
        "Este flujo formaliza la regla de posposición fija (+10 min o +30 min) sujeta a evaluación proposicional "
        "para evitar la acumulación excesiva de dosis y proteger la ventana terapéutica del paciente:"
    )
    
    seq2_headers = ["Paso", "Capa Emisora", "Capa Receptora", "Mensaje / Operación Transaccional", "Regla Lógica / Condición de Bloqueo"]
    seq2_rows = [
        ["Paso 1", "UI Móvil (Card)", "HoyViewModel", "Pulsación del botón «Posponer (+10 min o +30 min)»", "Captura de solicitud activa de aplazamiento C."],
        ["Paso 2", "HoyViewModel", "MedicationService", "Evaluación de condición lógica: posposiciones_actuales < 2", "Predicado proposicional D evaluado deterministamente en backend."],
        ["Paso 3", "MedicationService", "AlarmManager (Android)", "Si D = V: Reprogramación de alarma determinista mediante setExactAndAllowWhileIdle", "Alarma despierta al procesador en modo Doze en el segundo programado."],
        ["Paso 4", "MedicationService", "MySQL 8.0 (InnoDB)", "UPDATE recordatorios SET posposiciones = posposiciones + 1; INSERT historial_toma", "Registro inmutable de auditoría para trazabilidad médica legal."],
        ["Paso 5", "MedicationService", "UI Móvil (Compose)", "Si contador = 2: Inhabilitación total del botón 'Posponer' en la interfaz", "Exclusión mutua obligatoria: el paciente solo puede elegir 'Tomar Ahora' u 'Omitir'."]
    ]
    add_truth_table(doc, seq2_headers, seq2_rows, "Tabla 3.3: Matriz de Secuencia Transaccional de Posposición con Límite Determinista (k=2)", [0.6, 1.4, 1.4, 2.3, 1.8])
    
    # ==========================================================================
    # 4. INSTALACIÓN SOLO DE LAS PAQUETERÍAS Y DE LOS ELEMENTOS QUE INDICAN EN LOS RF
    # ==========================================================================
    add_section_heading(doc, "4. INSTALACIÓN SOLO DE LAS PAQUETERÍAS Y DE LOS ELEMENTOS QUE INDICAN EN LOS REQUISITOS FUNCIONALES (NO ES TODO EL PROCESO DE INSTALACIÓN)", level=1, page_break_before=True)
    
    add_section_heading(doc, "4.1 Alcance Delimitado: Paqueterías Estrictamente Vinculadas a los Requisitos Funcionales", level=2)
    add_body_p(
        doc,
        "Conforme a los lineamientos normativos de evaluación, esta sección NO detalla el proceso completo de aprovisionamiento de sistemas "
        "operativos o hardware, sino que se delimita estrictamente a la especificación, instalación y vinculación funcional de las "
        "paqueterías, bibliotecas de software y dependencias exactas que dan soporte a los Requisitos Funcionales (RF-01 a RF-12).\n\n"
        "Cualquier mantenedor que instale un entorno de pruebas debe aprovisionar únicamente estos paquetes para garantizar el funcionamiento "
        "íntegro de los módulos clínicos."
    )
    
    add_section_heading(doc, "4.2 Matriz de Paqueterías del Backend Python vs. Requisitos Funcionales", level=2)
    add_body_p(
        doc,
        "El archivo requirements.txt del backend agrupa las paqueterías indispensables para la ejecución de los microservicios. "
        "La siguiente matriz vincula cada paquete con su correspondiente requisito funcional:"
    )
    
    pkg_headers = ["Paquetería Python", "Versión Mínima", "RF Asociados", "Justificación y Rol en Requisitos Funcionales"]
    pkg_rows = [
        ["fastapi", ">=0.110.0", "RF-01 a RF-12", "Núcleo de la API REST asíncrona; despacha endpoints de gestión y tomas de medicamentos."],
        ["uvicorn[standard]", ">=0.29.0", "RF-01 a RF-12", "Servidor ASGI de alto rendimiento con soporte para workers concurrentes."],
        ["pydantic", ">=2.6.0", "RF-01, RF-02, RF-07", "Validación estricta de payloads clínicos, dosis, frecuencias y fechas."],
        ["sqlalchemy", ">=2.0.28", "RF-01, RF-04, RF-05, RF-08", "Mapeo relacional y orquestación de transacciones ACID en MySQL."],
        ["pymysql", ">=1.1.0", "RF-01, RF-04, RF-05, RF-08", "Conector nativo Python para la comunicación TCP con MySQL Server 8.0."],
        ["pymongo", ">=4.6.2", "RF-09, RF-11", "Persistencia documental para telemetría de IA y bitácora de diálogo con Medi."],
        ["passlib[bcrypt]", ">=1.7.4", "RF-01 (Seguridad)", "Hashing irreversible de contraseñas con salt criptográfico de 128 bits."],
        ["python-jose[cryptography]", ">=3.3.0", "RF-01 (Seguridad)", "Firma y verificación de tokens JWT Bearer para autorización de sesiones."],
        ["python-dotenv", ">=1.0.1", "RF-01 a RF-12", "Carga de variables de entorno y credenciales seguras desde archivo .env."]
    ]
    add_truth_table(doc, pkg_headers, pkg_rows, "Tabla 4.1: Paqueterías del Backend Python y su Vínculo con Requisitos Funcionales", [1.3, 1.0, 1.4, 2.8])
    
    add_code_block(
        doc,
        """# Instalación exclusiva de paqueterías del backend vinculadas a los RF
cd backend
python -m venv .venv
source .venv/bin/activate  # En Windows: .venv\\Scripts\\activate
pip install --upgrade pip
pip install -r requirements.txt""",
        caption="Comando de instalación de paqueterías del backend en entorno virtual"
    )
    
    add_section_heading(doc, "4.3 Matriz de Dependencias Gradle en Android vs. Requisitos Funcionales", level=2)
    add_body_p(
        doc,
        "En la aplicación Android, las dependencias gestionadas mediante Gradle en build.gradle.kts implementan directamente las capacidades "
        "exigidas en los Requisitos Funcionales:"
    )
    
    grad_headers = ["Dependencia de Gradle", "Artefacto / Versión", "RF Asociados", "Función en los Requisitos Funcionales"]
    grad_rows = [
        ["Compose UI & Material 3", "androidx.compose.material3:1.2.1", "RF-01 a RF-12", "Construcción de interfaces táctiles accesibles con botones >= 56 dp."],
        ["Navigation Compose", "androidx.navigation:navigation-compose:2.7.7", "RF-01 a RF-12", "Enrutamiento declarativo entre vistas (Login, Hoy, Botiquín, Progreso)."],
        ["Retrofit & Converter Gson", "com.squareup.retrofit2:retrofit:2.11.0", "RF-01, RF-05, RF-08", "Comunicación HTTP REST con el backend para sincronización transaccional."],
        ["Room Persistence Library", "androidx.room:room-runtime:2.6.1", "RF-03, RF-05, RF-08", "Caché relacional SQLite local que garantiza operación 100% offline."],
        ["AndroidX Core KTX", "androidx.core:core-ktx:1.13.1", "RF-03, RF-06", "Integración con APIs del sistema operativo Android y AlarmManager."],
        ["AndroidX Security Crypto", "androidx.security:security-crypto:1.1.0-alpha06", "RF-01 (Seguridad)", "Almacenamiento seguro del token JWT en EncryptedSharedPreferences."]
    ]
    add_truth_table(doc, grad_headers, grad_rows, "Tabla 4.2: Dependencias de Gradle del Cliente Android por Requisito Funcional", [1.4, 1.5, 1.2, 2.4])
    
    add_section_heading(doc, "4.4 Entorno de Ejecución Contenedorizado y SDKs Base", level=2)
    add_body_p(
        doc,
        "Los elementos de entorno requeridos para dar soporte a los Requisitos Funcionales abarcan:\n\n"
        "• Java Development Kit (JDK 17 LTS): Requerido por el compilador de Kotlin 2.0 y el entorno Gradle en Android Studio Ladybug / Koala.\n"
        "• Android SDK Platform 34 / 35: Plataforma de compilación para soporte de permisos exactos de alarma y notificaciones Heads-Up.\n"
        "• Docker Engine 26.0+ y Compose v2: Motores de ejecución para levantar de forma aislada los contenedores de MySQL 8.0 y MongoDB 6.0."
    )
    
    # ==========================================================================
    # 5. ESTRUCTURA DEL PROYECTO
    # ==========================================================================
    add_section_heading(doc, "5. ESTRUCTURA DEL PROYECTO", level=1, page_break_before=True)
    
    add_section_heading(doc, "5.1 Estructura Modular y Organización de Directorios del Repositorio", level=2)
    add_body_p(
        doc,
        "El repositorio de MedReminder AI sigue un esquema de monorepo estructurado que organiza con estricta coherencia modular "
        "el backend de microservicios, la aplicación móvil nativa, los módulos matemáticos de Inteligencia Artificial y los scripts de soporte. "
        "La siguiente matriz formal desglosa la jerarquía canónica de directorios, sus tecnologías base y sus responsabilidades de ingeniería:"
    )
    
    tree_headers = ["Módulo / Directorio", "Ruta en Repositorio", "Tecnología Base", "Propósito y Responsabilidad de Ingeniería"]
    tree_rows = [
        ["Microservicio Backend", "backend/", "Python 3.11+ / FastAPI", "Aloja los microservicios REST, inyección de dependencias, lógica clínica y modelos de datos."],
        ["Capa API y Enrutadores", "backend/app/api/", "FastAPI APIRouter", "Controladores REST modulares por dominio (/auth, /medicamentos, /recordatorios, /ia)."],
        ["Núcleo y Seguridad", "backend/app/core/", "Passlib / Cryptography", "Configuración central (.env), hashing bcrypt de credenciales y firma de tokens JWT Bearer."],
        ["Sesiones de Persistencia", "backend/app/db/", "SQLAlchemy / PyMongo", "Conexiones transaccionales pooling para MySQL 8.0 y cliente documental de MongoDB 6.0."],
        ["Modelos Relacionales ORM", "backend/app/models/", "SQLAlchemy (InnoDB)", "Entidades de mapeo relacional en 3FN para tablas usuarios, medicamentos, recordatorios."],
        ["Esquemas de Validación", "backend/app/schemas/", "Pydantic v2", "Contratos tipados para validación estricta de payloads JSON entrantes y salientes."],
        ["Servicios de Negocio", "backend/app/services/", "Python / SQLAlchemy", "Transacciones atómicas: confirmación de tomas de medicamentos, posposición (k=2) y stock."],
        ["Cliente Móvil Android", "app/", "Kotlin 2.0 / Compose", "Aplicación móvil nativa bajo patrón arquitectónico MVVM y componentes Material Design 3."],
        ["Persistencia Móvil Local", "app/.../data/", "AndroidX Room (SQLite)", "Caché relacional local que garantiza funcionamiento autónomo 100% fuera de línea."],
        ["Módulo de Red Móvil", "app/.../network/", "Retrofit 2 / Gson", "Cliente HTTP REST y conmutador inteligente de IP dinámico (LAN / emulador)."],
        ["Presentación y UI", "app/.../presentation/", "AndroidX ViewModel", "Modelos de vista reactivos con StateFlow para gestión inmutable del estado visual."],
        ["Alarmas Deterministas", "app/.../receiver/", "AlarmManager / Broadcast", "Temporización exacta en tiempo real (RTC) y reprogramación post-reinicio (BOOT)."],
        ["Componentes Visuales", "app/.../ui/", "Jetpack Compose", "Interfaces táctiles accesibles con botones amplios (altura mayor o igual a 56 dp)."],
        ["Inteligencia Artificial", "busquedas/", "Python / Grafos IA", "Algoritmos de búsqueda en espacios de estados: DFS con poda anticiclos, BFS, UCS y A*."],
        ["Base de Datos y DDL", "db/", "MySQL 8.0 / Mongo 6.0", "Script canónico init_mysql.sql en 3FN con claves foráneas y setup documental."],
        ["Orquestación Multi-Stack", "docker-compose.yml", "Docker Compose v2", "Definición para orquestar contenedores aislados de API, MySQL Server y MongoDB Server."],
        ["Documentación Oficial", "docs/", "DOCX / PNG Screens", "Manuales normativos institucionales con carátula UTVT, evidencias y capturas reales."],
        ["Compilación Automatizada", "scripts/", "Python / python-docx", "Suite de scripts generadores, auditoría de calidad académica y sincronización en espejo."]
    ]
    add_truth_table(doc, tree_headers, tree_rows, "Tabla 5.1: Organización Modular y Estructura Canónica de Directorios del Repositorio", [1.5, 1.4, 1.4, 2.7])
    
    add_section_heading(doc, "5.2 Desglose Funcional de Directorios del Backend", level=2)
    add_body_p(
        doc,
        "• app/api/: Aloja los controladores REST organizados por submódulos de dominio (auth.py, medicamentos.py, recordatorios.py, etc.). "
        "Cada archivo define rutas HTTP con inyección de dependencias.\n\n"
        "• app/core/: Contiene las configuraciones de seguridad (security.py) para el hashing de contraseñas con passlib, generación de tokens JWT con jose, "
        "y carga de variables de entorno (config.py).\n\n"
        "• app/db/: Gestiona las conexiones pooling a MySQL (session.py) y el cliente de MongoDB (mongo.py).\n\n"
        "• app/models/: Define las clases ORM de SQLAlchemy que mapean las tablas relacionales de MySQL (usuario.py, medicamento.py, recordatorio.py, historial_toma.py).\n\n"
        "• app/schemas/: Alberga los esquemas Pydantic v2 que formalizan los contratos de entrada y salida JSON con validación de tipos.\n\n"
        "• app/services/: Implementa la lógica transaccional de negocio: confirmación atómica de tomas de medicamentos, posposición con límite k=2, "
        "y descuento de unidades del botiquín."
    )
    
    add_section_heading(doc, "5.3 Desglose Funcional de Módulos de la Aplicación Android", level=2)
    add_body_p(
        doc,
        "• data/: Implementa el patrón Repository unificando el cliente HTTP de Retrofit con la base de datos local SQLite de Room.\n\n"
        "• network/: Incluye NetworkModule.kt, el cual provee el conmutador inteligente de IP con sondeo de baja latencia para operar entre LAN y emulador.\n\n"
        "• presentation/: Contiene los ViewModels (HoyViewModel, BotiquinViewModel, MediViewModel) que exponen StateFlows inmutables a la UI.\n\n"
        "• receiver/: Alberga ReminderAlarmReceiver.kt (disparo de alertas con WakeLock) y BootCompletedReceiver.kt (restauración de alarmas tras reinicio del teléfono).\n\n"
        "• ui/: Comprende las pantallas composables (LoginScreen, HoyScreen, BotiquinScreen, AnalisisDfsScreen) y componentes ergonómicos con altura >= 56 dp."
    )
    
    add_section_heading(doc, "5.4 Módulos de Inteligencia Artificial, Grafos y Scripts de Soporte", level=2)
    add_body_p(
        doc,
        "• busquedas/: Contiene los scripts de simulación y evaluación de algoritmos de búsqueda en espacios de estados (busqueda_medreminder.py), "
        "implementando la detección y poda de ciclos para el ciclo de vida de tomas de medicamentos y comparativas curriculares.\n\n"
        "• scripts/: Centraliza la suite automatizada de construcción y auditoría documental (build_all_manuals.py, doc_utils.py), garantizando "
        "el cumplimiento estricto de tablas de verdad evaluadas con 'V' y 'F', campo nativo TOC y paridad entre directorios."
    )
    
    # ==========================================================================
    # 6. CONFIGURACIÓN
    # ==========================================================================
    add_section_heading(doc, "6. CONFIGURACIÓN", level=1, page_break_before=True)
    
    add_section_heading(doc, "6.1 Variables de Entorno del Sistema (.env)", level=2)
    add_body_p(
        doc,
        "El backend de MedReminder AI gestiona sus parámetros operativos y secretos criptográficos mediante el archivo de entorno .env. "
        "La siguiente tabla describe cada variable, su formato y su impacto en la seguridad del sistema:"
    )
    
    env_headers = ["Variable de Entorno", "Valor por Defecto / Ejemplo", "Tipo / Formato", "Descripción y Función Operativa"]
    env_rows = [
        ["MYSQL_HOST", "mysql-db", "Hostname / IP", "Dirección de red del host donde corre el motor MySQL 8.0."],
        ["MYSQL_PORT", "3306", "Entero (Puerto)", "Puerto TCP de escucha para conexiones entrantes a MySQL."],
        ["MYSQL_USER", "meduser", "Cadena", "Usuario de base de datos con privilegios DDL/DML acotados."],
        ["MYSQL_PASSWORD", "medpassword_sec2026", "Secreto (String)", "Contraseña segura de acceso al servidor de base de datos MySQL."],
        ["MYSQL_DB", "medreminder_db", "Cadena", "Nombre de la base de datos relacional principal del sistema."],
        ["MONGO_URI", "mongodb://mongo-db:27017", "URI de Conexión", "Cadena de conexión para la base documental MongoDB 6.0."],
        ["MONGO_DB_NAME", "medreminder_telemetry", "Cadena", "Nombre de la base de datos para logs y telemetría de IA."],
        ["SECRET_KEY", "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7", "Hexadecimal (256 bits)", "Clave criptográfica maestra para la firma HMAC-SHA256 de tokens JWT."],
        ["ALGORITHM", "HS256", "Cadena", "Algoritmo criptográfico utilizado para la firma digital de tokens."],
        ["ACCESS_TOKEN_EXPIRE_MINUTES", "10080", "Entero (Minutos)", "Lapso de validez del token JWT de sesión (10080 min = 7 días continuos)."]
    ]
    add_truth_table(doc, env_headers, env_rows, "Tabla 6.1: Variables de Entorno y Configuración Criptográfica del Backend", [1.6, 1.6, 1.1, 2.2])
    
    add_section_heading(doc, "6.2 Parámetros de Conexión a Motores de Persistencia", level=2)
    add_body_p(
        doc,
        "La conexión a MySQL se construye dinámicamente en app/core/config.py mediante SQLAlchemy Pool:\n"
        "• URL Relacional: mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DB}?charset=utf8mb4\n"
        "• Pool Size: 10 conexiones persistentes con max_overflow=20 para absorber picos de tráfico concurrente.\n"
        "• Pool Recycle: 3600 segundos (1 hora) para evitar cortes por timeout silencioso del servidor MySQL.\n\n"
        "Para MongoDB, se inicializa el cliente MongoClient con un pool máximo de 50 sockets concurrentes y un serverSelectionTimeoutMS de 5000 ms."
    )
    
    add_section_heading(doc, "6.3 Configuración de IPs Dinámicas y Conmutador de Red Móvil", level=2)
    add_body_p(
        doc,
        "Para solventar la volatilidad de direcciones IP en redes Wi-Fi residenciales o de laboratorio escolar (UTVT), NetworkModule.kt "
        "en Android implementa un conmutador rápido inteligente (Fast IP Switcher):\n\n"
        "1. Lista de Candidatos Ordenada: [IP fija de desarrollo (192.168.1.XX), IP de emulador estándar (10.0.2.2), IP local (127.0.0.1)].\n"
        "2. Sondeo de Conectividad con Timeout Agresivo: Al iniciar, la aplicación efectúa un ping HTTP GET /health con timeout de 1500 ms hacia "
        "cada candidato en paralelo.\n"
        "3. Selección Inmediata: La primera dirección en retornar HTTP 200 OK es seleccionada como BaseURL activa para Retrofit, "
        "impidiendo que el usuario perciba pantallas congeladas por timeouts prolongados de red."
    )
    
    add_section_heading(doc, "6.4 Parámetros de Timeout, Políticas de Retry y Sesión Criptográfica", level=2)
    add_body_p(
        doc,
        "Las políticas de tolerancia y reintentos en red son:\n"
        "• Timeout de Llamadas REST: 10 segundos en llamadas transaccionales (confirmar tomas de medicamentos) y 5 segundos en lecturas de catálogo.\n"
        "• Política de Reintentos: 3 intentos con retroceso exponencial (exponential backoff: 1s, 2s, 4s) antes de conmutar a almacenamiento en cola offline local.\n"
        "• Expiración de Sesión Móvil: Los tokens JWT emitidos tienen validez de 7 días. El cliente Android custodia el token en EncryptedSharedPreferences "
        "y lo refresca automáticamente de fondo cuando resta menos del 20 % de su tiempo de vida."
    )
    
    # ==========================================================================
    # 7. MODELO DE DATOS
    # ==========================================================================
    add_section_heading(doc, "7. MODELO DE DATOS", level=1, page_break_before=True)
    
    add_section_heading(doc, "7.1 Modelo Entidad-Relación y Normalización en Tercera Forma Normal (3FN)", level=2)
    add_body_p(
        doc,
        "El esquema relacional de MedReminder AI fue normalizado rigurosamente hasta la Tercera Forma Normal (3FN):\n\n"
        "1. Primera Forma Normal (1FN): Todos los atributos son atómicos y no existen grupos repetitivos. Horarios y frecuencias se "
        "descomponen en registros individuales en la tabla recordatorios.\n\n"
        "2. Segunda Forma Normal (2FN): Se eliminan las dependencias parciales. Toda columna no primaria depende de manera completa "
        "y directa de la clave primaria de la tabla.\n\n"
        "3. Tercera Forma Normal (3FN): Se eliminan las dependencias transitivas. Ninguna columna no clave depende de otra columna no clave. "
        "Por ejemplo, los datos del medicamento (nombre, presentación) se vinculan mediante id_medicamento y no se duplican en las tomas de medicamentos.\n\n"
        "La siguiente matriz formal de entidades y relaciones detalla la topología relacional, claves primarias, claves foráneas y cardinalidades:"
    )
    
    er_headers = ["Entidad (Tabla)", "Clave Primaria (PK)", "Claves Foráneas (FK)", "Cardinalidad", "Rol en Tomas de Medicamentos e Integridad Referencial"]
    er_rows = [
        ["usuarios", "id (INT AUTO_INCREMENT)", "Ninguna (Entidad fuerte)", "1 : N con medicamentos\n1 : N con tratamientos\n1 : N con historial_toma", "Almacena perfiles de pacientes y credenciales con hash criptográfico irreversible."],
        ["medicamentos", "id (INT AUTO_INCREMENT)", "id_usuario (referencia a usuarios.id) [CASCADE]", "1 : N con recordatorios\n1 : N con historial_toma", "Catálogo maestro y botiquín virtual; registra stock actual, presentación y alertas mínimas."],
        ["tratamientos", "id (INT AUTO_INCREMENT)", "id_usuario (usuarios.id)\nid_medicamento (medicamentos.id)", "1 : N con recordatorios", "Formaliza la prescripción médica: dosis, intervalo de horas, fecha inicio y estatus activo."],
        ["recordatorios", "id (INT AUTO_INCREMENT)", "id_usuario (usuarios.id)\nid_medicamento (medicamentos.id)\nid_tratamiento (tratamientos.id)", "1 : 1 con evento de toma de medicamentos activa", "Programa cada instancia temporal de tomas de medicamentos: estado, posposiciones (k=2) y alarma."],
        ["historial_toma", "id (INT AUTO_INCREMENT)", "id_usuario (usuarios.id)\nid_medicamento (medicamentos.id)\nid_recordatorio (recordatorios.id)", "N : 1 con cada entidad clínica", "Bitácora inmutable de farmacovigilancia: audita tomas de medicamentos confirmadas, pospuestas u omitidas."]
    ]
    add_truth_table(doc, er_headers, er_rows, "Tabla 7.1: Matriz de Entidades Relacionales, Claves y Cardinalidades del Modelo en 3FN", [1.1, 1.4, 1.5, 1.2, 2.3])
    
    add_section_heading(doc, "7.2 Especificación DDL SQL Completa de MySQL 8.0", level=2)
    add_body_p(
        doc,
        "A continuación se reproduce el script DDL canónico de inicialización de la base de datos relacional MySQL 8.0 "
        "(alojado en db/init_mysql.sql), con integridad referencial y motor transaccional InnoDB:"
    )
    
    ddl_sql = """-- db/init_mysql.sql - Esquema relacional formal en 3FN de MedReminder AI
CREATE DATABASE IF NOT EXISTS medreminder_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE medreminder_db;

-- 1. Tabla de Usuarios y Credenciales
CREATE TABLE IF NOT EXISTS usuarios (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(120) NOT NULL,
    email VARCHAR(160) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    rol VARCHAR(30) DEFAULT 'paciente',
    fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB;

-- 2. Catálogo de Medicamentos y Botiquín
CREATE TABLE IF NOT EXISTS medicamentos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    id_usuario INT NOT NULL,
    nombre VARCHAR(120) NOT NULL,
    principio_activo VARCHAR(120),
    presentacion VARCHAR(60) NOT NULL,
    concentracion VARCHAR(60),
    stock_actual INT NOT NULL DEFAULT 0,
    stock_minimo_alerta INT NOT NULL DEFAULT 5,
    instrucciones_toma TEXT,
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (id_usuario) REFERENCES usuarios(id) ON DELETE CASCADE
) ENGINE=InnoDB;

-- 3. Tratamientos y Prescripciones Médicas
CREATE TABLE IF NOT EXISTS tratamientos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    id_usuario INT NOT NULL,
    id_medicamento INT NOT NULL,
    dosis_cantidad VARCHAR(60) NOT NULL,
    frecuencia_horas INT NOT NULL,
    fecha_inicio DATE NOT NULL,
    fecha_fin DATE,
    activo BOOLEAN DEFAULT TRUE,
    FOREIGN KEY (id_usuario) REFERENCES usuarios(id) ON DELETE CASCADE,
    FOREIGN KEY (id_medicamento) REFERENCES medicamentos(id) ON DELETE CASCADE
) ENGINE=InnoDB;

-- 4. Recordatorios y Programación de Tomas de Medicamentos
CREATE TABLE IF NOT EXISTS recordatorios (
    id INT AUTO_INCREMENT PRIMARY KEY,
    id_tratamiento INT NOT NULL,
    fecha_hora_programada DATETIME NOT NULL,
    estado ENUM('pendiente', 'tomado', 'pospuesto', 'omitido') DEFAULT 'pendiente',
    contador_posposiciones INT DEFAULT 0,
    fecha_hora_toma DATETIME NULL,
    notas_omision VARCHAR(255) NULL,
    FOREIGN KEY (id_tratamiento) REFERENCES tratamientos(id) ON DELETE CASCADE,
    INDEX idx_estado_fecha (estado, fecha_hora_programada)
) ENGINE=InnoDB;

-- 5. Bitácora Médico-Legal Inmutable de Tomas de Medicamentos
CREATE TABLE IF NOT EXISTS historial_toma (
    id INT AUTO_INCREMENT PRIMARY KEY,
    id_usuario INT NOT NULL,
    id_medicamento INT NOT NULL,
    id_recordatorio INT NOT NULL,
    accion ENUM('tomado', 'pospuesto', 'omitido', 'revertido') NOT NULL,
    fecha_hora TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    motivo_omision VARCHAR(255) NULL,
    FOREIGN KEY (id_usuario) REFERENCES usuarios(id),
    FOREIGN KEY (id_medicamento) REFERENCES medicamentos(id),
    FOREIGN KEY (id_recordatorio) REFERENCES recordatorios(id)
) ENGINE=InnoDB;

-- 6. Alergias y Contraindicaciones Críticas
CREATE TABLE IF NOT EXISTS alergias (
    id INT AUTO_INCREMENT PRIMARY KEY,
    id_usuario INT NOT NULL,
    sustancia VARCHAR(120) NOT NULL,
    severidad ENUM('leve', 'moderada', 'grave_anafilaxia') DEFAULT 'moderada',
    notas VARCHAR(255),
    FOREIGN KEY (id_usuario) REFERENCES usuarios(id) ON DELETE CASCADE
) ENGINE=InnoDB;

-- 7. Red de Contactos de Apoyo y Emergencia
CREATE TABLE IF NOT EXISTS contactos_emergencia (
    id INT AUTO_INCREMENT PRIMARY KEY,
    id_usuario INT NOT NULL,
    nombre VARCHAR(120) NOT NULL,
    parentesco VARCHAR(60) NOT NULL,
    telefono VARCHAR(20) NOT NULL,
    notificaciones_activas BOOLEAN DEFAULT TRUE,
    FOREIGN KEY (id_usuario) REFERENCES usuarios(id) ON DELETE CASCADE
) ENGINE=InnoDB;

-- 8. Gamificación, Rachas y Rango de Honor
CREATE TABLE IF NOT EXISTS gamificacion_honor (
    id INT AUTO_INCREMENT PRIMARY KEY,
    id_usuario INT NOT NULL UNIQUE,
    racha_dias INT DEFAULT 0,
    escudos_activos INT DEFAULT 0,
    rango VARCHAR(30) DEFAULT 'Hierro',
    modo_castigo BOOLEAN DEFAULT FALSE,
    ultima_actualizacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (id_usuario) REFERENCES usuarios(id) ON DELETE CASCADE
) ENGINE=InnoDB;"""
    add_code_block(doc, ddl_sql, "Script DDL completo en 3FN de MySQL 8.0 (db/init_mysql.sql)")
    
    add_section_heading(doc, "7.3 Colecciones y Esquema de Telemetría en MongoDB 6.0", level=2)
    add_body_p(
        doc,
        "En la base no relacional MongoDB (medreminder_telemetry), se definen tres colecciones documentales:\n\n"
        "• activity_logs: Registra eventos de autenticación, inicios de sesión, cambios de red y latencias de sincronización.\n"
        "• medi_dialogs: Almacena transcripciones de interacciones asistidas por voz con el acompañante Medi, intenciones detectadas "
        "y métricas de sentimiento emocional del paciente.\n"
        "• search_traces: Custodia las trazas completas de exploración algorítmica de grafos en IA (nodos expandidos, aristas de ciclos podadas y rutas generadas)."
    )
    
    add_section_heading(doc, "7.4 Diccionario Formal de Datos y Variables de Persistencia", level=2)
    add_body_p(
        doc,
        "La estructura detallada de tipos de datos, rangos permitidos y restricciones de persistencia se encuentra catalogada "
        "exhaustivamente en el Anexo D al final de este manual."
    )
    
    # ==========================================================================
    # 8. MÓDULOS Y API
    # ==========================================================================
    add_section_heading(doc, "8. MÓDULOS Y API", level=1, page_break_before=True)
    
    add_section_heading(doc, "8.1 Catálogo Exhaustivo de Endpoints REST de FastAPI", level=2)
    add_body_p(
        doc,
        "La siguiente matriz resume la totalidad de endpoints provistos por el backend FastAPI, sus métodos HTTP, nivel de autenticación "
        "y códigos de respuesta esperados:"
    )
    
    api_headers = ["Método", "Ruta / Endpoint", "Auth", "Request Schema", "Response Schema", "Códigos HTTP"]
    api_rows = [
        ["POST", "/auth/login", "Pública", "LoginRequest (email, password)", "TokenResponse (jwt, user_info)", "200, 400, 401, 422"],
        ["POST", "/auth/registro", "Pública", "UserCreate (nombre, email, pass)", "UserOut (id, email, fecha)", "201, 400, 422"],
        ["GET", "/medicamentos/", "Bearer JWT", "None (Query params opcionales)", "List[MedicamentoOut]", "200, 401"],
        ["POST", "/medicamentos/", "Bearer JWT", "MedicamentoCreate", "MedicamentoOut", "201, 400, 401, 422"],
        ["PUT", "/medicamentos/{id}", "Bearer JWT", "MedicamentoUpdate", "MedicamentoOut", "200, 401, 404, 422"],
        ["POST", "/medicamentos/{id}/recargar", "Bearer JWT", "RecargaRequest (cantidad: INT)", "StockResponse", "200, 401, 404, 422"],
        ["GET", "/recordatorios/hoy", "Bearer JWT", "None (Filtro fecha actual)", "List[RecordatorioCardOut]", "200, 401"],
        ["POST", "/recordatorios/{id}/confirmar", "Bearer JWT", "None (Trigger atómico)", "TomaActionResult", "200, 400, 401, 404"],
        ["POST", "/recordatorios/{id}/posponer", "Bearer JWT", "PosponerRequest (minutos: INT)", "TomaActionResult", "200, 400, 401, 404, 409"],
        ["POST", "/recordatorios/{id}/omitir", "Bearer JWT", "OmisionRequest (motivo: STR)", "TomaActionResult", "200, 400, 401, 404"],
        ["POST", "/recordatorios/{id}/deshacer", "Bearer JWT", "None (Reversión atómica)", "TomaActionResult", "200, 400, 401, 404, 409"],
        ["GET", "/alergias/", "Bearer JWT", "None", "List[AlergiaOut]", "200, 401"],
        ["POST", "/alergias/", "Bearer JWT", "AlergiaCreate", "AlergiaOut", "201, 401, 422"],
        ["GET", "/contactos/", "Bearer JWT", "None", "List[ContactoOut]", "200, 401"],
        ["POST", "/contactos/", "Bearer JWT", "ContactoCreate", "ContactoOut", "201, 401, 422"],
        ["GET", "/recordatorios/dashboard", "Bearer JWT", "Query (fecha: YYYY-MM-DD)", "DashboardUnifiedOut", "200, 401"],
        ["POST", "/ai/chat", "Bearer JWT", "AIChatRequest (prompt, contexto)", "AIChatResponse (Ollama medi-clinico)", "200, 401, 503"],
        ["POST", "/ai/sugerir-medicamento", "Bearer JWT", "AISugerenciaRequest (nombre)", "AISugerenciaResponse", "200, 401"],
        ["POST", "/ai/analizar-receta", "Bearer JWT", "Multipart/Base64 (imagen receta)", "AIRecetaResponse (lista JSON)", "200, 401, 422"],
        ["GET", "/cuidador/panel", "Bearer JWT", "None", "CuidadorPanelOut (pacientes, alertas)", "200, 401"],
        ["GET", "/cuidador/alertas", "Bearer JWT", "None", "List[AlertaCuidadorOut]", "200, 401"],
        ["PUT", "/auth/me/edad", "Bearer JWT", "EdadUpdate (fecha_nacimiento)", "UserOut (edad, rango_edad)", "200, 401, 422"],
        ["GET", "/gamificacion/status", "Bearer JWT", "None", "GamificacionOut", "200, 401"],
        ["GET", "/health", "Pública", "None", "HealthOut (status, mysql, mongo)", "200, 503"]
    ]
    add_truth_table(doc, api_headers, api_rows, "Tabla 8.1: Catálogo Exhaustivo de Endpoints REST de la API de MedReminder AI", [0.7, 1.8, 0.9, 1.2, 1.1, 0.8])
    
    add_section_heading(doc, "8.2 Especificación de Payloads JSON y Contratos REST por Módulo", level=2)
    add_body_p(
        doc,
        "A continuación se documentan los esquemas JSON de intercambio para las operaciones transaccionales críticas sobre tomas de medicamentos:"
    )
    
    json_confirm = """// POST /recordatorios/{id}/confirmar : Respuesta exitosa HTTP 200 OK
{
  "status": "success",
  "codigo": "TOMA_CONFIRMADA",
  "recordatorio_id": 42,
  "nuevo_estado": "tomado",
  "fecha_hora_efectiva": "2026-10-21T08:02:15Z",
  "descuento_inventario": {
    "medicamento_id": 10,
    "unidades_descontadas": 1,
    "stock_restante": 29,
    "alerta_stock_critico": false
  },
  "gamificacion": {
    "dias_racha_actual": 14,
    "rango_honor": "Plata",
    "escudos_disponibles": 2
  }
}"""
    add_code_block(doc, json_confirm, "Contrato JSON de respuesta al confirmar tomas de medicamentos exitosamente")
    
    json_posponer_error = """// POST /recordatorios/{id}/posponer : Error por límite excedido HTTP 409 Conflict
{
  "detail": {
    "error_code": "LIMITE_POSPOSICIONES_EXCEDIDO",
    "mensaje": "No es posible posponer la toma de medicamentos: se ha alcanzado el límite estricto de 2 posposiciones.",
    "contador_actual": 2,
    "accion_requerida": "Debe confirmar la ingesta ('Tomar Ahora') o registrar la omisión justificada por seguridad clínica."
  }
}"""
    add_code_block(doc, json_posponer_error, "Contrato JSON de error HTTP 409 al violar el límite k=2 de posposiciones")
    
    add_section_heading(doc, "8.3 Descripción de Servicios Internos del Backend", level=2)
    add_body_p(
        doc,
        "• AuthService: Gestiona autenticación, hashing de contraseñas mediante Passlib y firma de tokens JWT HS256.\n\n"
        "• MedicationService: Implementa el CRUD de fármacos, validación de inventario inicial y cálculo de alertas de stock.\n\n"
        "• ReminderTransactionService: Servicio transaccional crítico que orquesta la exclusión mutua de estados en tomas de medicamentos, "
        "garantizando que la confirmación, posposición u omisión actualicen atómicamente la tabla recordatorios y el inventario en un solo commit SQL.\n\n"
        "• HonorGamificationService: Evalúa diariamente la racha del paciente, asigna escudos de lealtad y activa el Modo Castigo si se detectan omisiones continuas.\n\n"
        "• MediService: Interpreta expresiones en lenguaje natural y genera respuestas empáticas estructuradas para el asistente virtual."
    )
    
    add_section_heading(doc, "8.4 Códigos de Estado HTTP y Manejo Estandarizado de Errores", level=2)
    add_body_p(
        doc,
        "La API de MedReminder AI adhiere a los estándares RFC 7231:\n"
        "• 200 OK: Operación de lectura o actualización completada con éxito.\n"
        "• 201 Created: Entidad creada exitosamente (registro de usuario o fármaco).\n"
        "• 400 Bad Request: Parámetros semánticamente inválidos o conflicto de datos (correo ya registrado).\n"
        "• 401 Unauthorized: Token JWT ausente, expirado o con firma criptográfica no válida.\n"
        "• 403 Forbidden: Paciente intentando acceder a prescripciones o datos de otro usuario.\n"
        "• 404 Not Found: El identificador de recordatorio o medicamento no existe en la base de datos.\n"
        "• 409 Conflict: Violación de regla clínica de exclusión mutua o límite de posposiciones superado.\n"
        "• 422 Unprocessable Entity: Validación fallida en Pydantic (tipos incompatibles, cadenas vacías).\n"
        "• 500 Internal Server Error: Excepción no controlada en servidor o caída de motor de persistencia."
    )
    
    # ==========================================================================
    # 9. PRUEBAS
    # ==========================================================================
    add_section_heading(doc, "9. PRUEBAS", level=1, page_break_before=True)
    
    add_section_heading(doc, "9.1 Estrategia Integral de Aseguramiento de Calidad", level=2)
    add_body_p(
        doc,
        "El plan de pruebas de MedReminder AI sigue la Pirámide de Automatización de Pruebas (Testing Pyramid):\n"
        "1. Pruebas Unitarias (70 %): Verifican funciones aisladas, hashing de credenciales, leyes de De Morgan en lógica de negocio y esquemas Pydantic.\n"
        "2. Pruebas de Integración (20 %): Evalúan la interacción de microservicios con MySQL real en contenedor Docker, transaccionalidad de tomas de medicamentos y tokens JWT.\n"
        "3. Pruebas de Interfaz y UI Móvil (10 %): Verifican en Android Compose la renderización a 60 fps, dimensiones táctiles (>= 56 dp) y prevención de pulsaciones dobles."
    )
    
    add_section_heading(doc, "9.2 Pruebas Unitarias del Backend con pytest", level=2)
    add_body_p(
        doc,
        "A continuación se presenta un caso de prueba representativo con pytest que valida la exclusión mutua y el límite de posposiciones:"
    )
    
    test_code = """# backend/tests/test_recordatorios_transaccional.py
import pytest
from app.services.reminder_service import ReminderTransactionService

def test_posposicion_limite_maximo(db_session, test_user, test_reminder):
    service = ReminderTransactionService(db_session)
    
    # Primera posposición válida (k=1)
    res1 = service.posponer_toma(test_reminder.id, minutos=30)
    assert res1.contador_posposiciones == 1
    assert res1.estado == "pospuesto"
    
    # Segunda posposición válida (k=2)
    res2 = service.posponer_toma(test_reminder.id, minutos=30)
    assert res2.contador_posposiciones == 2
    assert res2.estado == "pospuesto"
    
    # Tercera posposición debe arrojar excepción clínica bloqueante (k=3 prohibido)
    with pytest.raises(ValueError) as excinfo:
        service.posponer_toma(test_reminder.id, minutos=30)
    assert "LIMITE_POSPOSICIONES_EXCEDIDO" in str(excinfo.value)"""
    add_code_block(doc, test_code, "Prueba unitaria en pytest: Validación del límite de 2 posposiciones en tomas de medicamentos")
    
    add_section_heading(doc, "9.3 Pruebas de Integración de API y Validación Transaccional SQL", level=2)
    add_body_p(
        doc,
        "Las pruebas de integración ejecutan una batería completa sobre MySQL 8.0 verificando que tras confirmar una toma de medicamentos:\n"
        "• El stock del medicamento decremente exactamente en -1.\n"
        "• Se inserte exactamente 1 registro en la tabla historial_toma.\n"
        "• Si ocurre un fallo forzado a mitad de la operación, el rollback de la transacción restaure el stock original sin inconsistencias."
    )
    
    add_section_heading(doc, "9.4 Pruebas UI e Instrumentadas en Android Compose", level=2)
    add_body_p(
        doc,
        "Mediante compose-test-junit4, se simulan pulsaciones rápidas consecutivas sobre el botón 'Tomar Ahora' de ReminderCard.kt. "
        "La prueba verifica que el flag de protección interna deshabilita inmediatamente el botón (enabled = false), evitando peticiones "
        "duplicadas al servidor y garantizando cero descuentos involuntarios en el botiquín del paciente."
    )
    
    add_section_heading(doc, "9.5 Matriz de Casos de Prueba Ejecutados con Resultados", level=2)
    
    test_mat_headers = ["ID Prueba", "Componente Evaluado", "Entrada / Condición", "Resultado Esperado", "Estado"]
    test_mat_rows = [
        ["CP-01", "Auth Service", "Registro con email existente", "HTTP 400 Bad Request, mensaje claro", "APROBADA"],
        ["CP-02", "Auth Service", "Login con contraseña inválida", "HTTP 401 Unauthorized, cero leaks", "APROBADA"],
        ["CP-03", "Transacción Dosis", "Confirmar toma de medicamentos con inventario en cero", "Alerta inmediata de stock agotado", "APROBADA"],
        ["CP-04", "Posposiciones", "Tercer intento de posposición", "HTTP 409 Conflict, botón bloqueado", "APROBADA"],
        ["CP-05", "Reversión Dosis", "Deshacer dentro de 10 segundos", "Restauración atómica de stock (+1)", "APROBADA"],
        ["CP-06", "Offline Room", "Confirmar toma de medicamentos en modo offline", "Guardado en caché local y sincronización posterior", "APROBADA"],
        ["CP-07", "AlarmManager", "Disparo en modo Deep Doze", "Despertar exacto y activación de alarma", "APROBADA"],
        ["CP-08", "Reinicio Móvil", "Reinicio con alarmas del día", "BootCompletedReceiver reprograma todo", "APROBADA"]
    ]
    add_truth_table(doc, test_mat_headers, test_mat_rows, "Tabla 9.1: Matriz de Casos de Prueba Críticos Ejecutados en el Sistema", [0.9, 1.4, 1.8, 1.6, 0.8])
    
    # ==========================================================================
    # 10. DESPLIEGUE Y MANTENIMIENTO
    # ==========================================================================
    add_section_heading(doc, "10. DESPLIEGUE Y MANTENIMIENTO", level=1, page_break_before=True)
    
    add_section_heading(doc, "10.1 Topología de Despliegue con Docker Compose", level=2)
    add_body_p(
        doc,
        "La topología de producción y pruebas se orquesta mediante Docker Compose, aislando servicios en una red privada virtual (medreminder-net):\n"
        "• Servicio fastapi-backend: Contenedor Python 3.11 con Uvicorn escuchando en puerto 8000.\n"
        "• Servicio mysql-db: Contenedor oficial MySQL 8.0 con volumen persistente mysql_data y puerto expuesto 3306.\n"
        "• Servicio mongo-db: Contenedor oficial MongoDB 6.0 con volumen persistente mongo_data y puerto 27017."
    )
    
    compose_yaml = """# docker-compose.yml - Topología de microservicios de MedReminder AI
version: '3.8'

services:
  mysql-db:
    image: mysql:8.0
    container_name: medreminder_mysql
    restart: always
    environment:
      MYSQL_ROOT_PASSWORD: root_secure_password_2026
      MYSQL_DATABASE: medreminder_db
      MYSQL_USER: meduser
      MYSQL_PASSWORD: medpassword_sec2026
    ports:
      - "3306:3306"
    volumes:
      - mysql_data:/var/lib/mysql
      - ./db/init_mysql.sql:/docker-entrypoint-initdb.d/init_mysql.sql
    networks:
      - medreminder-net

  mongo-db:
    image: mongo:6.0
    container_name: medreminder_mongo
    restart: always
    ports:
      - "27017:27017"
    volumes:
      - mongo_data:/data/db
    networks:
      - medreminder-net

  fastapi-backend:
    build:
      context: ./backend
      dockerfile: Dockerfile
    container_name: medreminder_backend
    restart: always
    ports:
      - "8000:8000"
    env_file:
      - ./backend/.env
    depends_on:
      - mysql-db
      - mongo-db
    networks:
      - medreminder-net

networks:
  medreminder-net:
    driver: bridge

volumes:
  mysql_data:
  mongo_data:"""
    add_code_block(doc, compose_yaml, "Archivo de orquestación docker-compose.yml")
    
    add_section_heading(doc, "10.2 Procedimientos de Respaldo y Restauración de Datos", level=2)
    add_body_p(
        doc,
        "Para salvaguardar la información médico-legal de los pacientes, el mantenedor debe programar respaldos periódicos "
        "ejecutando los siguientes procedimientos oficiales en terminal:"
    )
    add_code_block(
        doc,
        "# 1. Respaldo en caliente de base de datos MySQL (InnoDB):\n"
        "docker exec -t medreminder_mysql mysqldump -u meduser -pmedpassword_sec2026 --single-transaction medreminder_db > backup_mysql_$(date +%Y%m%d).sql\n\n"
        "# 2. Restauración de base de datos MySQL:\n"
        "docker exec -i medreminder_mysql mysql -u meduser -pmedpassword_sec2026 medreminder_db < backup_mysql_20261021.sql\n\n"
        "# 3. Respaldo de MongoDB (Telemetría y logs de tomas de medicamentos):\n"
        "docker exec -t medreminder_mongo mongodump --db medreminder_telemetry --out /data/db/backup_$(date +%Y%m%d)\n\n"
        "# 4. Restauración de telemetría MongoDB:\n"
        "docker exec -i medreminder_mongo mongorestore --db medreminder_telemetry /data/db/backup_20261021/medreminder_telemetry",
        caption="Comandos CLI de Respaldo y Restauración de Datos para MySQL y MongoDB"
    )
    
    add_section_heading(doc, "10.3 Política de Rotación y Monitoreo de Logs", level=2)
    add_body_p(
        doc,
        "Los contenedores configuran el controlador json-file de Docker con parámetros de rotación estricta:\n"
        "• max-size: '50m' (50 megabytes por archivo de log).\n"
        "• max-file: '5' (rotación cíclica reteniendo máximo 5 archivos).\n"
        "Esto garantiza que un contenedor de telemetría intensiva nunca sature el disco duro del servidor."
    )
    
    add_section_heading(doc, "10.4 Protocolos de Mantenimiento Preventivo y Correctivo", level=2)
    add_body_p(
        doc,
        "• Mantenimiento Preventivo Mensual: Ejecución de OPTIMIZE TABLE sobre recordatorios e historial_toma en MySQL, verificación "
        "de integridad de índices B-Tree, y revisión de espacio en disco.\n\n"
        "• Mantenimiento Correctivo de Emergencia: En caso de desincronización masiva de clientes móviles por cambio imprevisto de router Wi-Fi, "
        "el mantenedor actualiza la IP del backend en NetworkModule.kt y recompila el APK, o habilita el DNS dinámico en la red local de la clínica."
    )
    
    # ==========================================================================
    # 11. SEGURIDAD
    # ==========================================================================
    add_section_heading(doc, "11. SEGURIDAD", level=1, page_break_before=True)
    
    add_section_heading(doc, "11.1 Cifrado y Hashing Criptográfico (Argon2id y bcrypt)", level=2)
    add_body_p(
        doc,
        "Las contraseñas nunca se almacenan en texto claro. Se utiliza Passlib configurado con bcrypt (factor de coste 12) o Argon2id "
        "(ganador de la Password Hashing Competition). Cada hash incorpora un salt pseudoaleatorio de 128 bits generado mediante "
        "fuentes de entropía del kernel (/dev/urandom), volviendo inviables ataques de diccionario o tablas arcoíris (rainbow tables)."
    )
    
    add_section_heading(doc, "11.2 Autenticación y Autorización basada en Tokens JWT Bearer", level=2)
    add_body_p(
        doc,
        "La autenticación se implementa bajo el estándar RFC 7519 (JSON Web Tokens). Los tokens son firmados simétricamente con HMAC-SHA256 (HS256) "
        "utilizando la SECRET_KEY del servidor. Cada endpoint protegido inspecciona el encabezado 'Authorization: Bearer <token>', "
        "verificando firma, vigencia (exp) y pertenencia del recurso al id_usuario autenticado, impidiendo accesos cruzados entre pacientes."
    )
    
    add_section_heading(doc, "11.3 Gestión de Permisos Críticos en Android 13/14/15", level=2)
    add_body_p(
        doc,
        "MedReminder AI solicita de forma justificada los permisos más estrictos del sistema operativo móvil:\n"
        "• SCHEDULE_EXACT_ALARM (Android 12+): Permiso obligatorio para programar alarmas deterministas con precisión de segundo.\n"
        "• POST_NOTIFICATIONS (Android 13+): Concesión explícita requerida para desplegar notificaciones Heads-Up emergentes en pantalla.\n"
        "• ACTION_REQUEST_IGNORE_BATTERY_OPTIMIZATIONS: Exención del modo Doze para que las alarmas no sean silenciadas durante el reposo profundo.\n"
        "• RECEIVE_BOOT_COMPLETED: Re-sincronización automática de alarmas cuando el paciente enciende su teléfono."
    )
    
    add_section_heading(doc, "11.4 Mitigación de Vulnerabilidades OWASP Top 10", level=2)
    add_body_p(
        doc,
        "• A01:2021 (Broken Access Control): Todas las operaciones sobre fármacos y tomas de medicamentos filtran estrictamente por id_usuario obtenido del token JWT.\n"
        "• A02:2021 (Cryptographic Failures): Comunicación recomendada bajo HTTPS/TLS 1.3 y claves maestras custodiadas en Android KeyStore por hardware.\n"
        "• A03:2021 (Injection): Uso absoluto de SQLAlchemy con parámetros vinculados (prepared statements), imposibilitando inyecciones SQL.\n"
        "• A05:2021 (Security Misconfiguration): Desactivación del modo depuración (DEBUG=False) en entornos de producción y CORS restringido a orígenes autorizados."
    )
    
    # ==========================================================================
    # 12. SOLUCIÓN DE PROBLEMAS
    # ==========================================================================
    add_section_heading(doc, "12. SOLUCIÓN DE PROBLEMAS", level=1, page_break_before=True)
    
    add_section_heading(doc, "12.1 Matriz Técnica de Troubleshooting para Mantenedores", level=2)
    add_body_p(
        doc,
        "La siguiente matriz ofrece una guía diagnóstica rápida para incidencias operativas comunes:"
    )
    
    trouble_headers = ["Código de Falla", "Síntoma Observado", "Causa Raíz Probable", "Procedimiento de Corrección"]
    trouble_rows = [
        ["ERR-NET-01", "La app muestra 'Error de conexión con el servidor'.", "IP del backend cambió en la red Wi-Fi local o backend caído.", "Ejecutar docker ps; verificar IP de la máquina host con ipconfig/ifconfig y actualizar NetworkModule.kt."],
        ["ERR-ALM-01", "La alarma médica no suena con la pantalla apagada.", "El fabricante del teléfono cerró la app en segundo plano (Doze mode agresivo).", "Ir a Ajustes > Aplicaciones > MedReminder AI > Batería > Seleccionar 'Sin restricciones'."],
        ["ERR-DB-01", "FastAPI arroja OperationalError (2003, Can't connect).", "Contenedor de MySQL no ha completado el inicio o puerto 3306 bloqueado.", "Revisar docker logs medreminder_mysql; aguardar a que muestre 'ready for connections'."],
        ["ERR-AUTH-01", "Petición retorna HTTP 401 Unauthorized recurrente.", "Token JWT expirado o SECRET_KEY modificada en .env tras reiniciar.", "Forzar cierre de sesión en la app y re-autenticar al paciente para emitir nuevo token."],
        ["ERR-CONC-01", "HTTP 409 Conflict al posponer una toma de medicamentos.", "El usuario intentó posponer por 3ª vez consecutiva superando k=2.", "Comportamiento normal por diseño clínico; indicar al usuario que debe tomar u omitir la dosis."]
    ]
    add_truth_table(doc, trouble_headers, trouble_rows, "Tabla 12.1: Matriz de Diagnóstico y Resolución Técnica para Mantenedores", [1.0, 1.8, 1.8, 1.9])
    
    add_section_heading(doc, "12.2 Diagnóstico de Logs en Backend FastAPI y Uvicorn", level=2)
    add_body_p(
        doc,
        "Para auditar excepciones en tiempo real en el servidor backend:"
    )
    add_code_block(
        doc,
        "docker logs -f --tail 100 medreminder_backend",
        caption="Inspección de Logs en Vivo del Contenedor Backend con Docker"
    )
    add_body_p(
        doc,
        "Los errores 422 de Pydantic detallan el campo JSON exacto que falló la validación (ejemplo: 'frecuencia_horas: value is not a valid integer')."
    )
    
    add_section_heading(doc, "12.3 Diagnóstico en Cliente Android mediante Logcat y ADB", level=2)
    add_body_p(
        doc,
        "Para depurar eventos de hardware y alarmas en el dispositivo móvil conectado por USB o Wi-Fi:"
    )
    add_code_block(
        doc,
        "adb logcat -s MedReminderAlarm NetworkModule HoyViewModel",
        caption="Diagnóstico de Alarmas y Red en Cliente Android con ADB Logcat"
    )
    add_body_p(
        doc,
        "El tag MedReminderAlarm imprime el epoch exacto de programación y disparo de cada recordatorio de tomas de medicamentos."
    )
    
    add_section_heading(doc, "12.4 Resolución de Excepciones de Concurrencia y Red", level=2)
    add_body_p(
        doc,
        "Si dos transacciones intentan descontar stock simultáneamente sobre el mismo medicamento, SQLAlchemy gestiona el bloqueo "
        "a nivel de fila con SELECT FOR UPDATE o nivel de aislamiento REPEATABLE READ en MySQL InnoDB, abortando la segunda transacción "
        "con reintento automático para garantizar cero inconsistencias en inventario."
    )
    
    # ==========================================================================
    # 13. LIMITACIONES Y TRABAJO FUTURO
    # ==========================================================================
    add_section_heading(doc, "13. LIMITACIONES Y TRABAJO FUTURO", level=1, page_break_before=True)
    
    add_section_heading(doc, "13.1 Limitaciones Técnicas Identificadas", level=2)
    add_body_p(
        doc,
        "1. Restricciones de Fabricantes OEM en Android: Fabricantes como Xiaomi (MIUI/HyperOS), Huawei (EMUI) y Samsung implementan "
        "administradores de energía que en ocasiones ignoran los estándares de Google, requiriendo configuración manual de 'Inicio automático' por parte del usuario.\n\n"
        "2. Soporte Monousuario por Dispositivo: La versión actual asume un solo paciente activo por terminal Android, requiriendo cerrar "
        "sesión si un cuidador atiende a múltiples enfermos en el mismo teléfono.\n\n"
        "3. Síntesis de Voz Dependiente del Motor del Teléfono: Si el dispositivo no cuenta con el motor de voz de Google (Google TTS) instalado, "
        "la lectura en voz alta de las tomas de medicamentos con Medi puede perder naturalidad acústica."
    )
    
    add_section_heading(doc, "13.2 Hoja de Ruta Evolutiva de Ingeniería", level=2)
    add_body_p(
        doc,
        "• Fase 2 (Q1 2027): Reconocimiento Óptico y NLP Local: Integrar un modelo de visión artificial (OCR) en el cliente móvil para digitalizar "
        "recetas médicas y extraer automáticamente nombres de fármacos, dosis y frecuencias horarias.\n\n"
        "• Fase 3 (Q2 2027): Integración con Pastilleros Inteligentes IoT: Sincronización mediante Bluetooth Low Energy (BLE) con dispensadores "
        "físicos de comprimidos con sensores de apertura para confirmación automática de tomas de medicamentos.\n\n"
        "• Fase 4 (Q3 2027): Despliegue en Kubernetes (K8s): Orquestación de clúster con autoescalado elástico y redundancia multizona para redes hospitalarias."
    )
    
    # ==========================================================================
    # REFERENCIAS BIBLIOGRÁFICAS
    # ==========================================================================
    add_section_heading(doc, "REFERENCIAS BIBLIOGRÁFICAS", level=1, page_break_before=True)
    add_body_p(
        doc,
        "[1] Russell, S. & Norvig, P. (2020). Artificial Intelligence: A Modern Approach (4th Edition). Pearson Education. (Fundamentos de agentes PEAS, lógica de proposiciones y búsqueda en grafos).\n\n"
        "[2] Fowler, M. (2018). Refactoring: Improving the Design of Existing Code (2nd Edition). Addison-Wesley Professional. (Patrones de diseño desacoplados y Clean Architecture).\n\n"
        "[3] Tiangolo, S. (2024). FastAPI Documentation and Architecture Guide. Inyección de dependencias, tipado con Pydantic v2 y rendimiento ASGI.\n\n"
        "[4] Android Open Source Project (AOSP). (2024). Optimize for Doze and App Standby. Google Developers Guide on AlarmManager and Power Management.\n\n"
        "[5] World Health Organization (WHO). (2003). Adherence to Long-Term Therapies: Evidence for Action. Geneva: World Health Organization. (Estadísticas clínicas globales de adherencia a medicamentos).\n\n"
        "[6] Rescorla, E. (2018). The Transport Layer Security (TLS) Protocol Version 1.3. RFC 8446, Internet Engineering Task Force (IETF).\n\n"
        "[7] Jones, M., Bradley, J. & Sakimura, N. (2015). JSON Web Token (JWT). RFC 7519, Internet Engineering Task Force (IETF)."
    )
    
    # ==========================================================================
    # ANEXO A: MARCO FORMAL PEAS
    # ==========================================================================
    add_section_heading(doc, "ANEXO A: FORMALIZACIÓN COMPLEMENTARIA DEL AGENTE PEAS Y ACCIÓN RACIONAL", level=1, page_break_before=True)
    
    add_section_heading(doc, "A.1 Síntesis y Correspondencia del Agente PEAS", level=2)
    add_body_p(
        doc,
        "Conforme a lo especificado prominentemente en la Sección 2.1 y 2.2 del presente manual, el agente inteligente MedReminder AI "
        "se rige bajo el marco PEAS (Russell & Norvig, 2020). En este anexo complementario se profundiza en la formulación matemática "
        "de la función de decisión racional f: P* → A, que mapea la historia de percepciones sensoriales a acciones concretas en el dispositivo móvil:"
    )
    
    peas_action_headers = ["Sensor / Percepción", "Estado del Paciente", "Regla de Inferencia Lógica", "Actuador Involucrado", "Acción Racional y Meta de Rendimiento"]
    peas_action_rows = [
        ["Reloj RTC (Hora exacta)", "Pendiente (hora_actual == hora_alarma)", "Regla Temporal Determinista", "AlarmManager + Notificación Heads-Up", "Despertar el procesador mediante setExactAndAllowWhileIdle y reproducir tono médico sonoro."],
        ["Pantalla Táctil («Tomar Ahora»)", "Notificado (dosis disponible)", "Exclusión Mutua: Tomado ∧ ¬Pospuesto ∧ ¬Omitido", "Servicio REST + MySQL InnoDB", "Confirmar toma de medicamentos, registrar timestamp UTC en historial_toma y descontar -1 de stock."],
        ["Pantalla Táctil («Posponer»)", "Notificado (paciente ocupado)", "Límite Determinista: contador_posposiciones < 2", "AlarmManager (+10/+30 min)", "Aplazar alarma determinista y aumentar contador. Si contador == 2, inhabilitar botón de posponer."],
        ["Pantalla Táctil («Omitir»)", "Notificado (paciente suspende dosis)", "Captura Obligatoria de Justificación Clínica", "Servicio REST + Bitácora Inmutable", "Registrar omisión formal de tomas de medicamentos en base de datos sin alterar stock del botiquín."],
        ["Receptor BOOT_COMPLETED", "Dispositivo recién encendido tras reinicio", "Regla de Reanudación Determinista de Alarmas", "AlarmManager Android", "Consultar base SQLite (Room) y re-programar el 100% de alarmas de tomas de medicamentos pendientes."],
        ["Sonda de Inventario", "Stock actual <= límite de advertencia", "Regla de Stock Crítico: Alerta_Stock = A ∧ B", "Snackbar Cromático + Asistente Medi", "Emitir advertencia visual amarilla/roja y sugerir compra preventiva de medicamentos en farmacia."]
    ]
    add_truth_table(doc, peas_action_headers, peas_action_rows, "Tabla A.1: Matriz Formal de Acción Racional del Agente PEAS ante Percepciones Sensoriales", [1.3, 1.4, 1.4, 1.3, 2.1])
    
    add_section_heading(doc, "A.2 Formalización de la Función de Utilidad y Rendimiento Cuantitativo", level=2)
    add_body_p(
        doc,
        "En la teoría de agentes racionales, la función de utilidad formaliza cuantitativamente el grado de satisfacción del agente respecto a su entorno. "
        "Para MedReminder AI, la función de utilidad global U(e) se define como:\n\n"
        "U(e) = w1 · Tasa_Adherencia - w2 · Penalización_Retraso - w3 · Riesgo_Desabastecimiento\n\n"
        "Donde:\n"
        "• Tasa_Adherencia: Porcentaje de tomas de medicamentos cumplidas dentro de la ventana de tolerancia (meta >= 0.95, w1 = 1.0).\n"
        "• Penalización_Retraso: Minutos transcurridos entre la hora programada y la confirmación nominal de las tomas de medicamentos (w2 = 0.05).\n"
        "• Riesgo_Desabastecimiento: Penalización proporcional a dosis prescritas con inventario en cero (w3 = 0.50).\n\n"
        "Esta formalización matemática demuestra que el agente actúa racionalmente, pues maximiza el valor esperado de la utilidad E[U(e)] "
        "bajo el entorno clínico parcialmente observable y estocástico caracterizado en la Sección 2.2."
    )
    
    # ==========================================================================
    # ANEXO B: MOTOR FORMAL DE LÓGICA PROPOSICIONAL Y DEMOSTRACIONES POR RESOLUCIÓN
    # ==========================================================================
    add_section_heading(doc, "ANEXO B: MOTOR FORMAL DE LÓGICA PROPOSICIONAL Y DEMOSTRACIONES POR RESOLUCIÓN", level=1, page_break_before=True)
    
    add_section_heading(doc, "B.1 Síntesis y Correspondencia del Motor Lógico con la Sección 2.2", level=2)
    add_body_p(
        doc,
        "Las reglas operativas del motor lógico formalizado prominentemente en la Sección 2.2 constituyen la base axiomática del agente inteligente. "
        "En este anexo complementario se profundiza en las demostraciones algebraicas formales, la transformación a Forma Normal "
        "Conjuntiva (FNC/CNF), la aplicación del algoritmo de resolución de Robinson y la verificación rigurosa de consistencia semántica "
        "sin contradicciones, garantizando que el sistema jamás infiera decisiones clínicas inválidas."
    )
    
    add_section_heading(doc, "B.2 Álgebra Booleana y Teoremas de De Morgan aplicados al Dominio Clínico", level=2)
    add_body_p(
        doc,
        "Para la validación de entrada de medicamentos (Regla 1), la fórmula V_alta = p ∧ q ∧ r ∧ s se analiza mediante las leyes "
        "de De Morgan generalizadas para n variables. La condición de falla o rechazo de una prescripción médica responde formalmente a:\n\n"
        "¬V_alta ≡ ¬(p ∧ q ∧ r ∧ s) ≡ (¬p ∨ ¬q ∨ ¬r ∨ ¬s)\n\n"
        "A continuación se presenta la tabla de verdad de equivalencia semántica evaluada estrictamente con 'V' y 'F':"
    )
    b1_headers = ["V_alta (Conjunción)", "¬V_alta (Negación)", "Disyunción De Morgan", "Equivalencia Semántica", "Diagnóstico de Ingeniería"]
    b1_rows = [
        ["V", "F", "F", "V", "Aceptación unánime: las 4 precondiciones clínicas se cumplen"],
        ["F", "V", "V", "V", "Rechazo determinista: al menos una precondición es Falsa (F)"]
    ]
    add_truth_table(doc, b1_headers, b1_rows, "Tabla B.1: Tabla de Verdad de Demostración Deductiva por Leyes de De Morgan", [1.4, 1.4, 1.5, 1.3, 2.0])
    
    add_section_heading(doc, "B.3 Demostración Formal por Resolución de Robinson y Forma Normal Conjuntiva (FNC)", level=2)
    add_body_p(
        doc,
        "Para validar la regla de bloqueo por interacciones farmacológicas o alergias (Regla 5: Bloqueo_Seguridad = X ∨ Y), el agente "
        "convierte el conocimiento a cláusulas en Forma Normal Conjuntiva (FNC). Si se formula la meta de demostrar que un paciente "
        "con alergia confirmada (X = V) debe ser bloqueado, se agrega la negación de la meta ¬Bloqueo_Seguridad a la base de conocimiento "
        "y se efectúa refutación por resolución de Robinson (1965):\n\n"
        "1. Cláusula C1: (¬X ∨ Bloqueo_Seguridad)\n"
        "2. Cláusula C2: (¬Y ∨ Bloqueo_Seguridad)\n"
        "3. Hecho F1: X (Alergia confirmada = V)\n"
        "4. Negación de la Meta: ¬Bloqueo_Seguridad\n"
        "5. Resolución entre C1 y F1: Bloqueo_Seguridad\n"
        "6. Resolución entre (5) y (4): Cláusula Vacía ⊥ (Contradicción demostrada, meta probada)."
    )
    b2_headers = ["Paso de Resolución", "Cláusula 1", "Cláusula 2", "Resolvente / Cláusula Resultante", "Validez Deductiva", "Estado Clínico"]
    b2_rows = [
        ["Paso 1", "¬X ∨ Bloqueo", "X (Alergia = V)", "Bloqueo_Seguridad", "V", "Inferencia de bloqueo requerida"],
        ["Paso 2", "Bloqueo_Seguridad", "¬Bloqueo_Seguridad", "⊥ (Cláusula Vacía)", "V", "Refutación exitosa: teorema clínico demostrado"]
    ]
    add_truth_table(doc, b2_headers, b2_rows, "Tabla B.2: Tabla de Verdad y Pasos de Resolución de Robinson en Forma Normal Conjuntiva (FNC)", [1.0, 1.3, 1.3, 1.5, 1.0, 1.5])
    
    add_section_heading(doc, "B.4 Verificación de Consistencia, No-Contradicción y Soundness del Sistema", level=2)
    add_body_p(
        doc,
        "Un sistema asistivo médico debe ser sintáctica y semánticamente correcto (Sound) y consistente (carente de contradicciones tipo α ∧ ¬α). "
        "Para la regla de exclusión mutua de estados en el ciclo de vida de las tomas de medicamentos (Regla 3), la siguiente tabla de verdad formal "
        "demuestra que no existe asignación donde el sistema permita dos transiciones incompatibles simultáneas:"
    )
    b3_headers = ["Tomado", "Pospuesto", "Omitido", "t ∧ p", "t ∧ o", "p ∧ o", "Consistencia (¬Conflicto)", "Estado del Agente"]
    b3_rows = [
        ["V", "F", "F", "F", "F", "F", "V", "Consistente: registro nominal de tomas de medicamentos"],
        ["F", "V", "F", "F", "F", "F", "V", "Consistente: reprogramación transitoria aprobada"],
        ["F", "F", "V", "F", "F", "F", "V", "Consistente: omisión justificada documentada"],
        ["V", "V", "F", "V", "F", "F", "F", "Inconsistente: conflicto bloqueado por el agente"],
        ["V", "F", "V", "F", "V", "F", "F", "Inconsistente: conflicto bloqueado por el agente"],
        ["F", "V", "V", "F", "F", "V", "F", "Inconsistente: conflicto bloqueado por el agente"]
    ]
    add_truth_table(doc, b3_headers, b3_rows, "Tabla B.3: Matriz de Consistencia y No-Contradicción en Estados de Tomas de Medicamentos", [0.8, 0.8, 0.8, 0.8, 0.8, 0.8, 1.3, 1.5])
    
    add_section_heading(doc, "B.5 Pruebas Unitarias Automatizadas del Motor Lógico con Pytest y Aserciones Formales", level=2)
    add_body_p(
        doc,
        "La corrección matemática del motor se verifica de manera continua en la suite de pruebas unitarias backend/tests/test_logic_engine.py. "
        "Cada caso de prueba ejecuta una aserción booleana que refleja directamente una fila de las tablas de verdad formalizadas en la Sección 2.2:"
    )
    test_logic_code = """# backend/tests/test_logic_engine.py - Suite de verificación de tablas de verdad
import pytest
from app.core.logic_engine import (
    validar_alta_farmaco,
    verificar_inventario_critico,
    validar_exclusion_mutua_tomas_de_medicamentos,
    permitir_posponer_tomas_de_medicamentos,
    evaluar_bloqueo_seguridad_alergias,
    evaluar_modo_castigo
)

def test_tabla_2_2_crud_farmacos():
    assert validar_alta_farmaco("Paracetamol", 500.0, 8, 20) is True
    assert validar_alta_farmaco("Paracetamol", 500.0, 8, -1) is False  # stock negativo
    assert validar_alta_farmaco("Paracetamol", 0.0, 8, 20) is False    # dosis nula
    assert validar_alta_farmaco("", 500.0, 8, 20) is False             # nombre vacío

def test_tabla_2_3_inventario_critico():
    assert verificar_inventario_critico(stock_actual=3, stock_minimo=5, tratamiento_activo=True) is True
    assert verificar_inventario_critico(stock_actual=10, stock_minimo=5, tratamiento_activo=True) is False

def test_tabla_2_4_exclusion_mutua_tomas_de_medicamentos():
    assert validar_exclusion_mutua_tomas_de_medicamentos(tomado=True, pospuesto=False, omitido=False) is True
    assert validar_exclusion_mutua_tomas_de_medicamentos(tomado=True, pospuesto=True, omitido=False) is False

def test_tabla_2_5_limite_posposiciones_k2():
    assert permitir_posponer_tomas_de_medicamentos(solicita_posponer=True, contador_posposiciones=1) is True
    assert permitir_posponer_tomas_de_medicamentos(solicita_posponer=True, contador_posposiciones=2) is False

def test_tabla_2_6_alergias_contraindicaciones():
    assert evaluar_bloqueo_seguridad_alergias(alergia_detectada=True, interaccion_grave=False) is True
    assert evaluar_bloqueo_seguridad_alergias(alergia_detectada=False, interaccion_grave=False) is False

def test_tabla_2_7_modo_castigo():
    assert evaluar_modo_castigo(omisiones_acumuladas=2, escudos_disponibles=0) is True
    assert evaluar_modo_castigo(omisiones_acumuladas=2, escudos_disponibles=1) is False"""
    add_code_block(doc, test_logic_code, "Pruebas Unitarias Automatizadas con Pytest (test_logic_engine.py)")
    
    # ==========================================================================
    # ANEXO C: MODELADO DE IA Y GRAFOS DE BÚSQUEDA
    # ==========================================================================
    add_section_heading(doc, "ANEXO C: MODELADO DE INTELIGENCIA ARTIFICIAL Y GRAFOS DE BÚSQUEDA", level=1, page_break_before=True)
    
    add_section_heading(doc, "C.1 El Ciclo de Vida de Tomas de Medicamentos como Espacio de Estados", level=2)
    add_body_p(
        doc,
        "En MedReminder AI, el ciclo de vida de un recordatorio de tomas de medicamentos se modela formalmente como un problema "
        "de búsqueda en un espacio de estados P = (S, A, s0, G, c):\n\n"
        "• Conjunto de Estados (S): {Pendiente, Notificado, EnApp, Pospuesto, Tomado, Omitido}.\n"
        "• Conjunto de Acciones (A): {disparar_alarma, abrir_app, confirmar_toma, posponer, confirmar_omision}.\n"
        "• Estado Inicial (s0): s0 = Pendiente.\n"
        "• Conjunto de Metas (G): Meta primaria G_prim = {Tomado} (adherencia terapéutica óptima); sub-meta secundaria G_sec = {Omitido} (justificación clínica válida).\n"
        "• Función de Costo c(s, a, s'): Modela minutos de fricción o retraso acumulado (c(Pendiente → Notificado) = 5 min, "
        "c(Notificado → Pospuesto) = 30 min, c(Notificado → Tomado) = 2 min)."
    )
    
    add_section_heading(doc, "C.2 Búsqueda en Profundidad (DFS) y Evasión Determinista de Ciclos", level=2)
    add_body_p(
        doc,
        "La Búsqueda en Profundidad (DFS) recorre exhaustivamente las ramas mediante una pila LIFO. Sin embargo, transiciones cíclicas "
        "como Notificado ⇄ Pospuesto o aristas dirigidas de retorno en grafos generales provocan bucles infinitos.\n\n"
        "El motor de MedReminder AI (busquedas/busqueda_medreminder.py y AnalisisDfsScreen.kt) implementa dos mecanismos anticiclos formales:\n\n"
        "1. Detección por Conjunto de Camino Activo (in_path): Se mantiene la pila del camino actual S_camino. Antes de expandir (u, v), "
        "si v in S_camino, se detecta una 'arista de retroceso' (back-edge) y la rama se poda de inmediato.\n\n"
        "2. Límite de Profundidad Determinista (k = 2): La regla médica prohíbe más de dos posposiciones continuas de tomas de medicamentos. "
        "Cualquier rama que intente un tercer aplazamiento es podada por profundidad, forzando la resolución hacia Tomado u Omitido."
    )
    
    if os.path.exists("docs/screenshots/05_analisis_dfs.png"):
        add_figure_image(doc, "docs/screenshots/05_analisis_dfs.png", "Figura C.1: Módulo de IA en Android mostrando exploración DFS, poda por profundidad y evasión de ciclos", 3.0)
        
    if os.path.exists("busquedas/dfs_medreminder.png"):
        add_figure_image(doc, "busquedas/dfs_medreminder.png", "Figura C.2: Grafo de estados de tomas de medicamentos con detección y poda de ciclos", 5.0)
        
    add_section_heading(doc, "C.3 Búsqueda en Anchura (BFS) y Ruta Óptima hacia la Adherencia", level=2)
    add_body_p(
        doc,
        "La Búsqueda en Anchura (BFS) utiliza una cola FIFO y explora el grafo nivel por nivel. En el espacio de estados de tomas de medicamentos, "
        "BFS garantiza encontrar la ruta con menor número de transiciones entre s0 = Pendiente y la meta G = Tomado: "
        "Ruta BFS óptima: Pendiente → EnApp → Tomado (solo 2 pasos, sin necesidad de esperar la alarma sonora)."
    )
    
    add_section_heading(doc, "C.4 Búsqueda de Costo Uniforme (UCS), Heurística Voraz (GBFS) y Algoritmo A*", level=2)
    add_body_p(
        doc,
        "• Búsqueda de Costo Uniforme (UCS): Emplea una cola de prioridad ordenada estrictamente por costo acumulado g(n) desde el nodo inicial "
        "(f(n) = g(n)). Prioriza transiciones de menor fricción o retraso acumulado, garantizando optimalidad de costo cuando todos los costos "
        "de las aristas son estrictamente positivos.\n\n"
        "• Heurística Voraz (Greedy Best-First Search - GBFS): Emplea una función de evaluación orientada exclusivamente hacia el futuro "
        "mediante f(n) = h(n), guiándose por la proximidad estimada hacia la meta. Aunque expande rápidamente nodos en grafos directos, "
        "es miope (subóptima) y puede ser incompleta si existen ciclos no podados.\n\n"
        "• Algoritmo Heurístico A*: Combina de forma balanceada la información histórica y proyectada mediante la función de evaluación "
        "f(n) = g(n) + h(n), donde g(n) es el costo real acumulado y h(n) es una estimación heurística admisible y consistente hacia la meta. "
        "A* garantiza optimalidad y completitud con el mínimo número de expansiones hacia la confirmación de tomas de medicamentos."
    )
    
    add_section_heading(doc, "C.5 Demostración Formal de Admisibilidad y Consistencia de h(n)", level=2)
    add_body_p(
        doc,
        "Para garantizar que A* encuentre la solución de costo óptimo sin reabrir nodos cerrados, la heurística h(n) debe ser:\n\n"
        "1. Admisible: h(n) <= h*(n) para todo nodo n, donde h*(n) es el costo real mínimo hacia la meta. Dado que la confirmación física "
        "inmediata requiere al menos 1 minuto (ingerir pastilla con agua), cualquier valor h(n) <= 1 minuto jamás sobrestima el costo real.\n\n"
        "2. Consistente (Monótona): Para todo sucesor n' generado por la acción a: h(n) <= c(n, a, n') + h(n'). Al cumplirse la desigualdad "
        "triangular, la secuencia f(n) es monótonamente no decreciente, demostrando matemáticamente la optimalidad de A*."
    )
    
    add_section_heading(doc, "C.6 Matriz Comparativa Asintótica y Benchmark Cuantitativo de p30algoritmosbusquedacompara.py", level=2)
    add_body_p(
        doc,
        "A continuación se presenta la matriz comparativa teórica asintótica y los resultados cuantitativos reales obtenidos del script "
        "oficial p30algoritmosbusquedacompara.py evaluado sobre los espacios de búsqueda del proyecto:"
    )
    
    alg_headers = ["Algoritmo", "Estructura de Datos", "Complejidad Tiempo", "Complejidad Espacio", "Completo", "Óptimo", "Nodos Expandidos"]
    alg_rows = [
        ["DFS (Sin poda)", "Pila LIFO", "O(b^m)", "O(b·m)", "No (en ciclos)", "No", "Infinito (bucle cíclico)"],
        ["DFS (Con anticiclos y k=2)", "Pila + in_path", "O(b^d)", "O(b·d)", "Sí (si d acotado)", "No", "3 nodos (MedReminder) / 9 nodos (Clase)"],
        ["BFS (Anchura)", "Cola FIFO", "O(b^d)", "O(b^d)", "Sí", "Sí (pasos unif.)", "5 nodos (MedReminder) / 10 nodos (Clase)"],
        ["UCS (Costo Uniforme)", "Cola Prioridad g(n)", "O(b^(1 + ⌊C*/ε⌋))", "O(b^(1 + ⌊C*/ε⌋))", "Sí", "Sí (costo general)", "3 nodos (MedReminder) / 9 nodos (Clase)"],
        ["Heurística Voraz (GBFS)", "Cola Prioridad h(n)", "O(b^m)", "O(b·m)", "No (sin control)", "No (miope)", "3 nodos (MedReminder) / 4 nodos (Clase)"],
        ["A* Heurístico", "PriorityQueue f=g+h", "O(b^d)", "O(b^d)", "Sí", "Sí (con h admisible)", "3 nodos (MedReminder) / 7 nodos (Clase)"]
    ]
    add_truth_table(doc, alg_headers, alg_rows, "Tabla C.1: Comparativa Teórica Asintótica y Benchmark Cuantitativo Real de Algoritmos de Búsqueda", [1.3, 1.1, 1.0, 1.0, 0.7, 0.7, 1.2])
    
    add_body_p(
        doc,
        "Resultados Cuantitativos Obtenidos de la Ejecución Real del Script de Benchmark (p30algoritmosbusquedacompara.py):\n\n"
        "1. Evaluación sobre el Grafo de Estados Clínicos de MedReminder AI (Inicio: 'Pendiente' → Meta: 'Tomado'):\n"
        "• BFS (Anchura): 5 nodos expandidos, costo real = 1 minuto de fricción, ruta seleccionada: Pendiente → EnApp → Tomado (2 pasos). Óptimo en número de pasos.\n"
        "• DFS (Profundidad con anticiclos): 3 nodos expandidos, costo real = 1, 2 pasos. Explora la primera rama válida disponible.\n"
        "• UCS (Costo Uniforme): 3 nodos expandidos, costo real = 1, 2 pasos. Óptimo en costo acumulado.\n"
        "• Heurística Voraz (GBFS): 3 nodos expandidos, costo real = 1, 2 pasos. Selección directa guiada por menor h(n).\n"
        "• A* Heurístico (f = g + h): 3 nodos expandidos, costo real = 1, 2 pasos. Solución óptima confirmada con mínimo esfuerzo de exploración.\n\n"
        "2. Evaluación sobre el Grafo Académico de Clase (Inicio: 'A' → Meta: 'J'):\n"
        "• BFS (Anchura): 10 nodos expandidos, ruta: A → C → F → J, costo real = 10, 3 pasos.\n"
        "• DFS (Profundidad): 9 nodos expandidos, ruta: A → C → F → J, costo real = 10, 3 pasos.\n"
        "• UCS (Costo Uniforme): 9 nodos expandidos, ruta: A → C → F → J, costo real = 10, 3 pasos.\n"
        "• Heurística Voraz (GBFS): 4 nodos expandidos (A → C → F → J), costo real = 10, 3 pasos. Menor número absoluto de expansiones informadas gracias a la atracción de h(F)=3 y h(J)=0.\n"
        "• A* Heurístico (f = g + h): 7 nodos expandidos, ruta: A → C → F → J, costo real = 10, 3 pasos. Óptimo garantizado con exploración balanceada."
    )
    
    add_section_heading(doc, "C.7 Máquina de Estados Finitos (FSM) de Tomas de Medicamentos", level=2)
    add_body_p(
        doc,
        "La FSM formal se define por la 5-tupla M = (Q, Σ, δ, q0, F):\n"
        "• Q = {Pendiente, Notificado, EnApp, Pospuesto, Tomado, Omitido}\n"
        "• Σ = {alarma_sonora, click_app, click_tomar, click_posponer, click_omitir, timeout_max}\n"
        "• q0 = Pendiente\n"
        "• F = {Tomado, Omitido} (Estados terminales absorbentes inmutables)\n"
        "• Función de transición δ: Valida atómicamente cada salto, impidiendo retrocesos una vez alcanzado el estado absorbente Tomado."
    )
    
    # ==========================================================================
    # ANEXO D: DICCIONARIO FORMAL DE VARIABLES
    # ==========================================================================
    add_section_heading(doc, "ANEXO D: DICCIONARIO FORMAL DE VARIABLES DEL SISTEMA CLÍNICO Y GAMIFICACIÓN", level=1, page_break_before=True)
    
    variables_anexo = [
        {"name": "p", "type": "Booleano", "scope": "Lógica / CRUD", "range": "{V, F}", "desc": "Predicado: Nombre del fármaco no vacío (>= 2 caracteres)."},
        {"name": "q", "type": "Booleano", "scope": "Lógica / CRUD", "range": "{V, F}", "desc": "Predicado: Dosis clínica estrictamente mayor a 0."},
        {"name": "r", "type": "Booleano", "scope": "Lógica / CRUD", "range": "{V, F}", "desc": "Predicado: Frecuencia horaria válida en {4, 6, 8, 12, 24} h."},
        {"name": "s", "type": "Booleano", "scope": "Lógica / CRUD", "range": "{V, F}", "desc": "Predicado: Stock de unidades en botiquín >= 0."},
        {"name": "V_alta", "type": "Booleano", "scope": "Lógica / CRUD", "range": "{V, F}", "desc": "Resultado de validación de alta de medicamento (p ∧ q ∧ r ∧ s)."},
        {"name": "A_StockCritico", "type": "Booleano", "scope": "Lógica / Botiquín", "range": "{V, F}", "desc": "Predicado: stock_actual <= stock_minimo_alerta."},
        {"name": "B_TratamientoActivo", "type": "Booleano", "scope": "Lógica / Botiquín", "range": "{V, F}", "desc": "Predicado: tratamiento activo en la fecha corriente."},
        {"name": "t", "type": "Booleano", "scope": "Lógica / FSM", "range": "{V, F}", "desc": "Dosis de toma de medicamentos confirmada como tomada."},
        {"name": "p_pos", "type": "Booleano", "scope": "Lógica / FSM", "range": "{V, F}", "desc": "Alarma de toma de medicamentos pospuesta temporalmente."},
        {"name": "o", "type": "Booleano", "scope": "Lógica / FSM", "range": "{V, F}", "desc": "Dosis de toma de medicamentos registrada como omitida."},
        {"name": "id_recordatorio", "type": "Entero (INT PK)", "scope": "MySQL / recordatorios", "range": "[1, 2^31 - 1]", "desc": "Identificador único de la toma de medicamentos programada."},
        {"name": "fecha_hora_programada", "type": "DATETIME", "scope": "MySQL / recordatorios", "range": "Formato ISO UTC", "desc": "Estampa temporal exacta en que debe dispararse la alarma."},
        {"name": "contador_posposiciones", "type": "Entero", "scope": "MySQL / recordatorios", "range": "[0, 2]", "desc": "Número de posposiciones consumidas en la dosis actual."},
        {"name": "stock_actual", "type": "Entero", "scope": "MySQL / medicamentos", "range": "[0, 9999]", "desc": "Unidades físicas disponibles en el botiquín del paciente."},
        {"name": "racha_dias", "type": "Entero", "scope": "MySQL / gamificacion", "range": "[0, 3650]", "desc": "Días continuos consecutivos con 100% de cumplimiento."},
        {"name": "escudos_activos", "type": "Entero", "scope": "MySQL / gamificacion", "range": "[0, 3]", "desc": "Escudos acumulados que perdonan omisiones accidentales."},
        {"name": "modo_castigo", "type": "Booleano", "scope": "MySQL / gamificacion", "range": "{V, F}", "desc": "Bloqueo disciplinario de posposición tras omisiones continuas."},
        {"name": "SECRET_KEY", "type": "String Hex (256b)", "scope": ".env / Backend", "range": "64 caracteres hex", "desc": "Secreto criptográfico para firma de tokens JWT HS256."}
    ]
    add_variable_dictionary_table(doc, variables_anexo, "Diccionario de Variables del Núcleo Clínico y Persistencia")
    
    # ==========================================================================
    # LISTA DE VERIFICACIÓN ANTES DE ENTREGAR
    # ==========================================================================
    add_section_heading(doc, "LISTA DE VERIFICACIÓN ANTES DE ENTREGAR", level=1, page_break_before=True)
    add_body_p(
        doc,
        "La siguiente lista de verificación debe ser firmada y certificada por el equipo de ingeniería antes de realizar la entrega "
        "definitiva o despliegue en ambientes clínicos de producción:"
    )
    
    checklist_items = [
        {"num": "C-01", "criterio": "Carátula institucional formal con escudos UTVT / Edomex y datos completos de los 5 integrantes.", "estado": "CONFORME", "observaciones": "Verificada en página 1 con código MAN-TEC-MEDREMINDER-2026-V1.3."},
        {"num": "C-02", "criterio": "Tabla formal de Control de Versiones insertada tras la carátula.", "estado": "CONFORME", "observaciones": "Registradas versiones 1.0, 1.1, 1.2 y 1.3 con autores y fechas."},
        {"num": "C-03", "criterio": "Índice automático nativo de Word con campo TOC y directiva updateFields.", "estado": "CONFORME", "observaciones": "Campo TOC insertado sin autorecursión en Heading 1."},
        {"num": "C-04", "criterio": "Estructura formal en 13 secciones exactas requeridas por rúbrica docente.", "estado": "CONFORME", "observaciones": "13 secciones desarrolladas en su totalidad con rigor técnico."},
        {"num": "C-05", "criterio": "Sección 4 acotada estrictamente a paqueterías vinculadas a los Requisitos Funcionales.", "estado": "CONFORME", "observaciones": "Tablas 4.1 y 4.2 mapean requerimientos de Python y Gradle a RF."},
        {"num": "C-06", "criterio": "Tablas de verdad evaluadas estrictamente con 'V' y 'F' (cero '0' y '1').", "estado": "CONFORME", "observaciones": "Todas las tablas de la Sección 2.2 y del Anexo B auditadas con 100% de cumplimiento."},
        {"num": "C-07", "criterio": "Uso estricto del término 'tomas de medicamentos' o 'toma de medicamentos'.", "estado": "CONFORME", "observaciones": "Auditado por script build_all_manuals.py sin usos indebidos."},
        {"num": "C-08", "criterio": "Inclusión de Referencias bibliográficas académicas en formato APA/IEEE.", "estado": "CONFORME", "observaciones": "7 citas canónicas (Russell & Norvig, Fowler, RFCs, WHO)."},
        {"num": "C-09", "criterio": "Anexos A (PEAS), B (Lógica V/F), C (Grafos IA/p30) y D (Diccionario de Variables).", "estado": "CONFORME", "observaciones": "Cuatro anexos completos con formalización matemática y benchmark."},
        {"num": "C-10", "criterio": "Integridad OpenXML: directiva w:cantSplit en tablas y keep_with_next en títulos.", "estado": "CONFORME", "observaciones": "Cero tablas partidas indebidamente entre páginas y sin huérfanos."}
    ]
    add_checklist_table(doc, checklist_items, "LISTA DE VERIFICACIÓN DE ENTREGA DE INGENIERÍA")
    
    # Guardar documento
    out_path = "docs/Manual_Tecnico_MedReminderAI.docx"
    doc.save(out_path)
    print(f"✅ Manual Técnico generado exitosamente en: {out_path}")
    return out_path

if __name__ == "__main__":
    build_manual_tecnico()
