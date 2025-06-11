from fastapi import FastAPI, Query, HTTPException
from pydantic import BaseModel
from typing import List
from datetime import date

app = FastAPI(
    title="API de Reportes de Gastos por Campaña",
    description="Devuelve el desglose de gastos por fecha y total acumulado para campañas específicas.",
    version="1.0.0"
)

class GastoFecha(BaseModel):
    fecha: date
    monto: float

class GastoCampañaResponse(BaseModel):
    total: float
    detalle: List[GastoFecha]

GASTOS_FECHA = {
    1: [
        {"fecha": date(2025, 6, 1), "monto": 1500.0},
        {"fecha": date(2025, 6, 2), "monto": 2000.0},
        {"fecha": date(2025, 6, 3), "monto": 2500.0}
    ],
    2: [
        {"fecha": date(2025, 6, 1), "monto": 500.0},
        {"fecha": date(2025, 6, 4), "monto": 800.0}
    ]
}

# ----------------- ENDPOINT -----------------

@app.get("/reportes/gastos-campaña", response_model=GastoCampañaResponse, summary="Desglose de gastos por fecha")
async def obtener_gastos_campaña(
    id_campaña: int = Query(..., description="ID de la campaña"),
    fecha_inicio: date = Query(..., description="Fecha de inicio del rango"),
    fecha_fin: date = Query(..., description="Fecha de fin del rango")
):
    datos = GASTOS_FECHA.get(id_campaña)
    if not datos:
        raise HTTPException(status_code=404, detail="No se encontraron gastos para esta campaña.")

    # Filtrar por rango de fechas
    detalle_filtrado = [
        g for g in datos if fecha_inicio <= g["fecha"] <= fecha_fin
    ]
    total = sum(g["monto"] for g in detalle_filtrado)

    return {
        "total": total,
        "detalle": detalle_filtrado
    }
