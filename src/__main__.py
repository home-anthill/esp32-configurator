import argparse
import os
from pathlib import Path

import yaml
from jinja2 import Environment, FileSystemLoader, select_autoescape, StrictUndefined
from pydantic import TypeAdapter

from src.models.secrets import Secrets

template_file_name = 'secrets.h'


def read_template(source_file_path: str) -> Secrets | None:
    secrets_from_file: Secrets | None = parse_yaml_as_obj(path=Path(source_file_path))
    print(f'{secrets_from_file}\n\n')
    return secrets_from_file


def write_template(secrets: Secrets, model_name: str, destination_path: str):
    env: Environment = get_jinja_env()
    secrets_renderer: str = env.get_template(template_file_name).render(secrets=secrets, model_name=model_name)

    print(f'{secrets_renderer}\n\n')
    print(f'Destination path = {os.path.join(destination_path,  template_file_name)}\n\n')

    with open(os.path.join(destination_path,  template_file_name), 'w') as f:
        f.write(secrets_renderer)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument('--model', help='unique model name', type=str)
    parser.add_argument('--source', help='path of the .yaml template with inputs', type=str)
    parser.add_argument('--destination', help='path of the firmwares folder where to save the resulting .h file', type=str)
    args = parser.parse_args()

    model_arg = args.model
    source_arg = args.source
    destination_arg = args.destination
    if not model_arg:
        raise "--model name is mandatory"
    if not source_arg:
        raise "--source path is mandatory"
    if not destination_arg:
        raise "--destination path is mandatory"

    print('model_arg: ' + model_arg)
    print('source_arg: ' + source_arg)
    print('destination_arg: ' + destination_arg)

    secrets: Secrets | None = read_template(source_file_path=source_arg)
    if secrets is not None:
      write_template(secrets=secrets, model_name=model_arg, destination_path=destination_arg)


def parse_yaml_as_obj(path: Path) -> Secrets | None:
    with open(path, 'r') as stream:
        try:
            adapter = TypeAdapter(Secrets)
            return adapter.validate_python(yaml.safe_load(stream))
        except yaml.YAMLError as err:
            print(err)


def get_jinja_env() -> Environment:
    env: Environment = Environment(
        loader=FileSystemLoader([os.path.join(os.getcwd(), 'templates')]),
        autoescape=select_autoescape(),
        undefined=StrictUndefined,
        trim_blocks=True,
        lstrip_blocks=True,
        keep_trailing_newline=True,
    )
    return env


if __name__ == '__main__':
    main()
