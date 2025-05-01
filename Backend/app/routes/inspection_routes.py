from fastapi import APIRouter, Depends
from app.schemas.inspection_schema import InspectionSchema
from app.database import db
from app.utils.auth import get_current_user
from datetime import datetime
from bson import ObjectId
from bson.errors import InvalidId
from fastapi import HTTPException
from fastapi import Query

router = APIRouter()

@router.post("/inspecciones")
def crear_inspeccion(inspeccion: InspectionSchema, usuario=Depends(get_current_user)):
    data = inspeccion.dict()
    data["fecha_creacion"] = datetime.utcnow()
    data["creado_por"] = usuario["sub"]

    resultado = db["inspecciones"].insert_one(data)
    return {"mensaje": "Inspección registrada", "id": str(resultado.inserted_id)}

@router.get("/inspecciones")
def obtener_inspecciones(
    status: str = Query(None),
    usuario=Depends(get_current_user)
):
    filtro = {"creado_por": usuario["sub"]}
    if status:
        filtro["estatus"] = status

    inspecciones = []
    for i in db["inspecciones"].find(filtro):
        i["_id"] = str(i["_id"])
        inspecciones.append(i)
    return inspecciones

@router.get("/inspecciones/{id}")
def obtener_inspeccion(id: str, usuario=Depends(get_current_user)):
    try:
        inspeccion = db["inspecciones"].find_one({"_id": ObjectId(id), "creado_por": usuario["sub"]})
    except InvalidId:
        raise HTTPException(status_code=400, detail="ID inválido")

    if not inspeccion:
        raise HTTPException(status_code=404, detail="Inspección no encontrada")

    inspeccion["_id"] = str(inspeccion["_id"])
    return inspeccion

@router.put("/inspecciones/{id}")
def actualizar_inspeccion(id: str, datos: InspectionSchema, usuario=Depends(get_current_user)):
    try:
        filtro = {"_id": ObjectId(id), "creado_por": usuario["sub"]}
    except InvalidId:
        raise HTTPException(status_code=400, detail="ID inválido")

    nuevos_valores = {"$set": datos.dict()}
    resultado = db["inspecciones"].update_one(filtro, nuevos_valores)

    if resultado.matched_count == 0:
        raise HTTPException(status_code=404, detail="Inspección no encontrada o no autorizada")

    return {"mensaje": "Inspección actualizada correctamente"}

@router.delete("/inspecciones/{id}")
def eliminar_inspeccion(id: str, usuario=Depends(get_current_user)):
    try:
        filtro = {"_id": ObjectId(id), "creado_por": usuario["sub"]}
    except InvalidId:
        raise HTTPException(status_code=400, detail="ID inválido")

    resultado = db["inspecciones"].delete_one(filtro)

    if resultado.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Inspección no encontrada o no autorizada")

    return {"mensaje": "Inspección eliminada correctamente"}

