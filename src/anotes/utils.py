# -*- coding: utf-8 -*-
"""This modules contains helper functions."""

from logging import getLogger
import os
from pathlib import Path
import re
from subprocess import run
from typing import Optional

import converter
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
    newTopicFilePath = os.path.join(parentTopic.filePath, stripSpecialCharacters(newTopicName))
    newTopic = Topic(filePath=newTopicFilePath, name=newTopicName, parent=parentTopic.id)
    relPath = newTopicFilePath[1:]
    os.makedirs(os.path.join(getRawDirPath(), relPath), exist_ok=True)
    newTopic.save()


def getRawDirPath() -> str:
    """Returns the root directory where the raw files of notes.py are saved."""
    path = os.path.join(os.getcwd(), 'raw')
    if not os.path.exists(path):
        os.makedirs(path)
    return path


def getHTMLDir() -> Path:
    """Returns the directory to store html outputs."""
    path = os.path.join(os.getcwd(), 'outputs', 'html')
    if not os.path.exists(path):
        os.makedirs(path)
    return path
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
    note = Note()
    filePath = Path(topic.filePath) / Path(stripSpecialCharacters(noteName))
    note.filePath = str(filePath.with_suffix('.' + ext))
# todo: Make sure filePath is truely unique or the above code will raise an exception.
    note.title = noteName
    note.topic = topic.id
    note.save()


def convertRawFile(path: str):
    """Converts a note to HTML."""
    rawFilePath = Path(os.path.join(getRawDirPath(), path[1:]))
    with open(rawFilePath) as rawFile:
        raw = rawFile.read()
    match rawFilePath.suffix:
        case '.md':
            export = converter.md2HTML(raw)
        case '.tex':
            export = converter.tex2HTML(raw)
        case _:
            export = raw

    exportPath = Path(os.path.join(getHTMLDir(), path[1:]))  # remove leading slash
    exportPath = exportPath.with_suffix('.html')
    log.debug(f"Export file path is {exportPath}")
    if not os.path.exists(exportPath.parent):
        # Create it!
        os.makedirs(exportPath.parent)
    with open(exportPath, 'w') as exportFile:
        exportFile.write(export)
