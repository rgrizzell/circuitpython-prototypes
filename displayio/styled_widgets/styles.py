from adafruit_display_shapes.rect import Rect
from adafruit_display_shapes.roundrect import RoundRect
from adafruit_display_text.label import Label


class Style:
    def __init__(self, name=None):
        self.name = name

    def render(self, widget):
        raise NotImplementedError("Subclasses should override the render function!")


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


class RoundedBox(ButtonStyle):
    def __init__(self, radius, *args, **kwargs):
        self.radius = radius
        super().__init__(*args, **kwargs)

    def _render(self, widget):
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
        if widget.text is not None:
            widget[1] = Label(
                self.font,
                scale=self.font_scale,
                text=widget.text,
                anchor_point=(0.5, 0.5),
                anchored_position=(widget.width // 2, widget.height // 2)
            )
