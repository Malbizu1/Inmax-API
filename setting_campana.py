from fastapi import FastAPI, HTTPException, Query, Path
from pydantic import BaseModel
from typing import List, Dict, Optional
from datetime import date

app = FastAPI(
    title="API de Campañas - Reportes Avanzados",
    description="Incluye endpoints de alertas, gastos, inversión, cupones, exportación y ventas.",
    version="1.0.0"
)

class GastoDetalle(BaseModel):
    fecha: date
    monto: float
    descripcion: Optional[str] = None

class GastoResumen(BaseModel):
    gasto_total: float
    fechas: List[date]
    detalles: List[GastoDetalle]

class InversionLocalidad(BaseModel):
    localidad: str
    monto: float

class InversionProducto(BaseModel):
    producto: str
    monto: float

class GastoPorFecha(BaseModel):
    fecha: date
    monto: float

class Cupon(BaseModel):
    codigo: str
    descuento: float
    valido_hasta: date

class ArchivoResponse(BaseModel):
    archivo: str

class VentaDetalle(BaseModel):
    fecha: date
    canal: str
    monto: float

class VentasResponse(BaseModel):
    total_ventas: float
    detalles: List[VentaDetalle]

class ExportFiltro(BaseModel):
    temporalidad: str
    campana: str
    demografia: str
    geolocalizacion: str

# ---------------- MOCK DATA ----------------

ALERTAS = {
    1: ["Presupuesto agotado", "Inactividad reciente"]
}

GASTOS = {
    1: GastoResumen(
        gasto_total=12000.0,
        fechas=[date(2025, 6, 1), date(2025, 6, 2)],
        detalles=[
            GastoDetalle(fecha=date(2025, 6, 1), monto=5000.0, descripcion="Publicidad"),
            GastoDetalle(fecha=date(2025, 6, 2), monto=7000.0, descripcion="Producción")
        ]
    )
}

INVERSION_LOCALIDAD = {
    1: [
        {"localidad": "Santiago", "monto": 3000.0},
        {"localidad": "Valparaíso", "monto": 2000.0}
    ]
}

INVERSION_PRODUCTO = {
    1: [
        {"producto": "Facebook Ads", "monto": 4000.0},
        {"producto": "Google Ads", "monto": 3500.0}
    ]
}

EVOLUCION_GASTOS = {
    1: [
        {"fecha": date(2025, 6, 1), "monto": 3000.0},
        {"fecha": date(2025, 6, 2), "monto": 4000.0}
    ]
}

CUPONES = {
    1: [
        {"codigo": "DESCUENTO10", "descuento": 10.0, "valido_hasta": date(2025, 7, 1)}
    ]
}

VENTAS = {
    1: {
        "total_ventas": 35000.0,
        "detalles": [
            {"fecha": date(2025, 6, 1), "canal": "online", "monto": 15000.0},
            {"fecha": date(2025, 6, 2), "canal": "tienda", "monto": 20000.0}
        ]
    }
}

# ---------------- ENDPOINTS ----------------

@app.get("/campanas/{id}/alertas", response_model=List[str], summary="Obtiene alertas activas de la campaña")
async def get_alertas(id: int = Path(..., description="ID de la campaña")):
    return ALERTAS.get(id, [])

@app.get("/reportes/gastos-campana", response_model=GastoResumen, summary="Gastos detallados de la campaña")
async def get_gastos_campana(
    id_campana: int = Query(...),
    fecha_inicio: Optional[date] = Query(None),
    fecha_fin: Optional[date] = Query(None)
):
    if id_campana not in GASTOS:
        raise HTTPException(status_code=404, detail="No se encontraron gastos para esta campaña.")
    return GASTOS[id_campana]

@app.get("/reportes/inversion/localidad", response_model=List[InversionLocalidad], summary="Inversión por localidad")
async def get_inversion_localidad(id_campana: int = Query(...)):
    return INVERSION_LOCALIDAD.get(id_campana, [])

@app.get("/reportes/inversion/producto", response_model=List[InversionProducto], summary="Inversión por tipo de producto")
async def get_inversion_producto(id_campana: int = Query(...)):
    return INVERSION_PRODUCTO.get(id_campana, [])

@app.get("/reportes/evolucion-gastos", response_model=List[GastoPorFecha], summary="Evolución de gastos por día")
async def get_evolucion_gastos(id_campana: int = Query(...)):
    return EVOLUCION_GASTOS.get(id_campana, [])

@app.get("/campanas/{id}/cupones", response_model=List[Cupon], summary="Cupones asociados a una campaña")
async def get_cupones(id: int = Path(...)):
    return CUPONES.get(id, [])

@app.get("/campanas/{id}/exportar", response_model=ArchivoResponse, summary="Exporta data de campaña")
async def exportar(id: int = Path(...)):
    return {"archivo": f"campana_{id}_data.csv"}

@app.get("/campanas/{id}/ventas", response_model=VentasResponse, summary="Ventas de la campaña")
async def get_ventas(id: int = Path(...)):
    return VENTAS.get(id, {"total_ventas": 0.0, "detalles": []})
