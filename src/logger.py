# -*- coding: utf-8 -*-
"""Configures logging."""

import os
import sys
import logging

# Set up logging
logger = logging.getLogger()
logger.setLevel(logging.DEBUG if os.environ.get("NOTE_PY_DEBUG") else logging.DEBUG)

# Create a console handler and set the level
ch = logging.StreamHandler(sys.stdout)
ch.setLevel(logging.DEBUG)

# Create a formatter and set the formatter for the handler
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)

# Add the handler to the logger
logger.addHandler(ch)

# If Check NOTE_PY_LOGGING
if not os.environ.get("NOTE_PY_LOGGING"):
    logs_directory = "logs"
    os.makedirs(logs_directory, exist_ok=True)

    log_file = os.path.join(logs_directory, "notes.py.log")

    # Create a file handler
    fh = logging.FileHandler(log_file)
    fh.setLevel(logging.INFO)  # Log info-level messages to the file

    # Set the formatter for the file handler
    fh.setFormatter(formatter)

    # Add the file handler to the logger
    logger.addHandler(fh)
