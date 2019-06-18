#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The setup script."""

from os import path
from setuptools import setup, find_packages
{% if cookiecutter.use_cython == 'y' %}
import sys
import os
import multiprocessing
from setuptools import Extension
from Cython.Build import cythonize
from setuptools.command.build_ext import build_ext
{% endif %}

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('CHANGELOG.rst') as history_file:
    history = history_file.read()


def parse_requirements_txt(filename='requirements.txt'):
    requirements = open(path.join(path.dirname(__file__), filename)).readlines()
    # remove whitespaces
    requirements = [line.strip().replace(' ', '') for line in requirements]
    # remove all the requirements that are comments
    requirements = [line for line in requirements if not line.startswith('#')]
    # remove empty lines
    requirements = list(filter(None, requirements))
    return requirements


{% if cookiecutter.use_cython == 'y' %}
def solve_transitive_dependencies(cython_extensions):
    """
    Solves the dependencies based on the information of its dependencies.
    If file A depends on B, and B depends on C, then A also depends on C.

    :type cython_extensions: list(dict)
    :param cython_extensions: all the information of the extensions to create
        to cythonize the files. Each dict has the following keys:

        - name: the extension's full package name
        - sources: a list with the python or cython file
        - depends: a list of dependencies. It can be the path to the PXD file
            or another name on the list. When possible we should add the
            referneces to this dict, so it can add the dependencies tree
            correctly

    :rtype: list(:class:`.Extension`)
    :returns: all the extensions used to cythonize the files
    """
    # create a map with all the names of the extensions
    cython_extensions_map = {
        extension['name']: extension
        for extension in cython_extensions
    }

    for extension in cython_extensions:
        extension['finished'] = False

    changed = True
    while changed:
        changed = False
        for extension in cython_extensions:
            finished = True
            final_dependencies = set()
            if extension['finished']:
                # the dependencies are final
                continue

            for dependency in extension['depends']:
                cython_dependency = cython_extensions_map.get(dependency, None)
                if cython_dependency is None:
                    # in this case is must reference a file
                    final_dependencies.add(dependency)
                    continue
                if not cython_dependency['finished']:
                    finished = False
                    break

                final_dependencies.update(cython_dependency['depends'])

            if finished:
                # make sure that it is finished and all the dependencies
                # have been replaced for the corresponding files
                not_pxd_files = [filename for filename in final_dependencies if not filename.endswith('.pxd')]
                if not_pxd_files:
                    raise Exception(
                        "Extension %s was finished but a dependency isn't a PXD file: %s" % (
                            extension['name'],
                            not_pxd_files
                        )
                    )

                extension['depends'] = list(final_dependencies)
                extension['finished'] = True
                changed = True

    # if all the values have been changed make sure that
    # all the extension are finished
    not_finished = [extension for extension in cython_extensions if not extension['finished']]
    if not_finished:
        raise Exception("At least one extension hasn't finish: %s" % not_finished)

    extension_modules = [
        Extension(
            extension['name'],
            extension['sources'],
            depends=extension['depends']
        )
        for extension in cython_extensions
    ]
    return extension_modules


# maps all the information of the files that should be cythonized and it's
# dependencies. Check :meth:`.solve_transitive_dependencies` to get more information
# about the values on the dict. The depends should only include the cimported
# dependencies
cython_extensions = []
extension_modules = solve_transitive_dependencies(cython_extensions)
include_dirs = os.environ.get('CYTHON_INCLUDE_DIRS', '.').split(':')

force_cython = '--force-cython' in sys.argv
if force_cython:
    del sys.argv[sys.argv.index('--force-cython')]

parallel = None
if '-j' in sys.argv:
    jobpos = sys.argv.index('-j')
    parallel = int(sys.argv[jobpos+1])
    del sys.argv[jobpos:jobpos+2]

    if parallel == 1:
        parallel = None
else:
    parallel = multiprocessing.cpu_count()

