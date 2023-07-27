# pylint: skip-file
# TODO [bug] fix astroid-error
# TODO [improvement] define empty classes for errors
# TODO [improvement] add @staticmethod decorator in correspondant methods
# TODO [improvement] encapsulate methods when necessary
"""
Models Neo4j Data Warehouse Connector,
with data validation, cypher str representation and queries ready to use

- Currency: for currencies representation
- Price: A price amount with its currency.
- Location: geographical location with latitude and longitude.

- Neo4jBase: Base dataclass with type validation and a method for building Cypher queries for Neo4j nodes.
    - Node: Dataclass representing a generic Neo4j node.
        - BusStationNode: Dataclass representing a Neo4j node model for bus stations.
    - NodeRelationShip: Dataclass representing a Neo4j node model for relationships between nodes.
- UnstructuredGraph: Dataclass for temporarily storing homogeneous nodes and their relationships.
- Neo4JConn: Dataclass representing a connection with a Neo4j database instance.
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
from pydantic import StrictStr, validator
from pydantic.dataclasses import dataclass

from neo4j_graph.utils import get_cypher_core_data_type, snake_to_upper_camel
from settings import APP_NAME

logger = logging.getLogger(APP_NAME)
logger.setLevel(logging.DEBUG)

from enum import Enum


class Currency(Enum):
    """
    Enum class representing different currencies with their corresponding codes and names.
    """

    USD = "United States Dollar"
    EUR = "Euro Member Countries"
    BRL = "Brazil Real"


@dataclass
class Price:
    """
    Dataclass representing a price amount with its currency.
    It ensures that the amount is numeric and greater than zero.
    """

    amount: float | None = None
    currency: Currency | None = None

    def __post_init__(self):
        if self.amount:
            try:
                self.amount = float(self.amount)
            except ValueError:
                # TODO [bug], fix this! For some reason pydantic is not validating this
                raise TypeError(f"price amount must be a numeric not {type(self.amount)}")
            if self.amount < 0:
                raise TypeError(f"price must be higher than zero, not {self.amount}")

    def __str__(self):
        # TODO [research] how to manage amounts and currencies in neo4j (cypher)
        return f'"{round(self.amount, 2)} {self.currency.name}"'


@dataclass
class Location:
    """
    A cypher point - like Dataclass based on Neo4J
    representing a geographical location with latitude and longitude.
    It validates that latitude is between -90 and 90, and longitude is between -180 and 180
    and includes a str cypher representation.
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

    def __str__(self) -> str:
        """
        str cypher representation according to https://neo4j.com/docs/cypher-manual/current/functions/spatial/
        """
        return f"point({{ longitude: {self.longitude}, latitude: {self.latitude} }})"


