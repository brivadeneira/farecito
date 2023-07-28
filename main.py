"""
Look for cheap trips process
"""
import asyncio
import logging

import nest_asyncio

from flixbus_trips_alerts import get_flixbus_trips

nest_asyncio.apply()
# patches asyncio to allow nested use of asyncio.run
# and loop.run_until_complete

logging.basicConfig(
    format="%(asctime)s,%(msecs)03d %(levelname)-8s [%(pathname)s:%(lineno)d] %(message)s",
    datefmt="%Y-%m-%d:%H:%M:%S",
    level=logging.DEBUG,
)

if __name__ == "__main__":
    # region = "EU"  # TODO [improvement] read region from env
    # asyncio.run(load_flixbus_cities(region=region))  # TODO [bug] FIX THIS!
    asyncio.run(get_flixbus_trips())
