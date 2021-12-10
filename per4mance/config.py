import os


def get_env(key: str, default: str = None, optional: bool = False) -> str:
    env = os.getenv(key, default)
    if not optional and env is None:
        raise KeyError(f"It requires '{key}' env variable")
    return env


ROOT_PATH = get_env("ROOT_PATH", "")
DB_USER = get_env("DB_USER")
DB_PASSWORD = get_env("DB_PASSWORD")
DB_HOST = get_env("DB_HOST")
DB_NAME = get_env("DB_NAME")
DB_URL = f"postgresql+asyncpg://{DB_USER}:{DB_PASSWORD}@db/per4mance"
