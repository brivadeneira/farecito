"""
Implements pipeline classes for flixbus.
"""
from typing import Any

from pydantic.dataclasses import dataclass

from neo4j_graph import Neo4JConn, get_popular_cities_cypher_query
from pipelines import BaseDataGetter, BaseDataLoader, BaseDataProcessor
from pipelines.settings import NEO4J_PASSWORD, NEO4J_URI, NEO4J_USERNAME


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

    async def get_stored_data(self):
        conn = self.conn
        region = self.region

        db_cities_result = await conn.execute_query(get_popular_cities_cypher_query(region=region))

        # TODO: make this code resilient
        return [{city["from_city_uuid"]: city["to_city_uuids"]} for city in db_cities_result]


@dataclass
class FlixbusTripsDataProcessor(BaseDataProcessor):
    """
    Base class for cleaning and validate flixbus bus trips
    """

    def alert_cheap_tickets(self):
        """
        Performs data processing tasks such as cleaning, validation for each item
        """
        # self.parsed_data
        # avg_price = calculate_average_trip_price(clean_items)
        # trips_to_alert = filter_trips_by_price(clean_items, avg_price)

        """
        relation_type: StrictStr = "CAN_TRANSFER_TO"
        travel_mode: StrictStr = "bus"
        schedules: List[datetime.datetime] = None
        average_duration: datetime.timedelta = None
        average_price: Price = None
        """


@dataclass
class FlixbusTripsDataLoader(BaseDataLoader):
    """
    Base class for store items after being clean and validated from scrapers
    """

    processed_data: list[Any]
    conn: Any = None
    chunk_size: int = 100  # TODO research what is the best value

    def __post_init__(self):
        if not self.conn:
            self.conn = Neo4JConn(
                uri=NEO4J_URI,
                user_name=NEO4J_USERNAME,
                password=NEO4J_PASSWORD,
            )

    def build_cypher_queries(self) -> list[str]:
        ...

    async def load_items(self):
        """
        Stores items into a neo4j graph instance by chunks
        """
