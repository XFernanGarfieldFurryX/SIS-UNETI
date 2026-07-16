-- ==========================================
-- SIS-UNETI - ESQUEMA DE BASE DE DATOS
-- ==========================================

-- Tabla: usuarios
CREATE TABLE IF NOT EXISTS usuarios (
    id_usuario INT AUTO_INCREMENT PRIMARY KEY,
    usuario VARCHAR(50) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    rol ENUM('administrador', 'docente', 'estudiante') NOT NULL,
    email VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabla: docentes
CREATE TABLE IF NOT EXISTS docentes (
    id_docente INT AUTO_INCREMENT PRIMARY KEY,
    id_usuario INT NOT NULL,
    nombres VARCHAR(100) NOT NULL,
    apellidos VARCHAR(100) NOT NULL,
    cedula VARCHAR(20) UNIQUE NOT NULL,
    especialidad VARCHAR(100),
    telefono VARCHAR(20),
    email VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (id_usuario) REFERENCES usuarios(id_usuario) ON DELETE CASCADE
);

-- Tabla: estudiantes
CREATE TABLE IF NOT EXISTS estudiantes (
    id_estudiante INT AUTO_INCREMENT PRIMARY KEY,
    id_usuario INT NOT NULL,
    nombres VARCHAR(100) NOT NULL,
    apellidos VARCHAR(100) NOT NULL,
    cedula VARCHAR(20) UNIQUE NOT NULL,
    carrera VARCHAR(100) NOT NULL,
    semestre INT,
    telefono VARCHAR(20),
    email VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (id_usuario) REFERENCES usuarios(id_usuario) ON DELETE CASCADE
);

-- Tabla: solicitudes
CREATE TABLE IF NOT EXISTS solicitudes (
    id_solicitud INT AUTO_INCREMENT PRIMARY KEY,
    id_usuario INT NOT NULL,
    fecha DATE NOT NULL,
    tipo_solicitud VARCHAR(100) NOT NULL,
    descripcion TEXT,
    estado ENUM('Pendiente', 'Aprobada', 'Rechazada') DEFAULT 'Pendiente',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (id_usuario) REFERENCES usuarios(id_usuario) ON DELETE CASCADE
);

-- Tabla: beneficios
CREATE TABLE IF NOT EXISTS beneficios (
    id_beneficio INT AUTO_INCREMENT PRIMARY KEY,
    id_estudiante INT NOT NULL,
    nombre_beneficio VARCHAR(200) NOT NULL,
    descripcion TEXT,
    fecha_solicitud DATE NOT NULL,
    estado ENUM('Activo', 'Inactivo', 'Pendiente') DEFAULT 'Pendiente',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (id_estudiante) REFERENCES estudiantes(id_estudiante) ON DELETE CASCADE
);

-- Tabla: reportes
CREATE TABLE IF NOT EXISTS reportes (
    id_reporte INT AUTO_INCREMENT PRIMARY KEY,
    titulo VARCHAR(200) NOT NULL,
    descripcion TEXT,
    tipo VARCHAR(100) NOT NULL,
    fecha_generacion DATE NOT NULL,
    generado_por INT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (generado_por) REFERENCES usuarios(id_usuario) ON DELETE CASCADE
);

-- Tabla: evaluaciones
CREATE TABLE IF NOT EXISTS evaluaciones (
    id_evaluacion INT AUTO_INCREMENT PRIMARY KEY,
    id_estudiante INT NOT NULL,
    asignatura VARCHAR(100) NOT NULL,
    nota DECIMAL(5,2),
    periodo VARCHAR(20) NOT NULL,
    observacion TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (id_estudiante) REFERENCES estudiantes(id_estudiante) ON DELETE CASCADE
);

-- Tabla: observaciones
CREATE TABLE IF NOT EXISTS observaciones (
    id_observacion INT AUTO_INCREMENT PRIMARY KEY,
    id_usuario INT NOT NULL,
    tipo VARCHAR(100) NOT NULL,
    descripcion TEXT,
    fecha DATETIME NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (id_usuario) REFERENCES usuarios(id_usuario) ON DELETE CASCADE
);

-- Tabla: auditoria
CREATE TABLE IF NOT EXISTS auditoria (
    id_auditoria INT AUTO_INCREMENT PRIMARY KEY,
    id_usuario INT NOT NULL,
    usuario VARCHAR(50) NOT NULL,
    rol ENUM('administrador', 'docente', 'estudiante') NOT NULL,
    accion VARCHAR(255) NOT NULL,
    modulo VARCHAR(100) NOT NULL,
    fecha DATETIME NOT NULL,
    ip VARCHAR(45) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (id_usuario) REFERENCES usuarios(id_usuario) ON DELETE CASCADE
);

-- Tabla: detalle_auditoria
CREATE TABLE IF NOT EXISTS detalle_auditoria (
    id_detalle INT AUTO_INCREMENT PRIMARY KEY,
    id_auditoria INT NOT NULL,
    campo VARCHAR(100) NOT NULL,
    valor_anterior TEXT,
    valor_nuevo TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (id_auditoria) REFERENCES auditoria(id_auditoria) ON DELETE CASCADE
);

-- Tabla: reset_codigos
CREATE TABLE IF NOT EXISTS reset_codigos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    id_usuario INT NOT NULL,
    codigo VARCHAR(6) NOT NULL,
    fecha_expiracion DATETIME NOT NULL,
    usado BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (id_usuario) REFERENCES usuarios(id_usuario) ON DELETE CASCADE
);
