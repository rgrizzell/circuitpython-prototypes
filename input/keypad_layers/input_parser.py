""" a """
import supervisor
from keymap import LayeredKeyMap

try:
    from typing import Any, Dict, List, Tuple
except ImportError:
    pass


class InputParser:
    """ a """
    def __init__(self, device: any):
        self._device = device

    def get_events(self):
        """ a """
        raise NotImplementedError("InputParser is not to be used directly. Override this function with a subclass.")

    def initialize(self):
        """ a """
        raise NotImplementedError("InputParser is not to be used directly. Override this function with a subclass.")


class KeypadInputParser(InputParser):
    """ a """
    SHIFT = b"\x0e"

    def __init__(
            self,
            device: Any,
            keymap: LayeredKeyMap
    ):
        self.repeat_interval = 300
        self._keymap = keymap
        self._presses = dict()
        self._double_shift = 0
        self._double_shift_t = supervisor.ticks_ms()
        super().__init__(device=device)

    def initialize(self):
        """ a """
        pass

    @property
    def layers(self):
        """

        :return:
        """
        return self._keymap.key_mapping.keys()

    def get_events(self):
        """

        :return:
        """
        events = []
        while len(self._device.events) > 0:
            event = self._device.events.get()
            keycode = self._keymap[event.key_number]

            if event.pressed:
                self._presses[event.key_number] = event.timestamp

            if event.released:
                if event.key_number in self._presses.keys():
                    events.append(keycode)
                    if keycode == self.SHIFT:
                        if self._double_shift >= 1 and (event.timestamp - self._double_shift_t) < 1000:
                            self._keymap.next_layer()
                            print(f"New Layer: {self._keymap.layer}")
                            self._double_shift = 0
                        else:
                            self._double_shift += 1
                        self._double_shift_t = event.timestamp
                    self._presses.pop(event.key_number)

        for key_number, timestamp in self._presses.items():
            now = supervisor.ticks_ms()
            if (now - timestamp) > self.repeat_interval:
                keycode = self._keymap[key_number]
                events.append(keycode)
                self._presses[key_number] = now

        return events
