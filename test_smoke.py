"""Test de humo para el homebanking de Caja Arequipa.

Valida que la app arranca, el endpoint raíz responde y los routers están registrados.
Ejecutar: pytest test_smoke.py -v
"""
import pytest
from fastapi.testclient import TestClient

# Patch de settings antes de importar la app (para no requerir .env en CI)
import os
os.environ.setdefault("DATABASE_URL", "postgresql://postgres:test@localhost:5432/bd_test")
os.environ.setdefault("SECRET_KEY", "test-secret-key-caja-arequipa-homebanking")

from main import app  # noqa: E402

client = TestClient(app, raise_server_exceptions=False)


def test_raiz():
    resp = client.get("/")
    assert resp.status_code == 200
    data = resp.json()
    assert "Caja Arequipa" in data["servicio"]
    assert data["estado"] == "ok"
    assert "cajaarequipa" in data["contacto"]


def test_docs_disponibles():
    resp = client.get("/docs")
    assert resp.status_code == 200


def test_openapi_json():
    resp = client.get("/openapi.json")
    assert resp.status_code == 200
    spec = resp.json()
    assert "Caja Arequipa" in spec["info"]["title"]


def test_login_sin_body_retorna_422():
    resp = client.post("/auth/login", json={})
    assert resp.status_code == 422


def test_cuentas_sin_token_retorna_401():
    resp = client.get("/cuentas/ahorro")
    assert resp.status_code == 401


def test_creditos_sin_token_retorna_401():
    resp = client.post("/creditos/solicitar", json={})
    assert resp.status_code == 401


def test_operaciones_servicios_sin_token_retorna_401():
    resp = client.get("/operaciones/servicios")
    assert resp.status_code == 401


def test_transferencia_sin_token_retorna_401():
    resp = client.post("/operaciones/transferencia", json={})
    assert resp.status_code == 401
