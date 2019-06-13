#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `{{ cookiecutter.project_slug }}` package."""

{% if cookiecutter.use_pytest == 'n' -%}
import unittest
{%- endif %}

from {{ cookiecutter.project_slug }} import {{ cookiecutter.project_slug }}

{% if cookiecutter.use_pytest == 'y' %}
def test_sum():
    assert 1 + 1 == 2
{% else %}
class Test{{ cookiecutter.project_slug|title }}(unittest.TestCase):
    """Tests for `{{ cookiecutter.project_slug }}` package."""

    def test_sum(self):
        """Test something."""
        self.assertEqual(1 + 1, 2)
{% endif %}
