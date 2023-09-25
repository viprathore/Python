build:
	sudo docker-compose build

start:
	sudo docker-compose up

build-up:
	sudo docker-compose up --build

down:
	sudo docker-compose down 

down-v:
	sudo docker-compose down -v

migrate:
	sudo docker exec -it gym-service-backend  python manage.py migrate

migrations:
	sudo docker exec -it gym-service-backend  python manage.py makemigrations

test:
	sudo docker exec -it gym-service-backend  pytest --nomigrations

shell:
	sudo docker exec -it gym-service-backend  /bin/bash

superuser:
	sudo docker exec -it gym-service-backend python manage.py createsuperuser

init-db:
	sudo docker exec -it gym_service_postgres_1 bash -c "psql -U postgres -c 'CREATE DATABASE gymdb;'"

