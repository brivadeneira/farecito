"""
Implements pipeline classes for flixbus.
"""
import logging
import sys
import uuid
from typing import Any

from pydantic.dataclasses import dataclass

from neo4j_graph import Neo4JConn, get_popular_cities_cypher_query
from pipelines import BaseDataGetter, BaseDataTracker
from pipelines.settings import NEO4J_PASSWORD, NEO4J_URI, NEO4J_USERNAME
from settings import APP_NAME

logger = logging.getLogger(APP_NAME)
logger.setLevel(logging.INFO)


@dataclass
class FlixbusCitiesDataGetter(BaseDataGetter):
    """
    Base class for store items after being clean and validated from scrapers
    """

    conn: Any = None
    region: str = "EU"

    def __post_init__(self):
        if not self.conn:
            self.conn = Neo4JConn(
                uri=NEO4J_URI,
                user_name=NEO4J_USERNAME,
                password=NEO4J_PASSWORD,
            )

    async def get_stored_data(self) -> list[dict[str, Any]]:
        """
        Get the set of popular cities
        :return: (list[dict])
        """
        conn = self.conn
        region = self.region

        trace_uuid = str(uuid.uuid4())
        logger.info(f"[{trace_uuid}] Trying to get popular cities.")

        db_cities_result = await conn.execute_query(get_popular_cities_cypher_query(region=region))

        if not db_cities_result:
            logger.error(f"[{trace_uuid}] No cities result, existing.")
            sys.exit(1)

        logger.info(f"[{trace_uuid}] Successfully got {len(db_cities_result)} popular cities.")
        return [{city["from_city_uuid"]: city["to_city_uuids"]} for city in db_cities_result]


@dataclass
class FlixbusTripsTracker(BaseDataTracker):
    """
    Base class for tracking the cheap trips from scraped data
    (tickets with at least 50% off)
    """

    discount_threshold: int = 0.5  # at least 50% off

    async def track_data_of_interest(self, processed_data: dict[str, Any]):
        """
        Gets the result of get_data() method, parses it to be proceeded and stored
        """
        discount_threshold = self.discount_threshold

        trace_uuid = str(uuid.uuid4())
        logger.info(f"[{trace_uuid}] Looking for cheap tickets.")
        for response in processed_data:
            cheap_trips = [
                {
                    "from_city_name": response["cities"][trip["departure_city_id"]]["name"],
                    "to_city_name": response["cities"][trip["arrival_city_id"]]["name"],
                    "departure_city_uuid": trip["departure_city_id"],
                    "arrival_city_uuid": trip["arrival_city_id"],
                    "departure_date": trip["date"],
                    "uid": result_key,
                    "status": result_value["status"],
                    "provider": result_value["provider"],
                    "duration_hours": result_value["duration"]["hours"],
                    "duration_minutes": result_value["duration"]["minutes"],
                    "price_total": result_value["price"]["total"],
                    "seats_available": result_value["available"]["seats"],
                }
                for trip in response["trips"]
                for result_key, result_value in trip["results"].items()
                if result_value["price"]["total"]
                < discount_threshold * result_value["price"]["original"]
                and result_value["available"]["seats"]
            ]
            if not cheap_trips:
                logger.info(f"[{trace_uuid}] No cheap tickets for now.")
            else:
                logger.info(f"[{trace_uuid}] Found {len(cheap_trips)} cheap tickets!")

            return cheap_trips
