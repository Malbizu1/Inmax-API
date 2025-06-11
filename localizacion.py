from fastapi import FastAPI, HTTPException, Path, Query
from pydantic import BaseModel, Field
from typing import List, Optional, Union
from datetime import date

app = FastAPI(
    title="API de Geolocalización y Mapas Interactivos",
    description="Endpoints para métricas geográficas e interactivas de campañas publicitarias.",
    version="1.0.0"
)

# ---------------------------------------------------
class PuntoGeografico(BaseModel):
    lat: float
    lon: float
    ciudad: str
    impresiones: int

class DatosMapaInteractivo(BaseModel):
    zonas: List[str]
    nivel: str
    metricas: dict

# ---------------------------------------------------
GEODISTRIBUCION_CAMPAÑAS = {
    1: [
        {"lat": -33.4489, "lon": -70.6693, "ciudad": "Santiago", "impresiones": 1000},
        {"lat": -32.8908, "lon": -71.2748, "ciudad": "Valparaíso", "impresiones": 500}
    ]
}

MAPA_INTERACTIVO_CAMPAÑAS = {
    1: {
        "zonas": ["Zona A", "Zona B"],
        "nivel": "medio",
        "metricas": {"clics": 150, "impresiones": 2000}
    }
}

# ---------------------------------------------------

@app.get("/campañas/geolocalizacion", response_model=List[PuntoGeografico], summary="Puntos geográficos de impacto")
async def puntos_geograficos(
    id_campaña: int = Query(..., description="ID de la campaña"),
    region: Optional[str] = Query(None, description="Región específica"),
    fecha_inicio: Optional[date] = Query(None),
    fecha_fin: Optional[date] = Query(None)
):
    """
    Devuelve la lista de puntos geográficos con métricas de impacto de una campaña.
    """
    puntos = GEODISTRIBUCION_CAMPAÑAS.get(id_campaña)
    if not puntos:
        raise HTTPException(status_code=404, detail="Campaña no encontrada o sin datos geográficos.")
    return puntos

# 36) GET /campañas/{id}/mapa-interactivo
@app.get("/campañas/{id}/mapa-interactivo", response_model=DatosMapaInteractivo, summary="Mapa interactivo de la campaña")
async def mapa_interactivo(
    id: int = Path(..., description="ID de la campaña"),
    nivel_detalle: Optional[str] = Query("medio", description="Nivel de detalle (bajo, medio, alto)")
):
    """
    Muestra el mapa interactivo asociado a la campaña, con zonas y métricas.
    """
    datos = MAPA_INTERACTIVO_CAMPAÑAS.get(id)
    if not datos:
        raise HTTPException(status_code=404, detail="Campaña no encontrada o sin datos de mapa interactivo.")
    # Ajustar nivel de detalle si se envía
    datos["nivel"] = nivel_detalle
    return datos

# ---------------------------------------------------
# Endpoint raíz
@app.get("/", summary="API de Geolocalización y Mapa lista")
def read_root():
    return {"message": "API de Geolocalización y Mapa de Campañas operativa."}
