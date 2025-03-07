#!/usr/bin/env python
import os
import shutil

PROJECT_DIRECTORY = os.path.realpath(os.path.curdir)


def complete_path(filepath):
    return os.path.join(PROJECT_DIRECTORY, filepath)


def remove_file(filepath):
    os.remove(complete_path(filepath))


if __name__ == '__main__':

    if '{{ cookiecutter.use_pytest }}' == 'y':
        remove_file('tests/__init__.py')

    if 'Not open source' == '{{ cookiecutter.open_source_license }}':
        remove_file('AUTHORS.rst')
        remove_file('docs/authors.rst')
        remove_file('CONTRIBUTING.rst')
        remove_file('docs/contributing.rst')

    if '{{ cookiecutter.is_library }}' == 'n':
        remove_file('docs/deploy_notes.rst')

    if os.path.exists('.git'):
        shutil.move(
            complete_path('pre-commit'),
            complete_path('.git/hooks/pre-commit')
        )
    else:
        remove_file('pre-commit')
