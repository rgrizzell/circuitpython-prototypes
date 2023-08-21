"""3rd Attempt"""
try:
    from circuitpython_typing import Union
except ImportError:
    pass

try:
    from functools import partial
    from types import GeneratorType
except (ImportError, NameError):
    from decorators.applets.lib.circuitpython_functools import partial
    from _types import GeneratorType

import random


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
    """Defines how an applet is to be run by the Scheduler."""
    _tasks = {}

    def __init__(self, name):
        self._name = name

    @property
    def name(self):
        """The Applet's name.

        :return str: String object representing the Applet name.
        """
        return self._name

    def task(self, task_id: str = None, **func_args):
        """Registers the function as a task to be executed later.

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

        self._tasks.update({
            task_id: partial(func, *args, **kwargs)
        })

    def remove_task(self, task_id: str) -> None:
        """Remove a task associated with the given ID.

        :param str task_id: Identification string for the task.
        """
        del self._tasks[task_id]

    @property
    def all_tasks(self) -> GeneratorType:
        """Get all tasks associated with the Applet.

        :return: Iterable of tasks executed by the Applet.
        :rtype: GeneratorType
        """
        for task_id, task in self._tasks.items():
            yield task, task_id

    def run(self):
        """ Executes the applet """
        print(f"Starting {self._name}")
        for task, task_id in self.all_tasks:
            print(f"Executing: {task_id}")
            task()
