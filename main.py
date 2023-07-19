"""
Look for cheap trips process
"""
import asyncio

import nest_asyncio

from flixbus_trips_alerts import get_flixbus_trips

# patches asyncio to allow nested use of asyncio.run
# and loop.run_until_complete


nest_asyncio.apply()

# for region in ["US", "EU", "BRA"]:
# TODO: this must be a cron
# asyncio.run(load_flixbus_cities(region=region))

while True:
    asyncio.run(get_flixbus_trips(region="EU"))
