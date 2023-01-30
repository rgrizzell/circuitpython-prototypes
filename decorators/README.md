# Decorators
Flask-like implementation of decorators on CircuitPython.

## Requires
* [CircuitPython_Functools](https://github.com/tekktrik/CircuitPython_Functools) (CircuitPython Community Bundle)

## Notes
* Multiple decorators are registered in a bottom-up order. In essense, the decorator closest to the function is 
registered first.
* Function objects are immutable and can not have new attributes assigned to it. A `functool.partial()` is used instead.
This could be extended to Asyncio Coroutines instead.