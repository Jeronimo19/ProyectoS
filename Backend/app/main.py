from fastapi import FastAPI
from app.routes.user_routes import router as user_router
from app.routes.inspection_routes import router as inspection_router
from routes.auth_routes import auth_router


app = FastAPI()

# Ruta base para comprobar funcionamiento
@app.get("/")
def read_root():
    return {"mensaje": "API funcionando correctamente 🚀"}

# Incluir rutas
app.include_router(auth_router, prefix="/api/auth")       # rutas como /api/auth/login
app.include_router(user_router, prefix="/api/users")       # si lo deseas más estructurado
app.include_router(inspection_router, prefix="/api/inspections")