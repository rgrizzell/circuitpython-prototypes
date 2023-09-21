"""a"""
import displayio
from displayio import Display, Group, TileGrid
from adafruit_displayio_layout.widgets.widget import Widget

try:
    from typing import List, Type, Union
except ImportError:
    pass


class View(Group):
    """Abstraction of a :class:`displayio.Group` with convenient helper functions.

    Design Goals
    - List of navigable elements/widgets, auto-generated from the self-contained layers.
    - Dictates which inputs keys are valid, executes Actions based on input.
    """

    def __init__(self, view_id: str, *args, **kwargs) -> None:
        self.view_id = view_id
        super().__init__(*args, **kwargs)

    def __call__(self, display: Display) -> None:
        display.show(self)

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.view_id})"

    def append(self, *layers: Union[Group, TileGrid]) -> None:
        """Append a layer to the group. It will be drawn
        above other layers.
        """
        for i in layers:
            self.insert(len(self), i)

    def widgets(self, widget_type: Type[Widget] = Widget) -> list:
        """Returns a tree list of widgets, used primarily for user navigation

        :param widget_type:
        :type widget_type: type
        """
        if not issubclass(widget_type, Widget):
            raise TypeError(f"{widget_type.__class__.__name__} must be a subclass of 'Widget'")
        return filter_group(
            self, filter_func=lambda obj: issubclass(type(obj), widget_type)
        )


def filter_group(group: Group, filter_func: callable = lambda x: x) -> list:
    """Returns a recursive list of contents inside a :class:`displayio.Group`.

    :param group: The group to filter.
    :type group: displayio.Group
    :param filter_func: The function used to determine if an object should be returned. Return True to include and False
    to exclude the object.
    :type filter_func: callable
    """
    elements = []
    for layer in group:
        if type(layer) == Group:
            elements.append(filter_group(layer, filter_func=filter_func))
        elif filter_func(layer):
            elements.append(layer)
    return elements
