# -*- coding: utf-8 -*-
"""Paths related code."""

from logging import getLogger
import os
import sys
from typing import Optional

log = getLogger("paths")


def getDevelopmentDir() -> str | None:
    """Where to store data when in development.
    Returns:
    str: Path to current folder if running in dev mode.
    None: When not in development
    """
    if os.getenv("ANOTES_ENV") == "development":
        return os.path.join(os.path.dirname(__file__), 'data')


def getDataDir() -> str:
    """Returns where raw files are stored."""
    if getDevelopmentDir() is not None:
        path = getDevelopmentDir()
    elif sys.platform.startswith("linux"):
        path = os.path.expanduser("~/.local/share/anotes")
    elif sys.platform == "win32":
        path = os.path.join(os.getenv("appdata"), "anotes")
    elif sys.platform == "darwin":
        path = os.path.expanduser("~/Library/Application Support/anotes")
    else:
        path = os.path.dirname(__file__)
    return path


def getConfigDir() -> str:
    """Returns config file directory."""
    if getDevelopmentDir() is not None:
        path = getDevelopmentDir()
    else:
        match sys.platform:
            case "linux":
                path = os.path.expanduser("~/.config/anotes")
            case "darwin":
                path = os.path.expanduser("~/Library/Preferences/anotes")
            case "win32":
                path = os.path.join(os.getenv("LOCALAPPDATA"), "anotes")
            case _:
                log.warning("Unsupported OS: {sys.platform}")
                msg = [
                    "No idea where your config file is.\n",
                    "Using default configuration.\n",
                    "Please, open an issue on the project's github page with info on your system.",
                ]
                print("".join(msg))
                path = os.path.dirname(__file__)
    return path


def getLogDir():
    """Returns a directory to store temporary files."""
    path = "/var/log/anotes"
    os.makedirs(path)
    return path
