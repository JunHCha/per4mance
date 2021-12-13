# !/bin/bash
poetry install --no-interaction --no-ansi
python manage.py migrate
uvicorn --factory per4mance:create_app --host 0.0.0.0 --reload
