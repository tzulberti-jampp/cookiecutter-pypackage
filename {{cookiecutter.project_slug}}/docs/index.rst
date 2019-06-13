Welcome to {{ cookiecutter.project_name }}'s documentation!
======================================

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   readme
   installation
   usage
   modules
   {% if cookiecutter.open_source_license != 'Not open source' -%}authors{% endif %}
   {% if cookiecutter.open_source_license != 'Not open source' -%}contributing{% endif %}
   changelog

Indices and tables
==================
* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
