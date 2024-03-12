# -*- coding: utf-8 -*-
"""Manages configuration file (init script)."""

from logging import getLogger
import sys
import os

from .paths import getConfigDir


log = getLogger('config')


class Config:
    """Represents user config."""

    def __init__(self):
        """Initialize init script."""
        try:
            import init
            log.info("init script imported successfully")
        except ModuleNotFoundError:
            log.info("Init script not found, using defaults.")
            init = Container()
        self.init = init

    @property
    def editor(self):
        """Editor used for editing files."""
        if getattr(self.init, 'editor') is not None:
            return self.init.editor
        match sys.platform:
            case 'win32':
                return 'notepad'
            case 'linux':
                return 'nano'
            case 'darwin':
                return 'textedit'
        log.error("Couldn't determine text editor to use.")
        print("Have no idea which text editor to use. Specify one in your init.py file.")
        sys.exit()


class Container:
                ...


def setup():
    """make `import init` to import user init script."""
    log.info("Setting up init script.")
    path = getConfigDir()
    sys.path.insert(1, path)
