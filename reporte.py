from fastapi import FastAPI, Query
from pydantic import BaseModel
from typing import List, Optional
from datetime import date

app = FastAPI(
    title="API Resumen de Campañas",
    description="Retorna campañas con información resumida, organizadas por ciudad.",
    version="1.0.0"
)

class CampañaResumen(BaseModel):
    id: int
    nombre: str
    presupuesto: float
    estado: str
    fecha_inicio: date
    fecha_fin: date
    ciudad: str

CAMPAÑAS_RESUMIDAS = [
    {
        "id": 1,
        "nombre": "Campaña Invierno",
        "presupuesto": 12000.0,
        "estado": "activa",
        "fecha_inicio": date(2025, 6, 1),
        "fecha_fin": date(2025, 7, 15),
        "ciudad": "Santiago"
    },
    {
        "id": 2,
        "nombre": "Campaña Verano",
        "presupuesto": 18000.0,
        "estado": "finalizada",
        "fecha_inicio": date(2025, 1, 10),
        "fecha_fin": date(2025, 2, 28),
        "ciudad": "Valparaíso"
    },
    {
        "id": 3,
        "nombre": "Campaña Escolar",
        "presupuesto": 9500.0,
        "estado": "activa",
        "fecha_inicio": date(2025, 3, 1),
        "fecha_fin": date(2025, 4, 10),
        "ciudad": "Santiago"
    }
]

# ---------------- Endpoint ----------------

@app.get("/campañas/resumen", response_model=List[CampañaResumen], summary="Lista de campañas resumidas")
async def obtener_resumen_campañas(
    ciudad: Optional[str] = Query(None, description="Filtrar por ciudad"),
    estado: Optional[str] = Query(None, description="Filtrar por estado (ej: activa, finalizada)")
):
    resultados = CAMPAÑAS_RESUMIDAS

    if ciudad:
        resultados = [c for c in resultados if c["ciudad"].lower() == ciudad.lower()]
    if estado:
        resultados = [c for c in resultados if c["estado"].lower() == estado.lower()]

    return resultados
