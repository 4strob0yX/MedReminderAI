CREATE TABLE usuario (
    id_usuario INT AUTO_INCREMENT PRIMARY KEY,
    nombre_completo VARCHAR(255) NOT NULL,
    correo VARCHAR(255) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    fecha_nacimiento DATE NULL,
    rol VARCHAR(30) NOT NULL DEFAULT 'paciente',
    fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE medicamento (
    id_medicamento INT AUTO_INCREMENT PRIMARY KEY,
    id_usuario INT NOT NULL,
    nombre VARCHAR(255) NOT NULL,
    principio_activo VARCHAR(255) NULL,
    dosis VARCHAR(100) NOT NULL,
    cantidad_stock INT NOT NULL DEFAULT 0,
    stock_inicial INT NOT NULL DEFAULT 30,
    forma_farmaceutica VARCHAR(40) NOT NULL DEFAULT 'comprimidos',
    color_pastilla VARCHAR(40) NOT NULL DEFAULT 'blanco',
    instrucciones_toma VARCHAR(255) NULL,
    proposito VARCHAR(120) NULL,
    permite_posponer BOOLEAN NOT NULL DEFAULT TRUE,
    es_critico BOOLEAN NOT NULL DEFAULT FALSE,
    contraindicaciones TEXT NULL,
    FOREIGN KEY (id_usuario) REFERENCES usuario(id_usuario) ON DELETE CASCADE
);

CREATE TABLE alergia_usuario (
    id_alergia INT AUTO_INCREMENT PRIMARY KEY,
    id_usuario INT NOT NULL,
    sustancia VARCHAR(255) NOT NULL,
    severidad ENUM('leve', 'moderada', 'grave') DEFAULT 'grave',
    reaccion VARCHAR(255) NULL,
    fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (id_usuario) REFERENCES usuario(id_usuario) ON DELETE CASCADE,
    INDEX idx_alergia_usuario (id_usuario)
);

CREATE TABLE contacto_apoyo (
    id_contacto INT AUTO_INCREMENT PRIMARY KEY,
    id_usuario INT NOT NULL,
    nombre_completo VARCHAR(255) NOT NULL,
    telefono VARCHAR(50) NOT NULL,
    parentesco VARCHAR(100) NOT NULL,
    correo VARCHAR(255) NULL,
    es_principal BOOLEAN DEFAULT TRUE,
    fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (id_usuario) REFERENCES usuario(id_usuario) ON DELETE CASCADE,
    INDEX idx_contacto_usuario (id_usuario)
);

CREATE TABLE tratamiento (
    id_tratamiento INT AUTO_INCREMENT PRIMARY KEY,
    id_medicamento INT NOT NULL,
    frecuencia_horas INT NOT NULL,
    fecha_inicio TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    fecha_fin TIMESTAMP NULL,
    estado ENUM('activo', 'inactivo') DEFAULT 'activo',
    FOREIGN KEY (id_medicamento) REFERENCES medicamento(id_medicamento) ON DELETE CASCADE
);

-- Planificacion teorica. La toma real se audita en historial_toma.
CREATE TABLE recordatorio (
    id_recordatorio INT AUTO_INCREMENT PRIMARY KEY,
    id_tratamiento INT NOT NULL,
    hora_programada TIMESTAMP NOT NULL,
    estado ENUM('pendiente', 'tomado', 'pospuesto', 'omitido') DEFAULT 'pendiente',
    veces_pospuesto TINYINT NOT NULL DEFAULT 0,
    FOREIGN KEY (id_tratamiento) REFERENCES tratamiento(id_tratamiento) ON DELETE CASCADE,
    INDEX idx_recordatorio_trat_hora (id_tratamiento, hora_programada)
);

-- Log de auditoria de acciones: NO es unico por recordatorio
-- (ej. 2 pospuestos + 1 tomado = 3 filas para el mismo id_recordatorio).
CREATE TABLE historial_toma (
    id_historial INT AUTO_INCREMENT PRIMARY KEY,
    id_recordatorio INT NOT NULL,
    fecha_accion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    estado_final ENUM('tomado', 'pospuesto', 'omitido') NOT NULL,
    notas TEXT NULL,
    FOREIGN KEY (id_recordatorio) REFERENCES recordatorio(id_recordatorio) ON DELETE CASCADE,
    INDEX idx_historial_recordatorio_fecha (id_recordatorio, fecha_accion)
);

-- Alertas persistentes enviadas al cuidador (adultos mayores / medicamentos criticos).
CREATE TABLE alerta_cuidador (
    id_alerta INT AUTO_INCREMENT PRIMARY KEY,
    id_usuario INT NOT NULL,
    tipo_alerta VARCHAR(40) NOT NULL DEFAULT 'advertencia_normal',
    accion_origen VARCHAR(40) NOT NULL DEFAULT 'posponer',
    nombre_medicamento VARCHAR(160) NOT NULL,
    dosis VARCHAR(80) NOT NULL DEFAULT '',
    es_critico BOOLEAN NOT NULL DEFAULT FALSE,
    mensaje VARCHAR(500) NOT NULL,
    nombre_cuidador VARCHAR(160) NOT NULL DEFAULT 'Cuidador Principal',
    telefono_cuidador VARCHAR(60) NOT NULL DEFAULT '',
    atendida BOOLEAN NOT NULL DEFAULT FALSE,
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (id_usuario) REFERENCES usuario(id_usuario) ON DELETE CASCADE,
    INDEX ix_alerta_cuidador_usuario (id_usuario)
);
