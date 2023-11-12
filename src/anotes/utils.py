# -*- coding: utf-8 -*-
"""This modules contains helper functions."""

from logging import getLogger
import os
from pathlib import Path
import re
import sys
from subprocess import run
from typing import Optional

from .paths import getDataDir
from . import converter
from .database import Topic, Note
from . import config
from . import template


log = getLogger("utils")
config = config.Config()


def stripSpecialCharacters(string: str) -> str:
    """Remove special characters except underscore and dash and replace spaces with dashes.
    parameters:
    - string: A string that might contain special characters
    returns: @`string` but without special characters.
    """
    cleanedString = re.sub(r"[^\w\- ]", "", string)
    cleanedString = cleanedString.replace(" ", "-")
    cleanedString = re.sub(r"[-]+", "-", cleanedString)
    return cleanedString.lower().strip()


def promptUser(prompt: str) -> Optional[str]:
    """Prompts a user for a topic name.
    parameters:
    - prompt: Prompt to display to the user.
    returns:
    - str: string the user entered,
    - None: user canceled prompt.
    """
    log.info("Prompting the user for topic name.")
    try:
        newTopicName = input(prompt)
    except KeyboardInterrupt:
        log.info(f"User canceled prompt.")
        return
    else:
        return newTopicName


def createTopic(parentTopic: Topic) -> Topic:
    """Creates a new topic."""
    log.info("Creating a new topic...")
    newTopicName = promptUser("Enter topic name. Type ctrl+c to cancel: ")
    if not newTopicName:
        return
    return Topic.create(name=newTopicName, parent=parentTopic)


def getRawDirPath() -> str:
    """Returns root directory of raw files"""
    path = os.path.join(getDataDir(), "raw")
    if not os.path.exists(path):
        os.makedirs(path)
    return path


def getHTMLDir() -> str:
    """Returns the directory to store html outputs."""
    path = os.path.join(getDataDir(), "outputs", "html")
    if not os.path.exists(path):
        os.makedirs(path)
    return path
