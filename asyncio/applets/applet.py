"""Applet"""
from __future__ import annotations


try:
    import types
    from typing import Callable, Coroutine, Iterator
except ImportError:
    import _types as types


import asyncio


_c = types.CoroutineType
_f = types.FunctionType


class Applet:
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

    # noinspection PyPep8Naming
    class Job(object):
        """Defines how Jobs should be run by the Scheduler.

        Design Goals:
        - Act as a decorator for functions
        - Decorator can be applied multiple times
        - Instruct the scheduler when to run the task
        - Disable a background task after it's been registered with the Scheduler
        - Timeout for tasks that take too long

        Thoughts:
            In general, an Observer Pattern is utilized. Inspiration comes from Flask and other apps that make heavy use of
            decorators. It's ability to abstract the complexities away from the user allows novice developers to focus on
            developing their own applets and hardware drivers. Jobs are abstractions of Asyncio tasks.

            When decorating the functions, they should allow for multiple definitions of the same decorator, but with
            different parameters. It should also allow for a single function to act as both a foreground task and background
            task.

            After Jobs are passed to the Scheduler, there should be a mechanism to disabled or suspend the Job from running
            again. Allowing for this on the Scheduler side would prevent the task objects from needlessly being executed,
            wasting both memory and compute cycles.

            If a task takes too long to complete, there should be some way to interrupt or time it out. Essentially a
            watchdog timer, but at the Scheduler level rather than the system level. When the software is unresponsive, only
            reset the device if absolutely necessary.
        """

        def __init__(self, coro: Callable, interval=10):
            self.coro = coro
            self.interval = interval

        def __call__(self, coro: Callable, *args: any, **kwargs: any):
            if not hasattr(coro, "send"):
                raise TypeError("Coroutine expected")
            self.coro = coro

            def _add_task(*args: any, **kwargs: any):
                return coro(*args, **kwargs)

            _add_task.__name__ = coro.__name__
            _add_task.__doc__ = coro.__doc__
            return _add_task

        def coro(self):
            """Returns the coroutine object

            :return:
            """
            return self.coro

    __instance = None
    __version__ = "0.0.0"

    def __init__(self, *args: any, **kwargs: any) -> None:
        pass

    def __new__(cls, *args: any, **kwargs: any):
        """Creates a Singleton"""
        if not isinstance(cls.__instance, cls):
            cls.__instance = super(Applet, cls).__new__(cls)
        return cls.__instance

    def all_jobs(self) -> dict[str, Coroutine]:
        """
        :return:
        """
        for name in dir(self):
            job = getattr(self, name)
            if isinstance(job, Applet.Job):
                if isinstance(job.coro, _f):
                    continue
                if hasattr(job.coro(self), "send"):
                    yield job

    def add_config(self):
        """Adds applet's configuration"""
        return

    async def run_applet(self) -> None:
        """Run the applet"""
        pass

    async def stop_applet(self) -> None:
        """Stop the applet"""
        pass
