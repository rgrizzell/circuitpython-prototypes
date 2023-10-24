"""  """
try:
    from supervisor import ticks_ms as ts
except ImportError:
    from time import time as ts


try:
    from typing import Union
except ImportError:
    pass


class Event:
    """Event object to be handled by an EventHandler

    :param name:
    :type name: str
    :param timestamp:
    :type timestamp: int
    """

    def __init__(self, name: str, timestamp: int = None):
        self.name = name
        self.timestamp = timestamp or ts()

    def __eq__(self, other):
        if isinstance(other, Event):
            return self.__key() == other.__key()
        return False

    def __hash__(self):
        return hash(self.__key())

    def __repr__(self):
        return f"Event({self.name})>"

    def __str__(self):
        return self.name

    def __key(self):
        return self.name


class KeyPressEvent(Event):
    """Key Press Event object to be handled by an EventHandler

    :param name:
    :type name: str
    :param modifiers:
    :type modifiers:
    :param timestamp:
    :type timestamp: int
    """

    def __init__(self, name: str, modifiers: list[str] = None, timestamp: int = None):
        super().__init__(name=name, timestamp=timestamp)
        self.modifiers = sorted(modifiers) if modifiers else list()

    def __repr__(self):
        return f"KeypressEvent({self.name}, modifiers={self.modifiers}>"

    def __str__(self):
        return "+".join(self.__key())

    def __key(self):
        return *self.modifiers, self.name


class EventHandler:
    def __init__(self):
        self._callbacks = {}

    def add_callbacks(self, event: Event, callbacks: Union[callable, list[callable]]):
        """Adds a callback or list of callbacks for a given Event.

        :param event: List of events in which to add callbacks.
        :type event: list[Event]
        :param callbacks: A function or list of functions to execute when an Event is received.
        :type callbacks: Union[callable, list[callable]]
        """
        if callable(callbacks):
            callbacks = [callbacks]
        if event in self._callbacks:
            self._callbacks[event].extend(callbacks)
        else:
            self._callbacks[event] = callbacks

    def remove_callbacks(
        self, event: Event, callbacks: Union[callable, list[callable]] = None
    ):
        """Removes some or all of the registered callbacks for a given Event.

        :param event: List of events in which to clear callbacks.
        :type event: list[Event]
        :param callbacks: A function or list of functions to remove from the callbacks.
        :type callbacks: Union[callable, list[callable]]
        """
        if event in self._callbacks.keys():
            if callbacks:
                if callable(callbacks):
                    callbacks = [callbacks]
                for c in callbacks:
                    try:
                        self._callbacks[event].remove(c)
                    except ValueError:
                        pass
            else:
                del self._callbacks[event]

    def clear_callbacks(self, events: list[Event] = None):
        """Clears all the registered callbacks for all Events or a given list of Events.

        :param events: List of events in which to clear callbacks.
        :type events: list[Event]
        """
        if isinstance(events, Event):
            events = [events]
        if events:
            for e in events:
                self.remove_callbacks(e)
        else:
            self._callbacks = {}

    def handle_event(self, event: Event, *args, **kwargs):
        """Takes an event and executes any associated callbacks. Also accepts options arguments to pass as well.
        The Event object is accessible to callbacks in `kwargs["_event"]`.

        :param event: The Event to handle
        :type event: Event
        """
        if event in self._callbacks:
            if kwargs is None:
                kwargs = dict()
            kwargs["_event"] = event
            for callback in self._callbacks[event]:
                callback(*args, **kwargs)
