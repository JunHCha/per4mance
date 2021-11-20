# !/bin/bash
poetry install --no-interaction --no-ansi
uvicorn per4mance:app --host 0.0.0.0 --reload
