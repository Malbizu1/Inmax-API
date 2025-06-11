from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel
from typing import List, Optional
from datetime import date

app = FastAPI()  

class EvolucionPorFecha(BaseModel):
    fecha: str
    valor: float

@app.get(
    "/reportes/evolucion-gastos",
    response_model=List[EvolucionPorFecha],
    summary="Devuelve la evolución temporal de un tipo de gasto desde una fecha específica"
)
async def obtener_evolucion_gastos(
    costo: str = Query(..., description="Tipo de costo o gasto a analizar"),
    fecha_inicio: Optional[date] = Query(None, description="Fecha de inicio del análisis")
):
    try:
        datos_simulados = [
            {"fecha": "2025-01-01", "valor": 500.0},
            {"fecha": "2025-02-01", "valor": 620.0},
            {"fecha": "2025-03-01", "valor": 580.0},
        ]

        if not datos_simulados:
            raise HTTPException(status_code=404, detail="No se encontraron datos de gastos")

        return datos_simulados

    except HTTPException as e:
        raise e
    except Exception:
        raise HTTPException(status_code=500, detail="Error interno del servidor")
