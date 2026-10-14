from fastapi import FastAPI

from app.api.routers import (
    alergias,
    auth,
    contactos,
    health,
    medicamentos,
    recordatorios,
    tratamientos,
)

app = FastAPI(title="MedReminder AI API")

app.include_router(health.router)
app.include_router(auth.router)
app.include_router(medicamentos.router)
app.include_router(tratamientos.router)
app.include_router(recordatorios.router)
app.include_router(alergias.router)
app.include_router(contactos.router)
