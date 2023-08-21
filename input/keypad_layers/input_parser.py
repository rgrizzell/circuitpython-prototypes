""" a """
import supervisor
from keymap import KeyMap

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
    def __init__(
            self,
            device: Any,
            keymap: KeyMap
    ):
        self.repeat_interval = 300
        self._keymap = keymap
        self._presses = dict()
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
            keycode = self._keymap.lookup(event.key_number)
            print(f"Event: {event}")

            if event.pressed:
                self._presses[event.key_number] = event.timestamp
                # if Shift key, set the next layer, double_shift += 1
                # else, double_shift = 0

            if event.released:
                if event.key_number in self._presses.keys():
                    events.append(keycode)
                    self._presses.pop(event.key_number)
                    # if Shift key, set the previous layer,
                        # if double_shift == 2, set the next layer
                    # else, double_shift = 0

        for key_number, timestamp in self._presses.items():
            now = supervisor.ticks_ms()
            if (now - timestamp) > self.repeat_interval:
                keycode = self._keymap.lookup(key_number)
                events.append(keycode)
                self._presses[key_number] = now

        return events
