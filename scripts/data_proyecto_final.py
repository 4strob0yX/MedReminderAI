# -*- coding: utf-8 -*-
"""
Contenido detallado y estructurado para el Proyecto Final:
Base de Datos y Arquitectura de Software - MedReminder AI.
Redactado en lenguaje natural fluido, profesional y 100% contextualizado al proyecto.
"""

# ==============================================================================
# SECCIÓN 1.0 - 1.4: CONTEXTO GENERAL, MODELO RELACIONAL Y DICCIONARIO DE DATOS
# ==============================================================================

SEC_1_NOMBRE = "1.0 Nombre del Proyecto"
SEC_1_NOMBRE_DESC = "MedReminder AI: Sistema Inteligente de Gestión, Supervisión Clínica y Recordatorio Farmacológico"

SEC_1_DESC = "1.1 Descripción del Proyecto"
SEC_1_DESC_TEXT = (
    "MedReminder AI es una plataforma tecnológica integral de salud digital diseñada para resolver uno de los problemas "
    "más críticos en la medicina preventiva y ambulatoria: la falta de adherencia al tratamiento farmacológico y el riesgo "
    "de complicaciones por errores de dosificación o polifarmacia.\n\n"
    "La solución combina una aplicación móvil nativa para el sistema operativo Android (construida con lenguaje Kotlin y "
    "el kit declarativo Jetpack Compose bajo el patrón arquitectónico MVVM), un ecosistema de backend en microservicios "
    "construido sobre FastAPI en Python, y un esquema de persistencia políglota híbrido que une la rigidez transaccional "
    "de MySQL 8.4 (para cuentas, prescripciones, posología y catálogo de medicamentos) con la velocidad y flexibilidad "
    "documental de MongoDB 7.0 (para telemetría clínica inmutable, auditoría de tomas y registro de eventos).\n\n"
    "Adicionalmente, el proyecto incorpora inteligencia artificial clínica local mediante Ollama (modelo especializado "
    "«medi-clinico»), permitiendo el escaneo automatizado de recetas médicas vía visión por computadora multimodal y "
    "asistencia conversacional médica contextualizada, garantizando en todo momento la privacidad de los datos de salud "
    "sin exponer información confidencial a servicios de terceros en la nube."
)

SEC_1_PROBLEMA = "1.2 Planteamiento del Problema"
SEC_1_PROBLEMA_TEXT = (
    "En la actualidad, según datos oficiales de la Organización Mundial de la Salud (OMS), más del 50% de los pacientes con "
    "enfermedades crónico-degenerativas (como hipertensión arterial, diabetes mellitus, insuficiencia renal o cardiopatías) "
    "no siguen adecuadamente las instrucciones de sus tratamientos médicos. En países como México, esta situación se agrava "
    "de manera exponencial en la población de adultos mayores (personas de 60 años o más), quienes padecen con frecuencia "
    "el fenómeno clínico conocido como polifarmacia, consistente en el consumo diario de cuatro o más fármacos simultáneos "
    "con horarios, dosis y contraindicaciones cruzadas.\n\n"
    "Las principales deficiencias identificadas en el entorno actual son:\n"
    "1. Olvidos recurrentes y confusión de horarios: La memoria a corto plazo suele deteriorarse en la vejez, lo que provoca "
    "omisiones involuntarias de tomas vitales o, lo que es peor, duplicidades accidentales que desencadenan intoxicaciones graves.\n"
    "2. Brecha digital y diseño inaccesible: La mayoría de las aplicaciones móviles en el mercado presentan interfaces saturadas "
    "de opciones confusas, tipografías minúsculas, contrastes pobres y flujos complejos que alienan y frustran al adulto mayor.\n"
    "3. Falta de integración del cuidador familiar: Las alarmas genéricas de los teléfonos celulares se quedan sonando de manera "
    "aislada; si el paciente no puede responder, ningún familiar o cuidador primario se entera a tiempo de que un fármaco de rescate "
    "o crítico fue ignorado.\n"
    "4. Inexistencia de auditoría y reportes clínicos confiables: Cuando el paciente asiste a su consulta de control, el médico "
    "no cuenta con un registro real y veraz de si se tomó el medicamento a la hora exacta, basándose únicamente en testimonios verbales "
    "imprecisos.\n\n"
    "MedReminder AI nace para erradicar estas problemáticas a través de alarmas nativas deterministas, diseño ergonómico de alta "
    "accesibilidad, supervisión reactiva para cuidadores y persistencia clínica auditada."
)

SEC_1_MODELO_REL = "1.3 Modelo Relacional"
SEC_1_MODELO_REL_TEXT = (
    "Para garantizar la integridad transaccional (propiedades ACID: Atomicidad, Consistencia, Aislamiento y Durabilidad) "
    "en los datos esenciales del sistema, se diseñó un modelo entidad-relación normalizado en Tercera Forma Normal (3NF). "
    "Este esquema asegura que los datos de los usuarios, sus medicamentos prescritos, esquemas de tratamiento y contactos "
    "de soporte no presenten redundancias anómalas ni inconsistencias ante operaciones concurrentes.\n\n"
    "El esquema está compuesto por 8 tablas relacionales interconectadas mediante llaves foráneas con políticas de "
    "integridad referencial estrictas (`ON DELETE CASCADE`), garantizando que la eliminación o modificación de un registro "
    "padre limpie de manera coherente sus entidades dependientes (por ejemplo, si se desactiva o borra un medicamento, se "
    "cancelan coherentemente sus tratamientos y recordatorios asociados)."
)

# Tablas del Modelo Relacional: descripción de entidades y cardinalidades
RELACIONES_TABLA_DATA = [
    ["usuario ── medicamento", "1 : N (Uno a Muchos)", "Un usuario puede tener registrados múltiples medicamentos en su botiquín personal. Cada medicamento pertenece obligatoriamente a un usuario.", "ON DELETE CASCADE"],
    ["usuario ── alergia_usuario", "1 : N (Uno a Muchos)", "Un paciente puede registrar múltiples alergias farmacológicas para prevenir interacciones graves. Cada alergia está ligada al usuario.", "ON DELETE CASCADE"],
    ["usuario ── contacto_apoyo", "1 : N (Uno a Muchos)", "Un usuario puede vincular uno o varios familiares o cuidadores que recibirán alertas. Cada contacto pertenece a un paciente.", "ON DELETE CASCADE"],
    ["medicamento ── tratamiento", "1 : N (Uno a Muchos)", "Un medicamento puede tener distintos esquemas terapéuticos a lo largo del tiempo (dosis, frecuencia y duración).", "ON DELETE CASCADE"],
    ["tratamiento ── recordatorio", "1 : N (Uno a Muchos)", "Un tratamiento genera múltiples recordatorios planificados en fechas y horas específicas en el calendario del paciente.", "ON DELETE CASCADE"],
    ["recordatorio ── historial_toma", "1 : N (Uno a Muchos)", "Un recordatorio puede registrar múltiples eventos de auditoría (por ejemplo, si fue pospuesto dos veces y luego tomado).", "ON DELETE CASCADE"],
    ["usuario ── alerta_cuidador", "1 : N (Uno a Muchos)", "Un usuario genera alertas clínicas de advertencia o peligro dirigidas a su red de apoyo cuando se pospone u omite un fármaco.", "ON DELETE CASCADE"]
]

