""" DisplayIO Layout Widgets with a bit of flair """
from adafruit_displayio_layout.widgets.widget import Widget
from styles import Style


class StyledWidget(Widget):
    def __init__(
            self,
            x=0,
            y=0,
            scale=1,
            width=None,
            height=None,
            anchor_point=None,
            anchored_position=None,
            style=Style()
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
        self._style.render(self)

    def _empty_self_group(self):
        while len(self) > 0:
            self.pop()

    def resize(self, new_width: int, new_height: int) -> None:
        self._width = new_width
        self._height = new_height

        self._bounding_box[2] = new_width
        self._bounding_box[3] = new_height

        self._style.render(self)
        self._update_position()

    @property
    def style(self) -> str:
        """ Get the style used by the button. """
        return self._style.name

    @style.setter
    def style(self, new_style: Style) -> None:
        if issubclass(type(new_style), Style):
            self._style = new_style
            self._style.render(self)


class Button(StyledWidget):
    """ Basic implementation of a Widget """

    def __init__(self, text, *args, **kwargs):
        self._text = str(text)
        super().__init__(*args, **kwargs)

    @property
    def text(self) -> str:
        """ Get the text displayed on the button. """
        return self._text

    @text.setter
    def text(self, new_text: str) -> None:
        self._text = str(new_text)
        self._style.render(self)
