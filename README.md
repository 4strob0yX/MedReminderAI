# MedReminder AI

Sistema de gestion y recordatorio farmacologico: app Android (Kotlin/Compose) + backend FastAPI + MySQL + Ollama (`medi-clinico`).

## Funciones
- Registro con fecha de nacimiento; racha y penalizacion de honor segun rango de edad.
- Vista de cuidador y alertas (automaticas en medicamentos criticos).
- Alarmas nativas y notificaciones; escaner de recetas con IA local.

## Inicio rapido
```
docker compose up -d --build   # MySQL + API (http://localhost:8000/docs)
```
App Android: abrir `android/` en Android Studio (ver `android/SETUP_AUTH.md`).

## Documentacion
`docs/` contiene los manuales (.docx). Regenerar y validar:
```
python3 scripts/build_all_manuals.py
python3 scripts/verify_solution.py
```

## Estructura del repositorio
| Carpeta | Contenido |
|---|---|
| `android/` | App Android (Kotlin + Compose) |
| `backend/` | API FastAPI (routers, servicios, modelos, esquemas) |
| `db/mysql/init/` | DDL de MySQL (`01_schema.sql`) |
| `busquedas_ia/` | Algoritmos de búsqueda (UCS, heurística) y comparador |
| `docs/` | Manuales `.docx`, portada, infografías, logos y capturas |
| `docs/pdf/` | PDFs de entrega |
| `scripts/` | Generación y verificación de documentos |
