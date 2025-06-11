from fastapi import FastAPI, HTTPException, Path, status, Header, Depends
from pydantic import BaseModel, Field
from typing import List, Dict, Optional

app = FastAPI(
    title="API de Roles",
    description="Endpoints para gestionar roles y permisos del sistema con autenticación básica.",
    version="1.1.0"
)

# ---------------------------------------------------
def fake_jwt_auth(authorization: Optional[str] = Header(None)):
    """
    Simulación de validación de JWT. En producción, usa tu proveedor real de autenticación (p. ej. Keycloak).
    """
    if authorization != "Bearer fake-jwt-token":
        raise HTTPException(status_code=401, detail="No autorizado. Token inválido o ausente.")
    return True

# ---------------------------------------------------
class Rol(BaseModel):
    id: int
    nombre: str
    descripcion: str
    permisos: List[str]

class CrearRolRequest(BaseModel):
    nombre: str = Field(..., description="Nombre del rol")
    descripcion: str = Field(..., description="Descripción del rol")
    permisos: List[str] = Field(..., description="Permisos asociados al rol")

class ActualizarRolRequest(BaseModel):
    nombre: str = Field(..., description="Nombre del rol")
    descripcion: str = Field(..., description="Descripción del rol")
    permisos: List[str] = Field(..., description="Permisos asociados al rol")

class MensajeResponse(BaseModel):
    message: str

class PermisosResponse(BaseModel):
    permisos: List[str]

class RolCreadoResponse(BaseModel):
    id: int
    message: str

class RolEliminadoResponse(BaseModel):
    id: int
    message: str

# ---------------------------------------------------
ROLES = [
    {"id": 1, "nombre": "Admin", "descripcion": "Administrador del sistema", "permisos": ["crear", "leer", "actualizar", "eliminar"]},
    {"id": 2, "nombre": "Editor", "descripcion": "Editor de contenido", "permisos": ["leer", "actualizar"]},
    {"id": 3, "nombre": "Usuario", "descripcion": "Usuario básico", "permisos": ["leer"]}
]

PERMISOS_DISPONIBLES = ["crear", "leer", "actualizar", "eliminar", "exportar"]

# ---------------------------------------------------
# 23) GET /roles
@app.get("/roles", response_model=List[Rol], summary="Lista todos los roles disponibles")
async def listar_roles(autorizacion: bool = Depends(fake_jwt_auth)):
    return ROLES

# 24) POST /roles
@app.post("/roles", response_model=RolCreadoResponse, status_code=201, summary="Crea un nuevo rol")
async def crear_rol(data: CrearRolRequest, autorizacion: bool = Depends(fake_jwt_auth)):
    nombre_normalizado = data.nombre.strip().lower()
    for rol in ROLES:
        if rol["nombre"].strip().lower() == nombre_normalizado:
            raise HTTPException(status_code=409, detail="El nombre del rol ya existe.")
    nuevo_id = max([rol["id"] for rol in ROLES], default=0) + 1
    nuevo_rol = {
        "id": nuevo_id,
        "nombre": data.nombre.strip(),
        "descripcion": data.descripcion.strip(),
        "permisos": data.permisos
    }
    ROLES.append(nuevo_rol)
    return {"id": nuevo_id, "message": "Rol creado correctamente."}

# 25) GET /roles/{id}
@app.get("/roles/{id}", response_model=Rol, summary="Retorna un rol específico por su ID")
async def obtener_rol(id: int = Path(..., description="ID del rol"), autorizacion: bool = Depends(fake_jwt_auth)):
    for rol in ROLES:
        if rol["id"] == id:
            return rol
    raise HTTPException(status_code=404, detail="Rol no encontrado.")

# 26) PUT /roles/{id}
@app.put("/roles/{id}", response_model=MensajeResponse, summary="Actualiza un rol existente")
async def actualizar_rol(
    id: int = Path(..., description="ID del rol a actualizar"),
    data: ActualizarRolRequest = ...,
    autorizacion: bool = Depends(fake_jwt_auth)
):
    nombre_normalizado = data.nombre.strip().lower()
    for rol in ROLES:
        if rol["id"] != id and rol["nombre"].strip().lower() == nombre_normalizado:
            raise HTTPException(status_code=409, detail="El nombre ya está en uso.")
    for rol in ROLES:
        if rol["id"] == id:
            rol.update({
                "nombre": data.nombre.strip(),
                "descripcion": data.descripcion.strip(),
                "permisos": data.permisos
            })
            return {"message": "Rol actualizado correctamente."}
    raise HTTPException(status_code=404, detail="Rol no encontrado.")

# 27) DELETE /roles/{id}
@app.delete("/roles/{id}", response_model=RolEliminadoResponse, summary="Elimina un rol por ID")
async def eliminar_rol(id: int = Path(..., description="ID del rol a eliminar"), autorizacion: bool = Depends(fake_jwt_auth)):
    for rol in ROLES:
        if rol["id"] == id:
            ROLES.remove(rol)
            return {"id": id, "message": "Rol eliminado correctamente."}
    raise HTTPException(status_code=404, detail="Rol no encontrado.")

# 28) GET /roles/permisos
@app.get("/roles/permisos", response_model=PermisosResponse, summary="Lista de permisos disponibles")
async def listar_permisos(autorizacion: bool = Depends(fake_jwt_auth)):
    return {"permisos": PERMISOS_DISPONIBLES}

# ---------------------------------------------------
# Endpoint raíz de prueba
@app.get("/", summary="API de Roles funcionando correctamente")
def read_root():
    return {"message": "API de Roles del sistema lista y operativa."}
