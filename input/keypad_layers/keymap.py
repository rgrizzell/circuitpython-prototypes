""" a """
from collections import OrderedDict


class KeyMap:
    """ a """

    def __init__(self, key_mapping):
        self.key_mapping = key_mapping

    def __getitem__(self, index: int):
        """ a """
        return self.key_mapping[index]


class LayeredKeyMap:
    """ a """

    def __init__(self, *key_mappings, default_layer=None, shift=None):
        super().__init__()
        self.key_mapping = OrderedDict()
        for keymap in key_mappings:
            self.key_mapping[keymap[0]] = KeyMap(keymap[1])

        self.layer = default_layer
        self.shift = shift

    @property
    def layer(self):
        """ a """
        return self._layer

    @layer.setter
    def layer(self, new_layer):
        """ a """
        layers = list(self.key_mapping)
        if new_layer in layers:
            self._layer = new_layer
        else:
            raise ValueError(f"Layer '{new_layer}' not in key mapping: {layers}")

    def next_layer(self):
        """ a """
        layers = list(self.key_mapping)
        index = layers.index(self._layer)
        new_index = (index + 1) % len(layers)
        self.layer = layers[new_index]

    def __getitem__(self, index):
        """ a """
        return self.key_mapping[self.layer][index]
