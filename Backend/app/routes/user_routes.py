from fastapi import APIRouter
from app.schemas.user_schema import UserSchema  # Esquema para validar
from app.database import db  # Conexión a MongoDB
from bson import ObjectId  # para convertir _id a string
from fastapi import HTTPException
from bson import ObjectId
from bson.errors import InvalidId
from app.utils.auth import hash_password
from app.utils.auth import verify_password
from pydantic import BaseModel
from app.utils.auth import create_access_token
from datetime import timedelta
from app.utils.auth import get_current_user
from fastapi import Depends

router = APIRouter()

@router.post("/usuarios")
def crear_usuario(usuario: UserSchema):
    usuario_dict = usuario.dict()  # Convertimos el schema en diccionario
    usuario_dict["password"] = hash_password(usuario_dict["password"])  # Hasheamos la contraseña

    resultado = db["usuarios"].insert_one(usuario_dict)  # Insertamos en MongoDB
    return {"mensaje": "Usuario creado", "id": str(resultado.inserted_id)}

@router.get("/usuarios")
def obtener_usuarios():
    usuarios = []
    for usuario in db["usuarios"].find():
        usuario["_id"] = str(usuario["_id"])  # Convertir ObjectId a string
        usuarios.append(usuario)
    return usuarios

@router.get("/usuarios/{id}")
def obtener_usuario_por_id(id: str):
    try:
        usuario = db["usuarios"].find_one({"_id": ObjectId(id)})
    except InvalidId:
        raise HTTPException(status_code=400, detail="ID inválido")

    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    usuario["_id"] = str(usuario["_id"])
    return usuario

@router.put("/usuarios/{id}")
def actualizar_usuario(id: str, datos_actualizados: UserSchema):
    try:
        filtro = {"_id": ObjectId(id)}
    except InvalidId:
        raise HTTPException(status_code=400, detail="ID inválido")

    nuevos_valores = {"$set": datos_actualizados.dict()}

    resultado = db["usuarios"].update_one(filtro, nuevos_valores)

    if resultado.matched_count == 0:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    return {"mensaje": "Usuario actualizado correctamente"}

@router.delete("/usuarios/{id}")
def eliminar_usuario(id: str):
    try:
        filtro = {"_id": ObjectId(id)}
    except InvalidId:
        raise HTTPException(status_code=400, detail="ID inválido")

    resultado = db["usuarios"].delete_one(filtro)

    if resultado.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    return {"mensaje": "Usuario eliminado correctamente"}


class LoginSchema(BaseModel):
    email: str
    password: str

@router.post("/login")
def login(datos: LoginSchema):
    usuario = db["usuarios"].find_one({"email": datos.email})

    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    if not verify_password(datos.password, usuario["password"]):
        raise HTTPException(status_code=401, detail="Contraseña incorrecta")

    # Crear token JWT
    token = create_access_token(
        data={"sub": str(usuario["_id"])},
        expires_delta=timedelta(minutes=30)
    )

    return {"access_token": token, "token_type": "bearer"}

@router.get("/perfil")
def perfil_usuario(usuario=Depends(get_current_user)):
    return {"mensaje": "Bienvenido", "usuario_id": usuario["sub"]}