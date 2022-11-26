from dataclasses import dataclass
from pathlib import Path
from typing import Any

__all__ = ['Arguments', 'TEMPLATES_DIR', 'insert_template']
__dir__ = Path(__file__).parent

TEMPLATES_DIR = __dir__ / 'templates'


@dataclass
class Arguments:
    type: str = ''
    language: str = ''
    project_name: str = ''
    license: str = 'MIT'
    full_name: str = ''


def insert_template(template: Path, target: Path, **template_params: Any):
    contents = template.read_text()
    if template_params:
        contents = contents.format(**template_params)
    target.write_text(contents)
