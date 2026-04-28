from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from . import api
from .common import env


# MARK: lifespan
@asynccontextmanager
async def lifespan(app: FastAPI):
    # app開始時の初期化処理
    # database.init()

    # app実行中
    yield

    # app終了時の終了処理
    # database.exit()


# MARK: create an app
def create_app(base_url: str = '') -> FastAPI:
    # Create an application instance
    app = FastAPI(lifespan=lifespan, root_path=base_url)

    # CORS対策
    if env.FRONTEND_ORIGIN:
        app.add_middleware(
            CORSMiddleware,
            allow_origins=[env.FRONTEND_ORIGIN],
            allow_credentials=True,
            allow_methods=['*'],
            allow_headers=['*'],
        )

    # Initialize application instance
    app.include_router(api.v1.create_router())

    return app
