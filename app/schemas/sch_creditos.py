"""Schemas pydantic para solicitud de crédito — Caja Arequipa.

Tipos disponibles en Banca por Internet:
  ME = Microempresa  (Crédito Microempresarial)
  CO = Consumo       (Crédito Personal / Quintuplica tu Sueldo / Descuento por Planilla)

Los créditos de Vivienda (MiVivienda, Caja Construye, Hipotecario) requieren
atención presencial en una agencia Caja Arequipa.
"""
from decimal import Decimal
from typing import Literal

from pydantic import BaseModel, Field


class SolicitudCreditoRequest(BaseModel):
    montosolicitud: Decimal = Field(..., gt=0, description="Monto solicitado en Soles")
    plazo: int = Field(..., gt=0, description="Número de cuotas / meses")
    codtipocredito: Literal["ME", "CO"] = Field(
        ...,
        description="ME=Microempresa, CO=Consumo. "
                    "Para créditos de Vivienda acérquese a una agencia Caja Arequipa.",
    )
    codactividadeconomica: str
    montoingresoneto: Decimal = Field(..., ge=0, description="Ingreso neto mensual en Soles")


class SolicitudCreditoResponse(BaseModel):
    mensaje: str
    pksolicitud: int
    codsolicitud: str
    estado: str
    montosolicitud: Decimal
    plazo: int
