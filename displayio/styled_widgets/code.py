import board
import busio
from displayio import Group, FourWire, release_displays
import terminalio
import time
import adafruit_st7789
import supervisor

from adafruit_display_shapes.rect import Rect
from adafruit_display_shapes.circle import Circle

from styles import Box
from widgets import Button

_WIDTH = 320
_HEIGHT = 240

_FILL = 0x000000
_OUTLINE = 0xFFFFFF

_FONT = terminalio.FONT
_FONT_W, _FONT_H = _FONT.get_bounding_box()
_FONT_SCALE = 2


if __name__ == "__main__":
    supervisor.runtime.autoreload = False

    """Define pins connected to the chip"""
    tft_sck = board.GP18
    tft_mosi = board.GP19
    tft_blk = board.GP20
    tft_dc = board.GP16
    tft_cs = board.GP21
    tft_rst = None

    """Reset the chip and re-initialize it"""
    release_displays()
    tft_spi = busio.SPI(tft_sck, tft_mosi)
    tft_bus = FourWire(
        spi_bus=tft_spi,
        command=tft_dc,
        chip_select=tft_cs,
        reset=tft_rst
    )
    display = adafruit_st7789.ST7789(
        bus=tft_bus,
        backlight_pin=tft_blk,
        rotation=270,
        width=_WIDTH,
        height=_HEIGHT
    )

    screen = Group()
    display.show(screen)

    workspace = Group(x=20, y=20)
    border = Rect(
        x=0,
        y=0,
        width=200,
        height=200,
        fill=_FILL,
        outline=_OUTLINE,
        stroke=1
    )
    workspace.append(border)

    calibration_square = Rect(
        x=0,
        y=0,
        width=20,
        height=20,
        fill=_FILL,
        outline=_OUTLINE,
        stroke=1
    )
    center_circle = Circle(
        x0=100,
        y0=100,
        r=10,
        fill=_FILL,
        outline=_OUTLINE,
        stroke=1
    )
    workspace.append(calibration_square)
    workspace.append(center_circle)

    button = Button(
        text="Test",
        width=100,
        height=40,
        anchor_point=(0.5, 0.5),
        anchored_position=(100, 100),
        style=Box(
            fill=_FILL,
            outline=_OUTLINE,
            font=_FONT,
            font_scale=_FONT_SCALE
        )
    )
    workspace.append(button)

    screen.append(workspace)
    big_time = 0
    while True:
        workspace.x = 20
        time.sleep(10)
        workspace.x = 80
        if big_time % 3:
            button.resize(60, 80)
        else:
            button.resize(100, 40)
        big_time += 1
        time.sleep(10)
