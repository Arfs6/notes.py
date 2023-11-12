# -*- coding: utf-8 -*-
"""Database module.
This module has code related to database and storage.
It contains two database models, `Topic` and `Note`.
`Topic` represents a topic while `Note` represents a note.
Each topic can have several notes except the base topic.
arfs6: I view the base topic as a shelf.
    All other topics as either a book or a group of related books. Perhaps different volumes.
"""

from pathlib import Path
import peewee as pw
import datetime
import os
from logging import getLogger
from typing import Optional

from .paths import getDataDir


log = getLogger("database")
db = pw.SqliteDatabase(os.path.join(getDataDir(), "anotes.db"))


class BaseModel(pw.Model):
    """Base class for all models"""

    class Meta:
        database = db


class Topic[Topic](BaseModel):
    """Topic Model."""

    id = pw.AutoField(primary_key=True, null=True)
    name = pw.CharField(null=False)
    filePath = pw.CharField(null=False, unique=True)
    parentId = pw.IntegerField(null=False)

    @property
    def parent(self) -> Optional[Topic]:
        """Returns the parent of the current topic"""
        if self.isRoot:
            return
        return type(self).get(type(self).id == self.parentId)

    @property
    def children(self):
        """Returns all the nested topics"""
        return list(self.__class__.select().where(self.__class__.parentId == self.id))

    def __init__(self, *args, **kwargs):
        """Initialize object."""
        super().__init__(*args, **kwargs)
        self.isRoot = True if self.parentId == 0 else False

    @classmethod
    def create(cls, name: str, parent: Topic) -> Topic:
        """Creates a topic.
        Parameters:
        - name: Name of topic
        - parentId: id of parent topic.
        Returns: topic object created.
        """
        new = cls()
        new.name = name
        new.parentId = parent.id
        from . import utils

        new.filePath = os.path.join(parent.filePath, utils.stripSpecialCharacters(name))
        new.save()
        os.makedirs(
            os.path.join(utils.getRawDirPath(), new.filePath[1:]), exist_ok=True
        )

        # Create index.html file
        from .template import render

        content = render("topic.html", content="", topic=new)
        exportsPath = os.path.join(utils.getHTMLDir(), new.filePath[1:], "index.html")
        os.makedirs(os.path.dirname(exportsPath), exist_ok=True)
        with open(exportsPath, "w") as fileObj:
            fileObj.write(content)

        # update parent
        new.parent.update()
        return new

    def update(self):
        """Updates a topic"""
        log.info(f"Updating topic <{self.name}>")
        from . import utils

        rawPath = os.path.join(utils.getRawDirPath(), self.filePath[1:], "index.md")
        from .converter import convert

        converted = convert(rawPath)
        from .template import render

        output = render("topic.html", content=converted, topic=self)
        exportsPath = Path(
            os.path.join(utils.getHTMLDir(), self.filePath[1:], "index.html")
        )
        os.makedirs(os.path.dirname(exportsPath), exist_ok=True)
        with open(exportsPath, "w") as fileObj:
            fileObj.write(output)


class Note[Note](BaseModel):
    """Note model."""

    id = pw.AutoField(primary_key=True, null=True)
    title = pw.CharField(null=False)
    filePath = pw.CharField(null=False, unique=True)
    createdAt = pw.DateTimeField(null=False, default=datetime.datetime.now)
    updatedAt = pw.DateTimeField(null=False, default=datetime.datetime.now)
    topic = pw.ForeignKeyField(Topic, backref="notes")

    def __init__(self, *args, **kwargs):
        """Initialize object."""
        super().__init__(*args, **kwargs)

    @classmethod
    def create(cls, title: str, ext: str, topic: Topic) -> Note:
        """Creates a new note
        Parameters:
        - title: Title of note
        - ext: file extension for note
        - topic: topic which note is under.
        Returns: created note.
        """
        new = cls()
        new.title = title
        new.topic = topic
        from . import utils

        new.filePath = os.path.join(
            topic.filePath,
            utils.stripSpecialCharacters(title) + "." + ext,
        )
        new.save()
        topic.update()
        from .template import render

        output = render("note.html", content="", note=new)
        exportPath = Path(os.path.join(utils.getHTMLDir(), new.filePath[1:]))
        with open(exportPath.with_suffix(".html"), "w") as fileObj:
            fileObj.write(output)
        return new

    def update(self):
        """Updates a note."""
        self.updatedAt = datetime.datetime.now()
        from .converter import convert
        from . import utils

        converted = convert(os.path.join(utils.getRawDirPath(), self.filePath[1:]))
        from .template import render

        output = render("note.html", content=converted, note=self)
        exportPath = Path(os.path.join(utils.getHTMLDir(), self.filePath[1:]))
        with open(exportPath.with_suffix(".html"), "w") as fileObj:
            fileObj.write(output)

    @property
    def htmlFilePath(self):
        """Returns the html output file path for this note"""
        return Path(self.filePath).with_suffix(".html")


def createBaseTopic():
    """Creates the base topic if it doesn't exist"""
    try:
        baseTopic = Topic.get(Topic.id == 1)
    except Topic.DoesNotExist:
        newBaseTopic = Topic(name="My Notes", filePath="/", parentId=0)
        newBaseTopic.save()
        newBaseTopic.update()


def setup():
    """Setup the database."""
    db.create_tables([Topic, Note])
    createBaseTopic()


def close():
    """Close the database connection."""
    db.close()
