
export UID=$(shell id -u)
export GID=$(shell id -g)
export HOST_ADDRESS=$(shell hostname -f)

# up: ## Start all containers
# 	docker-compose \
#                 -f  docker-compose.yaml \
#                 up -d --build simple-discord

run: build ## Run container connected
	docker-compose \
                -f  docker-compose.yaml \
                run --rm simple-discord
#         # Add -d to the up part later

build:
	docker-compose \
                -f docker-compose.yaml \
                build

down: ## Stop all containers
	docker-compose \
                -f  docker-compose.yaml \
                down

# logs: ## Display logs (follow)
# 	docker-compose \
#                 -f  docker-compose.yaml \
#                 logs --follow --tail=20

clean: ## Delete volumes
	docker system prune -f
	rm -rf .cache .ipynb_checkpoints .mypy_cache .pytest_cache dist .coverage .ipython .jupyter .local .coverage

debug: ## Start interactive python shell to debug with
	docker-compose \
                -f docker-compose.yaml \
                run --rm simple-discord /bin/bash

# start-debian: build ## Start interactive python shell to debug with
# 	docker-compose \
#                 -f docker-compose.yaml \
#                 run --rm debian /bin/bash
jupyter: ## Start a jupyter environment for debugging and such
	docker-compose \
                -f tools/jupyter/docker-compose.yaml \
                build
	docker-compose \
                -f  tools/jupyter/docker-compose.yaml \
                run --rm simple-discord-jupyter

test: ## Run all tests
	make build
	docker system prune -f
	docker-compose \
                -f  docker-compose.yaml \
                run --rm simple-discord-tests \
                python -m pytest --cov=src --durations=5 -vv --color=yes tests
	docker-compose \
                -f  docker-compose.yaml \
                run --rm simple-discord-tests \
                mypy src/simple_discord
	docker-compose \
                -f  docker-compose.yaml \
                run --rm simple-discord-tests \
                flake8


######################################################################################################################################################

help:
	@grep -E '^[0-9a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

.DEFAULT_GOAL := help

.PHONY: up down clean populate test build debug run