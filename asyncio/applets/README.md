# Asyncio - Applets
Async Applet Framework for CircuitPython

Influenced heavily by Flask, Applets are loosely decoupled modules
that are executed by the Scheduler. Tasks act as the abstract representation
of Asyncio Coroutines with Scheduler-specific information, such as run interval,
task ID, and arguments.

https://flask.palletsprojects.com/en/2.2.x/design/

## Requirements
- [Adafruit CircuitPython Ticks](https://github.com/adafruit/Adafruit_CircuitPython_Ticks)
- [Adafruit CircuitPython asyncio](https://github.com/adafruit/Adafruit_CircuitPython_asyncio)
- [CircuitPython Functools](https://github.com/tekktrik/CircuitPython_Functools)

## Running
1. Download the above requirements
2. Copy the requirements to `CIRCUITPY/lib`.
3. Copy the project files to `CIRCUITPY/`.
4. Reload/restart the device.

*Tested on Raspberry Pi Pico.*

## User Stories

As a core developer, I want to create a list (or generator) of Asyncio tasks
using decorators that accept parameters so that I can ensure that applets
can perform background tasks.

As an applet developer, I want to schedule tasks to run on interval, on boot,
or hardware state changes so that I can keep my code simple.

As a user, I want the interface to be responsive when I send inputs so that I
don't have to wait for background tasks to complete.
