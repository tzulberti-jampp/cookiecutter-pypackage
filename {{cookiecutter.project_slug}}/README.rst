{% set is_open_source = cookiecutter.open_source_license != 'Not open source' -%}
{{ '='  * ((cookiecutter.project_name|length)) }}
{{ cookiecutter.project_name }}
{{ '='  * ((cookiecutter.project_name|length)) }}

{%- if is_open_source %}
.. image:: https://img.shields.io/pypi/v/{{ cookiecutter.project_slug }}.svg
        :target: https://pypi.python.org/pypi/{{ cookiecutter.project_slug }}

.. image:: https://img.shields.io/travis/{{ cookiecutter.github_username }}/{{ cookiecutter.project_slug }}.svg
        :target: https://travis-ci.org/{{ cookiecutter.github_username }}/{{ cookiecutter.project_slug }}

.. image:: https://readthedocs.org/projects/{{ cookiecutter.project_slug | replace("_", "-") }}/badge/?version=latest
        :target: https://{{ cookiecutter.project_slug | replace("_", "-") }}.readthedocs.io/en/latest/?badge=latest
        :alt: Documentation Status
{%- endif %}


{{ cookiecutter.project_short_description }}

{%- if is_open_source %}
* Free software: {{ cookiecutter.open_source_license }}
* Documentation: https://{{ cookiecutter.project_slug | replace("_", "-") }}.readthedocs.io.
{%- endif %}

Features
========

* TODO


{% if cookiecutter.is_library == 'y' %}
Release
=======

- Check the test results on `Jenkins <https://ci.jampp.com/{{ cookiecutter.project_slug }}>`__
- Update the changelog release date on `CHANGELOG <CHANGELOG.rst>`__
- Commit the changes to master (there is no need to do an PR in this case)

  .. code-block:: console

      $ git commit CHANGELOG -m 'New release'

- Run the `Jenkins job <https://ci.jampp.com/{{ cookiecutter.project_slug }}_release>`__ to do the release
{% endif %}

Credits
=======

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage
