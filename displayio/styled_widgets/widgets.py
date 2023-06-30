""" DisplayIO Layout Widgets with a bit of flair """
from adafruit_displayio_layout.widgets.widget import Widget

from styles import Style


class StyledWidget(Widget):
    """This is a :class:`adafruit_displayio_layout.widgets.widget.Widget` that's rendered based on the
    :class:`styles.Style` applied to it. This makes it easy to change the appearance of the widget on the fly while
    retaining the attributes of the object.

    :param int x: pixel position
    :param int y: pixel position
    :param int width: width of the widget in pixels, set to None to auto-size relative to
     the height
    :param int height: height of the widget in pixels
    :param int scale:
    :param anchor_point: (X,Y) values from 0.0 to 1.0 to define the anchor point relative to the
     widget bounding box
    :type anchor_point: Tuple[float,float]
    :param anchored_position: (x,y) pixel value for the location of the anchor_point
    :type anchored_position: Tuple[int, int]
    :param style:
    :type style: Style
    """
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
    ) -> None:
        super().__init__(
            x=x,
            y=y,
            scale=scale,
            width=width,
            height=height,
            anchor_point=anchor_point,
            anchored_position=anchored_position
        )

        self.style = style

    def _empty_self_group(self) -> None:
        while len(self) > 0:
            self.pop()

    def resize(self, new_width: int, new_height: int) -> None:
        """Resizes the widget dimensions (for use with automated layout functions).

        :param new_width:
        :param new_height:
        :return: None
        """
        self._width = new_width
        self._height = new_height

        self._bounding_box[2] = new_width
        self._bounding_box[3] = new_height

        self._style.render(self)
        self._update_position()

    @property
    def style(self) -> str:
        """Get the style used by the button.

        :return: str
        """
        return repr(self._style)

    @style.setter
    def style(self, new_style: Style) -> None:
        """Set the style used by the button.
        :param new_style: The new style for the button to use.
        :type new_style: Style
        """
        if not issubclass(type(new_style), Style):
            raise TypeError(f"{type(new_style)} not a subclass of Style")
        self._style = new_style
        self._style.render(self)


class Button(StyledWidget):
    """Basic implementation of a :class:`StyledWidget`. Renders some text

    :param int x: pixel position
    :param int y: pixel position
    :param int width: width of the widget in pixels, set to None to auto-size relative to
     the height
    :param int height: height of the widget in pixels
    :param int scale:
    :param anchor_point: (X,Y) values from 0.0 to 1.0 to define the anchor point relative to the
     widget bounding box
    :type anchor_point: Tuple[float,float]
    :param anchored_position: (x,y) pixel value for the location of the anchor_point
    :type anchored_position: Tuple[int, int]
    :param style:
    :type style: Style
    :param str text: The label or name for the button.
    """
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
    ) -> None:
        self._text = text
        super().__init__(
            x=x,
            y=y,
            scale=scale,
            width=width,
            height=height,
            anchor_point=anchor_point,
            anchored_position=anchored_position,
            style=style
        )

    @property
    def text(self) -> str:
        """Get the text displayed on the button.

        :return: str
        """
        return self._text

    @text.setter
    def text(self, new_text: str) -> None:
        """Set the text displayed on the button.

        :param str new_text: The new name or label for the button.
        :return: None
        """
        self._text = new_text
        self._style.render(self)
