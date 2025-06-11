from fastapi import FastAPI, HTTPException, Path, status
from pydantic import BaseModel, Field
from typing import List
from datetime import datetime

app = FastAPI(
    title="API de Piezas de Campañas",
    description="Endpoints para gestionar y consultar piezas multimedia de campañas.",
    version="1.0.0"
)

# ---------------------------------------------------
class Pieza(BaseModel):
    pieza_id: int = Field(..., description="ID único de la pieza")
    tipo: str = Field(..., description="Tipo de pieza multimedia (imagen, video, etc.)")
    url: str = Field(..., description="URL de la pieza")
    formato: str = Field(..., description="Formato de la pieza (jpg, mp4, etc.)")
    fecha_creacion: str = Field(..., description="Fecha de creación de la pieza (ISO)")

# ---------------------------------------------------
PIEZAS_CAMPAÑAS = {
    1: [
        {
            "pieza_id": 101,
            "tipo": "imagen",
            "url": "https://example.com/pieza101.jpg",
            "formato": "jpg",
            "fecha_creacion": "2025-06-01T10:00:00"
        },
        {
            "pieza_id": 102,
            "tipo": "video",
            "url": "https://example.com/pieza102.mp4",
            "formato": "mp4",
            "fecha_creacion": "2025-06-02T12:00:00"
        }
    ],
    2: [
        {
            "pieza_id": 201,
            "tipo": "imagen",
            "url": "https://example.com/pieza201.jpg",
            "formato": "jpg",
            "fecha_creacion": "2025-06-03T09:30:00"
        }
    ]
}

# ---------------------------------------------------

# 29) GET /campañas/{id}/piezas
@app.get("/campañas/{id}/piezas", response_model=List[Pieza], summary="Lista piezas multimedia de una campaña")
async def listar_piezas(
    id: int = Path(..., description="ID de la campaña")
):
    """
    Retorna todas las piezas multimedia asociadas a una campaña específica.
    """
    piezas = PIEZAS_CAMPAÑAS.get(id)
    if piezas is None:
        raise HTTPException(status_code=404, detail="Campaña no encontrada o sin piezas.")
    return piezas

# 30) GET /campañas/{id}/piezas/{pieza_id}
@app.get("/campañas/{id}/piezas/{pieza_id}", response_model=Pieza, summary="Detalle de una pieza multimedia")
async def obtener_pieza(
    id: int = Path(..., description="ID de la campaña"),
    pieza_id: int = Path(..., description="ID de la pieza a consultar")
):
    """
    Retorna el detalle de una pieza multimedia específica.
    """
    piezas = PIEZAS_CAMPAÑAS.get(id)
    if piezas is None:
        raise HTTPException(status_code=404, detail="Campaña no encontrada o sin piezas.")
    for pieza in piezas:
        if pieza["pieza_id"] == pieza_id:
            return pieza
    raise HTTPException(status_code=404, detail="Pieza no encontrada.")

# ---------------------------------------------------
# Endpoint raíz de prueba
@app.get("/", summary="API de Piezas funcionando correctamente")
def read_root():
    return {"message": "API de Piezas de Campañas lista y operativa."}
