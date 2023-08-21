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
        if new_layer in self.key_mapping.keys():
            self._layer = new_layer

    def lookup(self, index, layer=None):
        """ a """
        layer = layer or self.layer
        return self.key_mapping[layer][index]
