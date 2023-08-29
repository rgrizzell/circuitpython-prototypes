"""Protected Attribute descriptor for Python classes"""


class ProtectedAttribute:
    """ Once the value is set, it can't be modified. Anti-Pythonic, but defensive. """
    # WARNING: PEP-487 is not implemented in the MicroPython core. A name must be provided via `__init__`.
    # def __set_name__(self, owner, name):
    #     self._name = name

    def __init__(self, name, default=None):
        self._name = f"_{name}"
        self._default = default

    def __get__(self, instance, owner):
        if instance is None:
            return self
        return getattr(instance, self._name, self._default)

    def __set__(self, instance, value):
        if hasattr(instance, self._name):
            raise ValueError("Attribute is protected and can't be modified")
        setattr(instance, self._name, value)

    def __delete__(self, instance):
        raise ValueError(f"Attribute is protected and can't be deleted")
