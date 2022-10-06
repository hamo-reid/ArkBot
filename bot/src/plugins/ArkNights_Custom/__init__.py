import asyncio
from .initlalize import costom_init


loop = asyncio.get_event_loop()
loop.run_until_complete(costom_init())