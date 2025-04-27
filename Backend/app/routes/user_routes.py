from fastapi import APIRouter
from app.schemas.user_schema import UserSchema  # Esquema para validar
from app.database import db  # Conexión a MongoDB

router = APIRouter()

@router.post("/usuarios")
def crear_usuario(usuario: UserSchema):
    # Insertar el usuario a la colección "usuarios"
    resultado = db["usuarios"].insert_one(usuario.dict())
    return {"mensaje": "Usuario creado", "id": str(resultado.inserted_id)}
