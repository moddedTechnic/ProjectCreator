from pathlib import Path

from _utils import Arguments, TEMPLATES_DIR, insert_template

__all__ = ['c']


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
