# BCV Scraper

[![Tests](https://github.com/xanv754/bcv-rate-tracker/actions/workflows/tests.yml/badge.svg)](https://github.com/xanv754/bcv-rate-tracker/actions/workflows/tests.yml)
[![Scrape](https://github.com/xanv754/bcv-rate-tracker/actions/workflows/scrape.yml/badge.svg)](https://github.com/xanv754/bcv-rate-tracker/actions/workflows/scrape.yml)

Scraper que consulta periódicamente el sitio del Banco Central de Venezuela ([bcv.org.ve](https://www.bcv.org.ve/)) para obtener las tasas de cambio oficiales (USD, EUR, CNY, TRY, RUB) y las almacena en PostgreSQL, manteniendo un histórico completo de cada publicación (no solo el último valor).

Cada corrida queda registrada en `scrape_runs` (éxito, fallo o parcial), lo que da trazabilidad y observabilidad sobre el proceso incluso cuando la extracción falla. Ver [`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md) y [`docs/MODELS.md`](docs/MODELS.md) para el detalle de capas y modelo de datos.

## Instalación

Requiere Python 3.10+ y una base de datos PostgreSQL accesible.

```bash
git clone <repo-url>
cd bcv-rate-tracker
python -m venv .venv
source .venv/bin/activate
pip install .
```

Para correr los tests también es necesario el extra `test`:

```bash
pip install ".[test]"
```

## Variables de entorno

Configúralas en un archivo `.env` en la raíz del proyecto (se carga automáticamente vía `python-dotenv`).

| Variable      | Requerida | Default     | Descripción                       |
| ------------- | :-------: | ----------- | ---------------------------------- |
| `DB_HOST`     | No        | `localhost` | Host del servidor PostgreSQL.      |
| `DB_PORT`     | No        | `5432`      | Puerto del servidor PostgreSQL.    |
| `DB_NAME`     | Sí        | —           | Nombre de la base de datos.        |
| `DB_USER`     | Sí        | —           | Usuario de conexión.               |
| `DB_PASSWORD` | Sí        | —           | Contraseña de conexión.            |
| `DB_SSLMODE`  | No        | —           | Modo SSL de la conexión (ej. `require` para Neon/proveedores gestionados). |

Ejemplo:

```dotenv
DB_HOST=localhost
DB_PORT=5432
DB_NAME=bcv_scraper
DB_USER=postgres
DB_PASSWORD=changeme
```

## Inicializar el proyecto

Con las variables de entorno configuradas, crea las tablas `exchange_rates` y `scrape_runs` (si no existen):

```bash
bcv-scraper init-db
```

## Ejecutar la captura del día

```bash
bcv-scraper run
```

Este comando obtiene el HTML del BCV, valida y normaliza las tasas publicadas, y las persiste en `exchange_rates`. Si el `official_date` ya fue registrado previamente para una divisa, no se reinserta (idempotencia). El resultado de la corrida (éxito, fallo o parcial) queda registrado en `scrape_runs`.

Para la operación periódica en producción, programar `bcv-scraper run` vía `cron` de lunes a viernes en la ventana 4:00pm–5:00pm VET (UTC-4), con reintentos cada 15 minutos hasta detectar una publicación nueva.
