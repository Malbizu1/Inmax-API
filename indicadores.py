from fastapi import FastAPI, Query, HTTPException
from pydantic import BaseModel
from typing import Optional, List
from datetime import date

app = FastAPI(
    title="API de Indicadores del Avisador",
    description="Endpoints de reportes e indicadores para campañas del avisador.",
    version="1.0.0"
)

class PaisCantidad(BaseModel):
    pais: str
    cantidad: int

class PaisUsuarios(BaseModel):
    pais: str
    usuarios: int

class PaisSesiones(BaseModel):
    pais: str
    sesiones: int

class PaisDuracion(BaseModel):
    pais: str
    duracion_promedio: float

class CanalUsuarios(BaseModel):
    canal: str
    usuarios: int

class ClicksPais(BaseModel):
    pais: str
    clicks: int

class EstadisticaUsuarios(BaseModel):
    fecha: date
    tipo: str
    cantidad: int

class TransaccionesResponse(BaseModel):
    total_transacciones: int

#datos de ejemplo
DATA_USUARIOS = [
    {"pais": "Chile", "usuarios": 1200, "sesiones": 3000, "duracion_promedio": 120},
    {"pais": "México", "usuarios": 950, "sesiones": 1800, "duracion_promedio": 90},
    {"pais": "Colombia", "usuarios": 800, "sesiones": 1500, "duracion_promedio": 150}
]

DATA_ADQUISICION = [
    {"canal": "social", "usuarios": 400},
    {"canal": "direct", "usuarios": 300},
    {"canal": "email", "usuarios": 200}
]

DATA_CLICKS = [
    {"pais": "Chile", "clicks": 700},
    {"pais": "México", "clicks": 600},
    {"pais": "Colombia", "clicks": 500}
]

DATA_ESTADISTICAS = [
    {"fecha": date(2025, 5, 27), "tipo": "activo", "cantidad": 300},
    {"fecha": date(2025, 5, 27), "tipo": "nuevo", "cantidad": 150},
    {"fecha": date(2025, 5, 27), "tipo": "suscriptor", "cantidad": 50}
]

# Endpoint raíz
@app.get("/", summary="API de Indicadores funcionando")
async def read_root():
    return {"message": "API de Indicadores OK"}

# 10) /avisador/mapa-usuarios
@app.get("/avisador/mapa-usuarios", response_model=List[PaisCantidad])
async def mapa_usuarios(
    fecha_inicio: date,
    fecha_fin: Optional[date] = None
):
    return [{"pais": d["pais"], "cantidad": d["usuarios"]} for d in DATA_USUARIOS]

# 11) /reportes/usuarios-top-paises
@app.get("/reportes/usuarios-top-paises", response_model=List[PaisUsuarios])
async def usuarios_top_paises(
    fecha_inicio: date,
    top_n: int = Query(..., ge=1, description="Cantidad de países a retornar"),
    fecha_fin: Optional[date] = None
):
    lista = [{"pais": d["pais"], "usuarios": d["usuarios"]} for d in DATA_USUARIOS]
    return lista[:top_n]

# 13) /reportes/sesiones-top-paises
@app.get("/reportes/sesiones-top-paises", response_model=List[PaisSesiones])
async def sesiones_top_paises(
    fecha_inicio: date,
    top_n: int = Query(..., ge=1, description="Cantidad de países a retornar"),
    fecha_fin: Optional[date] = None
):
    lista = [{"pais": d["pais"], "sesiones": d["sesiones"]} for d in DATA_USUARIOS]
    return lista[:top_n]

# 14) /avisador/duracion-promedio
@app.get("/avisador/duracion-promedio", response_model=List[PaisDuracion])
async def duracion_promedio(
    fecha_inicio: date,
    fecha_fin: date
):
    lista = [{"pais": d["pais"], "duracion_promedio": d["duracion_promedio"]} for d in DATA_USUARIOS]
    return lista

# 15) /avisador/estadisticas-usuarios
@app.get("/avisador/estadisticas-usuarios", response_model=List[EstadisticaUsuarios])
async def estadisticas_usuarios(
    fecha_inicio: date,
    fecha_fin: date
):
    return DATA_ESTADISTICAS

# 17) /avisador/transacciones (extra)
@app.get("/avisador/transacciones", response_model=TransaccionesResponse)
async def transacciones(
    fecha_inicio: date,
    fecha_fin: date
):
    total_transacciones = 213  # Ejemplo estático, reemplazar con consulta real
    return {"total_transacciones": total_transacciones}

# 8) /reportes/adquisicion-usuarios
@app.get("/reportes/adquisicion-usuarios", response_model=List[CanalUsuarios])
async def adquisicion_usuarios(
    fecha_inicio: date,
    fecha_fin: date
):
    return DATA_ADQUISICION

# 9) /reportes/clicks-pais
@app.get("/reportes/clicks-pais", response_model=List[ClicksPais])
async def clicks_pais(
    fecha_inicio: date,
    fecha_fin: date
):
    return DATA_CLICKS
