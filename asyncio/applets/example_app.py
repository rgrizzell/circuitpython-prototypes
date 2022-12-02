#!/usr/bin/env python3
"""Crappy Unit Testing"""
try:
    import asyncio
except ImportError:
    import _asyncio

from applet import Applet


class ExampleApp(Applet):
    __version__ = "0.0.1-dev"

    def __init__(self):
        super().__init__()
        self.welcome_msg = "'ello world!"
        self.question = "Wonderful weather, innit?"

    @Applet.Job
    async def first_task(self):
        print(self.question)
        await asyncio.sleep(2)

    # TODO: Job should take any number of optional parameters.
    @Applet.Job
    async def second_task(self, *args):
        self.welcome_msg = "Oy, mate!"
        print(self.welcome_msg)
        print(args)
        await asyncio.sleep(0.1)


class FauxApp(Applet):
    __version__ = "9.9.9"

    def __init__(self):
        super().__init__()

    @Applet.Job
    def not_a_task(self):
        print("If you can read this, its broken!")


def list_jobs(applet: Applet):
    """

    :param applet:
    """
    for job in applet.all_jobs():
        if isinstance(job, Applet.Job):
            print(job.__dict__)


async def main():
    """ Main Entry Point """
    myapp = ExampleApp()
    print(f"MyApp Version: {myapp.__version__}")
    list_jobs(myapp)

    fauxapp = FauxApp()
    print(f"FauxApp Version: {fauxapp.__version__}")
    list_jobs(fauxapp)

if __name__ == "__main__":
    asyncio.run(main())
