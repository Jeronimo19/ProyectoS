from app.database import db

# Documento de prueba
usuario_prueba = {
    "nombre": "Admin Test",
    "correo": "admin@test.com",
    "rol": "Administrador"
}

resultado = db["usuarios"].insert_one(usuario_prueba)

print("Documento insertado con ID:", resultado.inserted_id)

