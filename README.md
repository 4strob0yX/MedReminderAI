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
