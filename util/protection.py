import asyncio

protection_task = None

async def defence(stop_event):
    while not stop_event.is_set():
        print("Test")
        await asyncio.sleep(5)

async def startProtection():
    global protection_task
    if protection_task is None or protection_task.done():
        stop_event = asyncio.Event()
        protection_task = asyncio.create_task(defence(stop_event))
        return stop_event, protection_task
    else:
        print("Protection is already running.")
        return None, protection_task

async def stopProtection():
    global protection_task
    if protection_task is not None:
        stop_event, task = protection_task.get_coro().cr_frame.f_locals['stop_event'], protection_task
        stop_event.set()
        await task
        protection_task = None
