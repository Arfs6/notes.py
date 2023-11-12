# -*- coding: utf-8 -*-
import os
import sys
import logging

from .paths import getDataDir

def setupLogging():
    """Set up logging"""
    logger = logging.getLogger()

    # Set log level based on environment variable, default to INFO
    logLevelStr = os.environ.get("NOTES_PY_LOGGING_LEVEL", "INFO")
    logLevel = getattr(logging, logLevelStr, logging.INFO)

    logger.setLevel(logLevel)

    # Create a formatter
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    # Create a file handler
    logsDirectory = os.path.join(getDataDir(), "logs")
    os.makedirs(logsDirectory, exist_ok=True)
    logFile = os.path.join(logsDirectory, "notes.py.log")
    fileHandler = logging.FileHandler(logFile)
    fileHandler.setLevel(logLevel)
    fileHandler.setFormatter(formatter)

    # Add the file handler to the logger
    logger.addHandler(fileHandler)

    # Check if the environment variable 'NOTES_PY_LOGGING' is set to 'stdout'
    if os.environ.get("NOTES_PY_LOGGING") == "stdout":
        # Create a console handler and set the level
        consoleHandler = logging.StreamHandler(sys.stdout)
        consoleHandler.setLevel(logLevel)
        consoleHandler.setFormatter(formatter)

        # Add the console handler to the logger
        logger.addHandler(consoleHandler)
