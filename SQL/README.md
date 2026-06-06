# SQL

Carpeta de datos del backend PharmaTech.

- `pharmatech.sqlite3`: base SQLite usada por `app.py`.
- `schema.sql`: estructura de tablas para recrear la base si hace falta.

Credencial inicial creada automaticamente si no existe:

- Usuario: `admin`
- Clave: `12345`

La app prepara esta carpeta al iniciar. Si encuentra una base vieja en la raiz (`pharmatech.sqlite3`) y no existe la base dentro de `SQL/`, la copia automaticamente.
