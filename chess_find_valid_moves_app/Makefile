IMAGE_NAME := chess_app
CONTAINER_NAME := chess-app-container
PORT := 8000


# Build the Docker image
build:
	docker build -t $(IMAGE_NAME) .

# Run the Docker container
run:
	docker run -p $(PORT):$(PORT) --name $(CONTAINER_NAME) $(IMAGE_NAME)

# Stop and remove the Docker container
stop:
	docker stop $(CONTAINER_NAME) && docker rm $(CONTAINER_NAME)

# Print the logs of the image
logs:
	docker logs -f $(CONTAINER_NAME)

# Format all Python files using Black and isort
format:
	docker exec -it $(CONTAINER_NAME) black .
	docker exec -it $(CONTAINER_NAME) isort .


.PHONY: build run stop shell logs test