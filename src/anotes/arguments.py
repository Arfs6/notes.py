# -*- coding: utf-8 -*-
"""This module is responsible for parsing command line arguments."""

import argparse


def getArgs():
    """Parses command line arguments and returns a Namespace"""
    parser = argparse.ArgumentParser(
        prog="anotes",
        description="Notes manager",
    )

    subParser = parser.add_subparsers(dest="action")
    subParser.add_parser("edit", help="Edit a note.")
    subParser.add_parser("create", help="Create a new note")
    subParser.add_parser("serve", help="Start server.")
    topicParser = subParser.add_parser("topic", help="Create or Edit a topic.")

    topicSubparsers = topicParser.add_subparsers(
        dest="topicAction", title="Topic Subcommands", required=True, description="Topic actions"
    )
    topicSubparsers.add_parser("create", help="Create a new topic")
    topicSubparsers.add_parser("edit", help="Edit an existing topic")

    # Parse the command-line arguments
    args = parser.parse_args()
    return args
