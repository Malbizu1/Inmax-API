from fastapi import FastAPI, Query, HTTPException
from pydantic import BaseModel
from typing import List, Dict
from datetime import date

app = FastAPI(
    title="API de Inversión y Métricas por Ubicación",
    description="Endpoints para visualizar inversión por ciudad, mapa de inversión y métricas gráficas.",
    version="1.0.0"
)

class InversionUbicacion(BaseModel):
    ciudad: str
    pais: str
    inversion: float
    clicks: int
    roi: float

class CoordenadaConMetrica(BaseModel):
    lat: float
    lon: float
    ciudad: str
    total_inversion: float
    clicks: int
    roi: float

class PuntoGrafico(BaseModel):
    etiqueta: str  
    valor: float

INVERSION_LOCALIZACION = {
    1: [
        {"ciudad": "Santiago", "pais": "Chile", "inversion": 5000.0, "clicks": 1200, "roi": 2.5},
        {"ciudad": "Lima", "pais": "Perú", "inversion": 3000.0, "clicks": 800, "roi": 1.9}
    ]
}

MAPA_INVERSION = {
    1: [
        {"lat": -33.4489, "lon": -70.6693, "ciudad": "Santiago", "total_inversion": 5000.0, "clicks": 1200, "roi": 2.5},
        {"lat": -12.0464, "lon": -77.0428, "ciudad": "Lima", "total_inversion": 3000.0, "clicks": 800, "roi": 1.9}
    ]
}

METRICAS_GRAFICO = {
    1: {
        "revenue": [
            {"etiqueta": "2025-06-01", "valor": 1200.0},
            {"etiqueta": "2025-06-02", "valor": 1350.0}
        ],
        "clicks": [
            {"etiqueta": "2025-06-01", "valor": 500},
            {"etiqueta": "2025-06-02", "valor": 700}
        ],
        "roi": [
            {"etiqueta": "2025-06-01", "valor": 2.0},
            {"etiqueta": "2025-06-02", "valor": 2.5}
        ]
    }
}

# ------------------------- ENDPOINTS -------------------------

# 52) GET /reportes/inversion/localizacion
@app.get("/reportes/inversion/localizacion", response_model=List[InversionUbicacion], summary="Inversión por ciudad o país")
async def get_inversion_localizacion(
    id_campaña: int = Query(..., description="ID de la campaña"),
    fecha_inicio: date = Query(..., description="Fecha de inicio del período"),
    fecha_fin: date = Query(..., description="Fecha de fin del período")
):
    data = INVERSION_LOCALIZACION.get(id_campaña)
    if not data:
        raise HTTPException(status_code=404, detail="No se encontraron datos de localización para esta campaña.")
    return data

# 53) GET /reportes/inversion/mapa
@app.get("/reportes/inversion/mapa", response_model=List[CoordenadaConMetrica], summary="Coordenadas para mapa de inversión")
async def get_mapa_inversion(
    id_campaña: int = Query(..., description="ID de la campaña")
):
    data = MAPA_INVERSION.get(id_campaña)
    if not data:
        raise HTTPException(status_code=404, detail="No se encontraron datos para el mapa de inversión.")
    return data

# 54) GET /reportes/inversion/grafico
@app.get("/reportes/inversion/grafico", response_model=List[PuntoGrafico], summary="Métricas gráficas para ROI, clicks o ventas")
async def get_grafico_inversion(
    id_campaña: int = Query(..., description="ID de la campaña"),
    tipo_metrica: str = Query(..., description="Tipo de métrica: 'revenue', 'clicks', 'roi'")
):
    campaña = METRICAS_GRAFICO.get(id_campaña)
    if not campaña or tipo_metrica not in campaña:
        raise HTTPException(status_code=404, detail="No hay datos para la métrica solicitada.")
    return campaña[tipo_metrica]
