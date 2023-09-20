import board
import busio
from displayio import Group, FourWire, release_displays
import adafruit_st7789

from adafruit_display_shapes.rect import Rect
from adafruit_display_shapes.circle import Circle

_WIDTH = 320
_HEIGHT = 240

_FILL = 0x000000
_OUTLINE = 0xFFFFFF

screen = Group()


def init_display():
    # Define pins connected to the chip
    tft_sck = board.GP18
    tft_mosi = board.GP19
    tft_blk = board.GP20
    tft_dc = board.GP16
    tft_cs = board.GP21
    tft_rst = None

    # Reset the chip and re-initialize it
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
    return screen


def build_workspace():
    border = Rect(
        x=0,
        y=0,
        width=200,
        height=200,
        fill=_FILL,
        outline=_OUTLINE,
        stroke=1
    )
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

    workspace = Group()
    workspace.append(border)
    workspace.append(calibration_square)
    workspace.append(center_circle)
    return workspace


if __name__ == "__main__":
    screen = init_display()
    screen.append(build_workspace())

    while True:
        time.sleep(1)