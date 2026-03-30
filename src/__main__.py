import argparse
import sys
from pathlib import Path

import yaml
from jinja2 import Environment, FileSystemLoader, StrictUndefined
from pydantic import ValidationError

from src.models.secrets import Secrets

TEMPLATE_FILE_NAME = 'secrets.h'


def read_template(source_file_path: Path) -> Secrets:
    secrets = parse_yaml(path=source_file_path)
    print('Configuration parsed successfully.')
    return secrets


def write_template(secrets: Secrets, model_name: str, destination_path: Path) -> None:
    env = get_jinja_env()
    rendered = env.get_template(TEMPLATE_FILE_NAME).render(secrets=secrets, model_name=model_name)

    output_file = destination_path / TEMPLATE_FILE_NAME
    print(f'Writing output to {output_file}')

    output_file.write_text(rendered)


def main() -> None:
    parser = argparse.ArgumentParser(description='ESP32 devices and sensors configurator')
    parser.add_argument('--model', required=True, help='unique model name', type=str)
    parser.add_argument('--source', required=True, help='path of the .yaml template with inputs', type=Path)
    parser.add_argument('--destination', required=True, help='path of the firmwares folder where to save the resulting .h file', type=Path)
    args = parser.parse_args()

    secrets = read_template(source_file_path=args.source)
    write_template(secrets=secrets, model_name=args.model, destination_path=args.destination)


def parse_yaml(path: Path) -> Secrets:
    try:
        with path.open() as stream:
            data = yaml.safe_load(stream)
    except (OSError, yaml.YAMLError) as err:
        print(f'Error reading {path}: {err}', file=sys.stderr)
        sys.exit(1)

    try:
        return Secrets.model_validate(data)
    except ValidationError as err:
        print(f'Validation error: {err}', file=sys.stderr)
        sys.exit(1)


def get_jinja_env() -> Environment:
    return Environment(
        loader=FileSystemLoader([Path(__file__).parent.parent / 'templates']),
        autoescape=False,
        undefined=StrictUndefined,
        trim_blocks=True,
        lstrip_blocks=True,
        keep_trailing_newline=True,
    )


if __name__ == '__main__':
    main()
