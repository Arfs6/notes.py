#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Notes.py - A notes manager in your command line."""

from logging import getLogger

import logger
from arguments import getArgs
import actions


log = getLogger('notes.py')


def execute():
    """Parse command line argument and execute the appropriate action."""
    args = getArgs()
    match args.action:
        case 'create':
            actions.createNote()
        case 'edit':
            actions.editNote()
        case 'topic':
            if args.topicAction == 'edit':
                actions.editTopic()
            elif args.topicAction == 'create':
                actions.createTopic()


def run():
    """Entry point of notes.py
    it does setup actions, executes user command and then clean up.
    """
    import database as db
    db.setup()
    execute() 
    db.close()


if __name__ == '__main__':
    run() # Put this in a try block and log any error
