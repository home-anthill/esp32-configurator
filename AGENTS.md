# AGENTS.md

This file provides guidance to AI agents when working with code in this repository.

## Project Overview

ESP32 Configurator is a Python CLI tool that generates C header files from YAML configuration files for ESP32 microcontroller devices. It validates YAML input with Pydantic models, then renders output using Jinja2 templates.

## Commands

```bash
# Install dependencies
poetry install

# Run the CLI
python -m src --model <model_name> --source <yaml_path> --destination <output_path>

# Run the installed console script
esp32-configurator --model <model_name> --source <yaml_path> --destination <output_path>
```

Poetry is configured in `poetry.toml` to create an in-project `.venv` and use `/tmp/poetry_cache`.

Run tests with `poetry run python -m unittest discover -s tests -v`, and verify packaging with `poetry build`. There is no configured linter.

## Architecture

The codebase is small and follows a straightforward pipeline: **YAML input → Pydantic validation → Jinja2 rendering → C header output**.

- `src/__main__.py` — Entry point and all core logic: CLI argument parsing, YAML reading (`read_template`), Pydantic conversion (`parse_yaml`), Jinja2 environment setup (`get_jinja_env`), and file writing (`write_template`)
- `src/models/secrets.py` — shared credential, identity, and connection schema
- `templates/secrets.h` — single Jinja2 secrets template for all device models
- `tests/test_configurator.py` — credential rendering, validation, and CLI regression coverage
- `secrets-template.yaml` — shared credential and connection YAML template for every model
- `pyproject.toml` — Poetry package metadata and the `esp32-configurator` console script entry point

## Tech Stack

- Python 3.12+ with Poetry
- Pydantic for data validation, Jinja2 for templating, PyYAML for parsing
- GitHub Actions CI (`.github/workflows/build.yml`)

## Code Conventions

- Modern Python type hints (union syntax `X | None`)
- `pathlib.Path` for file paths; template loader anchored to `Path(__file__)`, not `Path.cwd()`
- Strict Jinja2 `StrictUndefined` to catch missing variables
- 2-space indentation (per `.editorconfig`)
- `pydantic.SecretStr` for sensitive fields (`wifi_password`, `api_token`, `mqtt_password`); call `.get_secret_value()` in templates
- `Secrets.model_validate()` (not `TypeAdapter`) for idiomatic Pydantic v2 BaseModel validation
- Required fields declared before optional fields in Pydantic models
- Keep model fields and `templates/secrets.h` in sync.

`--model` is device identity. All models use the same secrets template; there is no `--firmware` selection. Hardware settings belong in fixed firmware `config.h` files and must not be processed. The simulator requires no generated secrets. Legacy hardware YAML fields are ignored by Pydantic.