# 1.4 Diccionario de Datos: tablas detalladas
DICCIONARIOS = {
    "usuario": [
        ["id_usuario", "INT", "Auto-increment", "PK", "No", "Autonumérico", "Identificador único y secuencial asignado a cada paciente o usuario registrado."],
        ["nombre_completo", "VARCHAR", "255", "Ninguna", "No", "N/A", "Nombre y apellidos completos del paciente para personalización de interfaz y reportes."],
        ["correo", "VARCHAR", "255", "Ninguna (UNIQUE)", "No", "N/A", "Correo electrónico único utilizado como identificador de autenticación y acceso."],
        ["password_hash", "VARCHAR", "255", "Ninguna", "No", "N/A", "Huella criptográfica de la contraseña procesada con algoritmo seguro de hashing."],
        ["fecha_nacimiento", "DATE", "YYYY-MM-DD", "Ninguna", "Sí", "NULL", "Fecha de nacimiento del paciente; permite calcular la edad para habilitar modo adulto mayor."],
        ["rol", "VARCHAR", "30", "Ninguna", "No", "'paciente'", "Rol dentro de la plataforma ('paciente', 'cuidador', 'medico', 'administrador')."],
        ["fecha_registro", "TIMESTAMP", "Fecha y Hora", "Ninguna", "No", "CURRENT_TIMESTAMP", "Marca temporal inmutable del momento exacto del alta en el sistema."]
    ],
    "medicamento": [
        ["id_medicamento", "INT", "Auto-increment", "PK", "No", "Autonumérico", "Identificador unívoco del fármaco registrado en el inventario del paciente."],
        ["id_usuario", "INT", "Relación", "FK", "No", "N/A", "Llave foránea que referencia al paciente dueño del fármaco (`usuario.id_usuario`)."],
        ["nombre", "VARCHAR", "255", "Ninguna", "No", "N/A", "Nombre comercial o genérico del medicamento (ej. 'Losartán', 'Metformina')."],
        ["principio_activo", "VARCHAR", "255", "Ninguna", "Sí", "NULL", "Sustancia activa del compuesto químico para validación de alergias y contraindicaciones."],
        ["dosis", "VARCHAR", "100", "Ninguna", "No", "N/A", "Cantidad de sustancia por ingesta (ej. '50 mg', '1 cápsula', '10 ml')."],
        ["cantidad_stock", "INT", "Numérico >= 0", "Ninguna", "No", "0", "Cantidad física actual de pastillas o unidades disponibles en el botiquín del paciente."],
        ["stock_inicial", "INT", "Numérico >= 0", "Ninguna", "No", "30", "Unidades con las que inició la caja o envase; se usa para calcular porcentaje restante."],
        ["forma_farmaceutica", "VARCHAR", "40", "Ninguna", "No", "'comprimidos'", "Presentación del medicamento: comprimidos, jarabe, inyección, gotas, etc."],
        ["color_pastilla", "VARCHAR", "40", "Ninguna", "No", "'blanco'", "Color visual de la gragea o cápsula para facilitar reconocimiento gráfico al adulto mayor."],
        ["instrucciones_toma", "VARCHAR", "255", "Ninguna", "Sí", "NULL", "Instrucciones clínicas adicionales (ej. 'Tomar con abundante agua después de cenar')."],
        ["proposito", "VARCHAR", "120", "Ninguna", "Sí", "NULL", "Finalidad terapéutica del fármaco (ej. 'Control de Presión Arterial', 'Glucosa')."],
        ["permite_posponer", "BOOLEAN", "0 ó 1", "Ninguna", "No", "TRUE", "Indica si la app permite al paciente posponer la toma 10 minutos o si debe ser estricta."],
        ["es_critico", "BOOLEAN", "0 ó 1", "Ninguna", "No", "FALSE", "Bandera de alta prioridad: si es TRUE, su omisión dispara alerta inmediata al cuidador."],
        ["contraindicaciones", "TEXT", "Texto libre", "Ninguna", "Sí", "NULL", "Advertencias médicas relevantes, interacciones y precauciones particulares."]
    ],
    "alergia_usuario": [
        ["id_alergia", "INT", "Auto-increment", "PK", "No", "Autonumérico", "Identificador único del registro de alergia farmacológica."],
        ["id_usuario", "INT", "Relación", "FK", "No", "N/A", "Referencia al paciente que presenta la reacción alérgica (`usuario.id_usuario`)."],
        ["sustancia", "VARCHAR", "255", "Ninguna", "No", "N/A", "Nombre del compuesto o principio activo alérgeno (ej. 'Penicilina', 'Sulfas')."],
        ["severidad", "ENUM", "'leve', 'moderada', 'grave'", "Ninguna", "No", "'grave'", "Nivel de gravedad de la reacción alérgica."],
        ["reaccion", "VARCHAR", "255", "Ninguna", "Sí", "NULL", "Síntomas manifestados por el paciente (ej. 'Erupción cutánea', 'Anafilaxia')."],
        ["fecha_registro", "TIMESTAMP", "Fecha y Hora", "Ninguna", "No", "CURRENT_TIMESTAMP", "Fecha y hora en que se ingresó la alerta al perfil médico."]
    ],
    "contacto_apoyo": [
        ["id_contacto", "INT", "Auto-increment", "PK", "No", "Autonumérico", "Identificador único del contacto de soporte o familiar."],
        ["id_usuario", "INT", "Relación", "FK", "No", "N/A", "Paciente al que asiste y supervisa este contacto (`usuario.id_usuario`)."],
        ["nombre_completo", "VARCHAR", "255", "Ninguna", "No", "N/A", "Nombre y apellido del familiar, tutor o enfermero asignado."],
        ["telefono", "VARCHAR", "50", "Formato E.164", "No", "N/A", "Número telefónico con código de país para envío de SMS, WhatsApp o llamada."],
        ["parentesco", "VARCHAR", "100", "Ninguna", "No", "N/A", "Relación familiar con el paciente (ej. 'Hijo', 'Cónyuge', 'Cuidador')."],
        ["correo", "VARCHAR", "255", "Ninguna", "Sí", "NULL", "Dirección electrónica para copia de reportes y notificaciones push."],
        ["es_principal", "BOOLEAN", "0 ó 1", "Ninguna", "No", "TRUE", "Indica si es el contacto primario que se llamará primero ante emergencias."],
        ["fecha_registro", "TIMESTAMP", "Fecha y Hora", "Ninguna", "No", "CURRENT_TIMESTAMP", "Momento en que se vinculó a la red de soporte."]
    ],
    "tratamiento": [
        ["id_tratamiento", "INT", "Auto-increment", "PK", "No", "Autonumérico", "Identificador secuencial del ciclo o esquema de tratamiento."],
        ["id_medicamento", "INT", "Relación", "FK", "No", "N/A", "Medicamento recetado asociado a este tratamiento (`medicamento.id_medicamento`)."],
        ["frecuencia_horas", "INT", "Horas entre tomas", "Ninguna", "No", "N/A", "Periodicidad en horas con la que debe tomarse el fármaco (ej. 8, 12 o 24 hrs)."],
        ["fecha_inicio", "TIMESTAMP", "Fecha y Hora", "Ninguna", "No", "CURRENT_TIMESTAMP", "Día y hora de arranque de la primera dosis del tratamiento."],
        ["fecha_fin", "TIMESTAMP", "Fecha y Hora", "Ninguna", "Sí", "NULL", "Día y hora de culminación del tratamiento; si es crónico, el campo es NULL."],
        ["estado", "ENUM", "'activo', 'inactivo'", "Ninguna", "No", "'activo'", "Estado operativo del tratamiento en el motor de generación de recordatorios."]
    ],
    "recordatorio": [
        ["id_recordatorio", "INT", "Auto-increment", "PK", "No", "Autonumérico", "Identificador unívoco de la toma teórica programada."],
        ["id_tratamiento", "INT", "Relación", "FK", "No", "N/A", "Tratamiento médico que dio origen a esta alarma (`tratamiento.id_tratamiento`)."],
        ["hora_programada", "TIMESTAMP", "Fecha y Hora", "Ninguna", "No", "N/A", "Momento exacto en que debe activarse la notificación o alarma sonora."],
        ["estado", "ENUM", "'pendiente', 'tomado', 'pospuesto', 'omitido'", "Ninguna", "No", "'pendiente'", "Estado actual en el que se encuentra la dosis programada."],
        ["veces_pospuesto", "TINYINT", "Numérico 0-255", "Ninguna", "No", "0", "Contador de ocasiones en que el paciente presionó 'Posponer 10 min'."]
    ],
    "historial_toma": [
        ["id_historial", "INT", "Auto-increment", "PK", "No", "Autonumérico", "Identificador único de la línea de auditoría de acción del paciente."],
        ["id_recordatorio", "INT", "Relación", "FK", "No", "N/A", "Recordatorio al que hace referencia la interacción (`recordatorio.id_recordatorio`)."],
        ["fecha_accion", "TIMESTAMP", "Fecha y Hora", "Ninguna", "No", "CURRENT_TIMESTAMP", "Momento real en que el usuario tocó el botón en su teléfono celular."],
        ["estado_final", "ENUM", "'tomado', 'pospuesto', 'omitido'", "Ninguna", "No", "N/A", "Acción clínica ejecutada por el usuario en esta interacción."],
        ["notas", "TEXT", "Texto libre", "Ninguna", "Sí", "NULL", "Comentarios u observaciones agregadas por el paciente (ej. 'Me provocó náusea')."]
    ],
    "alerta_cuidador": [
        ["id_alerta", "INT", "Auto-increment", "PK", "No", "Autonumérico", "Identificador único de la notificación de supervisión generada."],
        ["id_usuario", "INT", "Relación", "FK", "No", "N/A", "Paciente que originó la situación clínica de riesgo (`usuario.id_usuario`)."],
        ["tipo_alerta", "VARCHAR", "40", "Ninguna", "No", "'advertencia_normal'", "Clasificación de severidad: 'emergencia_critica' o 'advertencia_normal'."],
        ["accion_origen", "VARCHAR", "40", "Ninguna", "No", "'posponer'", "Causa del disparo: 'posponer', 'omitir' o 'vencimiento_tiempo'."],
        ["nombre_medicamento", "VARCHAR", "160", "Ninguna", "No", "N/A", "Fármaco involucrado en la alerta para conocimiento inmediato del familiar."],
        ["dosis", "VARCHAR", "80", "Ninguna", "No", "''", "Dosificación prescrita del fármaco involucrado."],
        ["es_critico", "BOOLEAN", "0 ó 1", "Ninguna", "No", "FALSE", "Indica si el medicamento es vital para la estabilidad del paciente."],
        ["mensaje", "VARCHAR", "500", "Ninguna", "No", "N/A", "Texto explicativo redactado en lenguaje natural para el cuidador."],
        ["nombre_cuidador", "VARCHAR", "160", "Ninguna", "No", "'Cuidador Principal'", "Nombre del familiar o enfermero a quien va dirigido el aviso."],
        ["telefono_cuidador", "VARCHAR", "60", "Ninguna", "No", "''", "Número telefónico al cual se canalizó la alerta automática."],
        ["atendida", "BOOLEAN", "0 ó 1", "Ninguna", "No", "FALSE", "Indica si el cuidador ya revisó y confirmó la atención de la emergencia."],
        ["fecha_creacion", "TIMESTAMP", "Fecha y Hora", "Ninguna", "No", "CURRENT_TIMESTAMP", "Marca temporal precisa en que el sistema generó el incidente."]
    ]
}

