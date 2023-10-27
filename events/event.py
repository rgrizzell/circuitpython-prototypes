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
    class Handler(object):
        """Contains extra attributes that otherwise wouldn't
        be set on function or coroutine objects. Both are immutable and do not contain the `__dict__` attribute.
        """

        def __init__(
            self,
            func: callable,
            *args,
            **kwargs,
        ) -> None:
            """

            :param func: Function object to execute as a task.
            :type func: callable
            :param include_event: Whether to pass the event as an argument to the handler.
            :type include_event: bool
            :param args: List or Tuple of arguments to pass to the function.
            :type args: tuple
            :param kwargs: Dict of keyword arguments to pass to the function.
            :type kwargs: dict
            """
            self.func = func
            self.args = args
            self.kwargs = kwargs

        def __call__(self, event: Event = None, *args, **kwargs) -> None:
            n_kwargs = {**self.kwargs, **kwargs}
            self.func(event, *self.args, *args, **n_kwargs)

        def __eq__(self, other):
            if isinstance(other, self.__class__):
                return self.__key() == other.__key()
            return False

        def __hash__(self):
            return hash(self.__key())

        def __repr__(self) -> str:
            return f"{self.__class__.__name__}{self.__dict__}"

        def __key(self):
            return self.func, self.args, self.kwargs

    def __init__(self):
        self._handlers = {}

    def __getitem__(self, item):
        return self._handlers[item]

    def add_handler(self, event: Event, func: callable, *args, **kwargs):
        """Adds a handler or list of handlers for a given Event.

        :param event: List of events in which to add handlers.
        :type event: list[Event]
        :param func: A function or list of functions to execute when an Event is received.
        :type func: callable,
        """
        if not callable(func):
            raise TypeError("func must be a callable object")
        handler = self.Handler(func, *args, **kwargs)
        if event in self._handlers:
            self._handlers[event].append(handler)
        else:
            self._handlers[event] = [handler]

    def remove_handler(self, event: Event, handler: callable = None):
        """Removes some or all of the registered handlers for a given Event.

        :param event: List of events in which to clear handlers.
        :type event: list[Event]
        :param handler: A function or list of functions to remove from the handlers.
        :type handler: Union[callable, list[callable]]
        """
        if event in self._handlers.keys():
            if handler:
                for h in self._handlers[event]:
                    if h.func == handler:
                        self._handlers[event].remove(h)
            else:
                del self._handlers[event]

    def clear_handlers(self, events: Union[Event, list[Event]] = None):
        """Clears all the registered handlers for all Events or a given list of Events.

        :param events: List of events in which to clear handlers.
        :type events: Union[Event, list[Event]]
        """
        if events:
            if isinstance(events, Event):
                events = [events]
            for e in events:
                self.remove_handler(e)
        else:
            self._handlers = {}

    def handle_event(self, event: Event, *args, **kwargs):
        """Takes an event and executes any associated handlers. Also accepts options arguments to pass as well.
        The Event object is accessible to handlers in `kwargs["_event"]`.

        :param event: The Event to handle
        :type event: Event
        """
        if event in self._handlers:
            if kwargs is None:
                kwargs = dict()
            kwargs["_event"] = event
            for handler in self._handlers[event]:
                handler(event)
