import asyncio

from fastapi import FastAPI

from app.builder import Application
from app.rabbitmq_service.consumer import start_consumer
from app.rabbitmq_service.producer import start_producer


def get_app() -> FastAPI:
    application = Application()
    build = application.build_application()
    return build.app


app = get_app()


@app.on_event("startup")
async def startup_event():
    asyncio.create_task(start_producer())
    asyncio.create_task(start_consumer())
