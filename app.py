from flask import Flask, render_template, request, redirect, session, send_file, url_for, flash
import io
from datetime import datetime
import pymysql
from werkzeug.security import check_password_hash, generate_password_hash
from functools import wraps
from config import Config
from zoneinfo import ZoneInfo
import secrets
from datetime import timedelta
import os
from werkzeug.utils import secure_filename
import random

# ==========================================
# REPORTLAB PARA PDF
# ==========================================
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors

# ==========================================
# FLASK-MAIL PARA CORREOS
# ==========================================
from flask_mail import Mail, Message

# ==========================================
# DOTENV PARA VARIABLES DE ENTORNO
# ==========================================
from dotenv import load_dotenv
load_dotenv()

# ==========================
# APP
# ==========================
app = Flask(__name__)
app.config.from_object(Config)
app.secret_key = app.config["SECRET_KEY"]

print("🔍 CONFIGURACIÓN DE BASE DE DATOS:")
print(f"  HOST: {app.config['MYSQL_HOST']}")
print(f"  PORT: {app.config['MYSQL_PORT']}")
print(f"  USER: {app.config['MYSQL_USER']}")
print(f"  DB: {app.config['MYSQL_DB']}")

# ==========================
# SEGURIDAD DE SESIONES
# ==========================
app.config["PERMANENT_SESSION_LIFETIME"] = timedelta(minutes=30)
app.config["SESSION_COOKIE_HTTPONLY"] = True
app.config["SESSION_COOKIE_SAMESITE"] = "Lax"
app.config["SESSION_COOKIE_SECURE"] = True

# ==========================
# CONFIGURACIÓN DE CORREO
# ==========================
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
app.config['MAIL_USERNAME'] = 'docoutofernandodaniel@gmail.com'
app.config['MAIL_PASSWORD'] = 'xcxk gyhd aupy niwx'  
app.config['MAIL_DEFAULT_SENDER'] = 'docoutofernandodaniel@gmail.com'

# ==========================
# INICIALIZAR FLASK-MAIL
# ==========================
mail = Mail(app)

