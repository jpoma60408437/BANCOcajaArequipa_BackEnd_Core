"""Dependencia FastAPI para validar el JWT del cliente — Banca por Internet Caja Arequipa."""
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError

from app.core.cfg_security import decodificar_token

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


def get_cliente(token: str = Depends(oauth2_scheme)) -> dict:
    """Decodifica el JWT y devuelve el payload del cliente autenticado.

    Lanza 401 si el token es inválido o no corresponde a un cliente Caja Arequipa.
    """
    credenciales_exc = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="No autenticado o sesión expirada. Inicie sesión nuevamente en Banca por Internet Caja Arequipa.",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = decodificar_token(token)
    except JWTError:
        raise credenciales_exc

    if payload.get("tipo") != "cliente":
        raise credenciales_exc

    return payload
