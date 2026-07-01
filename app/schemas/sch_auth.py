"""Schemas pydantic para autenticación — Caja Arequipa."""
from pydantic import BaseModel, Field


class LoginRequest(BaseModel):
    numerodni: str = Field(..., examples=["11111111"])
    password: str = Field(..., examples=["demo1234"])


class ClienteInfo(BaseModel):
    codcliente: str
    nombre: str
    pkcliente: int


class LoginResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    expires_in_min: int
    cliente: ClienteInfo
