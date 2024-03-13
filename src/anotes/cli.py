#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Notes.py - A notes manager in your command line."""

from logging import getLogger


log = getLogger("notes.py")


def execute():
    """Parse command line argument and execute the appropriate action."""
    from .arguments import getArgs
    from . import actions

    args = getArgs()
    match args.action:
        case "create":
            actions.createNote(args)
        case "edit":
            actions.editNote(args)
        case "topic":
            if args.topicAction == "edit":
                actions.editTopic(args)
            elif args.topicAction == "create":
                actions.createTopic(args)


def run():
    """Entry point of notes.py
    it does setup actions, executes user command and then clean up.
    """
    from . import logger

    logger.setupLogging()
    from . import config

    config.setup()
    from . import database as db

    db.setup()
    execute()
    db.close()


if __name__ == "__main__":
    run()  # Put this in a try block and log any error
