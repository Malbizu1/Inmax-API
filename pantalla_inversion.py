from fastapi import FastAPI, Query, HTTPException
from pydantic import BaseModel
from typing import List
from datetime import date

app = FastAPI(
    title="API de Inversión por Localidad",
    description="Devuelve la inversión acumulada y evolución por fecha para una localidad.",
    version="1.0.0"
)

class InversionPorFecha(BaseModel):
    fecha: date
    monto: float

class InversionLocalidadResponse(BaseModel):
    inversion_total: float
    datos_por_fecha: List[InversionPorFecha]

INVERSION_LOCALIDAD = {
    "santiago": [
        {"fecha": date(2025, 6, 1), "monto": 2000.0},
        {"fecha": date(2025, 6, 2), "monto": 2500.0},
        {"fecha": date(2025, 6, 3), "monto": 1500.0}
    ],
    "valparaiso": [
        {"fecha": date(2025, 6, 1), "monto": 1000.0},
        {"fecha": date(2025, 6, 2), "monto": 1200.0}
    ]
}

# ------------------ ENDPOINT ------------------

@app.get("/reportes/inversion/localidad", response_model=InversionLocalidadResponse, summary="Inversión por localidad y evolución")
async def get_inversion_por_localidad(
    localidad: str = Query(..., description="Nombre de la localidad (ej: santiago, valparaiso)"),
    fecha_inicio: date = Query(..., description="Fecha desde la cual se analizarán los datos")
):
    datos = INVERSION_LOCALIDAD.get(localidad.lower())
    if not datos:
        raise HTTPException(status_code=404, detail="No se encontraron datos para la localidad indicada.")

    datos_filtrados = [d for d in datos if d["fecha"] >= fecha_inicio]
    total = sum(d["monto"] for d in datos_filtrados)

    return {
        "inversion_total": total,
        "datos_por_fecha": datos_filtrados
    }