@dataclass
class Neo4jBase:
    """
    Base dataclass for Neo4j entities
    includes type validation
    and a representation method for building Cypher queries for Neo4j nodes.
    """

    def __str__(self) -> str:
        """
        Convert objects into str, ready to add in a cypher query:
            - removing quotes from keys
            - keeping quotes for str values
            - converting into a point object with valid coordinates in Morón, provincia de Buenos Aires

        Example node: {'name': 'Micky Vainilla',
                       'location': {'longitude': -58.6199, 'latitude': -34.6545},
                       'year': 2006, 'show': 'Peter Capusotto y sus videos'}

        :return: (str) a ready-to-add cypher query
            e.g. 'name: "Micky Vainilla",
                 location: point({ longitude: -58.6199, latitude: -34.6545 }),
                 year: 2006, show: "Peter Capusotto y sus videos"'
        """
        items_as_str = []
        for field_name, field_def in self.__dataclass_fields__.items():
            if field_name in ["relation_type", "src_node_ids", "dst_node_ids"]:
                # Avoid NodeRelationShip attribute TODO [improvement]
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
    Dataclass representing a generic Neo4j node.
    It includes properties for the node's ID, node type, and reachable IDs.
    It provides methods to get the node's properties and build Cypher queries for creating nodes.
    """

    id: int
    node_type: StrictStr = "node"
    reachable_ids: list[int] | None = None

    @property
    def node_properties(self) -> set:
        """
        Get all property names of the node.

        :return: (set) A set containing the property names of the node.
                      Useful for comparing nodes' structures.
                      Example: {'Id', 'NodeType', 'ReachableIds', 'CharacterName', 'ShowName'}
        """
        return {
            snake_to_upper_camel(field_name) for field_name, _ in self.__dataclass_fields__.items()
        }

    @property
    def cypher_node_properties(self) -> list:
        """
        Builds a general Cypher representation for node properties.

        This method is useful for multiple node operations, such as creating or updating nodes.
        It returns a list of strings, where each string represents a property name in UpperCamelCase.

        Example:
        For a node with the following properties:
        {'id': 1,
         'node_type': 'character',
         'reachable_ids': [2, 3],
         'character_name': 'Peter Capusotto',
         'show_name': 'Peter Capusotto y sus videos'}

        The method will return:
        ['Id', 'NodeType', 'ReachableIds', 'CharacterName', 'ShowName']

        :return: (list[str]) A list of property names in UpperCamelCase.
        """
        return [
            snake_to_upper_camel(field_name) for field_name, _ in self.__dataclass_fields__.items()
        ]

    @property
    def cypher_create_query(self) -> str:
        """
        Builds a Cypher query for creating the node.

        The method constructs a Cypher query string in the format
        'CREATE (n:NodeType {property: value, ...})'
        where NodeType is the type of the node
        and property-value pairs represent the node's properties.

        e.g.
        For a character node with id=1, name='Violencia Rivas',
        and show='Peter Capusotto y sus videos':
        The method will return:
        'CREATE (n:Character {id: 1, name: 'Violencia Rivas',
        show: 'Peter Capusotto y sus videos'})'

        :return: (str) A string representing the Cypher query for creating the node.

        """
        label = snake_to_upper_camel(self.node_type)
        return f"CREATE ( n:{label} {{ {str(self)} }} )"


@dataclass(kw_only=True)
class BusStationNode(Node):
    """
    Dataclass representing a Neo4j node model for bus stations.
    Inherits from Node.
    It includes additional properties
    like city name, city UUID, region, location, etc.
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
    Dataclass representing a Neo4j node model for relationships between bus stations.
    Inherits from Neo4jBase.
    It includes properties for source node IDs, destination node IDs, relation type, etc.
    It provides methods to create Cypher queries for single and multiple node relationships.
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
    def cypher_str(self) -> str:
        """
        Get the Cypher representation for the relationship
        according to https://neo4j.com/docs/cypher-manual/current/clauses/create/

        :return: (str) e.g. '[r:CAN_TRANSFER_TO {travel_mode: "bus"}]'
        """
        return f"[r:{self.relation_type} {{ {str(self)} }}]"

    def create_single_node_relationships(self) -> str:
        """
            Build a Cypher query for creating single node relationships.

            The method constructs a Cypher query that merges relationships
            between a source node and a collection of destination nodes.

            :return: (str) e.g.
            For a relationship with src_node_ids=[1] and dst_node_ids=[2, 3, 4]
            and relation_type='CAN_TRANSFER_TO':

               (1) -CAN_TRANSFER_TO-> (2)
                |
        CAN_TRANSFER_TO
                |
                v
               (3) -CAN_TRANSFER_TO-> (4)

            'MATCH (a { Id: 1 }), (new_connections)
            WHERE a <> new_connections
            AND new_connections.Id IN [2, 3, 4]
            WITH a, COLLECT(new_connections) as conn
            FOREACH (b IN conn | MERGE (a)-[r:CAN_TRANSFER_TO {travel_mode: "bus"}]->(b))'

        """
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
        """
        Builds a Cypher query for creating relationships
        between a single source node and multiple destination nodes.
        It uses the `UNWIND` clause to iterate through
        the list of source node IDs and matches each source node
        with its corresponding destination nodes based on the `Id` property.
        Then, it creates the relationship
        between the source node and each destination node using the `MERGE` clause.

        :return: (str) a Cypher query for creating multiple node relationships. e.g.
              (1) -CAN_TRANSFER_TO-> (2)
              |
         CAN_TRANSFER_TO
              |
              v
            (3) -CAN_TRANSFER_TO-> (4)

            'WITH [1, 5, 9] AS node_ids
            UNWIND node_ids AS node_id
            MATCH (a {Id: node_id}), (new_connections)
            WHERE a <> new_connections
            AND new_connections.Id IN a.ReachableIds
            WITH a, COLLECT(new_connections) as conn
            FOREACH (b IN conn | MERGE (a)-[r:CAN_TRANSFER_TO {travel_mode: "bus"}]->(b))'
        """

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
        """
        Builds a Cypher query for creating relationships between nodes.
        If the node has only one source node ID (`src_node_ids`), the method will use the
        `create_single_node_relationships` method to create a relationship
        between the source node and the destination node.
        If the node has multiple source node IDs,
        the method will use the `create_multiple_node_relationships` method
        to create relationships between each source node and their respective destination nodes.

        :return: (str) a Cypher query for creating relationships between nodes.
        :raises: ValueError: If no source node IDs are provided.
        """
        if not self.src_node_ids:
            raise ValueError("At least a src_node_id is needed.")

        if len(self.src_node_ids) == 1:
            return self.create_single_node_relationships()

        return self.create_multiple_node_relationships()


