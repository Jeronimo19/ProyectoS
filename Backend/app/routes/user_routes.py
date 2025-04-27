from fastapi import APIRouter
from app.database import db

router = APIRouter()

@router.get("/usuarios")
def obtener_usuarios():
    usuarios = list(db.usuarios.find({}, {"_id": 0}))
    return usuarios
