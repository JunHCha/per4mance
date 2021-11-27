from fastapi import FastAPI
from sqlalchemy.orm.session import sessionmaker
from sqlalchemy import create_engine
from per4mance.config import ROOT_PATH, DB_URL


db_engine = create_engine(DB_URL, future=True, echo=True)
db_session = sessionmaker(autocommit=False, autoflush=False, bind=db_engine)


def init_views(app: FastAPI) -> None:
    @app.get("/ping")
    async def ping() -> str:
        return "pong"


def create_app() -> FastAPI:
    app = FastAPI(
        docs_url="/docs",
        openapi_url="/openapi.json",
        root_path=ROOT_PATH,
    )
    init_views(app)

    return app


app = create_app()
