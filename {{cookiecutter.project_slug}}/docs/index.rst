{{ '='  * ((cookiecutter.project_name|length) + 28) }}
Welcome to {{ cookiecutter.project_name }}'s documentation!
{{ '='  * ((cookiecutter.project_name|length) + 28) }}

.. include:: README.rst

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   readme
   installation
   usage
   modules
   {% if cookiecutter.open_source_license != 'Not open source' %}authors{% endif %}
   {% if cookiecutter.open_source_license != 'Not open source' %}contributing{% endif %}
   {% if cookiecutter.is_library != 'n' %}deploy_notes{% endif %}
   changelog
