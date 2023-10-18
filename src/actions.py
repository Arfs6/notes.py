# -*- coding: utf -8 -*-
"""This models contains functions that get executed based on command line arguments"""

from logging import getLogger
from pathlib import Path

import database as db
import utils
import widgets


log = getLogger('actions')


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
    import os
    selector = widgets.Selector(os.listdir('/'))
    selector.run()
    print(f"Selected path = {selector.selected}")
    log.debug("Editing an existing note...")


def createTopic():
    """Creates a new topic."""
    log.info("Creating new topic...")
    baseTopic = db.Topic.get(db.Topic.id == 1)
    if not baseTopic.children:  # No root topics, created em!
        print("You don't have any topics yet.")
        utils.createTopic(baseTopic)
        return
    parentTopic, selectedTopic = widgets.selectTopic(baseTopic)
    if not parentTopic: return
    utils.createTopic(parentTopic)


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
    filePath = Path(utils.getRawDirPath()) / Path(str(selectedTopic.filePath)) / Path('index.md')
    utils.openFile(str(filePath))
