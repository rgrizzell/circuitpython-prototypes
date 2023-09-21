""" Workspace used for display testing on an ST7789 """
import board
import busio
import displayio
from displayio import Group, FourWire, release_displays
import time

import adafruit_st7789
from adafruit_display_shapes.rect import Rect
from adafruit_display_shapes.circle import Circle


def init_display(width: int = 320, height: int = 240, rotation: int = 0) -> displayio.Display:
    release_displays()
    spi = busio.SPI(board.GP18, board.GP19)
    bus = FourWire(
        spi_bus=spi, command=board.GP16, chip_select=board.GP21, reset=None
    )
    display = adafruit_st7789.ST7789(
        bus=bus,
        backlight_pin=board.GP20,
        rotation=rotation,
        width=width,
        height=height,
    )

    return display


def workspace(width, height, fill, outline):
    border = Rect(
        x=0, y=0, width=width, height=height, fill=fill, outline=outline, stroke=1
    )
    center_circle = Circle(
        x0=width // 2, y0=height // 2, r=10, fill=fill, outline=outline, stroke=1
    )
    nw_square = Rect(
        x=0, y=0, width=20, height=20, fill=fill, outline=outline, stroke=1
    )
    ne_square = Rect(
        x=300, y=0, width=20, height=20, fill=fill, outline=outline, stroke=1
    )
    sw_square = Rect(
        x=0, y=220, width=20, height=20, fill=fill, outline=outline, stroke=1
    )
    se_square = Rect(
        x=300, y=220, width=20, height=20, fill=fill, outline=outline, stroke=1
    )

    g = Group()
    g.append(border)
    g.append(nw_square)
    g.append(ne_square)
    g.append(sw_square)
    g.append(se_square)
    g.append(center_circle)
    return g


if __name__ == "__main__":
    display = init_display(rotation=270)
    display.show(workspace(320, 240, 0x000000, 0xFFFFFF))

    while True:
        time.sleep(5)
