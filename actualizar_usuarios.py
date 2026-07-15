"""
=========================================================
SIS-UNETI
actualizar_usuarios.py
Actualización de usuarios del sistema
=========================================================
"""

import pymysql
from werkzeug.security import generate_password_hash


# ==========================
# CONEXIÓN MYSQL
# ==========================

conexion = pymysql.connect(

    host="localhost",

    user="root",

    password="",

    database="sis_uneti",

    charset="utf8mb4",

    cursorclass=pymysql.cursors.DictCursor

)


cursor = conexion.cursor()


# ==========================
# USUARIOS A CREAR / ACTUALIZAR
# ==========================

usuarios = [

    {
        "usuario": "Fernando Do Couto",
        "password": "estudiante123*",
        "rol": "estudiante"
    },


    {
        "usuario": "Omar Rivero",
        "password": "docente 123*",
        "rol": "docente"
    }

]


# ==========================
# PROCESO
# ==========================

for usuario in usuarios:


    password_hash = generate_password_hash(
        usuario["password"]
    )


    cursor.execute(
        """
        SELECT *
        FROM usuarios
        WHERE usuario=%s
        """,
        (usuario["usuario"],)
    )


    existe = cursor.fetchone()



    if existe:


        cursor.execute(
            """
            UPDATE usuarios

            SET

            password=%s,
            rol=%s

            WHERE usuario=%s
            """,

            (
                password_hash,
                usuario["rol"],
                usuario["usuario"]
            )

        )


        print(
            "✅ Usuario actualizado:",
            usuario["usuario"]
        )


    else:


        cursor.execute(
            """
            INSERT INTO usuarios
            (
            usuario,
            password,
            rol
            )

            VALUES
            (%s,%s,%s)

            """,

            (
                usuario["usuario"],
                password_hash,
                usuario["rol"]
            )

        )


        print(
            "✅ Usuario creado:",
            usuario["usuario"]
        )



conexion.commit()


cursor.close()

conexion.close()


print("\n🚀 Actualización completada correctamente.")
