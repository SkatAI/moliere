
DOCKER_USERNAME ?= alexis
APPLICATION_NAME_PROD ?= moliere
APPLICATION_NAME_DEV ?= moliere_dev

define find.functions
	@fgrep -h "##" $(MAKEFILE_LIST) | fgrep -v fgrep | sed -e 's/\\$$//' | sed -e 's/##//'
endef

help:
	@echo 'The following commands can be used.'
	@echo ''
	$(call find.functions)
.PHONY: help

init: ## Sets up environment and installs requirements
init:
	pip install -r requirements.txt
.PHONY: init

install: ## dependencies for local dev: black, ...
install: init
	pip install --upgrade pip
	pip install black

lint: ## formatting with black
lint:
	black --line-length 120 ./
.PHONY: lint

import-check: ## checks for unused imports
import-check:
	pylint --disable=all --enable=unused-import ./*py
.PHONY: import-check


build_dev: ## Build docker image
build_dev:
	docker build ./Dockerfile.dev --tag ${DOCKER_USERNAME}/${APPLICATION_NAME_DEV}:0.1
.PHONY: build


build: ## Build docker image
build:
	docker build . --tag ${DOCKER_USERNAME}/${APPLICATION_NAME_PROD}:0.1
.PHONY: build


run: ## Build, start and run docker image
run:
	docker run --rm -it -p 8501:8501 -v ${PWD}:/app/ --name facetious-sganarelle ${DOCKER_USERNAME}/${APPLICATION_NAME_PROD}:0.1
.PHONY: run

run_dev: ## Build, start and run docker image
run_dev:
	docker run --rm -it -p 8501:8501 -v ${PWD}:/app/ --name facetious-sganarelle ${DOCKER_USERNAME}/${APPLICATION_NAME_PROD}:0.1
.PHONY: run

test: # run test
test:
	pytest -rsa --log-cli-level=INFO
.PHONY: test

coverage: # test coverage
coverage:
	pytest --cov=./ tests/
.PHONY: coverage
