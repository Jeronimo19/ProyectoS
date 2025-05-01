from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.security import OAuth2PasswordRequestForm
from app.database import db
from app.utils.auth import verify_password, create_access_token
from datetime import timedelta

auth_router = APIRouter()

@auth_router.post("/login")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = await db["users"].find_one({"email": form_data.username})
    if not user:
        raise HTTPException(status_code=401, detail="Credenciales inválidas")

    if not verify_password(form_data.password, user["password"]):
        raise HTTPException(status_code=401, detail="Credenciales inválidas")

    token_data = {"sub": str(user["_id"]), "email": user["email"]}
    access_token = create_access_token(
        data=token_data, expires_delta=timedelta(minutes=60)
    )

    return {"access_token": access_token, "token_type": "bearer"}
