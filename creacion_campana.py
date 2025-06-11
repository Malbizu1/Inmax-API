from fastapi import FastAPI, HTTPException, status, UploadFile, File, Form
from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime

app = FastAPI(
    title="API de Campañas Publicitarias",
    description="Endpoint para la creación de campañas con medios, segmentación y fechas.",
    version="1.0.0"
)

class CrearCampañaRequest(BaseModel):
    nombre: str = Field(..., description="Nombre de la campaña")
    descripcion: str = Field(..., description="Descripción breve")
    presupuesto: float = Field(..., description="Presupuesto asignado")
    demografia: str = Field(..., description="Segmento demográfico (por ejemplo: '18-24')")
    canal: str = Field(..., description="Canal de la campaña (por ejemplo: 'social', 'email')")
    fecha_inicio: datetime = Field(..., description="Fecha de inicio (ISO)")
    fecha_fin: datetime = Field(..., description="Fecha de fin (ISO)")
    imagenes: List[str] = Field(..., description="Lista de URLs de imágenes")
    video: Optional[str] = Field(None, description="URL de video de la campaña")

class CampañaCreadaResponse(BaseModel):
    id_campaña: int
    estado: str
    mensaje: str
    confirmación: str

CAMPAÑAS = []
contador_campañas = 1

# ---------------------------------------------------
#Endpoint para crear una campaña
@app.post("/campañas", response_model=CampañaCreadaResponse, status_code=201, summary="Crea una nueva campaña")
async def crear_campaña(data: CrearCampañaRequest):
    global contador_campañas

    # Validaciones adicionales mínimas
    if data.fecha_fin <= data.fecha_inicio:
        raise HTTPException(status_code=422, detail="La fecha de fin debe ser posterior a la fecha de inicio.")
    if data.presupuesto <= 0:
        raise HTTPException(status_code=422, detail="El presupuesto debe ser positivo.")

    # Simulación de creación y asignación de ID
    nueva_campaña = data.dict()
    nueva_campaña["id_campaña"] = contador_campañas
    nueva_campaña["estado"] = "activa"
    CAMPAÑAS.append(nueva_campaña)
    contador_campañas += 1

    return {
        "id_campaña": nueva_campaña["id_campaña"],
        "estado": nueva_campaña["estado"],
        "mensaje": "Campaña creada correctamente",
        "confirmación": f"Campaña '{data.nombre}' registrada con éxito."
    }

# ---------------------------------------------------
# Endpoint raíz de prueba
@app.get("/", summary="API de Campañas funcionando correctamente")
def read_root():
    return {"message": "API de Campañas lista y operativa."}
