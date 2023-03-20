import time


class UserInput(object):
    def __init__(self, *validators):
        self._name = None
        self.validators = validators

    def __set_name__(self, owner, name):
        self._name = name

    def __get__(self, instance, owner):
        if instance is None:
            return self
        return instance.__dict__[self._name]

    def __set__(self, instance, value):
        self.validate(value)
        instance.__dict__[self._name] = value

    def validate(self, value):
        for validator in self.validators:
            validator(value)


class Validator:
    def __init__(self, func, exc):
        self.func = func
        self.exc = exc

    def __call__(self, value):
        if not self.func(value):
            raise ValueError(f"{value!r} {self.exc}")


class Widget:
    def __init__(self):
        self.value = UserInput(
            Validator(
                islower,
                "String must be lowercase"
            )
        )


def islower(x):
    return str(x) == str(x).lower()


if __name__ == "__main__":
    e1 = Widget()

    e1.value = "bar"
    print(e1.value)
    time.sleep(0.5)
    e1.value = "Foo"
    print(e1.value)