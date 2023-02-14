# Decorators
Flask-like implementation of decorators on CircuitPython. Multiple decorators are registered in a bottom-up order. In
essense, the decorator closest to the function is registered first. In CircuitPython function objects are immutable and
can not have new attributes assigned to it. A `functool.partial()` is used instead.
## Requirements
- [CircuitPython Functools](https://github.com/tekktrik/CircuitPython_Functools)

## Running
1. Download the above requirements
2. Copy the requirements to `CIRCUITPY/lib`.
3. Copy the project files to `CIRCUITPY/`.
4. Reload/restart the device.

*Tested on Raspberry Pi Pico.*