# ==============================================================================
# SECCIÓN 2.0 - 2.4: GESTIÓN Y OPERACIÓN DE DATOS DEL PROYECTO
# ==============================================================================

SEC_2_NECESIDADES = "2.0 Definición de las Necesidades de Información"
SEC_2_NECESIDADES_TEXT = (
    "Para que MedReminder AI cumpla satisfactoriamente con sus metas clínicas, preventivas y operativas, el sistema "
    "requiere procesar, almacenar y consultar de manera ágil los siguientes tipos de datos esenciales:\n"
    "1. Información de Identidad y Perfil del Paciente: Nombre completo, correo, fecha de nacimiento (para calcular edad "
    "y ajustar los parámetros de tamaño de fuente, contraste y sensibilidad del sistema de alertas para adultos mayores) "
    "y credenciales cifradas.\n"
    "2. Datos Farmacológicos y de Posología: Nombre genérico y comercial del fármaco, principio activo, presentación "
    "(tabletas, gotas, jarabe), color de la cápsula para reconocimiento visual, inventario físico de stock y nivel de criticidad.\n"
    "3. Horarios y Calendario Terapéutico: Frecuencia en horas, hora de primera toma, fecha de inicio y conclusión, permitiendo "
    "la generación determinista de la agenda de tomas a futuro.\n"
    "4. Red de Soporte y Cuidadores: Directorio de contactos de confianza, números telefónicos validados para mensajería y llamadas, "
    "parentesco y asignación de cuidadores principales.\n"
    "5. Trazabilidad de Auditoría y Cumplimiento: Registro de cada clic de toma, posposición y omisión con marca de tiempo precisa "
    "y comentarios del usuario, conformando el historial para el médico tratante.\n"
    "6. Telemetría y Eventos Clínicos Semi-estructurados: Bitácora de incidentes, cambios en el botiquín, fallas de conectividad "
    "y alertas emitidas para análisis estadístico y minería de datos."
)

SEC_2_UBICACION = "2.1 Descripción de la Ubicación y Características de los Datos"
SEC_2_UBICACION_TEXT = (
    "El sistema implementa una arquitectura de Persistencia Políglota Híbrida distribuida en tres niveles complementarios:\n\n"
    "A. Base de Datos Relacional (MySQL 8.4 Server):\n"
    "- Ubicación: Servidor de base de datos en contenedor Docker independiente, conectado a una red privada virtual de backend.\n"
    "- Características: Almacena las entidades fuertemente estructuradas bajo garantías ACID completas. Aquí residen usuarios, "
    "medicamentos, tratamientos, recordatorios y contactos. El volumen estimado es moderado (cientos de miles de filas) pero con "
    "una criticidad de integridad absoluta: no puede existir un recordatorio huérfano ni un paciente sin id válido.\n\n"
    "B. Base de Datos No Relacional (MongoDB 7.0):\n"
    "- Ubicación: Contenedor NoSQL optimizado para operaciones de lectura y escritura intensiva, accesible mediante la base de datos `medreminder_logs`.\n"
    "- Características: Almacena documentos en formato BSON semiestructurado en colecciones como `eventos_clinicos` y `auditoria_accesos`. "
    "Permite escrituras asíncronas no bloqueantes con latencia cercana a 0 ms para el hilo HTTP de la aplicación móvil. "
    "Posee un esquema dinámico y flexible, ideal para absorber cambios en los formatos de telemetría sin requerir migraciones DDL.\n\n"
    "C. Almacenamiento Local en Dispositivo Móvil (Android Room / SQLite & DataStore):\n"
    "- Ubicación: Memoria interna segura (`data/data/com.medreminder.app/`) del teléfono inteligente del usuario.\n"
    "- Características: Garantiza que la aplicación funcione en modo 100% offline. Las alarmas de toma se sincronizan localmente "
    "con el `AlarmManager` del sistema operativo Android, sonando con precisión de milisegundos aun cuando el paciente no disponga de conexión Wi-Fi ni datos móviles."
)

SEC_2_AUTOMATIZACION = "2.2 Descripción de las Tareas y sus Técnicas de Automatización"
SEC_2_AUTOMATIZACION_TEXT = (
    "Para reducir al mínimo el error humano y la fatiga operativa, MedReminder AI automatiza cinco procesos clave:\n\n"
    "1. Generación Automática de Ventanas de Toma: Mediante el servicio `recordatorio_service.py`, al registrar o renovar un "
    "tratamiento, el sistema calcula matemáticamente y genera en bloque las tomas para los siguientes 7 a 14 días según la "
    "frecuencia horaria, evitando que el usuario deba programar alarma por alarma manualmente.\n\n"
    "2. Detección Proactiva de Omisiones por Tiempo Vencido: Un worker en segundo plano evalúa continuamente los recordatorios "
    "en estado 'pendiente'. Si transcurren más de 30 minutos posteriores a la hora programada sin confirmación del usuario, el sistema "
    "actualiza automáticamente el estado a 'omitido' y evalúa la criticidad del fármaco.\n\n"
    "3. Disparo Reactivo de Alertas Clínicas al Cuidador: Cuando el paciente pospone un medicamento marcado como crítico "
    "(`es_critico = TRUE`) o cuando un adulto mayor ignora un fármaco de control regular, un pipeline reactivo genera un registro "
    "en `alerta_cuidador` y dispara automáticamente una notificación push de alta prioridad y una alerta dirigida al teléfono del familiar.\n\n"
    "4. Control de Inventario y Alerta de Desabasto: Cada confirmación de 'tomado' decrementa automáticamente una unidad en "
    "`cantidad_stock`. Cuando las unidades restantes caen por debajo del 20% del stock inicial, el sistema genera automáticamente "
    "un aviso de 'Resurtir Medicamento' para prevenir que el paciente se quede sin fármacos esenciales.\n\n"
    "5. Respaldos Automatizados de Datos (Cron Jobs): Rutinas automatizadas en el contenedor de infraestructura que ejecutan "
    "volcados lógicos diarios de MySQL y MongoDB con rotación de versiones y compresión para evitar sobrellenado de disco."
)

