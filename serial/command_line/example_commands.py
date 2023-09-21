""" Example of using the Commands class """
import time
from commands import Commands


class MyApplication(Commands):
    def a_ok(self):
        print("Action: Green LED")

    def a_warn(self):
        print("Action: Yellow LED")

    def a_crit(self):
        print("Action: Red LED")

    def br_set(self, *args):
        print(f"Action: Set brightness: {args[0]}%")

    def br_up(self, *args):
        print(f"Action: Increase brightness: +{args[0]}%")

    def br_down(self, *args):
        print(f"Action: Decrease brightness: -{args[0]}%")


if __name__ == "__main__":
    app = MyApplication()
    while True:
        app._listen()
        time.sleep(0.1)
