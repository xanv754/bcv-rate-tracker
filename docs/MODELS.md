
# Modelo de datos

**`exchange_rates`**
| Campo           | Tipo                 | Razón                                                                                                                                                      |
| --------------- | -------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `id`            | `SERIAL PRIMARY KEY` | `----`                                                                                                                                                     |
| `currency`      | `VARCHAR(3)`         | BCV publica varias tasas (USD, EUR, CNY, TRY, RUB). No asumas que solo es USD.                                                                             |
| `rate`          | `NUMERIC(18,8)`      | Nunca uses `FLOAT` para dinero, pierdes precisión. `NUMERIC` es obligatorio aquí.                                                                          |
| `official_date` | `DATE`               | La fecha que el BCV indica como vigente (suele estar en la misma página, distinta del día del scraping).                                                   |
| `scraped_at`    | `TIMESTAMPTZ`        | Cuándo tu bot capturó el dato. Diferenciar `official_date` de `scraped_at` es clave: el BCV a veces publica la tasa un día antes de que entre en vigencia. |

**Restricción importante:** `UNIQUE (currency, official_date)` — evita duplicados si corres el scraper varias veces el mismo día (el cron puede fallar y reintentar).

**`scrape_runs`**
| Campo               | Tipo                                    | Razón                                                                                                                                                                                                                  |
| ------------------- | --------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `id`                | `SERIAL PRIMARY KEY`                    | `----`                                                                                                                                                                                                                 |
| `started_at`        | `TIMESTAMPTZ`                           | Inicio de toda la operación.                                                                                                                                                                                           |
| `started_at`        | `TIM ESTAMPTZ`                          | Finalización de toda la operación.                                                                                                                                                                                     |
| `status`            | `ENUM ('success', 'failed', 'partial')` | Estatus de la operación finalizada.                                                                                                                                                                                    |
| `source_url`        | `TEXT`                                  | Trazabilidad — de dónde vino exactamente.                                                                                                                                                                              |
| `raw_html_snapshot` | `TEXT` o `NULL`                         | Opcional pero recomendado: guarda el fragmento HTML crudo del que extrajiste el dato. Si el BCV cambia el diseño y tu selector falla silenciosamente, tienes evidencia para debuggear sin volver a scrapear el pasado. |
| `error_message`    | `TEXT` o `NULL`                         | Mensaje de error si la operación falla total o parcialmente.                                                                                                                                                           |

- Da observabilidad: detectar fallos o cambios de estructura del sitio.

# Anotaciones del sistema

- Nunca usar `FLOAT` para `rate` — siempre `NUMERIC`.
- Cada corrida debe registrar su resultado en `scrape_runs`, incluso si falla.
- Si el `official_date` extraído ya existe en BD, no reinsertar (idempotencia).
- Selector HTML del BCV puede romperse sin aviso — capturar excepción de parseo, loggear, y marcar el `scrape_run` como `failed` en vez de crashear el proceso.
- Zona horaria del cron: configurar explícitamente en VET, no asumir el timezone del servidor.
- Tests obligatorios sobre el parser antes de tocar la capa de storage.