SEC_2_IMPORT_EXPORT = "2.3 Descripción del Método de Importación y Exportación"
SEC_2_IMPORT_EXPORT_TEXT = (
    "Métodos de Importación:\n"
    "- Importación Asistida por IA de Recetas Médicas: El paciente o cuidador fotografía la receta médica con la cámara del dispositivo móvil. "
    "La imagen es procesada por el microservicio de IA clínica (Ollama con modelo de visión multimodal `medi-clinico`), el cual "
    "realiza OCR inteligente, extrae los nombres de fármacos, dosis, frecuencias y duraciones, y los convierte automáticamente en un objeto "
    "JSON estructurado que se pre-llena en el formulario de la app para confirmación del usuario con un solo toque.\n"
    "- Inicialización y Sembrado de Esquema (DDL/DML): Carga masiva de catálogos y esquemas a través de scripts SQL (`01_schema.sql`) "
    "montados en el punto de entrada `/docker-entrypoint-initdb.d` de MySQL en la primera inicialización.\n\n"
    "Métodos de Exportación:\n"
    "- Reporte Clínico en Formato PDF y CSV: La plataforma permite exportar el historial de adherencia de los últimos 30, 60 o 90 días "
    "en un documento PDF estructurado y estilizado, listo para ser enviado por correo electrónico o impreso para el médico geriatra.\n"
    "- Exportación de Copias de Respaldo: Scripts de mantenimiento que ejecutan herramientas nativas de volcado lógico:\n"
    "  * MySQL: `mysqldump --single-transaction --routines --triggers -u root -p medreminder_db > backup_mysql.sql`\n"
    "  * MongoDB: `mongodump --uri=\"mongodb://...\" --db=medreminder_logs --gzip --archive=backup_mongo.gz`\n"
    "- Exportación de Telemetría: Descarga de logs de eventos en formato JSON mediante endpoints administrativos para auditoría externa."
)

SEC_2_SEGURIDAD = "2.4 Lineamientos de Seguridad que se Aplicarán en la Base de Datos"
SEC_2_SEGURIDAD_TEXT = (
    "Por tratarse de una plataforma que gestiona datos sensibles de salud personal, MedReminder AI aplica los más estrictos "
    "estándares de la industria (alineados a la Norma Oficial Mexicana NOM-024-SSA3-2012 y principios de HIPAA y GDPR):\n\n"
    "1. Principio de Menor Privilegio (Least Privilege): Las aplicaciones y microservicios no acceden como usuario 'root' ni 'sa'. "
    "Se crean usuarios dedicados para el backend con privilegios exclusivos sobre las bases de datos de la aplicación (`medreminder_db` "
    "y `medreminder_logs`), impidiendo comandos destructivos como `DROP DATABASE` o alteración de esquemas en tiempo de ejecución.\n\n"
    "2. Cifrado Criptográfico de Contraseñas: Se prohíbe el almacenamiento de contraseñas en texto plano. Se implementa hashing "
    "robusto mediante algoritmos con sal única y función de derivación de claves de alto costo computacional (PBKDF2 con SHA-256 o Bcrypt).\n\n"
    "3. Cifrado de Canales de Comunicación (TLS/SSL): Todo el tráfico entre la aplicación móvil Android y el servidor backend viaja "
    "obligatoriamente encapsulado en túneles HTTPS con TLS 1.3, mitigando ataques de intermediario (Man-in-the-Middle).\n\n"
    "4. Aislamiento de Red mediante Contenedores: Los puertos de bases de datos (3306 de MySQL y 27017 de MongoDB) no se exponen al exterior "
    "en entornos de producción. La comunicación ocurre estrictamente dentro de la red puente virtual de Docker (`medreminder-net`).\n\n"
    "5. Sanitización y Prevención de Inyecciones (SQL & NoSQL): Implementación rigurosa de ORM (SQLAlchemy) con consultas preparadas "
    "y tipado fuerte con Pydantic, impidiendo la inyección de sentencias SQL maliciosas o inyecciones de operadores de consulta en MongoDB.\n\n"
    "6. Políticas de Respaldos Cifrados y Verificación Periódica: Los archivos de respaldo se generan comprimidos, se cifran con clave simétrica "
    "AES-256 y se someten a simulacros de restauración mensual para garantizar el objetivo de tiempo de recuperación (RTO < 2 horas)."
)

# ==============================================================================
# SECCIÓN 3.0 - 3.4: ARQUITECTURA DE SOFTWARE DEL SISTEMA
# ==============================================================================

SEC_3_REQUERIMIENTOS = "3.0 Requerimientos Funcionales y No Funcionales de Desarrollo de Software"

REQUERIMIENTOS_FUNCIONALES = [
    ["RF-01", "Registro y Autenticación de Pacientes", "El sistema debe permitir a pacientes y cuidadores registrarse con nombre, correo, fecha de nacimiento y contraseña segura con validación JWT."],
    ["RF-02", "Gestión de Botiquín y Medicamentos", "Permite registrar, actualizar, visualizar y dar de baja medicamentos indicando nombre, dosis, stock físico, color de gragea y nivel de criticidad."],
    ["RF-03", "Programación Dinámica de Tomas", "Calcula y genera automáticamente los horarios de toma de acuerdo a la frecuencia horaria (cada 8, 12, 24 hrs) y fecha de inicio del tratamiento."],
    ["RF-04", "Alarmas Nativas Deterministas Offline", "La app móvil debe sincronizar alarmas locales con el `AlarmManager` de Android para sonar con sonido prioritario sin depender de internet."],
    ["RF-05", "Registro Interactivo de Tomas", "El paciente puede marcar cada dosis como 'Tomado', 'Posponer 10 min' o 'Omitido', actualizando el inventario y la bitácora de cumplimiento."],
    ["RF-06", "Alertas Reactivas a Cuidadores", "Si el usuario pospone u omite un fármaco crítico, el sistema debe generar una alerta inmediata con los datos de contacto del familiar registrado."],
    ["RF-07", "Escaneo Inteligente de Recetas con IA", "Permite capturar una foto de la receta médica y extraer con visión multimodal los medicamentos, dosis y frecuencias de forma automática."],
    ["RF-08", "Directorio de Red de Soporte", "Permite vincular a familiares o cuidadores primarios con parentesco y número telefónico para comunicación directa ante emergencias."],
    ["RF-09", "Gamificación y Racha de Adherencia", "Calcula y muestra la racha de días consecutivos cumplidos y nivel de honor según la edad del paciente, motivando la constancia clínica."],
    ["RF-10", "Exportación de Historial Clínico", "Genera reportes imprimibles en PDF o exportables en CSV con el detalle cronológico de tomas para ser presentado al médico especialista."]
]

REQUERIMIENTOS_NO_FUNCIONALES = [
    ["RNF-01", "Rendimiento y Latencia de API", "El tiempo de respuesta del backend en peticiones HTTP habituales no debe superar los 200 ms bajo una concurrencia normal."],
    ["RNF-02", "Disponibilidad del Servicio", "La infraestructura de microservicios en contenedores debe garantizar una disponibilidad mínima del 99.9% de tiempo en línea."],
    ["RNF-03", "Resiliencia y Operación Offline", "La aplicación móvil Android debe permitir consultar el botiquín y activar alarmas sonoras aun en ausencia total de conectividad a internet."],
    ["RNF-04", "Seguridad y Cifrado", "Todas las contraseñas deben cifrarse con algoritmos de hashing seguro; la comunicación móvil-servidor debe emplear HTTPS con TLS 1.3."],
    ["RNF-05", "Accesibilidad y Ergonomía (UX)", "La interfaz gráfica debe diseñarse considerando adultos mayores: tipografías legibles (>16sp), alto contraste, botones amplios y textos directos."],
    ["RNF-06", "Integridad Transaccional (ACID)", "El motor de base de datos relacional debe prevenir registros huérfanos y mantener consistencia absoluta en inventarios y recetas."],
    ["RNF-07", "Compatibilidad Móvil", "La app Android debe ser compatible con dispositivos que ejecuten desde Android 8.0 (API nivel 26) hasta las versiones más recientes."],
    ["RNF-08", "Mantenibilidad y Despliegue", "El sistema debe estar contenerizado con Docker y Docker Compose, facilitando su despliegue reproducible en cualquier entorno local o en la nube."]
]

