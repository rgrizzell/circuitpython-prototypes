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

## Write your Own

Import and name your Applet.
```python
from applet import Applet
app = Applet("MyApp")
```
Run a task once at start-up.
```python
@app.task()
async def major_tom():
    print("Ground control to Major Tom!")
```
Add multiple tasks based on one function. Set task IDs, interval, and keyword arguments.
```python
@app.task(task_id="ping", interval=2000, args=("*beep*",))
@app.task(task_id="hello", interval=5000, args=("Can you hear me Major Tom?", "Can you hear me Major Tom?"))
@app.task(task_id="listen", kwargs={"frequency": 9001})
async def contact(*args, **kwargs):
    for arg in args:
        print(arg)
    for key, val in kwargs.items():
        print(key, val)
    if len(args) > 0:
        if args[0] == "*beep*":
            print("*boop*")
        else:
            print("We read you ground control!")
```
Register the task later in the execution.
```python
async def guitar_solo():
    """ Where did you get that? """
    print("[wailing guitar solo from space]")

app.add_task(guitar_solo, interval=10000)
```

## User Stories

As a core developer, I want to create a list (or generator) of Asyncio tasks
using decorators that accept parameters so that I can ensure that applets
can perform background tasks.

As an applet developer, I want to schedule tasks to run on interval, on boot,
or hardware state changes so that I can keep my code simple.

As a user, I want the interface to be responsive when I send inputs so that I
don't have to wait for background tasks to complete.
