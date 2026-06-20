# Homebanking API — Banca por Internet Caja Arequipa

Backend FastAPI para el portal de **Banca por Internet** de **Caja Municipal de Ahorro y Crédito Arequipa**.  
Institución financiera líder en el sistema de cajas municipales del Perú.

---

## Descripción

Portal del cliente (homebanking). Proyecto **separado del core bancario**; se conecta a la base PostgreSQL ya existente `bd_core_financiero` (no crea tablas propias). Corre en el puerto **8002**.

> El core bancario (personal / asesores) corre en el puerto **8001**.

---

## Funcionalidades disponibles

| Módulo | Endpoint | Descripción |
|---|---|---|
| Auth | `POST /auth/login` | Login con usuario y contraseña → JWT |
| Cuentas ahorro | `GET /cuentas/ahorro` | Listado de cuentas de ahorro |
| Cuentas ahorro | `GET /cuentas/ahorro/{cod}/movimientos` | Últimos movimientos |
| Cuentas ahorro | `GET /cuentas/ahorro/{cod}/detalle` | Detalle por subproducto (PF / CTS / AP) |
| Cuentas crédito | `GET /cuentas/credito` | Créditos vigentes del cliente |
| Cuentas crédito | `GET /cuentas/credito/{cod}/cuotas` | Cronograma de cuotas |
| Operaciones | `POST /operaciones/pago-cuota` | Pago de cuota de crédito |
| Operaciones | `POST /operaciones/transferencia` | Transferencia entre cuentas propias |
| Operaciones | `GET /operaciones/servicios` | Catálogo de servicios afiliados |
| Operaciones | `POST /operaciones/pago-servicio` | Pago de servicios (LUZ, AGUA, SUNAT, AFP…) |
| Créditos | `POST /creditos/solicitar` | Solicitud de crédito Microempresa o Consumo |

**Nota:** Los créditos de Vivienda (MiVivienda, Caja Construye, Hipotecario) requieren atención presencial en una agencia Caja Arequipa.

---

## Requisitos

- Python 3.11+
- PostgreSQL con la base `bd_core_financiero` ya existente

## Instalación

```bash
python -m venv venv
source venv/bin/activate          # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

## Configuración

Copia `.env.example` a `.env` y ajusta los valores:

```bash
cp .env.example .env
```

Variables principales:

```env
DATABASE_URL=postgresql://postgres:TU_PASSWORD@localhost:5432/bd_core_financiero
SECRET_KEY=una-clave-larga-y-aleatoria
ACCESS_TOKEN_EXPIRE_MINUTES=480
PORT=8002
CORS_ORIGINS=http://localhost:5173,http://localhost:5174
```

## Levantar el servidor

```bash
uvicorn main:app --reload --port 8002
```

Documentación interactiva: [http://localhost:8002/docs](http://localhost:8002/docs)

## Tests

```bash
pytest test_smoke.py -v
```

---

## Contacto institucional

- **Web:** https://www.cajaarequipa.pe
- **Banca por Internet:** https://www.cajaarequipa.pe/banca-por-internet/
- **Email:** servicioalcliente@cajaarequipa.pe
- **Teléfono:** (51)(54) 380670
- **App móvil:** Caja Arequipa Móvil (Android / iOS)

---

*Caja Municipal de Ahorro y Crédito Arequipa — Más cerca, más fácil, más rápido.*
