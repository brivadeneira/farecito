"""
Implements classes for Neo4j-based data models.

Classes:
- Neo4jBase: Base class for Neo4j models with type validation and conversion methods.
- Location: Represents a geographic location with latitude and longitude values.
- Neo4JNode: Represents a node in the Neo4j graph database.
"""
from __future__ import annotations

import asyncio
import datetime
import logging
import uuid
from dataclasses import is_dataclass
from typing import List, TypeVar

from neo4j import AsyncGraphDatabase
from neo4j.exceptions import AuthError, DatabaseError, DriverError, Forbidden
from pydantic import StrictStr, ValidationError
from pydantic.dataclasses import dataclass

from neo4j_graph.utils import object_to_cypher_repr
from settings import APP_NAME, SLEEP_TIME

logger = logging.getLogger(APP_NAME)
logger.setLevel(logging.DEBUG)


@dataclass
class Location:
    """
    A cypher point - like class based on Neo4J
    """

    latitude: float | int
    longitude: float | int

    def __post_init__(self):
        if self.latitude < -90 or self.latitude > 90:
            raise ValueError("latitude must be between -90 and 90")

        if self.longitude < -180 or self.longitude > 180:
            raise ValueError("longitude must be between -180 and 180")

    def __str__(self):
        return f"point({{ longitude: {self.longitude}, latitude: {self.longitude} }})"


@dataclass
class Neo4jBase:
    """
    Base Neo4j class with type validation
    and repr method useful for queries.
    """

    def __str__(self) -> str:
        """
        Convert objects into str, ready to add in a cypher query:
            - removing quotes from keys
            - keeping quotes form str values
            - converting into a point object coordinates

        node e.g. {'name': 'Turanga',
                   'location': {'longitude': 3.14159, 'latitude': 1729},
                   'year': 3000, 'service': 'Planet express'}

        :return: (str) a ready to add cypher query
            e.g. 'name: "Turanga",
                 location: point({ longitude: 3.14159, latitude: 1729 }),
                 year: 3000, service: "Planet express"'
        """
        items_as_str = []
        for field_name, field_def in self.__dataclass_fields__.items():
            field_value = getattr(self, field_name)
            if is_dataclass(field_value):
                items_as_str.append(f"{field_name}: {str(field_value)}")
            else:
                items_as_str.append(f"{field_name}: {object_to_cypher_repr(field_value)}")
        return f'{", ".join(items_as_str)}'


@dataclass
class BusStationNode(Neo4jBase):
    """
    A Neo4j node model for bus stations,
    like class based on Neo4jBase
    """

    station_id: int  # id_for_reach
    city_name: StrictStr
    city_uuid: StrictStr
    region: StrictStr
    location: Location
    node_type: StrictStr = "bus_station"
    service: StrictStr = "flixbus"
    reachable_ids: list[int] | None = None
    station_uuid: StrictStr | None = None
    is_popular: bool = False


@dataclass
class NodeRelationShip(Neo4jBase):
    """
    A Neo4j node model for relationships between bus stations,
    like class based on Neo4jBase
    """

    relation_name: StrictStr = "CAN_TRANSFER_TO"
    service: StrictStr = "flixbus"
    schedules: List[datetime.datetime] = None
    average_duration: datetime.timedelta = None
    average_price: float = None  # TODO manage currencies


AsyncDriverType = TypeVar("neo4j.AsyncDriver")


@dataclass
class Neo4JConn:
    """
    Class for connecting with a neo4j db instance
    - using a driver
    - running cypher queries
    """

    uri: StrictStr
    user_name: StrictStr
    password: StrictStr
    db_name: StrictStr = "neo4j"
    auth: tuple[str, str] = None
    async_driver: AsyncDriverType = None

    def init_driver(self):
        try:
            self.async_driver = AsyncGraphDatabase.driver(
                self.uri, auth=self.auth, database=self.db_name
            )
        except DriverError as ex:
            logging.error(f"A node4j driver exception appeared: {ex}")

    def __post_init__(self):
        if not isinstance(self.uri, str):
            #  for some reason pydantic is not validating this
            raise ValidationError()

        self.auth = self.user_name, self.password

        if not self.async_driver:
            self.init_driver()

    async def _close_driver(self):
        await self.async_driver.close()

    async def execute_query(self, query: str, sleep_time: int = SLEEP_TIME):
        """
        Execute an async given neo4j_graph query
        :param query: (str) a valid neo4j_graph query to be executed
        :param sleep_time: (int) time to sleep in case of reconnecting driver, if not given SLEEP_TIME
        :return: (any) the data in the result of the query.
        """
        trace_uuid = str(uuid.uuid4())
        try:
            async with self.async_driver.session() as session:
                result = await session.run(query)
                data = await result.data()
                if data:
                    logger.debug(f"[{trace_uuid}] The data result for the query was: {data}")
                return data
        except (AuthError, Forbidden, DatabaseError, DriverError) as ex:
            logging.error(f"[{trace_uuid}] A node4j exception appeared: {ex}")
            await self.close_driver()
            await asyncio.sleep(sleep_time)
            self.init_driver()
            await self.run_query(query)
