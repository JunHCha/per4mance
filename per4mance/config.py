import os


def get_env(key: str, default: str = None, optional: bool = False) -> str:
    env = os.getenv(key, default)
    if not optional and env is None:
        raise KeyError(f"It requires '{key}' env variable")
    return env


ROOT_PATH = get_env("ROOT_PATH", "")