SEC_3_JUSTIFICACION = "3.1 Justificación de la Arquitectura Seleccionada"
SEC_3_JUSTIFICACION_TEXT = (
    "Para satisfacer las necesidades funcionales de MedReminder AI y cumplir con los altos estándares de seguridad médica "
    "y tolerancia a fallos, se seleccionó una Arquitectura en Capas Desacoplada (Clean Architecture) combinada con "
    "Microservicios REST y Persistencia Políglota. A continuación se justifica cada decisión técnica:\n\n"
    "1. ¿Por qué una Aplicación Móvil Nativa en Android (Kotlin + Jetpack Compose)?\n"
    "Las aplicaciones web progresivas (PWA) o híbridas sufren limitaciones severas en segundo plano: el sistema operativo "
    "Android puede matar sus procesos en reposo para ahorrar batería, perdiendo alarmas médicas vitales. Kotlin nativo junto a "
    "`AlarmManager` y `BroadcastReceiver` permite programar alarmas de alta prioridad (`setExactAndAllowWhileIdle`) que despiertan "
    "al procesador a la hora exacta, incluso si el dispositivo se encuentra en modo Doze o sin conexión a internet.\n\n"
    "2. ¿Por qué FastAPI en Python para el Backend?\n"
    "FastAPI es un framework moderno de alto rendimiento que opera sobre el estándar ASGI (`async`/`await`), permitiendo atender "
    "miles de peticiones concurrentes con consumo mínimo de recursos de CPU y memoria. Además, al estar escrito en Python, facilita "
    "la integración nativa y directa con bibliotecas de Inteligencia Artificial (Ollama, PyTorch, OpenCV, LangChain) sin recurrir a puentes externos lentos.\n\n"
    "3. ¿Por qué Persistencia Híbrida (MySQL + MongoDB)?\n"
    "El paradigma relacional (MySQL) es insuperable para datos estructurados con relaciones obligatorias (usuarios, medicamentos, posologías), "
    "donde la pérdida de integridad referencial arruinaría la dosificación del paciente. Por su parte, el paradigma no relacional (MongoDB) "
    "es idóneo para absorber ráfagas masivas de eventos de telemetría y logs de auditoría clínica en formato BSON sin impactar las tablas relacionales.\n\n"
    "4. ¿Por qué Inteligencia Artificial Local (Ollama)?\n"
    "Enviar fotografías de recetas médicas de pacientes a APIs públicas comerciales en la nube (como OpenAI o Google Cloud) violaría leyes "
    "de privacidad médica en diversos países al compartir datos sensibles. Ejecutar el modelo `medi-clinico` localmente en un contenedor "
    "aislado de Ollama garantiza soberanía de datos y cero costos por token de procesamiento."
)

SEC_3_DIAGRAMA_ARQ = "3.2 Diagrama de Arquitectura de Software"
SEC_3_DIAGRAMA_ARQ_TEXT = (
    "A continuación se presenta el esquema arquitectónico multicapa del sistema MedReminder AI, detallando la interacción "
    "entre los clientes móviles, las capas de seguridad, los microservicios de backend y la capa de persistencia políglota:"
)

# 3.3 Características y funciones de los componentes
COMPONENTES_DATA = [
    ["App Móvil Android (Cliente)", "Kotlin, Jetpack Compose, MVVM, Room, Retrofit, AlarmManager", "Interfaz táctil accesible para el paciente; gestión de caché local en Room; programación de alarmas nativas deterministas; captura de recetas con cámara y sincronización REST."],
    ["API Gateway & Seguridad", "FastAPI Core, OAuth2, JWT Bearer, CORS Middleware", "Punto de entrada único; validación criptográfica de tokens JWT; limitación de tasa (rate limiting); sanitización de encabezados y enrutamiento a controladores internos."],
    ["Módulo de Gestión Farmacológica", "FastAPI Routers, Pydantic Schemas, SQLAlchemy ORM", "CRUD de medicamentos; administración de dosis y presentaciones; control y decremento automático de stock; validación de contraindicaciones y alergias."],
    ["Módulo de Agenda y Recordatorios", "FastAPI Engine, Python DateTime, Workers Asíncronos", "Cálculo matemático de tomas a futuro según frecuencia horaria; monitoreo de ventanas de tolerancia; registro de acciones de toma/omisión."],
    ["Módulo de Cuidador y Alertas", "FastAPI Service, Push Notification Dispatcher", "Evaluación de medicamentos críticos; generación de avisos en tiempo real para familiares; historial de incidentes y confirmación de atención de emergencias."],
    ["Microservicio de IA Clínica", "Ollama Runner, Modelo de Visión `medi-clinico`", "Procesamiento de visión por computadora sobre fotos de recetas; extracción OCR contextual; devolución de datos estructurados JSON para precarga rápida."],
    ["Motor Relacional (MySQL)", "MySQL Server 8.4 InnoDB", "Persistencia transaccional ACID de usuarios, botiquín, tratamientos, recordatorios y red de apoyo; llaves foráneas con borrado en cascada."],
    ["Motor NoSQL (MongoDB)", "MongoDB 7.0 Community Engine", "Almacenamiento no relacional BSON de eventos clínicos inmutables, telemetría de uso y auditoría de accesos con alta velocidad de inserción."]
]

SEC_3_DIAGRAMAS_SECUENCIA = "3.4 Diagramas Necesarios de Acuerdo a la Arquitectura Seleccionada"
SEC_3_DIAGRAMAS_SECUENCIA_TEXT = (
    "Para comprender la dinámica en tiempo de ejecución del sistema, se presentan a continuación los diagramas de flujo, "
    "secuencia de interacción y topología física de contenedores:"
)

# ==============================================================================
# SECCIÓN 4.0 - 4.3: GESTIÓN DE BASE DE DATOS NO RELACIONAL (MONGODB)
# ==============================================================================

SEC_4_ESTRUCTURA = "4.0 Estructura de Almacenamiento Mediante Elementos No Relacionales"
SEC_4_ESTRUCTURA_TEXT = (
    "En MedReminder AI, el subsistema no relacional está implementado sobre MongoDB 7.0 y se organiza en torno a los "
    "cinco conceptos fundamentales del paradigma orientado a documentos:\n\n"
    "1. Base de Datos: Espacio lógico independiente donde se concentra la información de una aplicación. En nuestro proyecto, "
    "la base de datos se denomina `medreminder_logs` y aloja exclusivamente colecciones de auditoría y telemetría clínica.\n\n"
    "2. Colección: Conjunto de documentos agrupados bajo un mismo contexto de negocio (equivalente conceptual a una tabla relacional, "
    "pero sin un esquema rígido impuesto por el motor). En MedReminder AI se definen colecciones como:\n"
    "   * `eventos_clinicos`: Bitácora inmutable de tomas, posposiciones, omisiones y alertas disparadas.\n"
    "   * `auditoria_accesos`: Registro de inicios de sesión, IPs de origen y revocaciones de token.\n"
    "   * `telemetria_rendimiento`: Métricas de latencia de endpoints y tiempos de inferencia de IA.\n\n"
    "3. Documento: Registro individual que contiene la información formateada en BSON (Binary JSON), permitiendo estructuras "
    "jerárquicas ricas como arreglos y subdocumentos embebidos en un solo registro.\n\n"
    "4. Campo: Cada propiedad clave-valor que compone un documento (ej. `evento`, `id_usuario`, `timestamp`, `detalle`). "
    "Los campos pueden almacenar diversos tipos primitivos y complejos de BSON.\n\n"
    "5. Identificador (`_id`): Llave primaria obligatoria y única generada automáticamente para cada documento. Corresponde "
    "a un `ObjectId` de 12 bytes compuesto por: 4 bytes de marca temporal (timestamp Unix), 5 bytes de identificador aleatorio "
    "por proceso/máquina, y 3 bytes de contador incremental, lo que garantiza unicidad distribuida sin colisiones."
)

