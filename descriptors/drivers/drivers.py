""" Using descriptors to invert drivers and create a meta-device class. """
import board
import busio
import displayio
import adafruit_st7789

_WIDTH = 320
_HEIGHT = 240
_ROTATION = 270


class DriverAttribute:
    def __init__(self, *type_checks):
        self._hardware = None
        self._type_checks = type_checks

    def __get__(self, instance, owner):
        if instance is None:
            return self
        return self._hardware

    def __set__(self, instance, value):
        if self._hardware is None:
            self._validate(value)
            self._hardware = value
        else:
            raise ValueError("Attribute is protected and can't be modified")

    def __delete__(self, instance):
        raise ValueError(f"Attribute is protected and can't be deleted")

    def _validate(self, obj):
        if self._type_checks:
            if not isinstance(obj, self._type_checks):
                raise TypeError(f"Is not of type(s) {self._type_checks}")


class Device:
    display = DriverAttribute(displayio.Display)

    def __init__(self):
        self._initialize_display()

    def _initialize_display(self):
        spi = busio.SPI(board.GP18, board.GP19)
        bus = displayio.FourWire(
            spi_bus=spi,
            command=board.GP16,
            chip_select=board.GP21,
            reset=None
        )
        self.display = adafruit_st7789.ST7789(
            bus=bus,
            backlight_pin=board.GP20,
            rotation=_ROTATION,
            width=_WIDTH,
            height=_HEIGHT
        )


if __name__ == "__main__":
    gadget = Device()

    screen = displayio.Group()
    gadget.display.show(screen)
