from fastapi import FastAPI, Query, HTTPException
from pydantic import BaseModel
from typing import Optional, List
from datetime import date

app = FastAPI(
    title="API de Dashboard",
    description="Endpoints para reportes de usuarios, sesiones y más",
    version="1.0.0"
)

class PaisUsuarios(BaseModel):
    pais: str
    usuarios: int

class PaisSesiones(BaseModel):
    pais: str
    sesiones: int

class PaisDuracion(BaseModel):
    pais: str
    duracion: float

class CanalUsuarios(BaseModel):
    canal: str
    usuarios: int

class GrupoClicks(BaseModel):
    grupo: str
    clicks: int

# Datos de ejemplo
DATA_USUARIOS = [
    {"pais": "Chile", "usuarios": 1200},
    {"pais": "México", "usuarios": 950},
    {"pais": "Colombia", "usuarios": 800}
]

DATA_SESIONES = [
    {"pais": "Chile", "sesiones": 3000},
    {"pais": "Colombia", "sesiones": 2500},
    {"pais": "México", "sesiones": 1800}
]

DATA_DURACION = [
    {"pais": "Chile", "duracion": 120},
    {"pais": "México", "duracion": 90},
    {"pais": "Colombia", "duracion": 150}
]

DATA_ADQUISICION = [
    {"canal": "social", "usuarios": 400},
    {"canal": "direct", "usuarios": 300},
    {"canal": "email", "usuarios": 200}
]

DATA_CLICKS = [
    {"grupo": "Chile", "clicks": 700},
    {"grupo": "México", "clicks": 600},
    {"grupo": "Colombia", "clicks": 500}
]

# 4) /reportes/usuarios-top-paises
@app.get("/reportes/usuarios-top-paises", response_model=List[PaisUsuarios], summary="Top países con más usuarios únicos")
async def usuarios_top_paises(
    top_n: int = Query(..., description="Cantidad de países a retornar"),
    fecha_inicio: Optional[date] = Query(None, description="Fecha de inicio"),
    fecha_fin: Optional[date] = Query(None, description="Fecha de fin")
):
    if top_n < 1:
        raise HTTPException(status_code=400, detail="El parámetro top_n debe ser mayor que 0")
    return DATA_USUARIOS[:top_n]

# 5) /reportes/sesiones-top-paises
@app.get("/reportes/sesiones-top-paises", response_model=List[PaisSesiones], summary="Top países con más sesiones activas")
async def sesiones_top_paises(
    top_n: int = Query(..., description="Cantidad de países a retornar"),
    fecha_inicio: Optional[date] = Query(None, description="Fecha de inicio"),
    fecha_fin: Optional[date] = Query(None, description="Fecha de fin")
):
    if top_n < 1:
        raise HTTPException(status_code=400, detail="El parámetro top_n debe ser mayor que 0")
    return DATA_SESIONES[:top_n]

# 7) /reportes/duracion-promedio-pais
@app.get("/reportes/duracion-promedio-pais", response_model=List[PaisDuracion], summary="Duración promedio de usuarios por país")
async def duracion_promedio_pais(
    fecha_inicio: Optional[date] = Query(None, description="Fecha de inicio"),
    fecha_fin: Optional[date] = Query(None, description="Fecha de fin")
):
    return DATA_DURACION

# 8) /reportes/adquisicion-usuarios
@app.get("/reportes/adquisicion-usuarios", response_model=List[CanalUsuarios], summary="Muestra cómo se están adquiriendo usuarios")
async def adquisicion_usuarios(
    fecha_inicio: Optional[date] = Query(None, description="Fecha de inicio"),
    fecha_fin: Optional[date] = Query(None, description="Fecha de fin")
):
    return DATA_ADQUISICION

# 9) /reportes/clicks-pais
@app.get("/reportes/clicks-pais", response_model=List[GrupoClicks], summary="Distribuye clics o interacciones en campañas por país")
async def clicks_pais(
    fecha_inicio: Optional[date] = Query(None, description="Fecha de inicio"),
    fecha_fin: Optional[date] = Query(None, description="Fecha de fin")
):
    return DATA_CLICKS

# Endpoint raíz
@app.get("/", summary="Prueba del API")
def read_root():
    return {"message": "API de Dashboard funcionando correctamente."}
