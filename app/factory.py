from contextlib import asynccontextmanager
from typing import AsyncGenerator
from fastapi import FastAPI
from app.middleware.middleware import catch_exceptions_middleware
from app.routers import routers
from app.config.config import config
from fastapi.middleware.cors import CORSMiddleware

__all__ = ("create_app",)


def create_app() -> FastAPI:
    async def app_startup(application: FastAPI) -> None:
        print("程序开始启动.")

    async def app_shutdown(application: FastAPI) -> None:
        print("程序开始停止.")

    @asynccontextmanager
    async def lifespan(application: FastAPI) -> AsyncGenerator:
        await app_startup(application=application)
        yield
        await app_shutdown(application=application)

    app: FastAPI = FastAPI(
        title=config.app.title,
        description=config.app.description,
        version=config.app.version,
        lifespan=lifespan
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # app.middleware("http")(catch_exceptions_middleware)

    for router in routers:
        app.include_router(router=router)

    return app
