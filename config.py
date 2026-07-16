import os

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "SIS_UNETI_2026_SECRET_KEY")
    DEBUG = False

    MYSQL_HOST = os.getenv("MYSQL_PUBLIC_HOST", "zephyr.proxy.rlwy.net")
    MYSQL_PORT = int(os.getenv("MYSQL_PUBLIC_PORT", "13458"))
    MYSQL_USER = os.getenv("MYSQLUSER", "root")
    MYSQL_PASSWORD = os.getenv("MYSQLPASSWORD", "BjmwBzrHHRhbddiUzaZFwUNFAxQEUdNO")
    MYSQL_DB = os.getenv("MYSQLDATABASE", "railway")
    MYSQL_CHARSET = "utf8mb4"

    SESSION_PERMANENT = True
    SESSION_TYPE = "filesystem"
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = "Lax"
    SESSION_COOKIE_SECURE = True

    UPLOAD_FOLDER = "static/uploads"
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024
    ALLOWED_EXTENSIONS = {"pdf", "jpg", "jpeg", "png", "doc", "docx"}

    APP_NAME = "SIS-UNETI"
    APP_VERSION = "1.0"
    UNIVERSIDAD = "Universidad Nacional Experimental de las Telecomunicaciones e Informática"
    PAIS = "Venezuela"
    CIUDAD = "Caracas"
    ZONA_HORARIA = "America/Caracas"
