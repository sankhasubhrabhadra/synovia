import os
import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

from app.database.session import init_db
from app.routers.projects import router as projects_router

load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger("synovia")

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Initializing Synovia backend database...")
    await init_db()
    logger.info("Synovia backend successfully started.")
    yield
    logger.info("Shutting down Synovia backend...")

app = FastAPI(
    title="Synovia AI - Autonomous AI Co-Founder API",
    description="Multi-Agent AI system that converts startup ideas into investor-ready blueprints.",
    version="1.0.0",
    lifespan=lifespan
)

# Proper CORS configuration for mobile and web clients
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Dual-mount routes to support both local /api/projects AND Vercel Serverless /projects
app.include_router(projects_router, prefix="/api")
app.include_router(projects_router)

@app.get("/health")
@app.get("/api/health")
async def health_check():
    return {
        "status": "online",
        "service": "Synovia AI Startup Studio",
        "timestamp": os.getenv("ENV", "production")
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
