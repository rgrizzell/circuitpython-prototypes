from displayio import TileGrid
from adafruit_displayio_layout.widgets.widget import Widget
from adafruit_display_shapes.rect import Rect
from adafruit_display_shapes.roundrect import RoundRect
from adafruit_display_text.label import Label


class Style:
    def __init__(self, name: str = None):
        self._name = name

    def __repr__(self):
        return f"{self.__class__.__name__}('{self._name}')"

    def render(self, widget: Widget):
        pass
    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, new_name: str):
        self._name = str(new_name)


class ButtonStyle(Style):
    def __init__(self, fill, outline, font, font_scale, *args, **kwargs):
        self.fill = fill
        self.outline = outline
        self.font = font
        self.font_scale = font_scale
        super().__init__(*args, **kwargs)


class BoxButtonStyle(ButtonStyle):
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
    def __init__(self, radius, fill, outline, font, font_scale, *args, **kwargs):
        self.radius = radius
        super().__init__(fill, outline, font, font_scale, *args, **kwargs)

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
