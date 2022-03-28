import logging

import brotli
from aiokafka import AIOKafkaProducer
from fastapi import FastAPI, APIRouter, Query
from app.config import get_settings

log = logging.getLogger("uvicorn")

router = APIRouter(prefix="/kafka_producer")


async def compress(message: str) -> bytes:

    return brotli.compress(
        bytes(message, get_settings().file_encoding),
        quality=get_settings().file_compression_quality,
    )


@router.post("/")
async def produce_message(message: str = Query(...)) -> dict:
    return await producer.send_and_wait("jobs", await compress(message))


def create_application() -> FastAPI:
    """Create FastAPI application and set routes.

    Returns:
        FastAPI: The created FastAPI instance.
    """

    application = FastAPI(openapi_url="/kafka_producer/openapi.json", docs_url="/kafka_producer/docs")
    application.include_router(router, tags=["producer"])
    return application


def create_producer() -> AIOKafkaProducer:

    return AIOKafkaProducer(
        bootstrap_servers=get_settings().kafka_instance,
    )


app = create_application()
producer = create_producer()


@app.on_event("startup")
async def startup_event():
    """Start up event for FastAPI application."""
    log.info("Starting up...")
    await producer.start()


@app.on_event("shutdown")
async def shutdown_event():
    """Shutdown event for FastAPI application."""

    log.info("Shutting down...")
    await producer.stop()
