.DEFAULT_GOAL := up
SERVICE_NAME := app

build:
	docker network create my_network || true
	docker-compose build

up:
	docker-compose up $(SERVICE_NAME)

stop:
	docker-compose stop

down:
	docker-compose down

tests:
	echo WIP