@dataclass
class UnstructuredGraph:
    """
    A minimalist way of temporary store homogeneous nodes and their relationships,
    It ensures that all nodes have the same properties and node type.
    It provides a method to create a Cypher query for creating multiple nodes at once.
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
        Builds a Cypher query to create multiple nodes at once, ready to be executed.
        All nodes must have the same properties and 'node_type' attribute.
        If there is only one node in the list,
        the method returns the Cypher query for creating that single node.

        If there are multiple nodes in the list,
        the method generates a Cypher query using the 'FOREACH' clause to
        create each node using the 'MERGE' command, ensuring that duplicate nodes are not created.

        NOTE: All null values are replaced with an empty string '' in case of 'MERGE'.
        TODO: Improve the treatment for null values if necessary.

        :return: (str) a Cypher query to create multiple nodes at once, e.g.
            'FOREACH (node IN [{name: 'Micky Vainilla', age: 45, profession: 'Pop Singer'},
            {name: 'Violencia Rivas', age: 35, profession: 'Punk creator'}]
            | MERGE (n:Character {name: node.name, age: node.age, profession: node.profession}))'
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
    Dataclass representing a connection with a Neo4j database instance.
    It uses a driver to connect to the database and execute Cypher queries.
    It includes methods to execute queries
    and handle exceptions related to the database connection.
        - using a driver
        - running cypher queries
    """

    uri: StrictStr
    user_name: StrictStr
    password: StrictStr
    db_name: StrictStr = "neo4j"
    auth: tuple[str, str] = None
    async_driver: AsyncDriverType = None

    def init_driver(self) -> None:
        """
        Initialize the Neo4j driver for connecting to the database.

        This method creates an AsyncGraphDatabase driver
        using the provided URI, authentication details, and database name.
        The 'max_connection_lifetime' parameter is set to 200 milliseconds.

        :raises: DriverError if there is an issue with the Neo4j driver.
        """
        try:
            self.async_driver = AsyncGraphDatabase.driver(
                self.uri, auth=self.auth, database=self.db_name, max_connection_lifetime=200
            )
        except DriverError as ex:
            logging.error(f"A node4j driver exception appeared: {ex}")

    @validator("uri")
    def validate_nodes(cls, uri):
        # TODO [bug], fix this! For some reason pydantic is not validating this
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
