dev-up:
	docker-compose -f docker-compose.dev.yml up
dev-down:
	docker-compose -f docker-compose.dev.yml down $(args)
dev-shell:
	docker-compose -f docker-compose.dev.yml run --rm per4mance /bin/bash

dev-migrations:
	docker-compose -f docker-compose.dev.yml run --rm per4mance /bin/bash -c "python manage.py makemigrations $(app)"
dev-migrate:
	docker-compose -f docker-compose.dev.yml run --rm per4mance /bin/bash -c "python manage.py migrate $(app)"