from adafruit_display_shapes.rect import Rect
from adafruit_display_shapes.roundrect import RoundRect
from adafruit_display_text.label import Label

from widgets import StyledWidget


class Style:
    def __init__(self, name: str = None, *allowed_types):
        self._name = name
        self._allowed_types = allowed_types or StyledWidget

    def __repr__(self):
        return f"{self._name}"

    def _check_widget_type(self, widget: StyledWidget):
        """ TODO: Figure out a way to check only once instead of every render."""
        if not isinstance(widget, self._allowed_types):
            raise TypeError(f"{type(widget)} not of types {self._allowed_types}")

    def render(self, widget):
        self._check_widget_type(widget)


class ButtonStyle(Style):
    def __init__(self, fill, outline, font, font_scale, *args, **kwargs):
        self.fill = fill
        self.outline = outline
        self.font = font
        self.font_scale = font_scale
        super().__init__(*args, **kwargs)


class Box(ButtonStyle):
    def render(self, widget):
        widget[0] = Rect(
            x=0,
            y=0,
            width=widget.width,
            height=widget.height,
            fill=self.fill,
            outline=self.outline,
            stroke=1
        )

        if widget.text is not None:
            widget[1] = Label(
                self.font,
                scale=self.font_scale,
                text=widget.text,
                anchor_point=(0.5, 0.5),
                anchored_position=(widget.width // 2, widget.height // 2)
            )
        else:
            if widget[1]:
                del widget[1]


class RoundedBox(ButtonStyle):
    def __init__(self, radius, *args, **kwargs):
        self.radius = radius
        super().__init__(*args, **kwargs)

    def render(self, widget):
        widget[0] = RoundRect(
            x=0,
            y=0,
            r=self.radius,
            width=widget.width,
            height=widget.height,
            fill=self.fill,
            outline=self.outline,
            stroke=1
        )

        if widget.text:
            widget[1] = Label(
                self.font,
                scale=self.font_scale,
                text=widget.text,
                anchor_point=(0.5, 0.5),
                anchored_position=(widget.width // 2, widget.height // 2)
            )
        else:
            if widget[1]:
                del widget[1]
