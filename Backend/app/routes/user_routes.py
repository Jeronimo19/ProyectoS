from fastapi import APIRouter, HTTPException, Depends
from app.schemas.user_schema import UserSchema
from app.database import db
from bson import ObjectId
from bson.errors import InvalidId
from app.utils.auth import (
    hash_password,
    verify_password,
    create_access_token,
    get_current_user
)
from pydantic import BaseModel
from datetime import timedelta

router = APIRouter()

# Crear usuario
@router.post("/usuarios")
def crear_usuario(usuario: UserSchema):
    usuario_dict = usuario.dict()

    # Verificar si el usuario ya existe por email
    if db["usuarios"].find_one({"email": usuario_dict["email"]}):
        raise HTTPException(status_code=400, detail="El usuario ya existe")

    # Hashear contraseña antes de guardar
    usuario_dict["password"] = hash_password(usuario_dict["password"])

    resultado = db["usuarios"].insert_one(usuario_dict)
    return {"mensaje": "Usuario creado", "id": str(resultado.inserted_id)}

# Obtener todos los usuarios
@router.get("/usuarios")
def obtener_usuarios():
    usuarios = []
    for usuario in db["usuarios"].find():
        usuario["_id"] = str(usuario["_id"])
        usuario.pop("password", None)  # Ocultar contraseña
        usuarios.append(usuario)
    return usuarios

# Obtener usuario por ID
@router.get("/usuarios/{id}")
def obtener_usuario_por_id(id: str):
    try:
        usuario = db["usuarios"].find_one({"_id": ObjectId(id)})
    except InvalidId:
        raise HTTPException(status_code=400, detail="ID inválido")

    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    usuario["_id"] = str(usuario["_id"])
    usuario.pop("password", None)
    return usuario

# Actualizar usuario
@router.put("/usuarios/{id}")
def actualizar_usuario(id: str, datos_actualizados: UserSchema):
    try:
        filtro = {"_id": ObjectId(id)}
    except InvalidId:
        raise HTTPException(status_code=400, detail="ID inválido")

    nuevos_datos = datos_actualizados.dict()
    nuevos_datos["password"] = hash_password(nuevos_datos["password"])  # Rehashear contraseña

    nuevos_valores = {"$set": nuevos_datos}

    resultado = db["usuarios"].update_one(filtro, nuevos_valores)

    if resultado.matched_count == 0:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    return {"mensaje": "Usuario actualizado correctamente"}

# Eliminar usuario
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


# Esquema para login
class LoginSchema(BaseModel):
    email: str
    password: str

# Login y generación de token
@router.post("/login")
def login(datos: LoginSchema):
    usuario = db["usuarios"].find_one({"email": datos.email})

    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    if not verify_password(datos.password, usuario["password"]):
        raise HTTPException(status_code=401, detail="Contraseña incorrecta")

    token = create_access_token(
        data={"sub": str(usuario["_id"])},
        expires_delta=timedelta(minutes=30)
    )

    return {"access_token": token, "token_type": "bearer"}

# Perfil autenticado
@router.get("/perfil")
def perfil_usuario(usuario=Depends(get_current_user)):
    return {"mensaje": "Bienvenido", "usuario_id": usuario["sub"]}
