""" Tests event.py """
import unittest
from event import EventHandler, Event, KeyPressEvent


class TestEvent(unittest.TestCase):
    """Create a generic event and tests base class functionality."""

    def setUp(self):
        self.event = Event("test_event", 1000)

    def test_event_string(self):
        self.assertEqual(
            str(self.event), "test_event", "Event name does not return expected format."
        )

    def test_event_timestamp(self):
        self.assertEqual(self.event.timestamp, 1000, "Event timestamp not set.")

    def test_event_equals_event(self):
        self.assertEqual(
            self.event, Event("test_event"), "Event does not equal similar Event."
        )


class TestKeyPressEvent(unittest.TestCase):
    def setUp(self):
        self.event_basic = KeyPressEvent("k", timestamp=1000)
        self.event_modifiers = KeyPressEvent(
            "m", modifiers=["shift", "ctrl"], timestamp=2000
        )

    def test_event_string(self):
        self.assertEqual(
            str(self.event_basic), "k", "Event name does not return expected format."
        )
        self.assertEqual(
            str(self.event_modifiers),
            "ctrl+shift+m",
            "Event name with modifiers does not return expected format.",
        )

    def test_event_equals_event(self):
        self.assertEqual(
            self.event_basic,
            KeyPressEvent("k", timestamp=3000),
            "KeyPressEvent does not equal similar KeyPressEvent.",
        )
        self.assertEqual(
            self.event_modifiers,
            KeyPressEvent("m", modifiers=["ctrl", "shift"], timestamp=4000),
            "KeyPressEvent with modifiers does not equal similar KeyPressEvent with modifiers.",
        )

    def test_event_modifiers(self):
        event = KeyPressEvent("p", modifiers=["ctrl", "alt"])
        self.assertEqual(
            event.modifiers,
            ["alt", "ctrl"],
            "KeyPressEvent modifiers are not set or not sorted.",
        )


class TestEventHandler(unittest.TestCase):
    event_handler = EventHandler()
    keypress_event = KeyPressEvent("o")
    flag_raised = False

    @staticmethod
    def raise_flag(*args, **kwargs):
        TestEventHandler.flag_raised = True

    def test_add_callbacks(self):
        self.event_handler.add_callbacks(self.keypress_event, self.raise_flag)
        self.assertEqual(
            self.event_handler._callbacks[self.keypress_event],
            [self.raise_flag],
            "Callback not added to list of callbacks for given event.",
        )

    def test_eventhandler(self):
        self.event_handler.handle_event(self.keypress_event)
        self.assertEqual(
            self.flag_raised, True, "Callback not executed for given event."
        )

    def test_remove_callbacks(self):
        self.event_handler.remove_callbacks(self.keypress_event, self.raise_flag)
        self.assertNotIn(
            self.raise_flag, self.event_handler._callbacks[self.keypress_event],
            "Callback not removed from list of callbacks for given event."
        )


if __name__ == "__main__":
    unittest.main()
