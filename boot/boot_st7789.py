""" Bootstraps the display for convenient terminal output. """
import board
import busio
import displayio

_WIDTH = 320
_HEIGHT = 240

try:
    import adafruit_st7789

    """Define pins connected to the chip"""
    tft_sck = board.GP18
    tft_mosi = board.GP19
    tft_blk = board.GP20
    tft_dc = board.GP16
    tft_cs = board.GP21
    tft_rst = None

    """Reset the chip and re-initialize it"""
    displayio.release_displays()
    tft_spi = busio.SPI(tft_sck, tft_mosi)
    tft_bus = displayio.FourWire(
        spi_bus=tft_spi, command=tft_dc, chip_select=tft_cs, reset=tft_rst
    )
    display = adafruit_st7789.ST7789(
        bus=tft_bus, backlight_pin=tft_blk, rotation=270, width=_WIDTH, height=_HEIGHT
    )

    screen = displayio.Group()
    display.show(screen)
except ImportError as e:
    print(e)
    pass
