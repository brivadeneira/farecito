# pylint: skip-file
# TODO fix astroid-error
# TODO define empty classes for errors
# TODO add @staticmethod decorator in correspondant methods
# TODO encapsulate methods when necessary
"""
Implements classes for Neo4j-based data models.

Classes:
- Neo4jBase: Base class for Neo4j models with type validation and conversion methods.
- Location: Represents a geographic location with latitude and longitude values for node properties.
- Node: Represents a node in the Neo4j graph database.
- BusStationNode: A specific type of Neo4J node.
- NodeRelationShip: A Neo4J like class for relationships between nodes.
- Neo4JConn: A class for connections with a Neo4j graph db
"""
from __future__ import annotations

import asyncio
import datetime
import itertools
import logging
import uuid
from dataclasses import is_dataclass
from typing import Any, List, TypeVar

from neo4j import AsyncGraphDatabase
from neo4j.exceptions import AuthError, DatabaseError, DriverError, Forbidden, TransientError
from pydantic import BaseModel, StrictStr, validator
from pydantic.dataclasses import dataclass

from neo4j_graph.utils import get_cypher_core_data_type, snake_to_upper_camel

from .settings import APP_NAME

logger = logging.getLogger(APP_NAME)
logger.setLevel(logging.DEBUG)

from enum import Enum


class Currency(Enum):
    USD = "United States Dollar"
    EUR = "Euro Member Countries"
    BRL = "Brazil Real"


@dataclass
class Price:
    amount: float | None = None
    currency: Currency | None = None

    def __post_init__(self):
        if self.amount:
            try:
                self.amount = float(self.amount)
            except ValueError:
                # TODO, fix this! For some reason pydantic is not validating this
                raise TypeError(f"price amount must be a numeric not {type(self.amount)}")
            if self.amount < 0:
                raise TypeError(f"price must be higher than zero, not {self.amount}")

    def __str__(self):
        # TODO research how to manage amounts and currencies in neo4j (cypher)
        return f'"{round(self.amount, 2)} {self.currency.name}"'


@dataclass
class Location:
    """
    A cypher point - like class based on Neo4J
    according to https://neo4j.com/docs/cypher-manual/current/functions/spatial/
    """

    latitude: float | int
    longitude: float | int

    @validator("latitude")
    def validate_latitude(cls, latitude):
        if latitude < -90 or latitude > 90:
            raise ValueError("latitude must be between -90 and 90")
        return latitude

    @validator("longitude")
    def validate_longitude(cls, longitude):
        if longitude < -180 or longitude > 180:
            raise ValueError("longitude must be between -180 and 180")
        return longitude

    def __str__(self):
        return f"point({{ longitude: {self.longitude}, latitude: {self.latitude} }})"


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
            if field_name in ["relation_type", "src_node_ids", "dst_node_ids"]:
                # Avoid NodeRelationShip attribute
                # TODO improve this
                continue
            field_value = getattr(self, field_name)
            property_name = snake_to_upper_camel(field_name)
            if is_dataclass(field_value):
                items_as_str.append(f"{property_name}: {str(field_value)}")
            else:
                items_as_str.append(f"{property_name}: {get_cypher_core_data_type(field_value)}")
        return f'{", ".join(items_as_str)}'


@dataclass
class Node(Neo4jBase):
    """
    A Neo4j node elemental model
    like class based on Neo4jBase
    """

    id: int
    node_type: StrictStr = "node"
    reachable_ids: list[int] | None = None

    @property
    def node_properties(self) -> set:
        """
        Get all property names of the node
        useful for compare nodes structure
        :return: (set)
        """
        return {
            snake_to_upper_camel(field_name) for field_name, _ in self.__dataclass_fields__.items()
        }

    @property
    def cypher_node_properties(self) -> list:
        """
        Builds a general cypher representation for node properties,
        useful for multiple nodes operations.
        e.g. ['Id', 'NodeType', 'ReachableIds', ...]
        :return:
        """
        return [
            snake_to_upper_camel(field_name) for field_name, _ in self.__dataclass_fields__.items()
        ]

    @property
    def cypher_create_query(self) -> str:
        """
        Builds a cypher query for create the node,
        e.g. 'CREATE (n:BusStation {id: 123})'
        e.g. 'CREATE (n:City {name: 'Lisbon'})'
        """
        label = snake_to_upper_camel(self.node_type)
        return f"CREATE ( n:{label} {{ {str(self)} }} )"


@dataclass(kw_only=True)
class BusStationNode(Node):
    """
    A Neo4j node model for bus stations,
    like class based on Neo4jBase
    """

    city_name: StrictStr
    city_uuid: StrictStr
    region: StrictStr
    location: Location
    node_type: str = "BusStation"
    service: StrictStr = "flixbus"
    station_uuid: StrictStr | None = None
    is_popular: bool = False

    def __post_init__(self):
        self.node_type = snake_to_upper_camel(self.node_type)


