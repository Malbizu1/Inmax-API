from fastapi import FastAPI, Query
from pydantic import BaseModel
from typing import Optional, List
from datetime import date

app = FastAPI(
    title="API de Geolocalización",
    description="Endpoints de reportes de geolocalización para representar actividad en mapas y distribución de usuarios.",
    version="1.0.0"
)


class PaisDistribucion(BaseModel):
    pais: str
    cantidad: int
    porcentaje: float

class CoordenadasActividad(BaseModel):
    pais: str
    lat: float
    lon: float
    actividad: int

# Datos de ejemplo
DATA_DISTRIBUCION_USUARIOS = [
    {"pais": "Chile", "cantidad": 500, "porcentaje": 25.0},
    {"pais": "México", "cantidad": 450, "porcentaje": 22.5},
    {"pais": "Colombia", "cantidad": 300, "porcentaje": 15.0}
]

DATA_COORDENADAS_MAPA = [
    {"pais": "Chile", "lat": -33.4489, "lon": -70.6693, "actividad": 1500},
    {"pais": "México", "lat": 19.4326, "lon": -99.1332, "actividad": 1200},
    {"pais": "Colombia", "lat": 4.7110, "lon": -74.0721, "actividad": 800}
]

# 18) /reportes/geolocalizacion/usuarios
@app.get("/reportes/geolocalizacion/usuarios", response_model=List[PaisDistribucion], summary="Distribución geográfica de usuarios")
async def distribucion_usuarios(
    fecha_inicio: date,
    fecha_fin: Optional[date] = None
):
    """
    Retorna la lista de países con el conteo y porcentaje de usuarios en el período dado.
    """
    return DATA_DISTRIBUCION_USUARIOS

# 19) /reportes/geolocalizacion/mapa
@app.get("/reportes/geolocalizacion/mapa", response_model=List[CoordenadasActividad], summary="Datos geográficos para renderizar mapa")
async def coordenadas_mapa(
    fecha_inicio: date,
    fecha_fin: Optional[date] = None
):
    """
    Devuelve coordenadas (latitud, longitud) y actividad por país para visualización en mapas.
    """
    return DATA_COORDENADAS_MAPA

# Endpoint raíz de prueba
@app.get("/", summary="Prueba del API de geolocalización")
def read_root():
    return {"message": "API de Geolocalización funcionando correctamente"}
