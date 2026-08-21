# Arquitectura (capas)
```
scraper/     # fetch + parseo del HTML del BCV
transform/   # validación con Pydantic, normalización
storage/     # repositorio SQLAlchemy, queries de inserción/lectura
utils/       # otras dependencias necesarias, errores personalizados, salidas por consola personalizadas y administración del log del sistema
cli.py       # entrypoint invocado por cron
```