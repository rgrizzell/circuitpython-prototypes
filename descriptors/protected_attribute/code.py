"""Demonstration of using a descriptor to create constant-like values."""


class Protected:
    """ Once the value is set, it can't be modified. Anti-Pythonic, but defensive. """
    def __init__(self):
        self.value = None

    def __get__(self, instance, owner):
        if instance is None:
            return self
        return self.value

    def __set__(self, instance, value):
        if self.value is None:
            self.value = value
        else:
            raise ValueError("Attribute is protected and can't be modified")

    def __delete__(self, instance):
        raise ValueError(f"Attribute is protected and can't be deleted")


class NoApp:
    """A type of no-chamber"""
    config = Protected()

    def __init__(self):
        self.config = {"foo": "bar"}

    def __call__(self, *args, **kwargs):
        print(f"NoApp says 'foo' is '{self.config['foo']}'")


if __name__ == "__main__":
    app = NoApp()
    app()

    # The attribute can't be modified. It is protected.
    try:
        app.config = "foobar"
    except ValueError as e:
        print(e)

    # WARNING: Underlying data structures and classes can still be modified.
    try:
        app.config['foo'] = ["bar", "bat"]
        print(f"Underlying classes/structures can be modified, though: {app.config}")
    except ValueError as e:
        print(e)
