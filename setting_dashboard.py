from fastapi import FastAPI, HTTPException, Body
from pydantic import BaseModel, Field
from typing import List, Dict

app = FastAPI(
    title="API de Configuración del Dashboard",
    description="Endpoints para gestionar widgets, fuentes de datos y tipos de gráficos.",
    version="1.0.0"
)

class WidgetUpdateRequest(BaseModel):
    widgets: List[str] = Field(..., description="Lista de widgets a configurar para el usuario.")

class MessageResponse(BaseModel):
    message: str

WIDGETS_CONFIG: Dict[str, List[str]] = {
    "usuario_1": ["grafico_ventas", "mapa_impacto", "cuadro_alertas"]
}

DEFAULT_WIDGETS = ["grafico_ventas", "mapa_impacto"]

FUENTES_DATOS = ["ventas", "usuarios", "clicks", "sesiones", "impactos"]
TIPOS_GRAFICOS = ["línea", "barras", "torta", "dispersión", "área", "radar"]

# 47) GET /dashboard/widgets
@app.get("/dashboard/widgets", response_model=List[str], summary="Obtiene la configuración actual de widgets")
async def obtener_widgets():
    config = WIDGETS_CONFIG.get("usuario_1")
    if not config:
        raise HTTPException(status_code=404, detail="No hay configuración de widgets para el usuario.")
    return config

# 48) PUT /dashboard/widgets
@app.put("/dashboard/widgets", response_model=MessageResponse, summary="Guarda widgets personalizados del usuario")
async def guardar_widgets(payload: WidgetUpdateRequest):
    if not payload.widgets:
        raise HTTPException(status_code=400, detail="La lista de widgets no puede estar vacía.")
    WIDGETS_CONFIG["usuario_1"] = payload.widgets
    return {"message": "Configuración de widgets guardada exitosamente."}

# 49) POST /dashboard/widgets/reset
@app.post("/dashboard/widgets/reset", response_model=MessageResponse, summary="Restaura widgets a valores por defecto")
async def reset_widgets():
    WIDGETS_CONFIG["usuario_1"] = DEFAULT_WIDGETS
    return {"message": "Widgets restaurados a la configuración por defecto."}

# 50) GET /dashboard/data-fuentes
@app.get("/dashboard/data-fuentes", response_model=List[str], summary="Lista de fuentes de datos disponibles")
async def listar_fuentes_datos():
    return FUENTES_DATOS

# 51) GET /dashboard/graficos-disponibles
@app.get("/dashboard/graficos-disponibles", response_model=List[str], summary="Tipos de gráficos disponibles")
async def listar_tipos_graficos():
    return TIPOS_GRAFICOS

# Endpoint raíz
@app.get("/", summary="API de Dashboard operativa")
def root_dashboard():
    return {"message": "API del dashboard funcionando correctamente."}


