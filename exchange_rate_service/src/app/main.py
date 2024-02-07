from fastapi import FastAPI

from app.builder import Application


def get_app() -> FastAPI:
    application = Application()
    build = application.build_application()
    return build.app


app = get_app()
