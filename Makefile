
DOCKER_USERNAME ?= alexis
APPLICATION_NAME ?= grammar
OPENAI_API_KEY ?= $(echo $OPENAI_API_KEY)


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

spacy_models: # downloads spacy models
spacy_models:
	python -m spacy download en_core_web_trf
	python -m spacy download fr_core_news_sm
.PHONY: spacy_models




lint: ## formatting with black
lint:
	black ./
.PHONY: lint

import-check: ## checks for unused imports
import-check:
	pylint --disable=all --enable=unused-import ./*py
.PHONY: import-check



build: ## Build docker image
build:
	docker build . --tag ${DOCKER_USERNAME}/${APPLICATION_NAME}:0.1
.PHONY: build

# --env-file .env
run: ## Build, start and run docker image
run:
	docker run --rm -it -v ${PWD}:/app/ \
		--env OPENAI_API_KEY=${OPENAI_API_KEY} --name jubilant_beetle ${DOCKER_USERNAME}/${APPLICATION_NAME}:0.1
.PHONY: run

test: # run test
test:
	pytest -rsa --log-cli-level=INFO 
.PHONY: test

coverage: # test coverage
coverage:
	pytest --cov=./ tests/
.PHONY: coverage