JSON_EJEMPLO_BSON = """{
  "_id": ObjectId("672ccb3f8a1290d1e5a8f410"),
  "evento": "alerta_medicamento_critico_emitida",
  "id_usuario": 104,
  "timestamp": ISODate("2026-11-06T18:45:00.000Z"),
  "detalle": {
    "medicamento": "Losartán Potásico",
    "dosis": "50 mg",
    "es_critico": true,
    "accion_origen": "posponer_excesivo",
    "veces_pospuesto": 2,
    "cuidador_notificado": {
      "nombre": "Carlos Nava García",
      "parentesco": "Hijo",
      "telefono": "+527221234567",
      "canal_envio": "push_high_priority"
    },
    "ip_origen": "192.168.1.15",
    "dispositivo": "Samsung Galaxy A54 (Android 14)"
  }
}"""

SEC_4_CRUD = "4.1 Métodos de Manipulación de Datos (CRUD) en MongoDB"
SEC_4_CRUD_TEXT = (
    "A continuación se documentan los métodos de manipulación de datos en MongoDB aplicados a los casos de uso reales de MedReminder AI, "
    "incluyendo la sintaxis oficial de `mongosh` y su implementación en código Python con la librería `pymongo`:"
)

CRUD_OPERACIONES = [
    {
        "letra": "A",
        "titulo": "Crear una Base de Datos y Colección",
        "explicacion": "En MongoDB una base de datos y colección se crean dinámicamente al insertar el primer documento, o de forma explícita estableciendo validaciones de esquema o límites de tamaño (capped collections).",
        "mongosh": "// Conectar y cambiar al contexto de la base de datos\nuse medreminder_logs;\n\n// Crear explícitamente la colección de eventos clínicos\ndb.createCollection(\"eventos_clinicos\", {\n   validator: {\n      $jsonSchema: {\n         bsonType: \"object\",\n         required: [\"evento\", \"id_usuario\", \"timestamp\"],\n         properties: {\n            evento: { bsonType: \"string\" },\n            id_usuario: { bsonType: \"int\" },\n            timestamp: { bsonType: \"date\" }\n         }\n      }\n   }\n});",
        "pymongo": "from pymongo import MongoClient\nclient = MongoClient(\"mongodb://localhost:27017/\")\ndb = client[\"medreminder_logs\"]\ncoleccion = db[\"eventos_clinicos\"]"
    },
    {
        "letra": "B",
        "titulo": "Insertar un Documento (Create)",
        "explicacion": "Inserta un único registro de evento cuando el paciente confirma una toma en la aplicación móvil.",
        "mongosh": "db.eventos_clinicos.insertOne({\n  evento: \"toma_confirmada\",\n  id_usuario: NumberInt(104),\n  timestamp: new Date(),\n  detalle: {\n    medicamento: \"Metformina\",\n    dosis: \"850 mg\",\n    estado: \"tomado\",\n    a_tiempo: true\n  }\n});",
        "pymongo": "import datetime\ndocumento = {\n    \"evento\": \"toma_confirmada\",\n    \"id_usuario\": 104,\n    \"timestamp\": datetime.datetime.utcnow(),\n    \"detalle\": {\"medicamento\": \"Metformina\", \"dosis\": \"850 mg\", \"estado\": \"tomado\"}\n}\nresultado = db[\"eventos_clinicos\"].insert_one(documento)\nprint(f\"ID insertado: {resultado.inserted_id}\")"
    },
    {
        "letra": "C",
        "titulo": "Insertar Varios Documentos (Bulk Insert)",
        "explicacion": "Permite registrar en una sola operación atómica múltiples eventos acumulados durante un periodo de sincronización offline.",
        "mongosh": "db.eventos_clinicos.insertMany([\n  {\n    evento: \"alarma_disparada\",\n    id_usuario: NumberInt(104),\n    timestamp: new Date(\"2026-11-06T08:00:00Z\"),\n    detalle: { medicamento: \"Losartán\", hora_programada: \"08:00\" }\n  },\n  {\n    evento: \"alarma_disparada\",\n    id_usuario: NumberInt(104),\n    timestamp: new Date(\"2026-11-06T14:00:00Z\"),\n    detalle: { medicamento: \"Omeprazol\", hora_programada: \"14:00\" }\n  }\n]);",
        "pymongo": "lote = [\n    {\"evento\": \"alarma_offline_1\", \"id_usuario\": 104, \"timestamp\": datetime.datetime.utcnow()},\n    {\"evento\": \"alarma_offline_2\", \"id_usuario\": 104, \"timestamp\": datetime.datetime.utcnow()}\n]\nres = db[\"eventos_clinicos\"].insert_many(lote)\nprint(f\"Insertados {len(res.inserted_ids)} registros\")"
    },
    {
        "letra": "D",
        "titulo": "Consultar Todos los Registros (Read All)",
        "explicacion": "Recupera la totalidad de documentos de una colección (utilizado en rutinas de exportación o respaldo global).",
        "mongosh": "// Consultar todos con formato legible y límite de seguridad\ndb.eventos_clinicos.find().sort({ timestamp: -1 }).limit(50).pretty();",
        "pymongo": "cursor = db[\"eventos_clinicos\"].find().sort(\"timestamp\", -1).limit(50)\nfor doc in cursor:\n    print(doc[\"evento\"], doc.get(\"timestamp\"))"
    },
    {
        "letra": "E",
        "titulo": "Consultar un Registro Específico (Read One)",
        "explicacion": "Localiza un único documento exacto mediante su clave primaria `_id` de tipo `ObjectId`.",
        "mongosh": "db.eventos_clinicos.findOne({\n  _id: ObjectId(\"672ccb3f8a1290d1e5a8f410\")\n});",
        "pymongo": "from bson import ObjectId\ndoc = db[\"eventos_clinicos\"].find_one({\"_id\": ObjectId(\"672ccb3f8a1290d1e5a8f410\")})\nprint(doc)"
    },
    {
        "letra": "F",
        "titulo": "Actualizar Información (Update)",
        "explicacion": "Modifica atributos específicos de un documento sin sobreescribir el resto, como marcar una alerta como atendida.",
        "mongosh": "db.eventos_clinicos.updateOne(\n  { _id: ObjectId(\"672ccb3f8a1290d1e5a8f410\") },\n  {\n    $set: {\n      \"detalle.atendida\": true,\n      \"detalle.fecha_atencion\": new Date(),\n      \"detalle.atendido_por\": \"Enfermera María\"\n    }\n  }\n);",
        "pymongo": "db[\"eventos_clinicos\"].update_one(\n    {\"_id\": ObjectId(\"672ccb3f8a1290d1e5a8f410\")},\n    {\"$set\": {\"detalle.atendida\": True, \"detalle.fecha_atencion\": datetime.datetime.utcnow()}}\n)"
    },
    {
        "letra": "G",
        "titulo": "Eliminar un Registro (Delete)",
        "explicacion": "Elimina documentos específicos o en lote para depuración de registros obsoletos de auditoría tras cumplir periodos de retención.",
        "mongosh": "// Eliminar un documento específico\ndb.eventos_clinicos.deleteOne({\n  _id: ObjectId(\"672ccb3f8a1290d1e5a8f410\")\n});\n\n// Eliminar eventos de prueba o antiguos\ndb.eventos_clinicos.deleteMany({\n  evento: \"evento_prueba\"\n});",
        "pymongo": "db[\"eventos_clinicos\"].delete_one({\"_id\": ObjectId(\"672ccb3f8a1290d1e5a8f410\")})"
    },
    {
        "letra": "H",
        "titulo": "Consultar Mediante Condiciones y Operadores Avanzados",
        "explicacion": "Búsqueda con operadores de comparación (`$gt`, `$in`), lógicos (`$and`) y filtros sobre subdocumentos embebidos.",
        "mongosh": "// Buscar eventos de medicamentos críticos pospuestos u omitidos en las últimas 24 horas\ndb.eventos_clinicos.find({\n  $and: [\n    { \"id_usuario\": 104 },\n    { \"detalle.es_critico\": true },\n    { \"evento\": { $in: [\"toma_pospuesta\", \"toma_omitida\", \"alerta_medicamento_critico_emitida\"] } },\n    { \"timestamp\": { $gte: new Date(Date.now() - 24*60*60*1000) } }\n  ]\n}).sort({ timestamp: -1 });",
        "pymongo": "ayer = datetime.datetime.utcnow() - datetime.timedelta(days=1)\nfiltro = {\n    \"$and\": [\n        {\"id_usuario\": 104},\n        {\"detalle.es_critico\": True},\n        {\"evento\": {\"$in\": [\"toma_pospuesta\", \"toma_omitida\"]}},\n        {\"timestamp\": {\"$gte\": ayer}}\n    ]\n}\nresultados = db[\"eventos_clinicos\"].find(filtro)\nfor r in resultados:\n    print(r[\"evento\"], r[\"detalle\"][\"medicamento\"])"
    }
]