if '--no-cython' in sys.argv:
    cythonize = None  # noqa
    del sys.argv[sys.argv.index('--no-cython')]
    try:
        import cython

        # used to solve error when not using cython because it raises an
        # error that AttributeError: 'module' object has no attribute 'optimize'
        class CythonOptimizeMock(object):
            use_switch = lambda *p, **kw: (lambda f: f)  # noqa

        cython.optimize = CythonOptimizeMock()
    except ImportError:
        pass

cmd_class = {}
if cythonize is not None:
    if parallel is not None:
        try:
            from multiprocessing.pool import ThreadPool

            class parallel_build_ext(build_ext):
                def build_extensions(self):
                    # First, sanity-check the 'extensions' list
                    self.check_extensions_list(self.extensions)

                    for ext in self.extensions:
                        ext.sources = self.cython_sources(ext.sources, ext)

                    pool = ThreadPool(parallel)
                    pool.map(self.build_extension, self.extensions, chunksize=1)
                    pool.close()
                    pool.join()
            cmd_class['build_ext'] = parallel_build_ext
        except ImportError:
            parallel_build_ext = None

    try:
        from Cython.Utils import file_newer_than, modification_time
    except ImportError:
        # lint:disable
        file_newer_than = None
        modification_time = None
        # lint:enable
    if file_newer_than is not None:
        # Work around broken dependency tracking in cython
        basepath = os.path.dirname(__file__)
        for ext in extension_modules:
            if ext.depends:
                max_modtime = max([modification_time(os.path.join(basepath, dep)) for dep in ext.depends])
                for src in ext.sources:
                    src_path = os.path.join(basepath, src)
                    if not file_newer_than(src_path, max_modtime):
                        # touch source
                        os.utime(src, None)

    ext_modules = cythonize(
        extension_modules,
        include_path=include_dirs,
        nthreads=parallel,
        force=force_cython
    )
{% endif %}

{%- set license_classifiers = {
    'MIT license': 'License :: OSI Approved :: MIT License',
    'BSD license': 'License :: OSI Approved :: BSD License',
    'ISC license': 'License :: OSI Approved :: ISC License (ISCL)',
    'Apache Software License 2.0': 'License :: OSI Approved :: Apache Software License',
    'GNU General Public License v3': 'License :: OSI Approved :: GNU General Public License v3 (GPLv3)'
} %}


setup(
    author="{{ cookiecutter.full_name.replace('\"', '\\\"') }}",
    author_email='{{ cookiecutter.email }}',
{%- if cookiecutter.open_source_license in license_classifiers %}
    classifiers=[
        '{{ license_classifiers[cookiecutter.open_source_license] }}',
    ],
{%- endif %}
    description="{{ cookiecutter.project_short_description }}",
    install_requires=parse_requirements_txt(),
    extras_require={'dev': parse_requirements_txt('requirements_dev.txt')},
{%- if cookiecutter.open_source_license in license_classifiers %}
    license='{{ cookiecutter.open_source_license }}',
{%- endif %}
    long_description=readme + '\n\n' + history,
    long_description_content_type='text/x-rst',
    include_package_data=True,
    package_data={
        '': ['*.pxd', '*.pyx']
    },
    data_files=[
        ('', [
            'README.rst',
            'CHANGELOG.rst',
            'requirements.txt',
            'requirements_dev.txt',
            {% if 'Not open source' != '{{ cookiecutter.open_source_license }}'%}'LICENSE',{%- endif %}
        ]),
    ],
    keywords='{{ cookiecutter.project_slug }}',
    name='{{ cookiecutter.project_slug }}',
    packages=find_packages(include=['{{ cookiecutter.project_slug }}']),
    setup_requires=[{%- if cookiecutter.use_pytest == 'y' %}'pytest-runner',{%- endif %} ],
    test_suite='tests',
    tests_require=[{%- if cookiecutter.use_pytest == 'y' %}'pytest',{%- endif %} ],
    {%- if cookiecutter.use_cython == 'y' %}
    ext_modules=ext_modules,
    cmdclass=cmd_class,
    {%- endif %}
    url='https://github.com/{{ cookiecutter.github_username }}/{{ cookiecutter.project_slug }}',
    version='{{ cookiecutter.version }}',
    zip_safe=False,
)
