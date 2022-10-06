from .initialize import total_init
import asyncio

PLUGIN_NAME = "ArkNights_Core"

loop = asyncio.get_event_loop()
loop.run_until_complete(total_init())