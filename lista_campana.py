from fastapi import FastAPI, HTTPException, Query, Path, status
from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import date, datetime

app = FastAPI(
    title="API de Campañas",
    description="Endpoints para gestión completa de campañas publicitarias.",
    version="1.0.0"
)

# ---------------------------------------------------
class Campaña(BaseModel):
    id: int
    nombre: str
    descripcion: str
    estado: str
    fecha_inicio: datetime
    fecha_fin: datetime
    presupuesto: float
    canal: str

class MensajeResponse(BaseModel):
    message: str

# ---------------------------------------------------
CAMPAÑAS = [
    {
        "id": 1,
        "nombre": "Campaña de verano",
        "descripcion": "Promoción verano 2025",
        "estado": "activa",
        "fecha_inicio": datetime(2025, 6, 1, 10, 0),
        "fecha_fin": datetime(2025, 6, 30, 23, 59),
        "presupuesto": 10000,
        "canal": "social"
    },
    {
        "id": 2,
        "nombre": "Campaña de invierno",
        "descripcion": "Descuentos de invierno",
        "estado": "inactiva",
        "fecha_inicio": datetime(2025, 7, 1, 0, 0),
        "fecha_fin": datetime(2025, 7, 31, 23, 59),
        "presupuesto": 8000,
        "canal": "email"
    }
]

# ---------------------------------------------------
# 32) GET /campañas
@app.get("/campañas", response_model=List[Campaña], summary="Lista campañas con filtros")
async def listar_campañas(
    estado: Optional[str] = Query(None, description="Estado de la campaña (activa, inactiva)"),
    fecha_inicio: Optional[date] = Query(None),
    fecha_fin: Optional[date] = Query(None),
    orden: Optional[str] = Query(None, description="Campo para ordenar (ej: 'fecha_inicio')"),
    limite: Optional[int] = Query(10, ge=1, le=100, description="Cantidad de resultados"),
    buscar: Optional[str] = Query(None, description="Búsqueda por nombre o descripción")
):
    resultados = CAMPAÑAS.copy()

    if estado:
        resultados = [c for c in resultados if c["estado"].lower() == estado.lower()]
    if fecha_inicio:
        resultados = [c for c in resultados if c["fecha_inicio"].date() >= fecha_inicio]
    if fecha_fin:
        resultados = [c for c in resultados if c["fecha_fin"].date() <= fecha_fin]
    if buscar:
        resultados = [c for c in resultados if buscar.lower() in c["nombre"].lower() or buscar.lower() in c["descripcion"].lower()]

    if orden and orden in resultados[0]:
        resultados.sort(key=lambda x: x[orden])

    return resultados[:limite]

# 33) GET /campañas/{id}
@app.get("/campañas/{id}", response_model=Campaña, summary="Detalle de una campaña por ID")
async def obtener_campaña(id: int = Path(..., description="ID de la campaña a consultar")):
    for c in CAMPAÑAS:
        if c["id"] == id:
            return c
    raise HTTPException(status_code=404, detail="Campaña no encontrada.")

# 34) DELETE /campañas/{id}
@app.delete("/campañas/{id}", response_model=MensajeResponse, summary="Elimina o desactiva una campaña")
async def eliminar_campaña(id: int = Path(..., description="ID de la campaña a eliminar/desactivar")):
    for c in CAMPAÑAS:
        if c["id"] == id:
            if c["estado"] == "activa":
                raise HTTPException(status_code=403, detail="No se puede eliminar una campaña activa.")
            CAMPAÑAS.remove(c)
            return {"message": "Campaña eliminada correctamente."}
    raise HTTPException(status_code=404, detail="Campaña no encontrada.")

# ---------------------------------------------------
# Endpoint raíz
@app.get("/", summary="API de Campañas funcionando correctamente")
def read_root():
    return {"message": "API de Campañas lista y operativa."}
