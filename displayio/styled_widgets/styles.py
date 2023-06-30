import fontio
from adafruit_displayio_layout.widgets.widget import Widget
from adafruit_display_shapes.rect import Rect
from adafruit_display_shapes.roundrect import RoundRect
from adafruit_display_text.label import Label


class Style:
    """The way that a Widget is rendered."""
    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.__dict__})"

    def render(self, widget: Widget) -> None:
        """Takes the widget and renders the appearance of it.

        :param widget: The widget object that should be rendered with the chosen style.
        :type widget: widgets.StyledWidget
        :return: None
        """
        raise NotImplementedError("This function should be overridden by the subclass.")


class ButtonStyle(Style):
    """Basic implementation of a :class:`Style`.

    :param int|None fill: The color to fill the rounded-corner rectangle. Can be a hex value
                    for a color or ``None`` for transparent.
    :param int|None outline: The outline of the rounded-corner rectangle. Can be a hex value
                    for a color or ``None`` for no outline.
    :param font: A font class that has ``get_bounding_box`` and ``get_glyph``.
      Must include a capital M for measuring character size.
    :type font: ~fontio.FontProtocol
    :param int font_scale: Integer value of the pixel scaling
    """
    def __init__(
        self,
        fill: int,
        outline: int,
        font: fontio.FontProtocol,
        font_scale: int = 1
    ):
        self.fill = fill
        self.outline = outline
        self.font = font
        self.font_scale = font_scale
        super().__init__()

        self.background = None
        self.label = None


class BoxButtonStyle(ButtonStyle):
    """Renders the button in a generic rectangular box.

    :param int|None fill: The color to fill the rounded-corner rectangle. Can be a hex value
                    for a color or ``None`` for transparent.
    :param int|None outline: The outline of the rounded-corner rectangle. Can be a hex value
                    for a color or ``None`` for no outline.
    :param font: A font class that has ``get_bounding_box`` and ``get_glyph``.
           Must include a capital M for measuring character size.
    :type font: ~fontio.FontProtocol
    :param int font_scale: Integer value of the pixel scaling"""
    def __init__(
        self,
        fill: int,
        outline: int,
        font: fontio.FontProtocol,
        font_scale: int = 1
    ):
        super().__init__(
            fill=fill,
            outline=outline,
            font=font,
            font_scale=font_scale
        )

    def render(self, widget: Widget):
        self.background = Rect(
            x=0,
            y=0,
            width=widget.width,
            height=widget.height,
            fill=self.fill,
            outline=self.outline,
            stroke=1
        )

        if hasattr(widget, 'text'):
            self.label = Label(
                self.font,
                scale=self.font_scale,
                text=widget.text,
                anchor_point=(0.5, 0.5),
                anchored_position=(widget.width // 2, widget.height // 2)
            )

        widget.insert(0, self.background)
        widget.insert(1, self.label)
        while len(widget) > 2:
            widget.pop(-1)


class RoundedBoxButtonStyle(ButtonStyle):
    """Renders the button in a box with rounded corners.

    :param radius: The radius of the rounded corner.
    :param int|None fill: The color to fill the rounded-corner rectangle. Can be a hex value
                    for a color or ``None`` for transparent.
    :param int|None outline: The outline of the rounded-corner rectangle. Can be a hex value
                    for a color or ``None`` for no outline.
    :param font: A font class that has ``get_bounding_box`` and ``get_glyph``.
           Must include a capital M for measuring character size.
    :type font: ~fontio.FontProtocol
    :param int font_scale: Integer value of the pixel scaling
    """
    def __init__(
        self,
        radius: int,
        fill: int,
        outline: int,
        font: fontio.FontProtocol,
        font_scale: int = 1
    ):
        super().__init__(
            fill=fill,
            outline=outline,
            font=font,
            font_scale=font_scale
        )

        self.radius = radius

    def render(self, widget: Widget):
        self.background = RoundRect(
            x=0,
            y=0,
            r=self.radius,
            width=widget.width,
            height=widget.height,
            fill=self.fill,
            outline=self.outline,
            stroke=1
        )

        if hasattr(widget, 'text'):
            self.label = Label(
                self.font,
                scale=self.font_scale,
                text=widget.text,
                anchor_point=(0.5, 0.5),
                anchored_position=(widget.width // 2, widget.height // 2)
            )

        widget.insert(0, self.background)
        widget.insert(1, self.label)
        while len(widget) > 2:
            widget.pop(-1)