# ==========================
# CONFIGURACIÓN DE SUBIDA DE ARCHIVOS
# ==========================
UPLOAD_FOLDER = os.path.join('static', 'uploads')
ALLOWED_EXTENSIONS = {'pdf', 'png', 'jpg', 'jpeg', 'doc', 'docx'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# ==========================
# CONEXIÓN MYSQL
# ==========================
def obtener_conexion():
    try:
        conexion = pymysql.connect(
            host=app.config["MYSQL_HOST"],
            port=app.config["MYSQL_PORT"],
            user=app.config["MYSQL_USER"],
            password=app.config["MYSQL_PASSWORD"],
            database=app.config["MYSQL_DB"],
            charset=app.config["MYSQL_CHARSET"],
            cursorclass=pymysql.cursors.DictCursor,
            connect_timeout=10
        )
        conexion.ping(reconnect=True)
        print("✅ MYSQL RAILWAY CONECTADO")
        return conexion
    except Exception as error:
        print("❌ ERROR MYSQL:", error)
        return None

# ==========================
# FECHA Y HORA VENEZUELA
# ==========================
def obtener_fecha_venezuela():
    return datetime.now(ZoneInfo("America/Caracas"))

# ==========================================
# AUDITORÍA
# ==========================================
def registrar_auditoria(accion, modulo):
    if "id_usuario" not in session:
        return None
    conexion = obtener_conexion()
    if conexion is None:
        return None
    cursor = conexion.cursor()
    ip = request.remote_addr if request else "0.0.0.0"
    try:
        cursor.execute("""
            INSERT INTO auditoria (id_usuario, usuario, rol, accion, modulo, fecha, ip)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, (
            session.get("id_usuario"),
            session.get("usuario"),
            session.get("rol"),
            accion,
            modulo,
            obtener_fecha_venezuela(),
            ip
        ))
        conexion.commit()
        return cursor.lastrowid
    except Exception as e:
        print(f"❌ Error al registrar auditoría: {e}")
        return None
    finally:
        cursor.close()
        conexion.close()

def registrar_detalle_auditoria(id_auditoria, campo, valor_anterior, valor_nuevo):
    if not id_auditoria:
        return
    conexion = obtener_conexion()
    if conexion is None:
        return
    cursor = conexion.cursor()
    try:
        cursor.execute("""
            INSERT INTO detalle_auditoria (id_auditoria, campo, valor_anterior, valor_nuevo)
            VALUES (%s, %s, %s, %s)
        """, (id_auditoria, campo, valor_anterior, valor_nuevo))
        conexion.commit()
    except Exception as e:
        print(f"❌ Error al registrar detalle: {e}")
    finally:
        cursor.close()
        conexion.close()

# ==========================================
# CORREOS
# ==========================================
def enviar_correo(destinatario, asunto, mensaje_html):
    try:
        msg = Message(subject=asunto, recipients=[destinatario], html=mensaje_html)
        mail.send(msg)
        print(f"✅ Correo enviado a {destinatario}")
        return True
    except Exception as e:
        print(f"❌ Error al enviar correo: {e}")
        return False

# ==========================
# DECORADORES
# ==========================
def login_requerido(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if "usuario" not in session:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated

def rol_requerido(*roles):
    def decorador(f):
        @wraps(f)
        def protegida(*args, **kwargs):
            if "rol" not in session:
                return redirect("/login")
            if session["rol"] not in roles:
                return "⛔ Acceso no autorizado.", 403
            return f(*args, **kwargs)
        return protegida
    return decorador

# ============================================
# FUNCIONES DE INICIALIZACIÓN
# ============================================
def crear_tablas():
    conexion = obtener_conexion()
    if conexion is None:
        print("❌ No se pudo conectar para crear tablas")
        return
    cursor = conexion.cursor()
    sql = """
    CREATE TABLE IF NOT EXISTS usuarios (
        id_usuario INT AUTO_INCREMENT PRIMARY KEY,
        usuario VARCHAR(50) UNIQUE NOT NULL,
        password VARCHAR(255) NOT NULL,
        rol ENUM('administrador','docente','estudiante') NOT NULL,
        email VARCHAR(100),
        fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    CREATE TABLE IF NOT EXISTS estudiantes (
        id_estudiante INT AUTO_INCREMENT PRIMARY KEY,
        id_usuario INT NOT NULL,
        cedula VARCHAR(20) UNIQUE NOT NULL,
        nombres VARCHAR(100) NOT NULL,
        apellidos VARCHAR(100) NOT NULL,
        carrera VARCHAR(100),
        semestre INT,
        FOREIGN KEY (id_usuario) REFERENCES usuarios(id_usuario) ON DELETE CASCADE
    );
    CREATE TABLE IF NOT EXISTS docentes (
        id_docente INT AUTO_INCREMENT PRIMARY KEY,
        id_usuario INT NOT NULL,
        cedula VARCHAR(20) UNIQUE NOT NULL,
        nombres VARCHAR(100) NOT NULL,
        apellidos VARCHAR(100) NOT NULL,
        departamento VARCHAR(100),
        FOREIGN KEY (id_usuario) REFERENCES usuarios(id_usuario) ON DELETE CASCADE
    );
    CREATE TABLE IF NOT EXISTS solicitudes (
        id_solicitud INT AUTO_INCREMENT PRIMARY KEY,
        id_usuario INT NOT NULL,
        fecha DATE NOT NULL,
        tipo_solicitud VARCHAR(100) NOT NULL,
        descripcion TEXT,
        estado ENUM('Pendiente','Aprobada','Rechazada') DEFAULT 'Pendiente',
        fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (id_usuario) REFERENCES usuarios(id_usuario) ON DELETE CASCADE
    );
    CREATE TABLE IF NOT EXISTS beneficios (
        id_beneficio INT AUTO_INCREMENT PRIMARY KEY,
        id_estudiante INT NOT NULL,
        nombre_beneficio VARCHAR(100) NOT NULL,
        descripcion TEXT,
        fecha_solicitud DATE NOT NULL,
        estado ENUM('Pendiente','Aprobado','Rechazado') DEFAULT 'Pendiente',
        FOREIGN KEY (id_estudiante) REFERENCES estudiantes(id_estudiante) ON DELETE CASCADE
    );
    CREATE TABLE IF NOT EXISTS evaluaciones (
        id_evaluacion INT AUTO_INCREMENT PRIMARY KEY,
        id_estudiante INT NOT NULL,
        asignatura VARCHAR(100) NOT NULL,
        nota DECIMAL(5,2),
        periodo VARCHAR(20),
        observacion TEXT,
        FOREIGN KEY (id_estudiante) REFERENCES estudiantes(id_estudiante) ON DELETE CASCADE
    );
    CREATE TABLE IF NOT EXISTS reportes (
        id_reporte INT AUTO_INCREMENT PRIMARY KEY,
        titulo VARCHAR(200) NOT NULL,
        descripcion TEXT,
        tipo VARCHAR(50),
        fecha_generacion DATE NOT NULL,
        generado_por INT NOT NULL,
        FOREIGN KEY (generado_por) REFERENCES usuarios(id_usuario) ON DELETE CASCADE
    );
    CREATE TABLE IF NOT EXISTS observaciones (
        id_observacion INT AUTO_INCREMENT PRIMARY KEY,
        id_usuario INT NOT NULL,
        tipo VARCHAR(50),
        descripcion TEXT,
        fecha DATETIME NOT NULL,
        FOREIGN KEY (id_usuario) REFERENCES usuarios(id_usuario) ON DELETE CASCADE
    );
    CREATE TABLE IF NOT EXISTS auditoria (
        id_auditoria INT AUTO_INCREMENT PRIMARY KEY,
        id_usuario INT NOT NULL,
        usuario VARCHAR(50),
        rol VARCHAR(20),
        accion VARCHAR(100) NOT NULL,
        modulo VARCHAR(50),
        fecha DATETIME NOT NULL,
        ip VARCHAR(45),
        FOREIGN KEY (id_usuario) REFERENCES usuarios(id_usuario) ON DELETE CASCADE
    );
    CREATE TABLE IF NOT EXISTS detalle_auditoria (
        id_detalle INT AUTO_INCREMENT PRIMARY KEY,
        id_auditoria INT NOT NULL,
        campo VARCHAR(50),
        valor_anterior TEXT,
        valor_nuevo TEXT,
        FOREIGN KEY (id_auditoria) REFERENCES auditoria(id_auditoria) ON DELETE CASCADE
    );
    CREATE TABLE IF NOT EXISTS reset_codigos (
        id INT AUTO_INCREMENT PRIMARY KEY,
        id_usuario INT NOT NULL,
        codigo VARCHAR(6) NOT NULL,
        fecha_expiracion DATETIME NOT NULL,
        usado BOOLEAN DEFAULT FALSE,
        FOREIGN KEY (id_usuario) REFERENCES usuarios(id_usuario) ON DELETE CASCADE
    );
    """
    try:
        for cmd in sql.split(';'):
            if cmd.strip():
                cursor.execute(cmd)
        conexion.commit()
        print("✅ Tablas creadas exitosamente")
    except Exception as e:
        print(f"❌ Error al crear tablas: {e}")
    finally:
        cursor.close()
        conexion.close()

def inicializar_usuarios():
    conexion = obtener_conexion()
    if conexion is None:
        print("⚠️ No se pudo conectar para inicializar usuarios.")
        return
    cursor = conexion.cursor()
    try:
        # Usuario administrador
        cursor.execute("SELECT COUNT(*) AS total FROM usuarios WHERE rol = 'administrador'")
        if cursor.fetchone()["total"] == 0:
            password_hash = generate_password_hash("admin123")
            cursor.execute(
                "INSERT INTO usuarios (usuario, password, rol, email) VALUES (%s, %s, %s, %s)",
                ("admin", password_hash, "administrador", "admin@uneti.edu.ve")
            )
            print("✅ Usuario administrador creado: admin / admin123")

        # Usuario docente genérico
        cursor.execute("SELECT COUNT(*) AS total FROM usuarios WHERE usuario = 'docente'")
        if cursor.fetchone()["total"] == 0:
            password_hash = generate_password_hash("docente123")
            cursor.execute(
                "INSERT INTO usuarios (usuario, password, rol, email) VALUES (%s, %s, %s, %s)",
                ("docente", password_hash, "docente", "docente@uneti.edu.ve")
            )
            print("✅ Usuario docente genérico creado: docente / docente123")

        # Usuario estudiante genérico
        cursor.execute("SELECT COUNT(*) AS total FROM usuarios WHERE usuario = 'estudiante'")
        if cursor.fetchone()["total"] == 0:
            password_hash = generate_password_hash("estudiante123")
            cursor.execute(
                "INSERT INTO usuarios (usuario, password, rol, email) VALUES (%s, %s, %s, %s)",
                ("estudiante", password_hash, "estudiante", "estudiante@uneti.edu.ve")
            )
            print("✅ Usuario estudiante genérico creado: estudiante / estudiante123")

        # Usuario docente específico: Omar Rivero
        cursor.execute("SELECT COUNT(*) AS total FROM usuarios WHERE usuario = 'omar.rivero'")
        if cursor.fetchone()["total"] == 0:
            password_hash = generate_password_hash("docente123")
            cursor.execute(
                "INSERT INTO usuarios (usuario, password, rol, email) VALUES (%s, %s, %s, %s)",
                ("omar.rivero", password_hash, "docente", "omar.rivero@uneti.edu.ve")
            )
            id_usuario = cursor.lastrowid
            cursor.execute(
                "INSERT INTO docentes (id_usuario, cedula, nombres, apellidos, departamento) VALUES (%s, %s, %s, %s, %s)",
                (id_usuario, "12345678", "Omar", "Rivero", "Ingeniería")
            )
            print("✅ Usuario docente creado: Omar Rivero / docente123")

        # Usuario estudiante específico: Fernando Do Couto
        cursor.execute("SELECT COUNT(*) AS total FROM usuarios WHERE usuario = 'fernando.docouto'")
        if cursor.fetchone()["total"] == 0:
            password_hash = generate_password_hash("estudiante123")
            cursor.execute(
                "INSERT INTO usuarios (usuario, password, rol, email) VALUES (%s, %s, %s, %s)",
                ("fernando.docouto", password_hash, "estudiante", "fernando.docouto@uneti.edu.ve")
            )
            id_usuario = cursor.lastrowid
            cursor.execute(
                "INSERT INTO estudiantes (id_usuario, cedula, nombres, apellidos, carrera, semestre) VALUES (%s, %s, %s, %s, %s, %s)",
                (id_usuario, "87654321", "Fernando", "Do Couto", "Informática", 5)
            )
            print("✅ Usuario estudiante creado: Fernando Do Couto / estudiante123")

        conexion.commit()
    except Exception as e:
        print(f"❌ Error al crear usuarios: {e}")
    finally:
        cursor.close()
        conexion.close()

# ============================================
# RUTAS
# ============================================
@app.route("/")
def inicio():
    return render_template("inicio.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        usuario = request.form["usuario"]
        password = request.form["password"]
        conexion = obtener_conexion()
        if conexion is None:
            return render_template("login.html", error="Error de conexión con la base de datos.")
        cursor = conexion.cursor()
        cursor.execute("SELECT * FROM usuarios WHERE usuario=%s", (usuario,))
        usuario_db = cursor.fetchone()
        cursor.close()
        conexion.close()
        if usuario_db and check_password_hash(usuario_db["password"], password):
            session["id_usuario"] = usuario_db["id_usuario"]
            session["usuario"] = usuario_db["usuario"]
            session["rol"] = usuario_db["rol"]
            session.permanent = True
            registrar_auditoria("Inicio de sesión", "Login")
            if usuario_db["rol"] == "administrador":
                return redirect("/administrador")
            elif usuario_db["rol"] == "docente":
                return redirect("/docente")
            else:
                return redirect("/estudiante")
        else:
            return render_template("login.html", error="Usuario o contraseña incorrectos")
    return render_template("login.html")

@app.route("/logout")
@login_requerido
def logout():
    registrar_auditoria("Cerró sesión", "Login")
    session.clear()
    return redirect("/login")

@app.route("/administrador")
@login_requerido
@rol_requerido("administrador")
def administrador():
    return render_template("panel_administrador.html")

@app.route("/docente")
@login_requerido
@rol_requerido("docente")
def docente():
    return render_template("panel_docente.html")

@app.route("/estudiante")
@login_requerido
@rol_requerido("estudiante")
def estudiante():
    return render_template("panel_estudiante.html")

# ============================================
# ERRORES
# ============================================
@app.errorhandler(404)
def pagina_no_encontrada(error):
    return render_template("error404.html"), 404

@app.errorhandler(500)
def error_servidor(error):
    return render_template("error500.html"), 500

# ============================================
# INICIALIZACIÓN
# ============================================
with app.app_context():
    crear_tablas()
    inicializar_usuarios()

# ============================================
# INICIO
# ============================================
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
