-- =========================================================
-- SIS-UNETI
-- Base de Datos MySQL
-- Versión Inicial
-- =========================================================

CREATE DATABASE IF NOT EXISTS sis_uneti
CHARACTER SET utf8mb4
COLLATE utf8mb4_unicode_ci;

USE sis_uneti;
 

-- =========================================================
-- TABLA USUARIOS
-- =========================================================

CREATE TABLE IF NOT EXISTS usuarios (

    id_usuario INT AUTO_INCREMENT PRIMARY KEY,

    usuario VARCHAR(50) NOT NULL UNIQUE,

    password VARCHAR(100) NOT NULL,

    rol ENUM(
        'administrador',
        'docente',
        'estudiante'
    ) NOT NULL

);


-- =========================================================
-- USUARIOS INICIALES
-- =========================================================

INSERT INTO usuarios
(
usuario,
password,
rol
)

VALUES

(
'admin',
'admin123',
'administrador'
),

(
'docente',
'docente123',
'docente'
),

(
'estudiante',
'estudiante123',
'estudiante'
);



-- =========================================================
-- TABLA SOLICITUDES
-- =========================================================

CREATE TABLE IF NOT EXISTS solicitudes (

    id_solicitud INT AUTO_INCREMENT PRIMARY KEY,

    fecha DATE NOT NULL,

    tipo_solicitud VARCHAR(100) NOT NULL,

    descripcion TEXT NOT NULL,

    estado ENUM(
        'Pendiente',
        'Aprobada',
        'Rechazada'
    )
    DEFAULT 'Pendiente'

);



-- =========================================================
-- DATOS DE PRUEBA
-- =========================================================

INSERT INTO solicitudes
(
fecha,
tipo_solicitud,
tipo_solicitud,
descripcion,
estado
)

VALUES
(
'2026-07-06',
'Constancia de estudio',
'Solicitud inicial del sistema SIS-UNETI',
'Pendiente'
);


-- =========================================================
-- FIN BASE DE DATOS SIS-UNETI
-- =========================================================
