#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Notes.py - A notes manager in your command line."""

from logging import getLogger


log = getLogger('notes.py')


def execute():
    """Parse command line argument and execute the appropriate action."""
    from arguments import getArgs
    import actions
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
    import logger
    logger.setupLogging()
    import database as db
    db.setup()
    execute() 
    db.close()


if __name__ == '__main__':
    run() # Put this in a try block and log any error
