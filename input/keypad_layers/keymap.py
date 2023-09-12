""" a """


class KeyMap:
    """ a """
    key_mapping = ()

    def __init__(self, key_mapping=None):
        self.key_mapping = key_mapping or self.key_mapping

    def lookup(self, index: int):
        """ a """
        return self.key_mapping[index]


class LayeredKeyMap(KeyMap):
    """ a """
    key_mapping = {}

    def __init__(self, key_mapping=None, default_layer=None, shift=None):
        super().__init__(key_mapping=key_mapping)
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

    def lookup(self, index, layer=None):
        """ a """
        layer = layer or self.layer
        return self.key_mapping[layer][index]
