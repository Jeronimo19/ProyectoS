from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.security import OAuth2PasswordRequestForm
from app.database import db
from app.utils.auth import verify_password, create_access_token

router = APIRouter()

@router.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    # Buscar usuario por nombre de usuario
    usuario = db["usuarios"].find_one({"username": form_data.username})
    if not usuario:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Usuario no encontrado")

    # Verificar contraseña
    if not verify_password(form_data.password, usuario["password"]):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Contraseña incorrecta")

    # Generar token JWT
    token = create_access_token({"sub": usuario["username"]})
    return {"access_token": token, "token_type": "bearer"}
