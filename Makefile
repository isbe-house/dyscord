
export UID=$(shell id -u)
export GID=$(shell id -g)
export HOST_ADDRESS=$(shell hostname -f)
SHELL := /bin/bash

# up: ## Start all containers
# 	docker-compose \
#         -f  docker-compose.yaml \
#         up -d --build simple-discord

run: ## Run container connected
	make down
	docker-compose \
        -f  docker-compose.yaml \
        run --rm simple-discord

build:
	docker-compose \
        -f docker-compose.yaml \
        build

down: ## Stop all containers
	docker-compose \
        -f  docker-compose.yaml \
        down

docs: build build-docs ## Stop all containers
	docker-compose \
        -f  docker-compose.yaml \
        run --rm --service-ports documentation

build-docs: build
	docker-compose \
        -f  docker-compose.yaml \
        run --rm documentation mkdocs build

# logs: ## Display logs (follow)
# 	docker-compose \
#         -f  docker-compose.yaml \
#         logs --follow --tail=20

clean: ## Delete volumes
	docker system prune -f
	rm -rf .cache .ipynb_checkpoints .mypy_cache .pytest_cache dist .coverage .ipython .jupyter .local .coverage .python_history .bash_history site htmlcov src/simple_discord.egg-info
	find . | grep -E \(__pycache__\|\.pyc\|\.pyo\$\) | xargs rm -rf
	rm -rf src/simple_discord_jmurrayufo.egg-info

debug: ## Start interactive python shell to debug with
	docker-compose \
        -f docker-compose.yaml \
        run --rm simple-discord-tests /bin/bash
        # run --rm simple-discord-tests /bin/bash

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
	make test-pytest
	make test-mypy
	make test-flake8
#	make test-doc-strings
	make test-review

test-pytest:
	docker-compose \
        -f  docker-compose.yaml \
        run --rm simple-discord-tests \
        python -m pytest --cov=src --durations=5 -vv --color=yes tests
	docker-compose \
        -f  docker-compose.yaml \
        run --rm simple-discord-tests \
        coverage html

test-mypy:
	docker-compose \
        -f  docker-compose.yaml \
        run --rm simple-discord-tests \
        mypy src/simple_discord

test-flake8:
	docker-compose \
        -f  docker-compose.yaml \
        run --rm simple-discord-tests \
        flake8

test-doc-strings:
	docker-compose \
        -f  docker-compose.yaml \
        run --rm simple-discord-tests \
        pydocstyle --add-ignore=D407,D300,D203,D100,D104 --convention=google src

test-review:
	docker-compose \
        -f  docker-compose.yaml \
        run --rm simple-discord-tests \
        pip-review

######################################################################################################################################################

dist: clean
	make build-docs

release-test: dist
	docker-compose \
        -f  docker-compose.yaml \
        run --rm releaser \
        python3 -m build
	docker-compose \
        -f  docker-compose.yaml \
        run --rm releaser \
        python3 -m twine upload --repository testpypi dist/*

release:
	echo "${TWINE_USERNAME}"

######################################################################################################################################################

help:
	@grep -E '^[0-9a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

.DEFAULT_GOAL := help

.PHONY: up down clean populate test build debug run doc-strings build-docs dist release
# .SILENT: test up down up clean
