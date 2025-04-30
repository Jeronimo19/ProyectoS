from fastapi import FastAPI
from app.routes.user_routes import router as user_router
from app.routes.auth_routes import router as auth_router


app = FastAPI()

app.include_router(user_router)
@app.get("/")
def read_root():
    return {"mensaje": "API funcionando correctamente 🚀"}

app.include_router(auth_router)