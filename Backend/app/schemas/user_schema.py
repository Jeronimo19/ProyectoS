from pydantic import BaseModel

class UserSchema(BaseModel):
    nombre: str
    correo: str
    contrasena: str
