#!/usr/bin/env python3
"""Crappy Unit Testing"""
import asyncio
from applet import Applet, Job


class ExampleApp(Applet):
    __version__ = "0.0.1-dev"

    def __init__(self):
        super().__init__()
        self.welcome_msg = "'ello world!"
        self.question = "Wonderful weather, innit?"

    @Job
    async def first_task(self):
        print(self.question)

    # TODO: Job should take any number of optional parameters.
    @Job
    async def second_task(self):
        self.welcome_msg = "Oy, mate!"
        print(self.welcome_msg)


class FauxApp(Applet):
    __version__ = "9.9.9"

    def __init__(self):
        super().__init__()

    # TODO: Make sure jobs only apply to `async def`.
    @Job
    def not_a_task(self):
        print("No!")


async def main():
    myapp = ExampleApp()
    print(myapp.__version__)
    print(Job.all_jobs(myapp))

    fauxapp = FauxApp()
    print(fauxapp.__version__)
    print(Job.all_jobs(fauxapp))

if __name__ == "__main__":
    asyncio.run(main())
