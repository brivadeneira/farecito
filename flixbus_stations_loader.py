"""
Load all cities available in flixbus
"""
import logging
import uuid

import nest_asyncio

from pipelines.flixbus.bus_stations_pipeline import (
    FlixbusBusStationsDataLoader,
    FlixbusBusStationsDataProcessor,
)
from scrapers.flixbus.bus_stations_scraper import (
    FlixbusBusStationsParser,
    FlixbusBusStationsScraper,
)
from settings import APP_NAME

nest_asyncio.apply()
# patches asyncio to allow nested use of asyncio.run
# and loop.run_until_complete

logger = logging.getLogger(APP_NAME)
logger.setLevel(logging.INFO)


async def load_flixbus_cities(region: str = "EU"):
    """
    Load Flixbus cities data for a given region.

    This function orchestrates the process of loading
    Flixbus cities data for the specified region.
    It involves scraping the data from the Flixbus website,
    parsing the scraped data, processing the parsed data,
    and finally, loading the processed data into a data loader.

    :param region: (str, optional) The region for which cities data should be loaded
    (default is "EU").
    """
    trace_uuid = str(uuid.uuid4())
    logger.info(f"[{trace_uuid}] Trying to update Flixbus bus stations graph.")

    flixbus_stations_scraper = FlixbusBusStationsScraper(region=region)
    scraped_stations = flixbus_stations_scraper.get_data(method="POST")

    if scraped_stations:
        logger.info(f"[{trace_uuid}] Successfully scraped {len(scraped_stations)}.")
        flixbus_stations_parser = FlixbusBusStationsParser(
            region=region, scraped_data=scraped_stations
        )
        parsed_flixbus_stations = flixbus_stations_parser.parse_data()
        flixbus_data_processor = FlixbusBusStationsDataProcessor(
            parsed_data=parsed_flixbus_stations
        )
        processed_stations = flixbus_data_processor.process_items()
        flixbus_stations_loader = FlixbusBusStationsDataLoader(
            processed_data=processed_stations, region=region
        )
        await flixbus_stations_loader.load_items()
    else:
        logger.error(f"[{trace_uuid}] No bus station scraped.")
