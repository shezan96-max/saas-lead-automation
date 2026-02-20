from fastapi import FastAPI
from api.routers import health, leads, analytics, admin
from fastapi.staticfiles import StaticFiles

app = FastAPI("SaaS Lead Automation API")

app.include_router(health.router)

app.include_router(
    leads.router,
    prefix="/api/v1",
    tags=["Leads"]
)

app.include_router(
    analytics.router,
    prefix="/api/v1",
    tags=["Analytics"]
)

app.include_router(
    admin.router,
    prefix="/api/v1/admin",
    tags=["Admin"]
)

app.mount("/",StaticFiles(directory="frontend",html=True), name="frontend")