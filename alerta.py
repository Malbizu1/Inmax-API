from fastapi import FastAPI, Body, HTTPException, status
from pydantic import BaseModel, Field
from typing import List, Union

app = FastAPI(
    title="API de Alertas del Avisador",
    description="Endpoints para gestionar la configuración y disparo de alertas del avisador.",
    version="1.0.0"
)

class AlertaConfiguracion(BaseModel):
    ubicaciones: List[str] = Field(..., description="Lista de ubicaciones activas para la alerta")
    tipo_recepcion: str = Field(..., description="Tipo de recepción de la alerta (correo, SMS, push, etc.)")
    umbral_precio: float = Field(..., description="Umbral de precio para disparar la alerta")
    umbral_uso: int = Field(..., description="Umbral de uso para disparar la alerta")

class ActualizarAlertaRequest(BaseModel):
    ubicaciones: List[str]
    tipo_recepcion: str
    umbral_precio: float
    umbral_uso: int

class DisparoAlertaRequest(BaseModel):
    tipo_alerta: str = Field(..., description="Tipo de alerta a disparar (precio o uso)")
    campaña_id: str = Field(..., description="ID de la campaña relacionada")
    valor_actual: Union[int, float] = Field(..., description="Valor actual que dispara la alerta")

class MensajeResponse(BaseModel):
    message: str

class DisparoAlertaResponse(BaseModel):
    alerta_enviada: bool

ALERTAS_CONFIGURACION = {
    "ubicaciones": ["Chile", "México", "Colombia"],
    "tipo_recepcion": "correo",
    "umbral_precio": 50.0,
    "umbral_uso": 75
}

# 20) GET /avisador/alertas
@app.get(
    "/avisador/alertas",
    response_model=AlertaConfiguracion,
    summary="Obtiene la configuración actual de alertas",
    status_code=status.HTTP_200_OK
)
async def obtener_alertas():
    """
    Obtiene la configuración actual de alertas del avisador.
    """
    return ALERTAS_CONFIGURACION

# 21) PUT /avisador/alertas
@app.put(
    "/avisador/alertas",
    response_model=MensajeResponse,
    summary="Actualiza la configuración de alertas",
    status_code=status.HTTP_200_OK
)
async def actualizar_alertas(data: ActualizarAlertaRequest = Body(..., description="Nueva configuración de alertas")):
    """
    Actualiza la configuración actual de alertas del avisador.
    """
    if not data.ubicaciones:
        raise HTTPException(status_code=422, detail="Debe proporcionar al menos una ubicación.")
    global ALERTAS_CONFIGURACION
    ALERTAS_CONFIGURACION = data.dict()
    return {"message": "Configuración de alertas actualizada correctamente"}

# 22) POST /avisador/alertas/disparar-alerta
@app.post(
    "/avisador/alertas/disparar-alerta",
    response_model=DisparoAlertaResponse,
    summary="Dispara manualmente una alerta",
    status_code=status.HTTP_200_OK
)
async def disparar_alerta(data: DisparoAlertaRequest = Body(..., description="Parámetros para disparar la alerta")):
    """
    Dispara manualmente una alerta (útil para pruebas o tareas programadas).
    """
    if data.tipo_alerta not in ["precio", "uso"]:
        raise HTTPException(status_code=400, detail="Tipo de alerta inválido. Debe ser 'precio' o 'uso'.")

    if data.valor_actual <= 0:
        raise HTTPException(status_code=400, detail="El valor actual debe ser positivo para disparar la alerta.")

    # Aquí se integraría con el sistema real de envío de alertas
    return {"alerta_enviada": True}

# Endpoint raíz de prueba
@app.get("/", summary="API de Alertas funcionando correctamente")
def read_root():
    return {"message": "API de Alertas del Avisador lista y operativa."}
