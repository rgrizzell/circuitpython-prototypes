import board
import busio
import displayio
import terminalio
import time
import adafruit_st7789
import supervisor

from adafruit_display_shapes.rect import Rect
from adafruit_display_text import wrap_text_to_pixels
from adafruit_display_text.label import Label
from adafruit_display_text.scrolling_label import ScrollingLabel
from adafruit_displayio_layout.layouts.grid_layout import GridLayout
from adafruit_displayio_layout.widgets.widget import Widget

_WIDTH = 320
_HEIGHT = 240

_FILL = 0x000000
_OUTLINE = 0xFFFFFF

_FONT = terminalio.FONT
_FONT_W, _FONT_H = _FONT.get_bounding_box()
_FONT_SCALE = 2

_TITLE_BAR_HEIGHT = 30


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
            fill=_FILL,
            fill_active=_OUTLINE,
            outline=_OUTLINE,
            outline_active=_FILL,
            stroke=1,
            stroke_active=4,
            keep_aspect_ratio=False,
            text=None
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
        self._fill = fill
        self._outline = outline
        self._fill_active = fill_active
        self._outline_active = outline_active
        self._stroke = int(stroke)
        self._stroke_active = int(stroke_active)
        self._keep_aspect_ratio = keep_aspect_ratio
        self._active = False
        self._hover = False

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
            fill=self._fill,
            outline=self._outline,
            stroke=self._stroke
        )
        self._border = Rect(
            x=0,
            y=0,
            width=self._width,
            height=self._height,
            fill=self._fill,
            outline=self._outline,
            stroke=self._stroke_active
        )
        self._border.hidden = True
        if self._text is not None:
            self._label = Label(
                _FONT,
                scale=_FONT_SCALE,
                text=self._text,
                anchor_point=(0.5, 0.5),
                anchored_position=(self._width // 2, self._height // 2)
            )

        self.append(self._background)
        self.append(self._border)
        self.append(self._label)

    @property
    def hover(self):
        return self._hover

    @hover.setter
    def hover(self, hover=False):
        if hover:
            self.active = False

            self._hover = True
            self._border.hidden = False
        else:
            self._hover = False
            self._border.hidden = True

    @property
    def active(self):
        return self._active

    @active.setter
    def active(self, active=False):
        if active:
            self.hover = False

            self._active = True
            self._background.fill = self._fill_active
            self._background.outline = self._outline_active
            self._border.fill = self._fill_active
            self._border.outline = self._outline_active
            self._label.color = self._outline_active

        else:
            self._active = False
            self._background.fill = self._fill
            self._background.outline = self._outline
            self._border.fill = self._fill
            self._border.outline = self._outline
            self._label.color = self._outline

    def resize(self, new_width: int, new_height: int, keep_aspect_ratio=False) -> None:
        if keep_aspect_ratio or self._keep_aspect_ratio:
            # aspect_ratio = self._width/self._height
            # if width >= height:
            #   self._width = new_width
            #   self._height = new_width // aspect_ratio
            # else:
            #   self._width = new_height // aspect_ratio
            #   self._height = new_height
            pass
        else:
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


class ButtonLayout(GridLayout):
    def __init__(
            self,
            options,
            button_width=None,
            button_height=None,
            button_spacing=10,
            side_padding=10,
            bottom_padding=5,
            **kwargs
    ):
        super().__init__(
            grid_size=(len(options), 1),
            divider_lines=True,
            **kwargs)
        self._options = options
        self._side_padding = side_padding
        self._bottom_padding = bottom_padding
        self._button_spacing = button_spacing
        self._button_width = button_width
        self._button_height = button_height

        self._add_buttons()

    def _add_buttons(self):
        if self._button_width is None:
            self._button_width = self.cell_size_pixels[0] - self._button_spacing * 2
        if self._button_height is None:
            self._button_height = self.cell_size_pixels[1] - self._bottom_padding

        for i, opt in enumerate(self._options):
            self.add_content(
                Button(
                    text=opt,
                    width=self._button_width,
                    height=self._button_height,
                    anchor_point=(0.5, 0.5),
                    anchored_position=(self._button_width // 2, self._button_height // 2)
                ),
                grid_position=(i, 0),
                cell_size=(1, 1),
                cell_anchor_point=(0.5, 0.5)
            )


class Modal(displayio.Group):
    """
    Create modal boundary
       Compute boundary size from display size.
          display X - side margin value * 2
          display Y - status bar - top margin - bottom_margin
    Create title bar
    Compute lines from text
      How many characters fit on a line?
    Create labels/buttons based on options.
    """
    def __init__(self,
                 side_margin=0,
                 top_margin=0,
                 bottom_margin=0,
                 *args, **kwargs):
        super().__init__(x=side_margin, y=(_TITLE_BAR_HEIGHT + top_margin), *args, **kwargs)
        self.width = _WIDTH - (side_margin * 2)
        self.height = _HEIGHT - (_TITLE_BAR_HEIGHT + top_margin + bottom_margin)


class Choice(Modal):
    def __init__(
            self,
            title,
            text,
            options,
            fill=_FILL,
            outline=_OUTLINE,
            stroke=1,
            title_bar_height=30,
            side_margin=0,
            top_margin=0,
            bottom_margin=0,
            *args,
            **kwargs
    ):
        super().__init__(
            side_margin=side_margin,
            top_margin=top_margin,
            bottom_margin=bottom_margin,
            *args,
            **kwargs
        )
        self._title = title
        self._text = text
        self._options = options
        self._fill = fill
        self._outline = outline
        self._stroke = int(stroke)
        self._title_bar_height = title_bar_height

        self._create_modal()

    def _create_modal(self):
        # start with the background
        self.append(Rect(
            x=0,
            y=0,
            width=self.width,
            height=self.height,
            fill=self._fill,
            outline=self._outline,
            stroke=2
        ))

        # add the title bar
        title_bar_group = displayio.Group(x=0, y=0)
        title_bar_group.append(Rect(
            x=0,
            y=0,
            width=self.width,
            height=self._title_bar_height,
            fill=self._fill,
            outline=self._outline,
            stroke=3
        ))
        title_bar_group.append(Label(
            _FONT,
            scale=_FONT_SCALE,
            text=self._title,
            anchor_point=(0.5, 0.5),
            anchored_position=(self.width // 2, self._title_bar_height // 2)
        ))
        self.append(title_bar_group)

        # create the text box and wrap the lines
        text_box_group = displayio.Group()
        text_lines = wrap_text_to_pixels(self._text, font=_FONT, max_width=(self.width // _FONT_SCALE))
        for i, line in enumerate(text_lines):
            line_x = i * 20
            text_box_group.append(
                Label(
                    _FONT,
                    scale=_FONT_SCALE,
                    text=line,
                    anchor_point=(0, 0),
                    anchored_position=(5, line_x + 30)
                )
            )
        self.append(text_box_group)
        self.append(
            ButtonLayout(
                self._options,
                x=0,
                y=self.height - 30,
                width=self.width,
                height=30
            )
        )

    @property
    def options(self):
        return self._options

    @options.setter
    def options(self, options: list):
        if isinstance(options, str):
            self._options = [options]
        elif isinstance(options, list):
            self._options = options
        else:
            raise TypeError("Options much be list of strings")


def create_title_bar(text):
    max_char = ((_WIDTH // 2) // _FONT_W)
    title = ScrollingLabel(
        _FONT,
        x=5,
        y=15,
        max_characters=max_char,
        scale=_FONT_SCALE,
        text=text
    )

    g = displayio.Group()
    g.append(title)
    return g


def create_app_window():
    background = Rect(
        x=0,
        y=_TITLE_BAR_HEIGHT,
        width=_WIDTH,
        height=(_HEIGHT - _TITLE_BAR_HEIGHT),
        fill=_FILL,
        outline=_OUTLINE,
        stroke=1
    )

    g = displayio.Group()
    g.append(background)
    return g


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

    title_bar = create_title_bar("Modal Test")
    app_window = create_app_window()

    modal = Choice(
        "CATS",
        "How are you gentlemen!!",
        ["BACK", "NEXT", "OK", "EXIT"],
        top_margin=10,
        side_margin=10,
        bottom_margin=10
    )

    screen.append(title_bar)
    screen.append(app_window)
    screen.append(modal)

    button_active = 0
    num_options = len(modal.options)
    while True:
        if len(title_bar[0].full_text) > ((_WIDTH // 2) // _FONT_W):
            title_bar[0].update()

        button_layout = modal[-1]
        button = button_layout.get_cell((button_active % num_options, 0))
        button.hover = True
        time.sleep(3)
        button.active = True
        time.sleep(1)
        button.active = False
        button_active += 1

        if button_active % num_options == 0:
            modal.hidden = True
            time.sleep(2)
            modal.hidden = False