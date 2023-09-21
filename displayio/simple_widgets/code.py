import board
import busio
import displayio
import terminalio
import time
import adafruit_st7789
import supervisor

from adafruit_display_shapes.rect import Rect
from adafruit_display_shapes.circle import Circle
from adafruit_display_text.label import Label
from adafruit_displayio_layout.widgets.widget import Widget

_WIDTH = 320
_HEIGHT = 240

_FILL = 0x000000
_OUTLINE = 0xFFFFFF

_FONT = terminalio.FONT
_FONT_W, _FONT_H = _FONT.get_bounding_box()
_FONT_SCALE = 2


class Button(Widget):
    """ Basic implementation of a Widget """

    def __init__(
            self,
            x=0,
            y=0,
            scale=1,
            width=None,
            height=None,
            anchor_point=None,
            anchored_position=None,
            text=None,
            font=terminalio.FONT,
            fill=0x000000,
            outline=0xFFFFFF,
    ):
        super().__init__(
            x=x,
            y=y,
            scale=scale,
            width=width,
            height=height,
            anchor_point=anchor_point,
            anchored_position=anchored_position
        )
        self._text = text
        self._font = font
        self.fill = fill
        self.outline = outline

        self._create_button()

    def _empty_self_group(self):
        while len(self) > 0:
            self.pop()

    def _create_button(self):
        self._background = Rect(
            x=0,
            y=0,
            width=self._width,
            height=self._height,
            fill=self.fill,
            outline=self.outline,
            stroke=1
        )
        if self._text is not None:
            self._label = Label(
                self._font,
                scale=1,
                text=self._text,
                anchor_point=(0.5, 0.5),
                anchored_position=(self._width // 2, self._height // 2)
            )

        self.append(self._background)
        self.append(self._label)

    def resize(self, new_width: int, new_height: int) -> None:
        self._width = new_width
        self._height = new_height

        self._bounding_box[2] = new_width
        self._bounding_box[3] = new_height

        self._empty_self_group()
        self._create_button()
        self._update_position()

    @property
    def text(self):
        return self._text

    @text.setter
    def text(self, new_text):
        self._text = str(new_text)
        self._empty_self_group()
        self._create_button()


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
    displayio.release_displays()
    tft_spi = busio.SPI(tft_sck, tft_mosi)
    tft_bus = displayio.FourWire(
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

    screen = displayio.Group()
    display.show(screen)

    workspace = displayio.Group(x=20, y=20)
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
        font=_FONT,
        fill=_FILL,
        outline=_OUTLINE
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

