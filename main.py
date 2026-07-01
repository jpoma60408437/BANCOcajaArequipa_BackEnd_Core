"""HOMEBANKING — Backend FastAPI · Banca por Internet Caja Arequipa.

Portal del CLIENTE. Proyecto separado del core bancario; se conecta a la base
PostgreSQL YA EXISTENTE bd_core_financiero (no crea tablas). Corre en el puerto 8002.

Levantar:  uvicorn main:app --reload --port 8002
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.cfg_config import settings
from app.routes import route_auth, route_creditos, route_cuentas, route_operaciones

app = FastAPI(
    title="Banca por Internet Caja Arequipa — Homebanking API",
    description=(
        "Portal del cliente de Banca por Internet de Caja Arequipa. "
        "Solo consultas y operaciones del cliente del portal (dcliente / usuarios_homebanking). "
        "Institución financiera líder en el sistema de cajas municipales del Perú."
    ),
    version="1.0.0",
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://localhost:5174",
        "https://front-caj-aarequipa.vercel.app",
        "https://banc-ocaja-arequipa-front-end.vercel.app",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(route_auth.router)
app.include_router(route_cuentas.router)
app.include_router(route_operaciones.router)
app.include_router(route_creditos.router)  # ⚠️ este paréntesis debería cerrar add_middleware(), pero quedó después de los routers

@app.get("/", tags=["root"])
def raiz():
    return {
        "servicio": "Banca por Internet Caja Arequipa — Homebanking API",
        "version": "1.0.0",
        "estado": "ok",
        "docs": "/docs",
        "puerto": settings.PORT,
        "institucion": "Caja Municipal de Ahorro y Crédito Arequipa",
        "contacto": "servicioalcliente@cajaarequipa.pe",
    }
