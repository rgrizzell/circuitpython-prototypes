"""Examples of working with Displayio Groups and its layers"""
from displayio import Group
import time
from adafruit_display_shapes.rect import Rect
from adafruit_display_shapes.circle import Circle
import workspace  # ../tools/workspace.py


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


if __name__ == "__main__":
    screen = workspace.init_display()
    screen.append(workspace.workspace())

    fill = 0x000000
    outline = 0xFFFFFF
    tall_rect = Rect(
        x=20,
        y=20,
        width=20,
        height=80,
        fill=fill,
        outline=outline,
        stroke=1
    )
    big_circle = Circle(
        x0=75,
        y0=75,
        r=30,
        fill=fill,
        outline=outline,
        stroke=1
    )
    extra_shapes = Group()
    extra_shapes.append(tall_rect)
    extra_shapes.append(big_circle)
    screen.append(extra_shapes)

    print("Unfiltered")
    print(filter_group(screen))
    print("Filtered: Rect")
    print(filter_group(screen, filter_func=lambda x: isinstance(x, Rect)))
    print("Filtered: Circle")
    print(filter_group(screen, filter_func=lambda x: isinstance(x, Circle)))

    while True:
        time.sleep(1)
