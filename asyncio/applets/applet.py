"""Applet"""
import asyncio


class Singleton(type):
    """Creates a Singleton of the class and allows global access."""
    __instance = None

    def __call__(cls, *args, **kwargs):
        if not isinstance(cls.__instance, cls):
            cls.__instance = super(Singleton, cls).__call__(*args, **kwargs)
        return cls.__instance


class Applet(metaclass=Singleton):
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
    class job(object):
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

        def __init__(self, interval=10):
            self._interval = interval

        def __call__(self, coro, *args, **kwargs):
            def add_task(*args, **kwargs):
                return coro(*args, **kwargs)

            return add_task

        @classmethod
        def all_jobs(cls, subject):
            def find_coroutines():
                for name in dir(subject):
                    coro = getattr(subject, name)
                    if isinstance(coro, Applet.job):
                        yield name, coro

            return {name: coro for name, coro in find_coroutines()}

    __version__ = "0.0.0"

    def __init__(self) -> None:
        pass

    def add_config(self):
        return

    async def run_applet(self) -> None:
        pass

    async def stop_applet(self) -> None:
        pass
