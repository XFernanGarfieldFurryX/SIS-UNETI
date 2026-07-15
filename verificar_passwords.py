"""
=========================================================
SIS-UNETI
verificar_passwords.py

Verificación de contraseñas cifradas
=========================================================
"""

from werkzeug.security import check_password_hash


usuarios = {

    "admin": {
        "password_real": "admin123",
        "hash": "scrypt:32768:8:1$Subw0fMpFwriCtbw$f0bf39c5878251d608811463bf86fa3b587c36623234a576214e2d94e95835f34294bc33c7db0ae6841cc00fd3bb87328f59a1977ce6c80c3d5f278f339976e1"
    },


    "docente": {
        "password_real": "docente123",
        "hash": "scrypt:32768:8:1$qT1DHX2iEVrRiQQA$4601460d5c3c40703208ea6d971c1116fc8739654cd9a8d7c43e6df52c45b7432a8421ae4cdcad0df8e73619f808ecf8f1964645fd0d711d9d62c9c5d716fb57"
    },


    "estudiante": {
        "password_real": "estudiante123",
        "hash": "scrypt:32768:8:1$LT68LzYE47CHuy9h$d512f5ccf866b89e83f73f456c016c673f2d492047a20923ce160bee2be814fd98840403cf5a0e99b3734eee7cbd426715be1c2f3d2cf76cb8e11f539cea635a"
    },


    "Fernando Do Couto": {
        "password_real": "estudiante123*",
        "hash": "scrypt:32768:8:1$6lmfpyCFaSgKVcVP$58a5f899027f096f896bce4cb1ea92b9975ca41179b8a25028f6edb5b8367a4508eba0dedde1baa971ace5fee364ac89dd3ce831de73bb2b51d7f734a642a7f4"
    },


    "Omar Rivero": {
        "password_real": "docente 123*",
        "hash": "scrypt:32768:8:1$c9mjyRjwCuojqJVI$15d337f0fbdf0ee52e21a1c6333f11a98961ba60b0591604221b9fd0e960dd73ada6ebcdf44da25381807bfb2f8a567149e622938f15e8eeb77f6f5e7c02ae92"
    }

}


for usuario, datos in usuarios.items():

    resultado = check_password_hash(
        datos["hash"],
        datos["password_real"]
    )


    if resultado:

        print("✅ Contraseña correcta:", usuario)

    else:

        print("❌ Error de contraseña:", usuario)
