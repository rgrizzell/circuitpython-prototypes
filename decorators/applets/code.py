""" My Example Applet """
from applet import Applet

app = Applet("MyApp")


@app.task()
def major_tom():
    """ The one and only """
    print("Ground control to Major Tom!")


# Define multiple tasks with different parameters.
@app.task(task_id="ping", args=("*beep*",))
@app.task(task_id="hello", args=("Can you hear me Major Tom?", "Can you hear me Major Tom?"))
@app.task(task_id="listen", kwargs={"frequency": 9001})
def contact(*args, **kwargs):
    """ Contact the crew """
    for arg in args:
        print(arg)
    for key, val in kwargs.items():
        print(key, val)
    if len(args) > 0:
        if args[0] == "*beep*":
            print("*boop*")
        else:
            print("We read you ground control!")


# Call the decorator like a normal function to create a task.
def guitar_solo() -> None:
    """ Where did you get that? """
    print("[wailing guitar solo from space]")


app.add_task(guitar_solo, task_id="signoff")


if __name__ == "__main__":
    app.run()
