"""Applet"""
import asyncio
import random

try:
    from functools import partial
    from types import GeneratorType
except ImportError:
    from circuitpython_functools import partial
    from _types import GeneratorType

try:
    from circuitpython_typing import Union
except ImportError:
    pass


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


class Applet(object):
    """Defines how an applet is to be run by the Scheduler.

    Design Goals:
        - Act as a template and reduce the code footprint for actual Applets.
        - Handle interactions with the OS/Scheduler.
        - Make Applet development as easy as possible.

    Thoughts:
        The user should only be allowed to run one Applet at a time. Due to memory constraints, it will be important to
        be memory efficient. This can be achieved through a Singleton. Other methods for accomplishing the goal are
        being considered.

        Applets should have two types of asyncio tasks, foreground and background. Foreground tasks are run upon some
        sort of hardware input, pre-dominantly user key presses. Background tasks execute on an interval, on start, or
        on exit. Foreground tasks take priority. The user should be able to navigate the UI between background tasks.

        Decorators can be used to generate a list of tasks to pass to the scheduler, or it can simply be left up to the
        user to statically define these tasks in their subclass. The Applet parent class should have an API that
        supports both options.
    """
    __version__ = "0.0.0"
    __tasks__ = {}

    def __init__(self, name):
        self.__name__ = name

    def __repr__(self):
        return f"{self.__name__}(v{self.__version__})"

    def __str__(self):
        return self.__name__

    def task(self, task_id: str = None, **func_args):
        """Defines how tasks should be run by the Scheduler.

        Design Goals:
        - Act as a decorator for functions
        - Decorator can be applied multiple times
        - Instruct the scheduler when to run the task
        - Disable a background task after it's been registered with the Scheduler
        - Timeout for tasks that take too long

        Thoughts:
            In general, an Observer Pattern is utilized. Inspiration comes from Flask and other apps that make heavy use of
            decorators. It's ability to abstract the complexities away from the user allows novice developers to focus on
            developing their own applets and hardware drivers. Tasks are abstractions of Asyncio tasks.

            When decorating the functions, they should allow for multiple definitions of the same decorator, but with
            different parameters. It should also allow for a single function to act as both a foreground task and background
            task.

            After Tasks are passed to the Scheduler, there should be a mechanism to disabled or suspend the Task from running
            again. Allowing for this on the Scheduler side would prevent the task objects from needlessly being executed,
            wasting both memory and compute cycles.

            If a task takes too long to complete, there should be some way to interrupt or time it out. Essentially a
            watchdog timer, but at the Scheduler level rather than the system level. When the software is unresponsive, only
            reset the device if absolutely necessary.

        :param str task_id: Identification string for the task. Must be unique or any new tasks
        will be overwritten.
        :param func_args: Dict of arguments to pass to the function.
        :return callable: The decorator object that registers the task.
        """

        def decorator(func):
            """Registers the function as a task."""
            args = func_args.pop("args", tuple())
            kwargs = func_args.pop("kwargs", dict())
            self.add_task(func, task_id, *args, **kwargs)

            # Wrapper allows for multiple task decorators on a single function.
            def wrapper(*w_args, **w_kwargs):
                """ Do nothing; return as-is. """
                return func(*w_args, **w_kwargs)

            return wrapper
        return decorator

    def add_task(self, func: callable, task_id: str = None, *args, **kwargs):
        """Add a function with arguments as a task to be executed at a later time.

        :param func: Function object to execute as a task.
        :type func: callable
        :param str task_id: Identification string for the task. Must be unique or any new tasks
        with matching IDs will be overwritten.
        :param tuple args: List or Tuple of arguments to pass to the function.
        :param dict kwargs: Dict of keyword arguments to pass to the function.
        """
        # Generate task IDs if not provided
        if not task_id:
            task_id = gen_id()

        self.__tasks__.update({
            task_id: asyncio.create_task(func(*args, **kwargs))
        })

    def remove_task(self, task_id: str) -> None:
        """Remove a task associated with the given ID.

        :param str task_id: Identification string for the task.
        """
        del self.__tasks__[task_id]

    @property
    def all_tasks(self) -> GeneratorType:
        """Get all tasks associated with the Applet.

        :return: Iterable of tasks executed by the Applet.
        :rtype: GeneratorType
        """
        for task_id, task in self.__tasks__.items():
            yield task, task_id

    async def run(self):
        """ Executes the applet """
        print(f"Starting {self.__name__}")
        for task, task_id in self.all_tasks:
            print(f"Executing: {task_id}")
            task()

    async def stop(self):
        """ Stop the applet """
        raise NotImplementedError
