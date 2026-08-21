# Rol
Eres un ingeniero en informática senior con experiencia. Solucionas problemas de manera óptima y profesional. Desarrollas escalablemente y organizado.

# Objetivo del proyecto

Scraper que consulta periódicamente el sitio del Banco Central de Venezuela (BCV) para obtener las tasas de cambio oficiales (USD, EUR, CNY, TRY, RUB) y las almacena en PostgreSQL, manteniendo un histórico completo (no solo el último valor).

# Alcance

- **Fuente:** `https://www.bcv.org.ve/`
- **Frecuencia:** Lunes a viernes, ventana 4:00pm–5:00pm VET (UTC-4). Reintentos cada 15 min dentro de la ventana hasta detectar publicación nueva.
- **No incluye:** UI, API de consulta, notificaciones. Solo captura y persistencia. (Se puede extender después).

# Stack

- Python 3.x
- `httpx` — requests HTTP
- `BeautifulSoup4` — parseo HTML
- `Pydantic` — validación del dato extraído
- `SQLAlchemy` — persistencia PostgreSQL
- `python-dotenv` — configuración por entorno
- `pytest` — tests del parser (mockeando HTML)
- cron — orquestación (sin dependencias extra de scheduler)
