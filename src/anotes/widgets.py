# -*- coding: utf-8 -*-
"""This module has urwid related code."""
from logging import getLogger
import urwid
from typing import Optional, TYPE_CHECKING, Any
if TYPE_CHECKING:
    from .database import Topic, Note


log = getLogger('widgets')
PALETTE = [("normal", "black", "white"),
           ("highlighted", "black", "dark cyan")]


class Selector:
    """Selects an item from a list."""

    def handler(self, key: str):
        """Handels all key press events."""
        if key in ['q', 'Q', 'esc']:
            self.quit = True
            raise urwid.ExitMainLoop()
        elif key == "enter":
            try:
                self.selected = self._real[self.listBox.focus_position]
            except IndexError:
                log.info("Topic has no sub topic.")
            finally:
                    raise urwid.ExitMainLoop()

    def __init__(self, objects: list[str], real: list):
        """Select an object from a list of objects.
        parameters:
        - objects: A list of string to display.
        - real: The list of the main objects.
        """
        self.selected: Optional[Any] = None
        self.quit: bool = False
        self._real: list[Any] = real
        self.next = False # Change to True when right arrow is used to select.
        self.footer = "Type q | Q | ESC to cancel"
        contents = [urwid.AttrMap(urwid.SelectableIcon(obj), "normal", "highlighted") for obj in objects]
        self.walker = urwid.SimpleFocusListWalker(contents)
        self.listBox = urwid.ListBox(self.walker)
        self._loop = urwid.MainLoop(self.listBox, unhandled_input=self.handler)

    def run(self):
        """Start Selector UI."""
        self._loop.run()


class TopicSelector(Selector):
    """This selector specializes on selecting topics.
    Topics have children.
    """

    def handler(self, key: str):
        """Handels the tab and right arrow key.
        parameters:
        - key: The fired key.
        """
        if key in ['tab', 'right']:
            self.next = True
            self.selected = self._real[self.listBox.focus_position]
            raise urwid.ExitMainLoop
        super().handler(key)

    @property
    def hasChildren(self) -> bool:
        """Checks if the focused topic has children."""
        return True if self._real[self.listBox.focus_position].children else False


    def __init__(self, *args, **kwargs):
        """Initialize the next attribute."""
        self.next: bool = False
        super().__init__(*args, **kwargs)
def selectTopic(topic: 'Topic') -> tuple[Optional['Topic'], Optional['Topic']]:
    """Selects a topic.
    Selection starts from topic's children, i.e. `Topic.children`.
    parameters:
    - topic: `Topic` object, most probably base topic.
    returns: selected topic.
    """
    log.info("Selecting a topic...")
    pTopic: 'Topic' = topic
    while True:
        children = pTopic.children
        selector = TopicSelector([t.name for t in children], children)
        selector.run()
        if selector.next:
            log.debug(f"Parent topic is now: {pTopic}")
            pTopic = selector.selected
        else:
            break
    log.info("Topic selected or canceled.")
    if selector.quit:
        return None, None
    return pTopic, selector.selected


def selectNote(topic: 'Topic') -> Optional['Note']:
    """Selects a note.
    Selection of notes is based on topics. i.e. a topic will be selected first before notes in the topic will be selected.
    parameters:
    topic -> topic to start selection from.
    returns:
    - Note: Selected note
    - None: no selected note, user canceled operation.
    """
    log.info("Selecting topic.")
    pTopic, selectedTopic = selectTopic(topic)
    if not selectedTopic:
        return  # User canceled.
    notes = selectedTopic.notes
    log.debug(f"List of notes = {notes}")
    selector = Selector([note.title for note in notes], notes)
    selector.run()
    return selector.selected
