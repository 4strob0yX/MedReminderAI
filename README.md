# MedReminder AI

Sistema inteligente de gestión y recordatorio farmacológico: aplicación móvil Android (Kotlin/Compose) + microservicios backend FastAPI + base de datos MySQL + IA clínica local en Ollama (`medi-clinico`).

## Funciones Principales
- **Registro personalizado:** Cálculo de edad y ajuste de gamificación (racha de días y penalización de honor) según rango etario.
- **Supervisión y Cuidador:** Panel para cuidadores con alertas automáticas inmediatas ante omisiones o posposiciones de medicamentos críticos, y avisos de advertencia en fármacos normales para adultos mayores.
- **Alarmas Nativas:** Notificaciones locales deterministas y alarmas de alta prioridad (`AlarmManager`) independientes de la conectividad a internet.
- **Escáner Inteligente:** Extracción y precarga de recetas médicas mediante modelo de visión multimodal.

## Inicio Rápido

### Backend y Base de Datos
```bash
docker compose up -d --build
```
- API y documentación interactiva: `http://localhost:8000/docs`

### Aplicación Android
- Abrir la carpeta `android/` en Android Studio (ver [`android/SETUP_AUTH.md`](android/SETUP_AUTH.md)).

## Documentación Oficial
En la carpeta [`docs/`](docs/) se encuentran disponibles los manuales institucionales en formato `.docx`:
- **Manual Técnico Oficial:** Arquitectura, especificación formal PEAS, tablas de verdad y lógica proposicional.
- **Manual de Usuario:** Guías paso a paso para el paciente y familiares.
- **Manual de Instalación y Despliegue:** Guía de configuración y puesta en marcha del entorno.
- **Guía de Uso Rápido:** Resumen operativo de acciones frecuentes.

## Estructura del Repositorio
| Directorio | Descripción |
|---|---|
| `android/` | Aplicación móvil nativa Android (Kotlin, Jetpack Compose, MVVM) |
| `backend/` | API REST en FastAPI, servicios de IA clínica, autenticación y esquemas Pydantic |
| `db/mysql/init/` | Scripts de inicialización y definición del esquema relacional DDL (`01_schema.sql`) |
| `docs/` | Manuales oficiales del proyecto (.docx), carátula institucional y capturas |
