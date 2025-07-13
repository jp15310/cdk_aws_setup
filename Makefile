# Makefile for AWS CDK Python project

VENV := .venv
ACTIVATE := source $(VENV)/bin/activate
APP_CMD := --app \"python3 app.py\"

# Default target
.PHONY: help
help:
	@echo "Available targets:"
	@echo "  make init        - Create and activate virtualenv, install requirements"
	@echo "  make upgrade     - Upgrade CDK CLI and Python packages"
	@echo "  make bootstrap   - Bootstrap CDK environment"
	@echo "  make synth       - Synthesize CloudFormation template"
	@echo "  make deploy      - Deploy stack to AWS"
	@echo "  make destroy     - Destroy deployed stack"
	@echo "  make clean       - Remove virtual environment"

init:
	python3 -m venv $(VENV)
	$(ACTIVATE) && pip install --upgrade pip && source .venv/bin/activate && pip install -r requirements.txt

install: $(VIRTUAL_ENV)
	pip install -r requirements.txt

clean:
	[[ -d $(VIRTUAL_ENV) ]] && rm -rf $(VIRTUAL_ENV) || true
	[[ -d .pytest_cache ]] && rm -rf .pytest_cache || true
	[[ -d cdk.out ]] && rm -rf cdk.out || true
	[[ -f .coverage ]] && rm .coverage || true
	[[ -d cfnnag_output ]] && rm -rf cfnnag_output || true

upgrade:
	npm install -g aws-cdk
	@if [ -d "$(VENV)" ]; then rm -rf $(VENV); fi
	python3 -m venv $(VENV)
	$(ACTIVATE) && pip install --upgrade pip && pip install aws-cdk-lib constructs

bootstrap:
	$(ACTIVATE) && cdk bootstrap

synth:
	$(ACTIVATE) && cdk synth --all

diff:
	cdk diff

deploy: test
	$(ACTIVATE) && cdk deploy --all --require-approval never

destroy:
	$(ACTIVATE) && cdk destroy --all --force

test: lint 
	pytest --cov --cov-report term-missing

lint:
	flake8 .