import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.api.routes import router as payment_router
from app.api.internal import router as internal_router
from app.services.async_adapter import broker_adapter

logging.basicConfig(level=logging.INFO)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Connect to RabbitMQ
    await broker_adapter.connect()
    yield
    # Disconnect from RabbitMQ
    await broker_adapter.disconnect()

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    lifespan=lifespan
)

# Add CORS middleware for UI testing
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(payment_router, prefix="/payments", tags=["Public API Component"])
app.include_router(internal_router, prefix="/internal/payments", tags=["Internal API Component"])

@app.get("/health")
async def health_check():
    return {"status": "ok"}
