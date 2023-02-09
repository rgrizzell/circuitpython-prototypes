"""Applet"""
import asyncio
import random
from adafruit_ticks import *

# Compatibility for running under CPython.
try:
    from functools import partial
    from types import GeneratorType
except (ImportError, NameError):
    from circuitpython_functools import partial
    from _types import GeneratorType

try:
    from circuitpython_typing import Union
except (ImportError, NameError):
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

        Applets should have asyncio tasks. Tasks execute on an interval, and should be non-blocking(-ish). They should
        accept parameters and only execute after the Applet is run. They should have their own IDs so Applet developers
        can dynamically add and remove tasks.

        Decorators can be used to generate a list of tasks to pass to the scheduler, or it can simply be left up to the
        user to statically define these tasks in their subclass. The Applet parent class should have an API that
        supports both options.
    """
    __version__ = "0.0.0"
    __tasks__ = dict()

    def __init__(self, name: str):
        self.__name__ = name

    def __repr__(self) -> str:
        return f"{self.__name__}(v{self.__version__})"

    def __str__(self) -> str:
        return self.__name__

    def task(self, interval: int = 0, task_id: str = None, **func_args) -> callable:
        """Defines how tasks should be run by the Scheduler.

        Design Goals:
        - Act as a decorator for functions
        - Decorator can be applied multiple times
        - Instruct the scheduler when to run the task

        Thoughts:
            In general, an Observer Pattern is utilized. Inspiration comes from Flask and other apps that make heavy use
            of decorators. It's ability to abstract the complexities away from the user allows novice developers to
            focus on developing their own applets and hardware drivers. Tasks are abstractions of Asyncio tasks.

            When decorating the functions, they should allow for multiple definitions of the same decorator, but with
            different parameters. It should also allow for a single function to act as multiple tasks.

            After tasks are passed to the Scheduler, there should be a mechanism to disabled or suspend the task from
            running again. Allowing for this on the Scheduler side would prevent the task objects from needlessly being
            executed, wasting both memory and compute cycles.

        :param int interval: How often the scheduler should run the task, in milliseconds.
        :param str task_id: Identification string for the task. Must be unique or any new tasks
        will be overwritten.
        :param func_args: Dict of arguments to pass to the function.
        :return callable: The decorator object that registers the task.
        """

        def decorator(func: callable) -> callable:
            """Registers the function as a task."""
            args = func_args.pop("args", tuple())
            kwargs = func_args.pop("kwargs", dict())
            self.add_task(func, interval, task_id, *args, **kwargs)

            def wrapper(*w_args, **w_kwargs) -> callable:
                """Allows for multiple task decorators on a single function."""
                return func(*w_args, **w_kwargs)

            return wrapper
        return decorator

    def add_task(self, func: callable, interval: int = 0, task_id: str = None, *args, **kwargs) -> None:
        """Add a function with arguments as a task to be executed at a later time.

        :param func: Function object to execute as a task.
        :type func: callable
        :param int interval: How often the scheduler should run the task, in milliseconds.
        :param str task_id: Identification string for the task. Must be unique or any new tasks
        with matching IDs will be overwritten.
        :param tuple args: List or Tuple of arguments to pass to the function.
        :param dict kwargs: Dict of keyword arguments to pass to the function.
        """
        task_id = task_id or gen_id()
        self.__tasks__.update({
            task_id: self.AppTask(func, interval, task_id, *args, **kwargs)
        })

    def remove_task(self, task_id: str) -> None:
        """Remove a task associated with the given ID.

        :param str task_id: Identification string for the task.
        """
        del self.__tasks__[task_id]

    def get_task(self, task_id: str) -> 'AppTask':
        """Get all tasks associated with the Applet.

        :return: Iterable of tasks executed by the Applet.
        :rtype: GeneratorType
        """
        return self.__tasks__[task_id]

    def get_all_tasks(self) -> GeneratorType:
        """Get all tasks associated with the Applet.

        :return: Iterable of tasks executed by the Applet.
        :rtype: GeneratorType
        """
        yield from self.__tasks__.values()

    def get_scheduled_tasks(self) -> GeneratorType:
        """Get a list of tasks scheduled to be executed

        :param task:
        :return:
        """
        tasks = set()
        ticks = ticks_ms()
        for t in self.get_all_tasks():
            if ticks_less(t.next_run, ticks):
                if t.interval > 0:
                    # Generate a new coroutine object since they can only be used once.
                    tasks.add(t())
        yield from tasks

    async def run(self) -> None:
        """Executes the applet.

        Coroutine objects can not be re-used once awaited.
        New coroutine objects are created every loop.
        """
        print(f"Starting {self.__name__}")
        while True:
            await asyncio.gather(*self.get_scheduled_tasks())

    async def stop(self) -> None:
        """ Stop the applet """
        pass

    class AppTask(object):
        """ Abstraction of a task that get executed by the scheduler. Contains extra attributes that otherwise wouldn't
        be set on function or coroutine objects. Both are immutable and do not contain the `__dict__` attribute."""
        def __init__(self, func: callable, interval: int = 0, task_id: str = None, *args, **kwargs) -> None:
            """Add a function with arguments as a task to be executed at a later time.

            :param func: Function object to execute as a task.
            :type func: callable
            :param int interval: How often the scheduler should run the task, in milliseconds.
            :param str task_id: Identification string for the task. Must be unique or any new tasks
            with matching IDs will be overwritten.
            :param tuple args: List or Tuple of arguments to pass to the function.
            :param dict kwargs: Dict of keyword arguments to pass to the function.
            """
            # Generate task IDs if not provided
            self.task_id = task_id or gen_id()
            self.func = func
            self.args = args
            self.kwargs = kwargs
            self.interval = interval
            self.next_run = 0

        async def __call__(self, *args, **kwargs) -> None:
            print(f"Executing: {self.task_id}")
            self.next_run = ticks_add(ticks_ms(), self.interval)
            await self.func(*self.args, **self.kwargs)

        def __repr__(self) -> str:
            return f"{self.__class__.__name__}{self.__dict__}"
