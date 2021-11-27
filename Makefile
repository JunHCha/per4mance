dev-up:
	docker-compose -f docker-compose.dev.yml up --build
dev-down:
	docker-compose -f docker-compose.dev.yml down $(args)
dev-shell:
	docker-compose -f docker-compose.dev.yml run --rm per4mance /bin/bash

dev-migrations:
	docker-compose -f docker-compose.dev.yml run --rm per4mance /bin/bash -c "alembic revision --autogenerate"
dev-migrate:
	docker-compose -f docker-compose.dev.yml run --rm per4mance /bin/bash -c "alembic upgrade head"