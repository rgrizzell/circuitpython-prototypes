""" a """
import board
import time
from keypad import KeyMatrix
from input_parser import InputParser, KeypadInputParser
from keymap import LayeredKeyMap
from collections import OrderedDict
try:
    from typing import Any
except ImportError:
    pass


class UserInput:
    """ a """
    def __init__(self, input_parser):
        self.input_parser = input_parser

    @property
    def input_parser(self) -> 'InputParser':
        """The `InputParser` object used to convert incoming signals into characters.

        :return: InputParser
        """
        return self._input_parser

    @input_parser.setter
    def input_parser(self, new_parser: 'InputParser') -> None:
        """

        :param new_parser: The
        :type new_parser: InputParser
        """
        if issubclass(type(new_parser), InputParser):
            self._input_parser = new_parser
            self._input_parser.initialize()
        else:
            raise TypeError(f"{type(new_parser)} is not a subclass of InputParser.")

    def get(self) -> Any:
        """

        :return:
        """
        return self._input_parser.get_events()


if __name__ == "__main__":
    keys_cols = [board.GP1, board.GP2, board.GP3, board.GP4, board.GP5]
    keys_rows = [board.GP6, board.GP9, board.GP15, board.GP8, board.GP7, board.GP22]
    key_layers = LayeredKeyMap(
        key_mapping=OrderedDict([
            ("abc", [
                "ent", " ", "m", "n", "b", "del", "l", "k", "j", "h",
                "p", "o", "i", "u", "y", b"\x0e", "z", "x", "c", "v",
                "a", "s", "d", "f", "g", "q", "w", "e", "r", "t",
            ]),
            ("ABC", [
                "dn", ";", "M", "N", "B", "up", "L", "K", "J", "H",
                "P", "O", "I", "U", "Y", b"\x0e", "Z", "X", "C", "V",
                "A", "S", "D", "F", "G", "Q", "W", "E", "R", "T",
            ]),
            ("123", [
                "rt", ",", ">", "<", "'", "lt", "-", "*", "&", "+",
                "0", "9", "8", "7", "6", b"\x0e", "[", "]", "?", "/",
                "!", "@", "#", "$", "%", "1", "2", "3", "4", "5",
            ])
        ]),
        default_layer="abc"
    )
    keypad = KeyMatrix(keys_rows, keys_cols)
    parser = KeypadInputParser(keypad, key_layers)
    user_input = UserInput(parser)

    while True:
        for event in user_input.get():
            print(f"Input: {event}")
        time.sleep(0.01)
