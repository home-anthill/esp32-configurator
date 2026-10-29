.DEFAULT_GOAL := build

lint:
	poetry run pyrefly check
.PHONY: lint

check:
	poetry run pip-audit --skip-editable
.PHONY: check

test:
	poetry run python -m unittest discover -s tests -v
.PHONY: test

build:
	poetry build
.PHONY: build

run:
	poetry run python -m src $(ARGS)
.PHONY: run

deps:
	poetry install
.PHONY: deps
