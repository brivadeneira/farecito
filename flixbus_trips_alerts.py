"""
Alert for cheap trips
"""
from pipelines.flixbus.bus_trips_pipeline import FlixbusCitiesDataGetter
from scrapers.flixbus.trips_scraper import FlixbusTripsParser, FlixbusTripsScraper


async def get_flixbus_trips(region: str = "EU"):
    cities_getter = FlixbusCitiesDataGetter(region=region)
    popular_cities = await cities_getter.get_stored_data()

    for city in popular_cities:
        for departure_city, arrival_cities in city.items():
            flixbus_trips_scraper = FlixbusTripsScraper(
                departure_city_uuid=departure_city, arrival_city_uuids=arrival_cities
            )
            scraped_trips = flixbus_trips_scraper.get_data()
            flixbus_trips_parser = FlixbusTripsParser(region=region, scraped_data=scraped_trips)
            flixbus_trips_parser.parse_data()
