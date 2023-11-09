# -*- coding: utf-8 -*-
"""Templates related code."""

from jinja2 import Environment, ChoiceLoader, FileSystemLoader
import os

from . import paths


def render(name, **kwargs) -> str:
    """Renders a template and returns the rendered output.
    parameters:
    - name: name of template
    - kwargs: context to pass to template.
    """
    configPath = os.path.join(paths.getConfigDir(), 'templates')
    mainPath = os.path.join(os.path.dirname(__file__), 'templates')
    loader = ChoiceLoader([
        FileSystemLoader(configPath),
        FileSystemLoader(mainPath)
    ])
    env = Environment(loader=loader)
    template = env.get_template(name)
    return template.render(kwargs)
