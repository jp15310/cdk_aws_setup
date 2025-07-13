# Makefile for AWS CDK Python project
SHELL = /bin/bash -c
VENV := .venv
ACTIVATE := source $(VENV)/bin/activate
VIRTUAL_ENV = $(PWD)/.venv
export BASH_ENV=$(VENV)/bin/activate

$(VIRTUAL_ENV):
	python3 -m venv $(VIRTUAL_ENV)

.DEFAULT: help

help:
	@echo "Available targets:"
	@echo "  make install     - Createe virtualenv, install requirements"
	@echo "  make clean       - Clean virtual environment"
	@echo "  make kill        - Remove virtual environment"
	@echo "  make upgrade     - Upgrade CDK CLI and Python packages"
	@echo "  make bootstrap   - Bootstrap CDK environment"
	@echo "  make synth       - Synthesize CloudFormation template"
	@echo "  make diff        - Perform a diff to see infrastructure changes between AWS CDK stacks"
	@echo "  make deploy      - Deploy stack to AWS"
	@echo "  make destroy     - Destroy deployed stack"
	@echo "  make test.       - Execute test harness"
	@echo "  make lint        - Validate python code structure using flake8"

install: $(VIRTUAL_ENV)
	pip install --upgrade pip && pip install -r requirements.txt

init: install
	$(ACTIVATE)

clean:
	[[ -d $(VENV) ]] && rm -rf $(VENV) || true
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
	cdk synth --all

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

# $(VERBOSE).SILENT: