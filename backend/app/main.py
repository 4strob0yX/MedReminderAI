from fastapi import FastAPI

from app.api.routers import auth, health

app = FastAPI(title="MedReminder AI API")

app.include_router(health.router)
app.include_router(auth.router)
