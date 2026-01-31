import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pathlib import Path

from .routes.readings import router as readings_router
from .routes.settings import router as settings_router
from .routes.reference import router as reference_router

app = FastAPI(
    title="Solar Tracker",
    description="Track your solar panel yield and compare with reference data",
    version="1.0.0"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routes
app.include_router(readings_router)
app.include_router(settings_router)
app.include_router(reference_router)

# Serve frontend static files
frontend_path = Path(__file__).parent.parent / "frontend"

if frontend_path.exists():
    app.mount("/static", StaticFiles(directory=frontend_path), name="static")

    @app.get("/")
    async def serve_frontend():
        return FileResponse(frontend_path / "index.html")

    @app.get("/manifest.json")
    async def serve_manifest():
        return FileResponse(frontend_path / "manifest.json")

    @app.get("/sw.js")
    async def serve_sw():
        return FileResponse(frontend_path / "sw.js", media_type="application/javascript")

@app.get("/api/health")
async def health_check():
    return {"status": "healthy", "app": "Solar Tracker"}
