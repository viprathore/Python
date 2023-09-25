
# Gym Service
This is an application for gym athletes.
This repository contains backend API's for various operation performed by an athletes.
And these API's can be consumed by the frontend developers.

## Tech stack used
- python 3.8
- django 4.1
- django rest framework
- postgres
- docker and docker-compose
- pytest

## Linting tools
- black
- isort

## Setup project locally
- install docker and docker compose
- go to the project directory in terminal
- run the following commands from terminal
- `make build`
- `make start`

## Use this postman collection to access all API's
- `https://www.postman.com/collections/790a4b5777506cd13e85`
- Some of the operations are only perform by admin such as (creation/updation/deletion) of   (gym, equipments, exercises)

## To access django admin site
- run the below command from terminal 
- `make superuser` and create user
- go to this url in browser `http://127.0.0.1:8000/admin/` and login with created user credentials

## Run tests locally
- `make test`