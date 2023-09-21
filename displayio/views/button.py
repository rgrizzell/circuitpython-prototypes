""" a """
import terminalio
from adafruit_display_shapes.rect import Rect
from adafruit_display_text.label import Label
from adafruit_displayio_layout.widgets.widget import Widget


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
            outline=0xFFFFFF
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
            stroke=self.scale
        )
        if self._text is not None:
            self._label = Label(
                self._font,
                scale=self.scale,
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
