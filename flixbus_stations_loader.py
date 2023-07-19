"""
Load all cities available in flixbus
"""
import nest_asyncio

from pipelines.flixbus.bus_stations_pipeline import (
    FlixbusBusStationsDataLoader,
    FlixbusBusStationsDataProcessor,
)
from scrapers.flixbus.bus_stations_scraper import (
    FlixbusBusStationsParser,
    FlixbusBusStationsScraper,
)

# patches asyncio to allow nested use of asyncio.run
# and loop.run_until_complete


nest_asyncio.apply()


async def load_flixbus_cities(region: str = "EU"):
    flixbus_stations_scraper = FlixbusBusStationsScraper(region=region)
    scraped_stations = flixbus_stations_scraper.get_data(method="POST")
    flixbus_stations_parser = FlixbusBusStationsParser(region=region, scraped_data=scraped_stations)
    parsed_flixbus_stations = flixbus_stations_parser.parse_data()
    flixbus_data_processor = FlixbusBusStationsDataProcessor(parsed_data=parsed_flixbus_stations)
    processed_stations = flixbus_data_processor.process_items()
    flixbus_stations_loader = FlixbusBusStationsDataLoader(
        processed_data=processed_stations, region=region
    )
    await flixbus_stations_loader.load_items()
