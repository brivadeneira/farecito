"""
Alert for cheap trips
"""
import asyncio
import concurrent
import logging
import random

from pipelines.flixbus.bus_trips_pipeline import FlixbusCitiesDataGetter, FlixbusTripsTracker
from pipelines.trip_alerts import TripsAlertBot
from scrapers.flixbus.trips_scraper import FlixbusTripsScraper
from settings import APP_NAME

logger = logging.getLogger(APP_NAME)
logger.setLevel(logging.DEBUG)


async def get_flixbus_routes(region: str = "EU"):
    cities_getter = FlixbusCitiesDataGetter(region=region)
    popular_routes = await cities_getter.get_stored_data()

    scraped_routes = []

    for popular_route in popular_routes:
        for departure_city, arrival_cities in popular_route.items():
            for arrival_city in arrival_cities:
                routes = FlixbusTripsScraper(
                    departure_city_uuid=departure_city,
                    arrival_city_uuid=arrival_city,
                    default_days_range=90,
                )
                scraped_routes.append(routes)
    logger.info("added %s routes", {len(scraped_routes)})
    random.shuffle(scraped_routes)
    return scraped_routes


async def scrape_and_send_alerts(scraper):
    trips_tracker = FlixbusTripsTracker()
    cheap_trips = await trips_tracker.track_data_of_interest(scraper.get_data())
    if cheap_trips:
        logging.info("%s cheap trips found!", {len(cheap_trips)})
        for trip in cheap_trips:
            logger.info("sending alert for %s", trip)
            trips_alert_bot = TripsAlertBot(trip)
            await trips_alert_bot.send_alert_message()
    else:
        logger.info("no cheap trips")


async def get_flixbus_trips(region: str = "EU"):
    scraped_routes = await get_flixbus_routes(region)

    loop = asyncio.get_event_loop()
    tasks = [scrape_and_send_alerts(route) for route in scraped_routes]
    loop.run_until_complete(asyncio.gather(*tasks))


# Run the main function
if __name__ == "__main__":
    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
        executor.submit(asyncio.run, get_flixbus_trips())
