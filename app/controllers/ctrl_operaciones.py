"""Controlador de operaciones: pago de cuota, transferencia y pago de servicios — Caja Arequipa.

Servicios afiliados reconocidos por Caja Arequipa en su plataforma de pagos.
"""
from decimal import Decimal

from fastapi import HTTPException, status
from sqlalchemy.engine import Connection

from app.repositories import repo_cuentas, repo_operaciones


# Catálogo de servicios disponibles en Banca por Internet Caja Arequipa.
# (Refleja los servicios afiliados publicados en la plataforma digital de la institución.)
SERVICIOS = [
    {"codservicio": "LUZ",    "nombre": "Electricidad (SEAL / ELECTROSUR)"},
    {"codservicio": "AGUA",   "nombre": "Agua potable y alcantarillado (SEDAPAR)"},
    {"codservicio": "TEL",    "nombre": "Telefonía / Internet"},
    {"codservicio": "CABLE",  "nombre": "TV por cable"},
    {"codservicio": "GAS",    "nombre": "Gas natural (Cálidda / Contugas)"},
    {"codservicio": "MUNI",   "nombre": "Arbitrios municipales (MPA)"},
    {"codservicio": "SUNAT",  "nombre": "SUNAT — Tributos y multas"},
    {"codservicio": "AFP",    "nombre": "AFP — Aportes previsionales"},
    {"codservicio": "SEGURO", "nombre": "Seguro (SOAT / Vida)"},
]
_SERVICIOS_POR_COD = {s["codservicio"]: s for s in SERVICIOS}


def listar_servicios() -> list[dict]:
    return SERVICIOS


def pago_cuota(
    conn: Connection,
    pkcliente: int,
    codcuentacredito: str,
    monto: Decimal | None,
    cuenta_origen: str | None = None,
) -> dict:
    credito = repo_cuentas.buscar_cuenta_credito(conn, codcuentacredito)
    if credito is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Crédito no encontrado")
    if credito["pkcliente"] != pkcliente:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="El crédito no pertenece al cliente"
        )
    if credito.get("pkagencia") is None or credito.get("pkmoneda") is None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="El crédito no tiene datos vigentes en la cartera del periodo",
        )
    if monto is not None and monto <= 0:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="El monto debe ser > 0")

    origen = None
    if cuenta_origen:
        origen = repo_cuentas.buscar_cuenta_ahorro(conn, cuenta_origen)
        if origen is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Cuenta de ahorro origen no encontrada"
            )
        if origen["pkcliente"] != pkcliente:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="La cuenta de ahorro origen no pertenece al cliente",
            )

    try:
        res = repo_operaciones.pagar_cuota(conn, credito, monto, origen)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))

    return {
        "mensaje": "Pago de cuota registrado en Caja Arequipa"
                   + (" (debitado de ahorro)" if origen else ""),
        "codcuentacredito": codcuentacredito,
        "cuenta_origen": cuenta_origen.strip() if cuenta_origen else None,
        **res,
    }


def pago_servicio(
    conn: Connection,
    pkcliente: int,
    cuenta_origen: str,
    codservicio: str,
    codsuministro: str,
    monto: Decimal,
) -> dict:
    servicio = _SERVICIOS_POR_COD.get(codservicio.upper())
    if servicio is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Servicio '{codservicio}' no válido. Consulte GET /operaciones/servicios.",
        )
    origen = repo_cuentas.buscar_cuenta_ahorro(conn, cuenta_origen)
    if origen is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Cuenta de ahorro origen no encontrada"
        )
    if origen["pkcliente"] != pkcliente:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="La cuenta de ahorro no pertenece al cliente"
        )
    if origen["saldo"] is None or origen["saldo"] < monto:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="Saldo insuficiente en la cuenta de ahorro"
        )

    res = repo_operaciones.pagar_servicio(
        conn, origen, servicio["nombre"], codsuministro.strip(), monto
    )
    return {
        "mensaje": "Pago de servicio registrado en Caja Arequipa",
        "servicio": servicio["nombre"],
        "codsuministro": codsuministro.strip(),
        "cuenta_origen": cuenta_origen.strip(),
        "monto": monto,
        **res,
    }


def transferencia(
    conn: Connection,
    pkcliente: int,
    cuenta_origen: str,
    cuenta_destino: str,
    monto: Decimal,
) -> dict:
    if cuenta_origen.strip() == cuenta_destino.strip():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="La cuenta origen y destino no pueden ser la misma",
        )

    origen = repo_cuentas.buscar_cuenta_ahorro(conn, cuenta_origen)
    destino = repo_cuentas.buscar_cuenta_ahorro(conn, cuenta_destino)
    if origen is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Cuenta origen no encontrada")
    if destino is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Cuenta destino no encontrada")

    if origen["pkcliente"] != pkcliente or destino["pkcliente"] != pkcliente:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Ambas cuentas deben pertenecer al cliente",
        )
    if origen["saldo"] is None or origen["saldo"] < monto:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="Saldo insuficiente en la cuenta origen"
        )

    res = repo_operaciones.transferir(conn, origen, destino, monto)
    return {
        "mensaje": "Transferencia registrada en Caja Arequipa",
        "cuenta_origen": cuenta_origen.strip(),
        "cuenta_destino": cuenta_destino.strip(),
        "monto": monto,
        **res,
    }
