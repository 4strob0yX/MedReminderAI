from fastapi import FastAPI

from app.api.routers import auth, health, medicamentos, tratamientos

app = FastAPI(title="MedReminder AI API")

app.include_router(health.router)
app.include_router(auth.router)
app.include_router(medicamentos.router)
app.include_router(tratamientos.router)
