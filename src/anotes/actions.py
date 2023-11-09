# -*- coding: utf -8 -*-
"""This models contains functions that get executed based on command line arguments"""

from logging import getLogger
import os
from pathlib import Path

from . import database as db
from . import utils
from . import widgets
from . import template


log = getLogger("actions")


def createNote():
    """Creates a new note."""
    log.info("Creating new note...")
    baseTopic = db.Topic.get(db.Topic.id == 1)
    if not baseTopic:
        # todo: ask user if he / she wants to create a topic.
        print("No topics yet.")

    pTopic, selectedTopic = widgets.selectTopic(baseTopic)
    if not selectedTopic:
        return
    utils.createNote(selectedTopic)


def editNote():
    """Edit an existing note."""
    log.info("Editing note...")
    baseTopic = db.Topic.get(db.Topic.id == 1)
    note = widgets.selectNote(baseTopic)
    if not note:
        return
    filePath = utils.getRawDirPath() + note.filePath
    log.debug(f"Resolved path for note ={filePath}")
    utils.openFile(str(filePath))
    converted = utils.convertRawFile(str(filePath), "note.html", note=note)
    exportsPath = Path(os.path.join(utils.getHTMLDir(), note.filePath[1:]))
    exportsPath = exportsPath.with_suffix(".html")
    try:
        os.makedirs(os.path.dirname(exportsPath))
    except FileExistsError:
        pass
    with open(exportsPath, "w") as fileObj:
        fileObj.write(converted)


def createTopic():
    """Creates a new topic."""
    log.info("Creating new topic...")
    baseTopic = db.Topic.get(db.Topic.id == 1)
    if not baseTopic.children:  # No root topics, created em!
        print("You don't have any topics yet.")
        utils.createTopic(baseTopic)
        return
    parentTopic, selectedTopic = widgets.selectTopic(baseTopic)
    if not parentTopic:
        return
    topic: db.Topic = utils.createTopic(parentTopic)
    output = template.render("topic.html", content="", topic=topic)
    exportsPath = Path(os.path.join(utils.getHTMLDir(), topic.filePath[1:], "index.html"))
    os.makedirs(os.path.dirname(exportsPath), exist_ok=True)
    with open(exportsPath, 'w') as fileObj:
        fileObj.write(output)


def editTopic():
    """Edit an existing topic."""
    log.info("Editing topic...")
    baseTopic = db.Topic.get(db.Topic.id == 1)
    if not baseTopic.children:
        # todo: ask the user to create a new topic.
        print("No topics yet.")
        return
    pTopic, selectedTopic = widgets.selectTopic(baseTopic)
    if not selectedTopic:
        return
    filePath = os.path.join(
        utils.getRawDirPath(), selectedTopic.filePath[1:], "index.md"
    )
    utils.openFile(str(filePath))
    converted = utils.convertRawFile(str(filePath), "topic.html", topic=selectedTopic)
    exportsPath = os.path.join(
        utils.getHTMLDir(), selectedTopic.filePath[1:], "index.html"
    )
    try:
        os.makedirs(os.path.dirname(exportsPath))
    except FileExistsError:
        pass
    with open(exportsPath, "w") as fileObj:
        fileObj.write(converted)
