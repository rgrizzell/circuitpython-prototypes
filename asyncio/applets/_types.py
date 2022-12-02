"""Type classes"""
import asyncio


# Look, I spent hours trying to figure out how to find the complex types
# The types module doesn't exist, so I made my own.
def _f(): pass
FunctionType = type(_f)  # noqa


async def _c():
    await asyncio.sleep(0)
CoroutineType = type(_c())
