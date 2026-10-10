# MedReminder AI: contexto del proyecto

> Documento para retomar el trabajo en otra maquina o conversacion. Leer completo antes de generar codigo.

## Rol y modo de trabajo
- Rol del asistente: Ingeniero Arquitecto (Senior Full-Stack y Android).
- Las decisiones del Tech Lead son vinculantes. Ante ambiguedad, preguntar antes de asumir.
- Pedir confirmacion antes de cambios de alcance. Responder en espanol, de forma concisa.

## Producto
Sistema de gestion y seguimiento de medicamentos. UX/UI de carga cognitiva minima y cero tolerancia a errores tactiles (botones >= 56dp, deshabilitar mientras carga, evitar doble toque).

## Stack aprobado
| Capa | Tecnologia |
|---|---|
| Movil | Kotlin nativo, Jetpack Compose, MVVM (vistas pasivas, logica en ViewModels) |
| Backend | Python, FastAPI (REST) |
| Persistencia primaria | MySQL (modelo E-R estricto) |
| Persistencia secundaria | MongoDB, solo logs de actividad del backend |
| Entorno | Docker Compose (mysql, mongo, api; perfil `tools`: adminer, mongo-express) |

## Restriccion absoluta
Prohibido en el MVP: IA, NLP, reconocimiento de voz. Es un sistema transaccional y de notificaciones.

## Alcance del MVP (hito 28 de octubre)
1. Autenticacion de pacientes.
2. CRUD de Medicamentos y Tratamientos.
3. Generacion automatica de recordatorios en el backend.
4. Notificaciones locales en Android.
5. Registro de tomas (Tomado, Pospuesto, Omitido) en el historial.

Prioridad si hay riesgo de tiempo: auth, CRUD, recordatorios, alarmas locales, historial.

## Decisiones arquitectonicas del Tech Lead
**Notificaciones**
- 100 % locales. Sin FCM.
- `AlarmManager.setExactAndAllowWhileIdle` dispara; `WorkManager` solo sincroniza.
- Permisos: `POST_NOTIFICATIONS` y `SCHEDULE_EXACT_ALARM`. Si se deniegan, banner fijo bloqueante.
- Pendiente de implementar: receiver de `BOOT_COMPLETED` para reprogramar alarmas.

**Modo offline restringido**
- La app cachea en memoria los recordatorios del dia. Sin Room ni colas de sincronizacion.
- Si "Tomado" falla por falta de red: Snackbar de error y la UI no se actualiza hasta recibir 200 OK.

**Posponer**
- Valor fijo de 30 minutos, maximo 2 veces.
- Al tercer intento o al expirar el tiempo, el backend registra "Omitido" (timeout automatico).
- El endpoint de posponer: (1) inserta fila `pospuesto` en `historial_toma`, (2) suma 30 min a `recordatorio.hora_programada`, (3) suma 1 a `veces_pospuesto` y mantiene el estado `pendiente`.

**Horarios**
- El backend manda: FastAPI calcula todos los timestamps en UTC y los entrega pre-calculados.
- El frontend solo convierte a la zona horaria local y programa el `AlarmManager`.

**Historial**
- `historial_toma` es un log de auditoria, sin `UNIQUE(id_recordatorio)`.
- Ejemplo: 2 pospuestos + 1 tomado = 3 filas para el mismo recordatorio.

**Seguridad (obligatorio)**
- Contrasenas con bcrypt (passlib). Tokens JWT con PyJWT.
- UTC en MySQL. HTTPS en produccion.
- Secretos fuera del repo (`.env`).

## Estructura del repositorio
```
docker-compose.yml, .env.example
backend/   FastAPI (api/routers, services, schemas, models, core, db)
db/mysql/init/01_schema.sql   DDL final (se aplica al crear el volumen)
android/   app Kotlin (data, di, ui) y SETUP_AUTH.md
```

## Estado actual
**Hecho**
- Esquema MySQL final (`fecha_fin`, `veces_pospuesto`, `notas`, indices).
- Backend Auth: `POST /auth/register`, `POST /auth/login`, `GET /auth/me`.
- Esqueleto Android de Auth: Login/Registro en Compose, Retrofit, token cifrado.
- Stack Docker definido.

**Sin verificar**
- Nada se ha ejecutado aun. Docker no corrio en Windows (faltaba WSL2). Probar en Mac:
  `docker compose down -v && docker compose up -d --build`, luego `/health/db` y `/docs`.
- El codigo Android no se ha compilado (no existe aun el proyecto Gradle).

**Pendiente**
- `/auth/refresh` y renovacion automatica en Android al recibir 401.
- Proyecto Gradle base y navegacion (Home).
- CRUD de medicamentos y tratamientos.
- Generacion de recordatorios y endpoint de posponer/tomar/omitir.
- Alarmas locales, permisos y banner bloqueante.
- Logs de actividad en MongoDB.
- Mover `usesCleartextTraffic` a `src/debug` antes de release.
- Agregar `.gitattributes` (`* text=auto eol=lf`).
