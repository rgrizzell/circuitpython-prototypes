class Driver(object):
    """Acts as the interface between the application and the hardware.

    Since you can not set attributes on a function object, use __slots__, or metaclasses in CircuitPython,
    Abstract Base Classes are not supported.
    """
    def __set_name__(self, owner, name):
        self._name = name

    def __get__(self, instance, owner):
        if instance is None:
            return self
        return instance

    def __set__(self, instance, value):
        raise AttributeError("")

    def load(self, *args, **kwargs):
        raise NotImplementedError("")

    def unload(self, *args, **kwargs):
        pass


class LoRa(Driver):
    """LoRa Driver

    """
    def __init__(self, name=None):
        self._name = name
        self._radio = None

    def __get__(self, instance, owner):
        if instance is None:
            return self
        return instance

    def load(self, pins):
        import adafruit_rfm9x
        self._radio = adafruit_rfm9x.RFM9x(pins)


class MyApplication:
    lora_radio = Radio("lora")


if __name__ == "__main__":
    app = MyApplication()
