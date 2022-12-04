"""2nd Attempt"""
try:
    import functools
except ImportError:
    import _functools as functools

import random
import time


def applet(cls):
    """Initializes the applet"""
    if not hasattr(cls, '__tasks__'):
        cls.__tasks__ = {}
    for method_name in dir(cls):
        method = getattr(cls, method_name)
        if hasattr(method, '__tasks__'):
            cls.__tasks__.update({method_name: method.__tasks__})

    return cls


def gen_id(chars: int = 12) -> str:
    """Generate a random ID of a specified length.

    :param chars: Number of characters to use for the ID.
    :return:
    """
    ascii_lowercase = 'abcdefghijklmnopqrstuvwxyz'
    ascii_uppercase = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    digits = '0123456789'
    id_choice = ascii_lowercase + ascii_uppercase + digits
    return ''.join(random.choice(id_choice) for _ in range(chars))


def task(_func=None, task_id=None, interval=10, args=None, kwargs=None):
    """Generates a list of tasks associated with each function.

    :param _func:
    :param task_id: ID of the task.
    :param interval: How long to wait before running again (in seconds)
    :param args: Arguments passed to the function
    :param kwargs: Keyword arguments passed to the function
    :return:
    """
    if args is None:
        args = []
    if isinstance(args, str):
        args = [args]
    if kwargs is None:
        kwargs = dict()

    """Generate task IDs if not provided"""
    if not task_id:
        task_id = gen_id()

    def decorator(func):
        """Modifies the function and inserts the tasks."""
        if not hasattr(func, '__tasks__'):
            setattr(func, '__tasks__', {})
        getattr(func, '__tasks__').update({
            task_id: {
                'args': args,
                'interval': interval,
                'kwargs': kwargs,
            }
        })

        @functools.wraps(func)
        def wrapper(*w_args, **w_kwargs):
            """Return the function as-is."""
            return func(*w_args, **w_kwargs)

        return wrapper

    if _func is None:
        return decorator
    else:
        return decorator(_func)


class Applet(object):
    """Defines how an applet is to be run by the Scheduler."""
    __tasks__ = {}

    def __init__(self):
        pass

    @property
    def tasks(self):
        """Returns the list of tasks in the Applet."""
        return self.__tasks__

    @tasks.setter
    def tasks(self, *args, **kwargs):
        """Discourage the override of the __tasks__ variable."""
        raise AttributeError("Overriding tasks not allowed.")

    def remove_task(self, task_id):
        """Remove a task associated with the given ID."""
        for method in self.__tasks__:
            if hasattr(self.__tasks__, task_id):
                del self.__tasks__[method][task_id]
            method = getattr(self, method)
            if hasattr(method, task_id):
                del method.__tasks__[task_id]


""" =======
TEST APPLET
======= """


@applet
class MyApp(Applet):
    """Example Implementation"""

    # Most basic usage, runs every 30 seconds.
    @task
    def major_tom(self):
        print("Ground control to Major Tom!")

    # Define multiple tasks with different parameters.
    @task(task_id="ping", interval=15, args=["*beep*"])
    @task(task_id="hello", args=["Can you hear me Major Tom?", "Can you hear me Major Tom?"])
    def contact(self, *args):
        for arg in args:
            print(arg)
        if args[0] == "*beep*":
            print("*boop*")
        else:
            print("We read you ground control!")

    # Call the decorator like a normal function to create a task.
    def guitar_solo(self):
        print("[wailing guitar solo from space]")
    task(guitar_solo, task_id="signoff")


""" ==========
RUN THE APPLET
========== """


def run_all_tasks(app):
    all_tasks = app.tasks
    for method, tasks in all_tasks.items():
        call = getattr(app, method)
        for task_id, ctx in tasks.items():
            print(f"Executing: {task_id}")
            call(*ctx['args'], **ctx['kwargs'])
            time.sleep(ctx['interval'])


if __name__ == '__main__':
    myapp = MyApp()
    myapp.major_tom()
    myapp.contact("Come in Major Tom.", "*beep*")

    run_all_tasks(myapp)
