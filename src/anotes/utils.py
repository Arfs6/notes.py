# -*- coding: utf-8 -*-
"""This modules contains helper functions."""

from logging import getLogger
import os
import re
from typing import Optional

from . import config
from .database import Note, Topic
from .paths import getDataDir


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
    log.info(f"Prompting the user. Propt = {prompt}")
    try:
        ans = input(prompt)
    except KeyboardInterrupt:
        log.debug(f"User canceled prompt.")
        return
    else:
        log.debug(f"User typed: <{ans}>")
        return ans


def createTopic(parentTopic: Topic) -> Topic | None:
    """Creates a new topic."""
    log.info("Creating a new topic...")
    newTopicName = promptUser("Enter topic name. Type ctrl+c to cancel: ")
    if not newTopicName:
        return
    newTopic = Topic.create(name=newTopicName, parent=parentTopic)
    log.debug(f"Created new topic: <{newTopic}>")
    return newTopic


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


def createNote(topic: Topic):
    """Creates a new note.
    parameters:
    - topic: Topic the note belongs to.
    """
    log.info("Creating a new topic...")
    noteTitle = promptUser("Enter note name. Type ctrl+c to cancel: ")
    if not noteTitle:
        return
    ext = promptUser(
        "Which type of note is this? e.g. tex for latex. Type ctrl+c to cancel: "
    )
    if not ext:
        ext = "md"
    note = Note.create(noteTitle, ext, topic)
