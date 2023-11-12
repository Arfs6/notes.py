# -*- coding: utf-8 -*-
"""Server for viewing notes in browser locally."""
import signal
import subprocess
import sys
import os

from .utils import getHTMLDir
from .paths import getDataDir


class Server:
    """A server for serving local notes."""

    def run(self):
        """Starts the server."""
        logFilePath = os.path.join(getDataDir(), "logs", "server.log")
        os.makedirs(os.path.dirname(logFilePath), exist_ok=True)
        self.stdoutFile = open(logFilePath, "w")
        self.process = subprocess.Popen(
            [
                sys.executable,  # Current python interpreter
                "-m",
                "http.server",
                "-d",
                getHTMLDir(),
                "-b",  # bind address
                "127.0.0.1",  # localhost
                "7777",  # port
            ],
            stdout=self.stdoutFile,
            stderr=self.stdoutFile,
        )

    def stop(self):
        """Stops server."""
        self.process.send_signal(signal.SIGINT)
        self.process.wait()
        self.stdoutFile.close()
