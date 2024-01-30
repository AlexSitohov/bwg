from fastapi import FastAPI

from app.builder import Application
from app.db.connection import configure_engine


def get_app() -> FastAPI:
    engine = configure_engine()
    application = Application(engine).build_application().app
    return application


app = get_app()
