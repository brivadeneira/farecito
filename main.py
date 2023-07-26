"""
Look for cheap trips process
"""
import asyncio

import nest_asyncio

from flixbus_trips_alerts import get_flixbus_trips

# patches asyncio to allow nested use of asyncio.run
# and loop.run_until_complete


nest_asyncio.apply()

if __name__ == "__main__":
    # load_flixbus_cities(region=region)
    asyncio.run(get_flixbus_trips())
