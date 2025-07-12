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

upgrade:
	npm install -g aws-cdk
	@if [ -d "$(VENV)" ]; then rm -rf $(VENV); fi
	python3 -m venv $(VENV)
	$(ACTIVATE) && pip install --upgrade pip && pip install aws-cdk-lib constructs

bootstrap:
	$(ACTIVATE) && cdk bootstrap

synth:
	$(ACTIVATE) && cdk synth

deploy:
	$(ACTIVATE) && cdk deploy --require-approval never

destroy:
	$(ACTIVATE) && cdk destroy --force

clean:
	rm -rf $(VENV)
