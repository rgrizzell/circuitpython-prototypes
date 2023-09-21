"""Examples of working with Displayio Groups and its layers"""
import board
import busio
from displayio import Group, FourWire, release_displays
import time

import adafruit_st7789
from adafruit_display_shapes.rect import Rect
from adafruit_display_shapes.circle import Circle

from view import View
from button import Button

_WIDTH = 320
_HEIGHT = 240

_FILL = 0x000000
_OUTLINE = 0xFFFFFF


def init_display():
    release_displays()
    spi = busio.SPI(board.GP18, board.GP19)
    bus = FourWire(
        spi_bus=spi, command=board.GP16, chip_select=board.GP21, reset=None
    )
    display = adafruit_st7789.ST7789(
        bus=bus,
        backlight_pin=board.GP20,
        rotation=270,
        width=_WIDTH,
        height=_HEIGHT,
    )

    return display


def view_workspace():
    border = Rect(
        x=0, y=0, width=_WIDTH, height=_HEIGHT, fill=_FILL, outline=_OUTLINE, stroke=1
    )
    center_circle = Circle(
        x0=_WIDTH // 2, y0=_HEIGHT // 2, r=10, fill=_FILL, outline=_OUTLINE, stroke=1
    )
    nw_square = Rect(
        x=0, y=0, width=20, height=20, fill=_FILL, outline=_OUTLINE, stroke=1
    )
    ne_square = Rect(
        x=300, y=0, width=20, height=20, fill=_FILL, outline=_OUTLINE, stroke=1
    )
    sw_square = Rect(
        x=0, y=220, width=20, height=20, fill=_FILL, outline=_OUTLINE, stroke=1
    )
    se_square = Rect(
        x=300, y=220, width=20, height=20, fill=_FILL, outline=_OUTLINE, stroke=1
    )

    view = View('workspace')
    view.append(border, center_circle, nw_square, ne_square, sw_square, se_square)
    return view


if __name__ == "__main__":
    display = init_display()
    workspace = view_workspace()
    workspace(display)

    button = Button(
        text="Test",
        width=100,
        height=40,
        anchor_point=(0.5, 0.5),
        anchored_position=(_WIDTH // 2, _HEIGHT // 2),
    )
    workspace.append(button)

    print(workspace.widgets())

    while True:
        time.sleep(5)
