# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

ESP32 Configurator is a Python CLI tool that generates C header files from YAML configuration files for ESP32 microcontroller devices. It validates YAML input with Pydantic models, then renders output using Jinja2 templates.

## Commands

```bash
# Install dependencies
poetry install

# Run the CLI
python -m src --model <model_name> --source <yaml_path> --destination <output_path>
```

There are no test or lint commands configured.

## Architecture

The codebase is small and follows a straightforward pipeline: **YAML input → Pydantic validation → Jinja2 rendering → C header output**.

- `src/__main__.py` — Entry point and all core logic: CLI argument parsing, YAML reading (`read_template`), Pydantic conversion (`parse_yaml`), Jinja2 environment setup (`get_jinja_env`), and file writing (`write_template`)
- `src/models/secrets.py` — `Secrets` Pydantic BaseModel defining the configuration schema (WiFi, server, MQTT fields with defaults)
- `templates/secrets.h` — Jinja2 template that produces the C header file

## Tech Stack

- Python 3.12+ with Poetry 2.3.2+
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
