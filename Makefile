env ?= docker-compose

run:
	docker compose -f ${env}.yaml up --build

migrate:
	docker compose -f ${env}.yaml exec backend alembic revision --autogenerate -m "migration"

makemigrations:
	docker compose -f ${env}.yaml exec backend alembic upgrade head

populate_vehicles:
	docker compose -f ${env}.yaml exec backend sh -c "python -m populate_vehicles"

