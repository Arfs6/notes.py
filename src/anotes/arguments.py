# -*- coding: utf-8 -*-
"""This module is responsible for parsing command line arguments."""

import argparse


def getArgs():
    """Parses command line arguments and returns a Namespace"""
    parser = argparse.ArgumentParser(
        prog='notes.py',
        description='Notes manager',
    )

# Add the first positional argument
    parser.add_argument('action', choices=['edit', 'create', 'topic'], help="Specify the action to perform")

    # add topic related arguments.
    topicSubparsers = parser.add_subparsers(dest="topicAction", title="Topic Subcommands")
    topicSubparsers.add_parser("create", help="Create a new topic")
    topicSubparsers.add_parser("edit", help="Edit an existing topic")

# Parse the command-line arguments
    return parser.parse_args()
