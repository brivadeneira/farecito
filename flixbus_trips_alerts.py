"""
Scrap, proccess and alert for flixbus cheap trips
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
    """
    Get Flixbus routes data for a given region.

    This function retrieves popular routes data for the specified region,
    then creates a list of FlixbusTripsScraper
    instances for each departure and arrival city pair in the popular routes.
    The list of scraped routes is then     randomized before returning.

    :param region: (str, optional) The region for which routes data should be retrieved
    (default is "EU").
    :return: A list of FlixbusTripsScraper instances representing the scraped routes.
    """
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
    logger.info(f"Added {len(scraped_routes)} routes to scrap.")
    random.shuffle(scraped_routes)
    return scraped_routes


async def scrape_and_send_alerts(scraper):
    trips_tracker = FlixbusTripsTracker()
    cheap_trips = await trips_tracker.track_data_of_interest(scraper.get_data())
    if cheap_trips:
        for trip in cheap_trips:
            trips_alert_bot = TripsAlertBot(trip)
            await trips_alert_bot.send_alert_message()


async def get_flixbus_trips(region: str = "EU"):
    """
    Scrape Flixbus data, track cheap trips, and send alerts.

    This function takes a FlixbusTripsScraper instance as input,
    scrapes Flixbus data using the given scraper,
    tracks and identifies cheap trips using FlixbusTripsTracker,
    and sends alerts for the found cheap trips
    using TripsAlertBot.

    :param scraper: A FlixbusTripsScraper instance used for data scraping.
    """
    scraped_routes = await get_flixbus_routes(region)

    loop = asyncio.get_event_loop()
    tasks = [scrape_and_send_alerts(route) for route in scraped_routes]
    loop.run_until_complete(asyncio.gather(*tasks))


if __name__ == "__main__":
    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
        executor.submit(asyncio.run, get_flixbus_trips())
