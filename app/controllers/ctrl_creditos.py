"""Controlador de créditos: solicitar crédito (ME/CO/VI) — Caja Arequipa.

Caja Arequipa ofrece créditos de Consumo, Microempresa y Vivienda (MiVivienda /
Caja Construye / Hipotecario). En el homebanking se permite solicitar Microempresa
y Consumo; los créditos hipotecarios requieren atención presencial en agencia.
"""
from decimal import Decimal

from fastapi import HTTPException, status
from sqlalchemy.engine import Connection

from app.repositories import repo_creditos


def solicitar(
    conn: Connection,
    pkcliente: int,
    montosolicitud: Decimal,
    plazo: int,
    codtipocredito: str,
    codactividadeconomica: str,
    montoingresoneto: Decimal,
) -> dict:
    if codtipocredito not in repo_creditos.MAPA_TIPO_CREDITO:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=(
                "Tipo de crédito no disponible en Banca por Internet. "
                "Use ME (Microempresa) o CO (Consumo). "
                "Para créditos de Vivienda acérquese a una agencia Caja Arequipa."
            ),
        )
    try:
        res = repo_creditos.crear_solicitud(
            conn,
            pkcliente=pkcliente,
            montosolicitud=montosolicitud,
            plazo=plazo,
            codtipocredito=codtipocredito,
            codactividadeconomica=codactividadeconomica,
            montoingresoneto=montoingresoneto,
        )
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

    return {
        "mensaje": "Solicitud registrada exitosamente en Caja Arequipa (En Evaluación)",
        "estado": "En Evaluación",
        "montosolicitud": montosolicitud,
        "plazo": plazo,
        **res,
    }
