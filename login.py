from fastapi import FastAPI, HTTPException, Depends, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, EmailStr
from pymongo import MongoClient
from sqlalchemy import create_engine, text
from jose import jwt, JWTError
import requests
import os
import logging
from datetime import datetime

logging.basicConfig(level=logging.INFO)

KEYCLOAK_URL = "http://localhost:8080/auth/realms/mi-realm/protocol/openid-connect/token"
KEYCLOAK_CLIENT_ID = "cliente"
KEYCLOAK_CLIENT_SECRET = "secreto"
SECRET_KEY = "clave-secreta"
ALGORITHM = "HS256"

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# MongoDB
mongo_client = MongoClient("mongodb://localhost:27017")
mongo_db = mongo_client["avisadores"]
mongo_users = mongo_db["usuarios"]

# PostgreSQL
pg_engine = create_engine("postgresql://usuario:password@localhost:5432/avisadores")

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

class OlvidadaRequest(BaseModel):
    email: EmailStr

class ResetRequest(BaseModel):
    reset_token: str
    new_password: str

# Helper para Keycloak (obtiene el token JWT real)
def obtener_token_keycloak(email: str, password: str):
    data = {
        "grant_type": "password",
        "client_id": KEYCLOAK_CLIENT_ID,
        "client_secret": KEYCLOAK_CLIENT_SECRET,
        "username": email,
        "password": password
    }
    response = requests.post(KEYCLOAK_URL, data=data)
    if response.status_code != 200:
        logging.error(f"Keycloak error: {response.text}")
        raise HTTPException(status_code=401, detail="Credenciales inválidas")
    return response.json()

# Endpoint: /auth/login
@app.post("/auth/login", summary="Inicia sesión y retorna un token JWT")
async def login(req: LoginRequest):
    user = mongo_users.find_one({"email": req.email})
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    token_data = obtener_token_keycloak(req.email, req.password)
    return {
        "token": token_data["access_token"],
        "user_id": str(user["_id"]),
        "rol": user.get("rol", "usuario"),
        "expires_at": datetime.utcnow().isoformat()
    }

# Endpoint: /auth/olvidada
@app.post("/auth/olvidada", summary="Envía enlace o código de recuperación al correo")
async def olvidada(req: OlvidadaRequest):
    user = mongo_users.find_one({"email": req.email})
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    reset_token = jwt.encode({"email": req.email}, SECRET_KEY, algorithm=ALGORITHM)
    return {
        "message": "Enlace o código de recuperación enviado al correo",
        "reset_token": reset_token
    }

# Endpoint: /auth/resetear
@app.post("/auth/resetear", summary="Cambia la contraseña utilizando el token")
async def resetear(req: ResetRequest):
    try:
        payload = jwt.decode(req.reset_token, SECRET_KEY, algorithms=[ALGORITHM])
        email = payload.get("email")
    except JWTError:
        raise HTTPException(status_code=403, detail="Token inválido o expirado")

    with pg_engine.connect() as conn:
        conn.execute(
            text("UPDATE usuarios SET password = :p WHERE email = :e"),
            {"p": req.new_password, "e": email}
        )

    return {"message": "Contraseña actualizada correctamente"}

# Endpoint raíz
@app.get("/", summary="Página principal")
def read_root():
    return {"message": "Home"}
