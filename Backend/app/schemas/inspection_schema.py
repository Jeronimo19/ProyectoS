from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class InspectionSchema(BaseModel):
    titulo: str
    descripcion: str
    ubicacion: dict  # Ej: {"lat": 19.4, "lng": -99.1}
    estatus: Optional[str] = "pendiente"
    fecha_creacion: Optional[datetime] = None
    creado_por: Optional[str] = None  # id del usuario

    class Config:
        schema_extra = {
            "example": {
                "titulo": "Fuga de agua",
                "descripcion": "Hay una fuga en la calle Juárez",
                "ubicacion": {"lat": 19.4326, "lng": -99.1332},
            }
        }
