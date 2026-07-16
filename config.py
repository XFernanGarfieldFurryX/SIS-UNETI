"""
=========================================================
SIS-UNETI
config.py
Configuración General del Sistema
=========================================================
"""
import os

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "SIS_UNETI_2026_SECRET_KEY")
    DEBUG = False

    # MySQL Railway
    MYSQL_HOST = os.getenv("MYSQL_PUBLIC_HOST", "zephyr.proxy.rlwy.net")
    MYSQL_PORT = int(os.getenv("MYSQL_PUBLIC_PORT", "13458"))
    MYSQL_USER = os.getenv("MYSQLUSER", "root")
    MYSQL_PASSWORD = os.getenv("MYSQLPASSWORD", "BjmwBzrHHRhbddiUzaZFwUNFAxQEUdNO")
    MYSQL_DB = os.getenv("MYSQLDATABASE", "railway")
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
