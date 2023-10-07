.DEFAULT_GOAL := up
MAIN_SERVICE_NAME := app

build:
	docker compose build

up:
	docker compose up

up-d:
	docker compose up -d

stop:
	docker compose stop

down:
	docker compose down

run-tests:
	docker compose run --rm -e TESTING=true $(MAIN_SERVICE_NAME) pytest -v --cov --cov-report term tests/

deploy:
	$(MAKE) down
	docker network create mynetwork || true
	$(MAKE) build
	$(MAKE) up-d

db-restore:
	docker compose run --rm $(MAIN_SERVICE_NAME) python scripts/restore_data.py
