# Asyncio - Applets
Async Applet Framework for CircuitPython

Built around the Observer Pattern, Applets are loosely decoupled modules
that are executed by the Scheduler. Jobs act as the abstract representation
of Asyncio Coroutines with Scheduler-specific information, such as run interval,
run-on-boot, and hardware state changes.

## User Stories

As a core developer, I want to create a list (or generator) of Asyncio tasks
using decorators that accept parameters so that I can ensure that applets
can perform background tasks.

As an applet developer, I want to schedule tasks to run on interval, on boot,
or hardware state changes so that I can keep my code simple.

As a user, I want the interface to be responsive when I send inputs so that I
don't have to wait for background tasks to complete.

## TODO:
- Return list of Applet Jobs
- Job decorator accepts parameters
  - Triggers
    - On interval
    - On start
    - On exit
    - Hardware state
  - Timeout

