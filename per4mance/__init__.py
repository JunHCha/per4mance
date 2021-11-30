from fastapi import FastAPI
from sqlalchemy import create_engine
from sqlalchemy.orm.session import sessionmaker

from per4mance.config import DB_URL, ROOT_PATH

db_engine = create_engine(DB_URL, future=True, echo=True)
db_session = sessionmaker(autocommit=False, autoflush=False, bind=db_engine)


def init_views(app: FastAPI) -> None:
    from per4mance import endpoints

    @app.get("/ping")
    async def ping() -> str:
        return "pong"

    app.include_router(endpoints.router)


def create_app() -> FastAPI:
    app = FastAPI(
        docs_url="/docs",
        openapi_url="/openapi.json",
        root_path=ROOT_PATH,
    )
    init_views(app)

    return app


app = create_app()
