# -*- coding: utf-8 -*-
"""This module contains code that helps in converting files from one format to another."""

from pathlib import Path
import subprocess


def md2HTML(md: str) -> str:
    """Converts a markdown string to an HTML string."""
    result = subprocess.run(
            ['pandoc', '-f', 'markdown', '-t', 'html'],
            capture_output=True,
            text=True,
            input=md
            )
    return result.stdout


def tex2HTML(tex: str) -> str:
    """Converts a latex string to html."""
    result = subprocess.run(
            ['pandoc', '-f', 'latex', '-t', 'html', '--mathml'],
            text=True,
            capture_output=True,
            input=tex
            )
    return result.stdout


def convert(path: str) -> str:
    """Converts a file to the appropriate format."""
    try:
        with open(path) as fileObj:
            content = fileObj.read()
    except FileNotFoundError:
        return ''
    match Path(path).suffix:
        case ".md":
            return md2HTML(content)
        case ".tex":
            return tex2HTML(content)
        case _:
            return content