@dataclass
class NodeRelationShip(Neo4jBase):
    """
    A Neo4j node model for relationships between bus stations,
    like class based on Neo4jBase
    """

    src_node_ids: list[int] = None
    dst_node_ids: list[int] = None
    relation_type: StrictStr = "CAN_TRANSFER_TO"
    travel_mode: StrictStr = "bus"
    schedules: List[datetime.datetime] = None
    average_duration: datetime.timedelta = None
    average_price: Price = None

    def __post_init__(self):
        self.relation_type = self.relation_type.upper().replace("-", "_")

    @property
    def cypher_str(self):
        return f"[r:{self.relation_type} {{ {str(self)} }}]"

    def create_single_node_relationships(self) -> str:
        dst_node_ids = self.dst_node_ids

        reachable_ids = str(dst_node_ids) if dst_node_ids else "a.ReachableIds"

        [src_node_id] = self.src_node_ids
        return f"""
        MATCH (a {{ Id: {src_node_id} }}), (new_connections)
        WHERE a <> new_connections
        AND new_connections.Id IN {reachable_ids} WITH a,
        COLLECT(new_connections) as conn FOREACH (b IN conn
        | MERGE (a)-{self.cypher_str}->(b))
        """.strip()

    def create_multiple_node_relationships(self) -> str:
        src_node_ids = self.src_node_ids

        return f"""
        WITH {str(src_node_ids)} AS node_ids
        UNWIND node_ids AS node_id MATCH (a {{Id: node_id}}),
        (new_connections) WHERE a <> new_connections
        AND new_connections.Id IN a.ReachableIds WITH a,
        COLLECT(new_connections) as conn
        FOREACH (b IN conn | MERGE (a)-{self.cypher_str}->(b))
        """.strip()

    @property
    def create_relationship_query(self) -> str:
        if not self.src_node_ids:
            raise ValueError("At least a src_node_id is needed.")

        if len(self.src_node_ids) == 1:
            return self.create_single_node_relationships()

        return self.create_multiple_node_relationships()


@dataclass
class UnstructuredGraph:
    """
    A minimalist way of temporary store homogeneous nodes and their relationships,
    in order to make checks and build cypher queries for all of them at once.
    """

    nodes: list[Any]
    relationship: NodeRelationShip = None

    @validator("nodes")
    def validate_nodes(cls, nodes):
        """
        Validate all nodes are a subclass of Node
        and check for all of their properties and node_type that must be the same
        """
        if not all(issubclass(type(node), Node) for node in nodes):
            raise TypeError("Wrong type for 'nodes', must be subclass of Node")
        for a_node, another_node in itertools.combinations(nodes, 2):
            if not a_node.node_properties == another_node.node_properties:
                raise ValueError("Nodes must have the same properties")
            if not a_node.node_type == another_node.node_type:
                raise ValueError("Nodes must have the same node_type value")
        return nodes

    @property
    def create_nodes_query(self) -> str:
        """
        Builds the cypher query for create multiple nodes at once, ready for run.
        Nodes must have the same properties and 'node_type' attribute
        NOTE: All null values are going to be replaced with '' in case of MERGE
        # TODO improve this treatment.
        """

        if len(self.nodes) == 1:
            [node] = self.nodes
            return node.cypher_create_query

        cypher_node_core_str = [str(node) for node in self.nodes]
        node_ref = self.nodes[0]
        node_type, cypher_node_properties = node_ref.node_type, node_ref.cypher_node_properties
        properties_set = ", ".join(f"{prop}: node.{prop}" for prop in cypher_node_properties)

        return (
            f"FOREACH (node IN [{{ {' }, { '.join(cypher_node_core_str)} }}] "
            f"| MERGE (n: {snake_to_upper_camel(node_type)} {{ {properties_set} }}))".strip()
        )


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
                self.uri, auth=self.auth, database=self.db_name, max_connection_lifetime=200
            )
        except DriverError as ex:
            logging.error(f"A node4j driver exception appeared: {ex}")

    @validator("uri")
    def validate_nodes(cls, uri):
        # TODO, fix this! For some reason pydantic is not validating this
        if not isinstance(uri, str):
            raise TypeError(f"neo4jconn uri must be a str not {type(uri)}")
        return uri

    def __post_init__(self):
        self.auth = self.user_name, self.password

        if not self.async_driver:
            self.init_driver()

    async def _close_driver(self):
        await self.async_driver.close()

    async def execute_query(self, query: str, sleep_time: int = 60):
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
        except (AuthError, Forbidden, DatabaseError, DriverError, TransientError) as ex:
            logging.error(f"[{trace_uuid}] A node4j exception appeared: {ex}")
            await self._close_driver()
            await asyncio.sleep(sleep_time)
            self.init_driver()
            await self.execute_query(query)
        except Exception as ex:
            logging.error(f"[{trace_uuid}] A node4j exception appeared: {ex}")
