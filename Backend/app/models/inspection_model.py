# app/models/inspection_model.py

from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class Inspection(BaseModel):
    titulo: str
    descripcion: Optional[str] = None
    fecha: datetime = Field(default_factory=datetime.utcnow)
    ubicacion: dict  # ejemplo: {"lat": 19.43, "lng": -99.13}
    estatus: str = "pendiente"  # puede ser: pendiente, en_proceso, completado
