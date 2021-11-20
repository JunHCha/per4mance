from fastapi import FastAPI
from per4mance.config import ROOT_PATH


def init_views(app: FastAPI) -> None:
    @app.get("/ping")
    async def ping() -> str:
        return 'pong'


def create_app() -> FastAPI:
    app = FastAPI(
        docs_url="/docs",
        openapi_url="/openapi.json",
        root_path=ROOT_PATH,
    )
    init_views(app)

    return app


app = create_app()
