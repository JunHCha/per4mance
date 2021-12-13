from typing import Any, Dict

import click
from alembic.config import Config

from per4mance import config


@click.group()
def cli() -> None:
    pass


@cli.command(help="Make model migrations")
@click.option("-m", help="Migration message")
def makemigrations(m: str = None) -> None:
    from alembic.command import revision

    alembic_ini_path = "./alembic.ini"
    alembic_cfg = Config(alembic_ini_path)
    alembic_cfg.set_main_option("db_url", config.DB_URL)

    kwargs: Dict[str, Any] = {"autogenerate": True}
    if m is not None:
        kwargs["message"] = m

    revision(alembic_cfg, **kwargs)


@cli.command(help="Apply migrations to database")
def migrate() -> None:
    from alembic.command import upgrade

    alembic_ini_path = "./alembic.ini"
    alembic_cfg = Config(alembic_ini_path)
    alembic_cfg.set_main_option("sqlalchemy.url", config.DB_URL)

    upgrade(alembic_cfg, "head")


@cli.command(help="Revert recent migration")
@click.argument("revision", default="-1")
def downgrade(revision: str) -> None:
    from alembic.command import downgrade

    alembic_ini_path = "./alembic.ini"
    alembic_cfg = Config(alembic_ini_path)
    alembic_cfg.set_main_option("db_url", config.DB_URL)

    downgrade(alembic_cfg, revision)


if __name__ == "__main__":
    cli()
