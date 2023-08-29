""" Tests code.py """
import unittest
from protected import ProtectedAttribute


class MockClass(object):
    protected = ProtectedAttribute(name="protected")
    protected_default = ProtectedAttribute(name="protected_default", default=False)


class TestProtected(unittest.TestCase):
    def test_protected(self):
        mock = MockClass()
        self.assertIsNone(mock.protected)

        mock.protected = True
        self.assertTrue(mock.protected)
        with self.assertRaises(ValueError):
            mock.protected = False

        self.assertFalse(hasattr(mock.__dict__, "protected"))

    def test_protected_default(self):
        mock = MockClass()
        self.assertFalse(mock.protected_default)

        mock.protected_default = True
        self.assertTrue(mock.protected_default)
        with self.assertRaises(ValueError):
            mock.protected_default = False

        self.assertFalse(hasattr(mock.__dict__, "protected_default"))


if __name__ == "__main__":
    unittest.main()
