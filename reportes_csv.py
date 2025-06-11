from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import JSONResponse, StreamingResponse
from pydantic import BaseModel
from typing import List, Optional
from datetime import date
import json
from io import BytesIO

app = FastAPI()

class EvolucionPorFecha(BaseModel):
    fecha: str
    valor: float

@app.get(
    "/reportes/exportar",
    response_model=List[EvolucionPorFecha],
    summary="Devuelve evolución temporal de un tipo de gasto y permite exportación"
)
async def exportar_evolucion_gasto(
    costo: str = Query(..., description="Tipo de gasto a consultar"),
    fecha_inicio: Optional[date] = Query(None, description="Fecha desde la cual mostrar la evolución"),
    descargar: Optional[bool] = Query(False, description="Si es True, devuelve archivo descargable")
):
    try:
        datos = [
            {"fecha": "2025-01-01", "valor": 400.0},
            {"fecha": "2025-02-01", "valor": 450.0},
            {"fecha": "2025-03-01", "valor": 420.0},
        ]

        if not datos:
            raise HTTPException(status_code=404, detail="No se encontraron datos para el gasto solicitado")

        if descargar:
            json_data = json.dumps(datos, indent=2)
            buffer = BytesIO(json_data.encode("utf-8"))
            return StreamingResponse(
                buffer,
                media_type="application/json",
                headers={
                    "Content-Disposition": f"attachment; filename=exporte_{costo}.json"
                }
            )
        
        return datos

    except HTTPException as e:
        raise e
    except Exception as ex:
        raise HTTPException(status_code=500, detail=f"Error interno: {str(ex)}")
