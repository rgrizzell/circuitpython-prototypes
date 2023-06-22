from adafruit_displayio_layout.widgets.widget import Widget
from styles import Style


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
            style=Style(),
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
        self._style = style
        self._text = str(text)

        self._style.render(self)

    def _empty_self_group(self):
        while len(self) > 0:
            self.pop()

    def resize(self, new_width: int, new_height: int) -> None:
        self._width = new_width
        self._height = new_height

        self._bounding_box[2] = new_width
        self._bounding_box[3] = new_height

        self.style.render(self)
        self._update_position()

    @property
    def style(self):
        return self._style.name

    @style.setter
    def style(self, style):
        if issubclass(style, Style):
            self._style = style

    @property
    def text(self):
        return self._text

    @text.setter
    def text(self, new_text):
        self._text = str(new_text)
        self._style.render(self)