SEC_4_SEGURIDAD_MONGODB = "4.2 Métodos o Sintaxis Relacionados con la Seguridad y Niveles de Acceso en MongoDB en la Nube"
SEC_4_SEGURIDAD_MONGODB_TEXT = (
    "El aseguramiento de un motor de bases de datos no relacional alojado en infraestructura de nube (como MongoDB Atlas "
    "o servidores virtuales privados dedicados) requiere la implementación estricta de mecanismos de control de acceso "
    "basados en roles (RBAC - Role-Based Access Control) y cifrado de extremo a extremo:\n\n"
    "1. Métodos de Seguridad de Red y Cifrado:\n"
    "- Autenticación Criptográfica Robusta: Uso por defecto del protocolo SCRAM-SHA-256 (Salted Challenge Response Authentication "
    "Mechanism), que garantiza que las contraseñas nunca viajen ni se comparen en texto plano sobre la red.\n"
    "- Cifrado en Tránsito (TLS/SSL): Conexiones forzadas con certificados TLS 1.3, rechazando cualquier intento de conexión insegura.\n"
    "- Aislamiento Perimetral (IP Whitelisting & VPC Peering): Restricción estricta de las direcciones IP autorizadas para conectarse "
    "al clúster, permitiendo exclusivamente el tráfico proveniente de las IPs públicas/privadas fijas de la API de backend.\n\n"
    "2. Niveles de Acceso y Roles Nativos en MongoDB:\n"
    "- `read`: Otorga permisos exclusivos de lectura sobre una base de datos específica (consultas con `find`).\n"
    "- `readWrite`: Permite lectura y escritura (operaciones completas de CRUD: `insert`, `update`, `delete`, `find`).\n"
    "- `dbAdmin`: Otorga privilegios administrativos locales sobre una BD (crear índices, ver estadísticas y profiling) sin conceder lectura de datos.\n"
    "- `userAdmin`: Permite crear y modificar usuarios y asignar roles dentro de esa base de datos específica.\n"
    "- `clusterAdmin`: Rol administrativo de más alto nivel para gestionar réplicas, sharding y parámetros de nodo.\n\n"
    "3. Creación de Usuarios y Asignación de Roles en Sintaxis Oficial:"
)

CODIGO_MONGODB_RBAC = """// Conectarse a la base de datos administrativa 'admin'
use admin;

// 1. Crear el usuario de servicio exclusivo para la API backend de MedReminder AI
db.createUser({
  user: "app_medreminder",
  pwd: "C0mpl3x#P@ssw0rd!Med2026_SecureKey",
  roles: [
    { role: "readWrite", db: "medreminder_logs" }
  ]
});

// 2. Crear usuario de solo lectura para reportería médica y analítica clínica (BI)
db.createUser({
  user: "bi_medreminder_reader",
  pwd: "R3@dOnly#Clin1c@l_2026_TokenSafe",
  roles: [
    { role: "read", db: "medreminder_logs" }
  ]
});

// 3. Crear usuario administrador de operaciones de base de datos
db.createUser({
  user: "admin_medreminder_ops",
  pwd: "Sup3r#Dba!Admin_Ops_2026_P@ssw0rd",
  roles: [
    { role: "dbAdmin", db: "medreminder_logs" },
    { role: "userAdmin", db: "medreminder_logs" }
  ]
});"""

SEC_4_CONFIG_SEGURIDAD = "4.3 Configuración de Seguridad en MongoDB de Acuerdo al Proyecto"
SEC_4_CONFIG_SEGURIDAD_PUNTOS = [
    ["Usuarios independientes para cada función", "Se descarta terminantemente el uso de credenciales genéricas o cuentas compartidas. Se crean tres cuentas separadas con privilegios mínimos segregados: `app_medreminder` para las operaciones cotidianas de la API FastAPI, `bi_reader` para la generación de reportes y estadísticas sin riesgo de borrado accidental, y `admin_ops` para labores de indexación y mantenimiento por el DBA."],
    ["Configuración de contraseñas robustas", "Todas las credenciales de la base de datos se generan con una longitud mínima de 24 caracteres aleatorios que combinan caracteres alfanuméricos en mayúsculas, minúsculas y símbolos especiales de alta entropía. Se prohíbe el uso de palabras de diccionario o patrones predecibles."],
    ["Uso de direcciones IP autorizadas", "El firewall de MongoDB (o la lista Network Access de MongoDB Atlas) está configurado con una regla estricta que bloquea por defecto cualquier dirección IP externa (`0.0.0.0/0` está prohibido). Únicamente se autorizan las direcciones IP estáticas del clúster de servidores de backend donde corre FastAPI."],
    ["Uso de credenciales y variables de entorno", "Las cadenas de conexión completas (Connection Strings) jamás se escriben de manera fija en el código fuente de la aplicación (hardcoding). Se inyectan en tiempo de ejecución a través de variables de entorno seguras (`MONGO_URL`, `MONGO_DB`) gestionadas mediante archivos `.env` excluidos del repositorio Git (`.gitignore`) y resguardadas con Docker Secrets en producción."],
    ["Uso de respaldos periódicos", "Se implementa una política formal de respaldo automatizado: copias de seguridad incrementales cada 24 horas y completas semanales mediante `mongodump --gzip --archive`. Los volcados se transmiten de forma cifrada a un bucket de almacenamiento seguro (S3 / Google Cloud Storage) con una política de retención de 30 días y verificación automatizada de restauración."],
    ["Uso de registros de acceso y revisión de actividad", "Se activa el registro de auditoría de MongoDB (`--auditDestination`) para almacenar todos los intentos de autenticación exitosos y fallidos, comandos administrativos ejecutados y anomalías de conexión. Además, se habilita el profiling de consultas lentas (`db.setProfilingLevel(1, { slowms: 100 })`) para detectar cuellos de botella que afecten la experiencia del usuario."]
]

# ==============================================================================
# SECCIÓN 5.0 - 5.2: MÉTODOS DE CONEXIÓN Y CONSUMO DE DATOS EN LA NUBE
# ==============================================================================

SEC_5_METODOS_CONEXION = "5.0 Métodos de Conexión de Base de Datos en la Nube y las Aplicaciones"

