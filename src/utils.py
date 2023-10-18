# -*- coding: utf-8 -*-
"""This modules contains helper functions."""

from logging import getLogger
import os
from pathlib import Path
import re
from subprocess import run
from typing import Optional

from database import Topic, Note
import init as config


log = getLogger('utils')


def stripSpecialCharacters(string: str) -> str:
    """Remove special characters except underscore and dash and replace spaces with dashes.
    parameters:
    - string: A string that might contain special characters
    returns: @`string` but without special characters.
    """
    cleanedString = re.sub(r'[^\w\- ]', '', string)
    cleanedString = cleanedString.replace(' ', '-')
    return cleanedString


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


def createTopic(parentTopic: Topic):
    """Creates a new topic."""
    log.info("Creating a new topic...")
    newTopicName = promptUser("Enter topic name. Type ctrl+c to cancel: ")
    if not newTopicName: return
    newTopicFilePath = Path(str(parentTopic.filePath)) / Path(stripSpecialCharacters(newTopicName))
    newTopic = Topic(filePath=newTopicFilePath, name=newTopicName, parent=parentTopic.id)
    newTopic.save()


def getRawDirPath():
    """Returns the root directory where the raw files of notes.py are saved."""
    return Path(os.getcwd()) / Path('raw')


def openFile(path: str):
    """Opens the specified file in a text editor.
    parameters:
    - path: path to file.
    """
    run([config.editor, path])


def createNote(topic: Topic):
    """Creates a new note.
    parameters:
    - topic: Topic the note belongs to.
    """
    log.info("Creating a new topic...")
    noteName = promptUser("Enter note name. Type ctrl+c to cancel: ")
    if not noteName: return
    ext = promptUser("Which type of note is this? e.g. tex for latex. Type ctrl+c to cancel: ")
    if not ext: return
    note = Note(title=noteName)
    filePath = Path(topic.filePath) / Path(stripSpecialCharacters(noteName))
    note.filePath = str(filePath.with_suffix('.' + ext))
    note.topic = topic.id
