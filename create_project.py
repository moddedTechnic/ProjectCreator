#!/usr/bin/env python3

import os
import shutil
import subprocess
from datetime import datetime
from pathlib import Path

import _generate_project
from _generate_project import PROJECT_LANGUAGES, PROJECT_TYPES
from _utils import Arguments, TEMPLATES_DIR, insert_template

__dir__ = Path(__file__).parent


def parse_args(argv: list[str]) -> Arguments:
    args = iter(argv)
    arguments = Arguments()

    for arg in args:
        if arg in {'-t', '--type'}:
            typ = next(args)
            arguments.type = PROJECT_TYPES.get(typ, typ)
        elif arg in {'-l', '--license'}:
            arguments.license = next(args)
        elif arg in {'-f', '--fullname'}:
            arguments.full_name = next(args)
        else:
            arguments.project_name = arg

    arguments.language = PROJECT_LANGUAGES.get(arguments.type, arguments.type)

    return arguments


def check_arguments(arguments: Arguments) -> bool:
    if not arguments.project_name or not arguments.type:
        print('Usage: ', *sys.orig_argv, f'[OPTIONS...] NAME')
        return False
    if not (TEMPLATES_DIR / 'licenses' / arguments.license).exists():
        print(f'{arguments.license} is not a valid license')
        return False
    return True


def get_project_path(arguments: Arguments) -> Path:
    project_root = Path.home() / 'Documents' / 'code' / arguments.language
    if arguments.type != arguments.language:
        project_root /= arguments.type
    project_root /= arguments.project_name
    return project_root


def create_project_dir(project_path: Path) -> bool:
    if project_path.exists():
        while (confirm := input('Project directory already exists, do you want to override it (y/N)? ').lower()) not in {'y', 'n', ''}:
            pass
        if confirm == 'n' or confirm == '':
            print('Cancelling project creation')
            return False
        else:
            shutil.rmtree(str(project_path.absolute()))
    project_path.mkdir(parents=True, exist_ok=True)
    return True


def create_readme(arguments: Arguments, project_path: Path):
    insert_template(
        TEMPLATES_DIR / 'README.md',
        project_path / 'README.md',
        project_name=arguments.project_name
    )


def create_license(arguments: Arguments, project_path: Path):
    insert_template(
        TEMPLATES_DIR / 'licenses' / arguments.license,
        project_path / 'LICENSE',
        year=datetime.now().year, full_name=arguments.full_name
    )


def create_gitignore(arguments: Arguments, project_path: Path):
    gitignore = TEMPLATES_DIR / 'gitignore' / f'{arguments.language.capitalize()}.gitignore'
    if (gitignore.exists()):
        insert_template(gitignore, project_path / '.gitignore')
    else:
        print(f'No gitignore found for {arguments.language}')
    with (project_path / '.gitignore').open('a') as f:
        f.write((TEMPLATES_DIR / 'gitignore' / 'VisualStudio.gitignore').read_text())


def main(argv: list[str]) -> int:
    if len(argv) == 1:
        print('Usage: ', *sys.orig_argv, f'[OPTIONS...] NAME')
        return 1

    arguments = parse_args(argv[1:])
    if not check_arguments(arguments):
        return 1

    project_path = get_project_path(arguments)
    print(f'Creating a {arguments.type} project called {arguments.project_name}')
    if not create_project_dir(project_path):
        return 1
    create_readme(arguments, project_path)
    create_license(arguments, project_path)
    create_gitignore(arguments, project_path)

    generator = getattr(_generate_project, arguments.type, None)
    if callable(generator):
        if not generator(arguments, project_path):
            return 1

    subprocess.run('git init', cwd=project_path, shell=True, check=True)
    subprocess.run('git add .', cwd=project_path, shell=True, check=True)
    subprocess.run('git commit -m "Inital commit"', cwd=project_path, shell=True, check=True)
    subprocess.run('code .', cwd=project_path, shell=True, check=True)

    return 0


if __name__ == '__main__':
    import sys
    exit(main(sys.argv))