SEC_5_PASOS_CONEXION = "5.1 Describe los Pasos para Establecer la Conexión de la Base de Datos con la Aplicación"
PASOS_CONEXION_DETALLE = [
    ["Paso 1: Aprovisionamiento y Configuración del Clúster Cloud", "Se despliega una instancia gestionada de MongoDB (por ejemplo en MongoDB Atlas M0/M10 o un droplet dedicado). Se configuran la región más cercana (ej. `us-east-1` para menor latencia con México), los parámetros de hardware y el motor de almacenamiento WiredTiger."],
    ["Paso 2: Configuración de la Red y Lista de Acceso IP (IP Access List)", "En el panel de seguridad de red del proveedor cloud, se agrega la dirección IP estática pública de la máquina host del backend de FastAPI. Esto crea una barrera perimetral infranqueable para escaneos no autorizados."],
    ["Paso 3: Creación de Credenciales de Aplicación con Menor Privilegio", "Se genera el usuario `app_medreminder` con rol `readWrite` acotado exclusivamente a la base de datos `medreminder_logs`, asignando una contraseña de alta entropía generada criptográficamente."],
    ["Paso 4: Obtención y Construcción de la URI de Conexión Segura (Connection String)", "Se obtiene la cadena de conexión estandarizada con protocolo DNS Seedlist (`mongodb+srv://`) y parámetros de seguridad:\n`mongodb+srv://app_medreminder:<PASSWORD>@medreminder-cluster.xyz.mongodb.net/medreminder_logs?retryWrites=true&w=majority&authSource=admin`"],
    ["Paso 5: Inyección Segura en el Entorno del Backend FastAPI", "La URI se almacena en el archivo `.env` del servidor bajo la variable `MONGO_URL`. En el módulo `app/core/config.py`, la clase `Settings` de Pydantic carga y valida la variable de forma tipada y segura en el arranque."],
    ["Paso 6: Inicialización del Cliente Singleton con Connection Pooling", "En el archivo `app/core/mongo.py`, se implementa una función `get_mongo_client()` que mantiene un cliente único (`MongoClient`) con una piscina de conexiones optimizada (`maxPoolSize=16`, `connectTimeoutMS=1200`, `serverSelectionTimeoutMS=1200`), reutilizando sockets TCP para evitar sobrecarga de handshakes."],
    ["Paso 7: Verificación Activa mediante Ping y Healthcheck en Arranque", "Durante el ciclo de vida del servidor (evento `lifespan` en `main.py`), se ejecuta `client.admin.command('ping')`. Si el clúster responde exitosamente, el servicio reporta estado saludable en el endpoint `/health`."]
]

SEC_5_CONSUMO_DATOS = "5.2 Métodos de Consumo de Datos en la Nube"
SEC_5_CONSUMO_DATOS_PUNTOS = [
    {
        "subtitulo": "Descripción del Método de Consumo de Datos",
        "contenido": (
            "El consumo de información en MedReminder AI sigue un modelo desacoplado basado en una Arquitectura Orientada a "
            "Servicios (SOA) mediante APIs RESTful sin estado (stateless) sobre protocolo seguro HTTPS. La aplicación móvil Android "
            "nunca se conecta de forma directa a los motores de base de datos (ni a MySQL ni a MongoDB); en su lugar, todo el "
            "intercambio de información se realiza a través de contratos de interfaz en formato JSON estandarizado expuestos por el backend "
            "FastAPI.\n\n"
            "Este enfoque aporta tres ventajas fundamentales:\n"
            "1. Seguridad Total: Las credenciales de base de datos nunca viajan al dispositivo del usuario, impidiendo que ingeniería "
            "inversa sobre el archivo APK comprometa la infraestructura.\n"
            "2. Optimización de Red: El backend actúa como filtro y agregador, entregando únicamente los campos exactos requeridos "
            "por las pantallas móviles, reduciendo el consumo de datos celulares en los planes de los adultos mayores.\n"
            "3. Abstracción y Evolución Independiente: La estructura de tablas o colecciones puede evolucionar o migrar sin romper "
            "las versiones instaladas de la aplicación móvil."
        )
    },
    {
        "subtitulo": "Desarrolla Servicios Web para Intercambiar Información (Catálogo de Endpoints REST)",
        "contenido": (
            "El backend de MedReminder AI implementa un catálogo robusto de servicios web documentados interactivamente con Swagger/OpenAPI. "
            "A continuación se detallan los servicios principales utilizados para el consumo y sincronización de datos:"
        )
    }
]

ENDPOINTS_REST_DATA = [
    ["POST", "/api/v1/auth/login", "Público", "Recibe correo y contraseña; valida credenciales en MySQL y devuelve un token de acceso JWT Bearer con tiempo de expiración."],
    ["GET", "/api/v1/medicamentos", "Bearer Token", "Devuelve el listado completo de medicamentos activos en el botiquín del paciente autenticado, incluyendo stock disponible y criticidad."],
    ["POST", "/api/v1/medicamentos", "Bearer Token", "Registra un nuevo fármaco en el botiquín, validando contraindicaciones con Pydantic y sembrando el inventario inicial."],
    ["GET", "/api/v1/recordatorios/hoy", "Bearer Token", "Obtiene la agenda cronológica de tomas programadas para la fecha actual, indicando dosis, color de pastilla y estado actual."],
    ["POST", "/api/v1/recordatorios/{id}/accion", "Bearer Token", "Registra la acción del usuario ('tomado', 'pospuesto', 'omitido'). Decrementa stock en MySQL y despacha evento asíncrono a MongoDB."],
    ["GET", "/api/v1/alertas/cuidador", "Bearer Token", "Permite al panel del familiar consultar incidentes no atendidos (omisiones o posposiciones de medicamentos críticos)."],
    ["POST", "/api/v1/ia/escanear-receta", "Bearer Token", "Envía una imagen de receta médica a la IA local Ollama (`medi-clinico`), recibiendo de vuelta los datos estructurados en JSON."],
    ["GET", "/health", "Público", "Endpoint de monitoreo que ejecuta `ping` sobre MySQL y MongoDB, confirmando la operatividad de los enlaces en la nube."]
]

SEC_5_PROTECCION_DATOS = (
    "Reconoce la Importancia de Proteger la Información Almacenada en Servicios de Nube:\n\n"
    "Los datos gestionados en MedReminder AI no son simples registros de texto; representan la salud, la privacidad biológica y "
    "la vida misma de seres humanos vulnerables. La pérdida de confidencialidad en un registro médico puede generar discriminación "
    "laboral o aseguradora; peor aún, una alteración maliciosa en la dosis, frecuencia o criticidad de un fármaco dentro de la base de datos "
    "podría inducir una sobredosis letal o la suspensión inadvertida de un tratamiento cardiovascular de rescate.\n\n"
    "Por estos motivos, el proyecto reconoce que la seguridad no es un módulo optativo, sino un deber ético y legal de primer orden. "
    "La adhesión a la legislación mexicana (Ley Federal de Protección de Datos Personales en Posesión de los Particulares - LFPDPPP, "
    "y la NOM-024-SSA3-2012 para Sistemas de Información de Registro Electrónico para la Salud) nos exige salvaguardar el secreto profesional "
    "digital mediante autenticación multifactor, cifrado en reposo y en tránsito, y trazabilidad total mediante bitácoras inmutables."
)

SEC_5_CONSUMO_ANDROID = (
    "Describe el Consumo de Datos Mediante Servicios Web en la Aplicación Móvil Android:\n\n"
    "En el cliente móvil nativo Android, el consumo de los servicios web se implementa siguiendo las mejores prácticas de la "
    "arquitectura recomendada por Google (Clean Architecture + MVVM):\n\n"
    "1. Capa de Red con Retrofit 2 y OkHttp 3: Se define una interfaz en Kotlin con anotaciones (`@GET`, `@POST`, `@Body`, `@Path`) "
    "que modela los endpoints del backend. Un cliente `OkHttp` centralizado gestiona el pool de sockets y añade automáticamente "
    "un `Interceptor` de autenticación que adjunta el encabezado `Authorization: Bearer <TOKEN>` a cada solicitud saliente.\n\n"
    "2. Deserialización Tipada con Gson / Kotlinx Serialization: Las respuestas JSON provenientes de la nube se convierten de forma "
    "estricta en objetos de datos inmutables de Kotlin (`data class`), garantizando seguridad de tipos en tiempo de compilación y evitando "
    "errores de puntero nulo (`NullPointerException`).\n\n"
    "3. Concurrencia Asíncrona con Corrutinas de Kotlin: Todas las llamadas de red se ejecutan fuera del hilo principal de interfaz (UI Thread), "
    "empleando el despachador `Dispatchers.IO`. Esto garantiza que la interfaz de usuario de Jetpack Compose permanezca fluida a 60-120 cuadros por segundo, "
    "sin congelamientos molestos para el adulto mayor.\n\n"
    "4. Flujo Reactivo Unidireccional con StateFlow y ViewModel: El repositorio de datos procesa la respuesta del servicio web y "
    "actualiza un flujo de estado reactivo (`StateFlow<UiState>`). El ViewModel expone este estado a las funciones `@Composable` de "
    "Jetpack Compose, las cuales se recomponen instantáneamente para mostrar la agenda de medicamentos o notificar el éxito de la toma."
)

print("Módulo de datos cargado exitosamente.")
