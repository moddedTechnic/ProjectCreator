import subprocess
import sys
from pathlib import Path

from _utils import Arguments, TEMPLATES_DIR, insert_template

__all__ = [
    'PROJECT_LANGUAGES', 'PROJECT_TYPES',
    'c', 'python',
]


PROJECT_TYPES = {
    'py': 'python',
}

PROJECT_LANGUAGES = {}


def c(arguments: Arguments, project_path: Path) -> bool:
    src_dir = project_path / 'src'
    src_dir.mkdir()
    insert_template(
        TEMPLATES_DIR / 'c' / 'main.c',
        src_dir / 'main.c'
    )
    insert_template(
        TEMPLATES_DIR / 'c' / 'Makefile',
        project_path / 'Makefile',
        project_name=arguments.project_name,
    )
    return True


def python(arguments: Arguments, project_path: Path) -> bool:
    v = sys.version_info
    subprocess.run(['pipenv', '--python', f'{v.major}.{v.minor}.{v.micro}'])
    return True
