# -*- coding=utf-8 -*-
"""Editing notes and topic files."""
from logging import getLogger
import os
import subprocess
from threading import Event, Thread
import time

from .config import Config
from .server import Server


log = getLogger('editting')
config = Config()


def autoCompiler(filePath: str, obj, terminate: Event):
    """Recompiles files when file has been modified.
    Parameters:
    - filePath: path to file that is been edited.
    - obj: An object with an update method to recompile the file.
    - terminate: Flag that specifies when to stop execution.
    """
    try:
        lastModified = os.path.getmtime(filePath)
    except FileNotFoundError:
        lastModified = 0  # currentModified will always be greater than zero when file is created.

    while not terminate.is_set():
        try:
            currentModified = os.path.getmtime(filePath)
        except FileNotFoundError:
            time.sleep(0.5)
            continue  # No need to compare since file doesn't exist.
        if currentModified > lastModified:
            obj.update()
            lastModified = currentModified

        # Sleep for 0.5 seconds before the next iteration
        time.sleep(0.5)


def editFile(filePath: str, obj):
    """Opens a @filePath for user to edit.
    Parameters:
    - filePath: path to file to open.
    - obj: Object with an update method to update @filePath when saved.
    """
    terminateEvent = Event()
    autoCompilerThread = Thread(
        target=autoCompiler,
        args=(
            filePath,
            obj,
            terminateEvent
        )
    )
    autoCompilerThread.start()
    server = Server()
    server.run()
    subprocess.run([
        config.editor,
        filePath
    ])
    terminateEvent.set()
    autoCompilerThread.join()
    server.stop()
