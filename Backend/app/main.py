from fastapi import FastAPI
from app.routes.user_routes import router as user_router

app = FastAPI()

app.include_router(user_router)
@app.get("/")
def read_root():
    return {"mensaje": "API funcionando correctamente 🚀"}
