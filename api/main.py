from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from database.db import init_db
from api.routers import health, auth, leads, analytics, admin

app = FastAPI(title="SaaS Lead Automation API",version="1.0.0",description="AI Powered Lead Automation System with Webhook Integration")

@app.on_event("startup")
def startup_event():
    init_db()
    
app.include_router(health.router)

app.include_router(
    auth.router,
    prefix="/api/v1",
    tags=["Auth"]
)

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