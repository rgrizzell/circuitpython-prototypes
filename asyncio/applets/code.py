""" Async Scheduler """
import asyncio


async def scheduler():
    """ Loads and executes the applet. """
    import myapp
    app = myapp.app

    try:
        await app.run()
    finally:
        await app.stop()


if __name__ == "__main__":
    asyncio.run(scheduler(), debug=True)
