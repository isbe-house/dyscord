
export UID=$(shell id -u)
export GID=$(shell id -g)
export HOST_ADDRESS=$(shell hostname -f)
SHELL := /bin/bash

export TWINE_USERNAME=${TWINE_USERNAME:-"UNDEFINED"}
export TWINE_PASSWORD=${TWINE_PASSWORD:-"UNDEFINED"}

up: ## Start all containers
	docker-compose \
        -f  docker-compose.yaml \
        up -d --build dyscord

run: ## Run container connected
	make down
	docker-compose \
		-f  docker-compose.yaml \
		run --rm dyscord

build:
	docker-compose \
		-f docker-compose.yaml \
		build --parallel

rebuild:
	docker-compose \
		-f docker-compose.yaml \
		build --no-cache --parallel

down: ## Stop all containers
	docker-compose \
		-f  docker-compose.yaml \
		down

docs: ## Stop all containers
	docker-compose \
		-f  docker-compose.yaml \
		run --rm --service-ports documentation

build-docs: build
	docker-compose \
		-f  docker-compose.yaml \
		run --rm documentation mkdocs build

logs: ## Display logs (follow)
	docker-compose \
        -f  docker-compose.yaml \
        logs --follow --tail=20 dyscord

clean: ## Delete volumes
	rm -rf .cache .ipynb_checkpoints .mypy_cache .pytest_cache dist .coverage .ipython .jupyter .local .coverage .python_history .bash_history site htmlcov src/dyscord.egg-info
	find . | grep -E \(__pycache__\|\.pyc\|\.pyo\$\) | xargs rm -rf

debug: ## Start interactive python shell to debug with
	docker-compose \
		-f docker-compose.yaml \
		run --rm dyscord-tests /bin/bash
		# run --rm dyscord-tests /bin/bash

jupyter: ## Start a jupyter environment for debugging and such
	docker-compose \
		-f  docker-compose.yaml \
		run --rm jupyter

test: ## Run all tests
	make test-pytest
	make test-mypy
	make test-flake8
	make test-doc-strings
	make test-review

test-pytest:
	docker-compose \
		-f  docker-compose.yaml \
		run --rm dyscord-tests \
		python -m pytest --cov=src --durations=5 -vv --color=yes tests
	docker-compose \
		-f  docker-compose.yaml \
		run --rm dyscord-tests \
		coverage html

test-mypy:
	docker-compose \
		-f  docker-compose.yaml \
		run --rm dyscord-tests \
		mypy --pretty src/dyscord

test-flake8:
	docker-compose \
		-f  docker-compose.yaml \
		run --rm dyscord-tests \
		flake8

test-doc-strings:
	docker-compose \
		-f  docker-compose.yaml \
		run --rm dyscord-tests \
		pydocstyle --add-ignore=D407,D300,D203,D100,D104 --convention=google src

test-review:
	docker-compose \
		-f  docker-compose.yaml \
		run --rm dyscord-tests \
		pip-review

######################################################################################################################################################

dist: clean
	make build-docs

release-test:
	docker-compose \
		-f  docker-compose.yaml \
		run --rm releaser \
		printenv
	# docker-compose \
	# 	-f  docker-compose.yaml \
	# 	run --rm releaser \
	# 	python3 -m build
	# docker-compose \
	# 	-f  docker-compose.yaml \
	# 	run --rm releaser \
	# 	python3 -m twine upload --repository testpypi dist/*

release:
	docker-compose \
		-f  docker-compose.yaml \
		run --rm releaser \
		python3 -m build
	docker-compose \
		-f  docker-compose.yaml \
		run --rm releaser \
		python3 -m twine upload dist/*

######################################################################################################################################################

help:
	@grep -E '^[0-9a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

.DEFAULT_GOAL := help

.PHONY: up down clean populate test build debug run build-docs dist release docs
# .SILENT: test up down up clean
