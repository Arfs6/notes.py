# -*- coding: utf-8 -*-
"""Database module.
This module has code related to database and storage.
It contains two database models, `Topic` and `Note`.
`Topic` represents a topic while `Note` represents a note.
Each topic can have several notes except the base topic.
arfs6: I view the base topic as a shelf.
    All other topics as either a book or a group of related books. Perhaps different volumes.
"""

import peewee as pw
import datetime
import os

from .paths import getDataDir


db = pw.SqliteDatabase(os.path.join(getDataDir(), 'anotes.db'))


class BaseModel(pw.Model):
    """Base class for all models"""
    class Meta:
        database = db


class Topic[Topic](BaseModel):
    """Topic Model."""
    id = pw.AutoField(primary_key=True, null=True)
    name = pw.CharField(null=False)
    filePath = pw.CharField(null=False, unique=True)
    parent = pw.IntegerField(null=False)

    @property
    def children(self):
        """Returns all the nested topics"""
        return list(
            self.__class__.select().
            where(self.__class__.parent == self.id)
        )

    def __init__(self, *args, **kwargs):
        """Initialize object."""
        super().__init__(*args, **kwargs)


class Note(BaseModel):
    """Note model."""
    id = pw.AutoField(primary_key=True, null=True)
    title = pw.CharField(null=False)
    filePath = pw.CharField(null=False, unique=True)
    createdAt = pw.DateTimeField(null=False, default=datetime.datetime.now)
    updatedAt = pw.DateTimeField(null=False, default=datetime.datetime.now)
    topic = pw.ForeignKeyField(Topic, backref='notes')

    def __init__(self, *args, **kwargs):
        """Initialize object."""
        super().__init__(*args, **kwargs)


def createBaseTopic():
    """Creates the base topic if it doesn't exist"""
    try:
        baseTopic = Topic.get(Topic.id == 1)
    except Topic.DoesNotExist:
        newBaseTopic = Topic(name="My Notes", filePath='/', parent=0)
        newBaseTopic.save()


def setup():
    """Setup the database."""
    db.create_tables([Topic, Note])
    createBaseTopic()


def close():
    """Close the database connection."""
    db.close()
