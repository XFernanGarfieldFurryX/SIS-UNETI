"""
=========================================================
SIS-UNETI
config.py
Configuración General del Sistema
=========================================================
"""

import os


class Config:
    """
    Configuración principal del proyecto SIS-UNETI
    """

    # =====================================================
    # FLASK
    # =====================================================

    SECRET_KEY = os.environ.get(
        "SECRET_KEY",
        "SIS_UNETI_2026_SECRET_KEY"
    )

    DEBUG = True


    # =====================================================
    # MYSQL
    # =====================================================

    MYSQL_HOST = "localhost"

    MYSQL_PORT = 3306

    MYSQL_USER = "root"

    MYSQL_PASSWORD = ""

    MYSQL_DB = "sis_uneti"

    MYSQL_CHARSET = "utf8mb4"


    # =====================================================
    # SESIONES
    # =====================================================

    SESSION_PERMANENT = False

    SESSION_TYPE = "filesystem"


    # =====================================================
    # SUBIDA DE ARCHIVOS
    # =====================================================

    UPLOAD_FOLDER = "static/uploads"

    MAX_CONTENT_LENGTH = 16 * 1024 * 1024


    # =====================================================
    # EXTENSIONES PERMITIDAS
    # =====================================================

    ALLOWED_EXTENSIONS = {
        "pdf",
        "jpg",
        "jpeg",
        "png",
        "doc",
        "docx"
    }


    # =====================================================
    # NOMBRE DEL SISTEMA
    # =====================================================

    APP_NAME = "SIS-UNETI"

    APP_VERSION = "1.0"


    # =====================================================
    # UNIVERSIDAD
    # =====================================================

    UNIVERSIDAD = (
        "Universidad Nacional Experimental "
        "de las Telecomunicaciones e Informática"
    )


    # =====================================================
    # PAÍS
    # =====================================================

    PAIS = "Venezuela"

    CIUDAD = "Caracas"

    ZONA_HORARIA = "America/Caracas"
