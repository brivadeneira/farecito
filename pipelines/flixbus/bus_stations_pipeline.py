"""
Implements pipeline classes for flixbus bus stations.
"""
import asyncio
import logging
import uuid
from typing import Any

from pydantic.dataclasses import dataclass

from neo4j_graph import (
    BusStationNode,
    Location,
    Neo4JConn,
    NodeRelationShip,
    UnstructuredGraph,
    get_nodes_cypher_query,
)
from pipelines import BaseDataLoader, BaseDataProcessor
from pipelines.settings import NEO4J_PASSWORD, NEO4J_URI, NEO4J_USERNAME
from settings import APP_NAME

logger = logging.getLogger(APP_NAME)
logger.setLevel(logging.DEBUG)


@dataclass
class FlixbusBusStationsDataProcessor(BaseDataProcessor):
    """
    Base class for cleaning and validate flixbus bus stations (cities)
    """

    ranking_size: int = 20  # determine the size of most searched stations ranking (cities)
    chunk_size: int = 100  # TODO [research] the best value for this

    def __post_init__(self):
        self.mandatory_fields = ["id", "name", "uuid", "location", "search_volume", "reachable"]

    def process_items(self):
        """
        Performs data processing tasks such as cleaning, validation for each item
        """
        ranking_size = self.ranking_size
        data = self.parsed_data
        top_searched_threshold = data[min(ranking_size, len(data) - 1)]["search_volume"]

        processed_items = []

        trace_uuid = str(uuid.uuid4())
        logger.info(f"[{trace_uuid}] Trying to process {len(data)} items.")

        for item in data:
            if self.mandatory_fields:
                if not all(item[field] for field in self.mandatory_fields):
                    logger.error(f"[{trace_uuid}] Missing data in {item}")
                    continue

            reachable = item["reachable"]
            reachable_ids = [
                reach["id"] for reach in reachable if reach["id"] and isinstance(reach["id"], int)
            ]
            if not all(item["reachable"]):
                logger.error(f"[{trace_uuid}] No city reachable in {item}")
                continue

            lat, lon = item["location"]["lat"], item["location"]["lon"]
            location = Location(latitude=lat, longitude=lon)

            processed_item = {
                "id": item["id"],
                "city_name": item["name"],
                "city_uuid": item["uuid"],
                "region": item["region"],
                "location": location,
                "is_popular": item["search_volume"] >= top_searched_threshold
                if item["search_volume"]
                else False,
                "reachable_ids": reachable_ids,
            }

            processed_items.append(processed_item)

        logger.info(f"[{trace_uuid}] {len(processed_items)} items processed successfully.")
        return processed_items


@dataclass
class FlixbusBusStationsDataLoader(BaseDataLoader):
    """
    Base class for store items after being clean and validated from scrapers
    """

    processed_data: list[Any]
    conn: Any = None
    chunk_size: int = 100  # TODO [research] what is the best value
    region: str = "EU"

    def __post_init__(self):
        if not self.conn:
            self.conn = Neo4JConn(
                uri=NEO4J_URI,
                user_name=NEO4J_USERNAME,
                password=NEO4J_PASSWORD,
            )

    async def load_items(self):
        """
        Stores items into a neo4j graph instance by chunks
        """
        region = self.region
        data = self.processed_data
        chunk_size = self.chunk_size
        conn = self.conn

        # TODO [refactor] split next block

        create_node_queries, multi_node_relationship_queries, single_node_relationship_queries = (
            [],
            [],
            [],
        )

        db_existing_nodes_result = await conn.execute_query(
            get_nodes_cypher_query(region=region, properties=["id", "reachable_ids"])
        )

        if db_existing_nodes_result:
            db_existing_nodes = {
                node["n.Id"]: node["n.ReachableIds"] for node in db_existing_nodes_result
            }

            def stored(node):
                return node["id"] in db_existing_nodes

            existing_nodes, new_nodes = [node for node in data if stored(node)], [
                node for node in data if not stored(node)
            ]

            existing_nodes_dict = {node["id"]: node["reachable_ids"] for node in existing_nodes}

            # TODO [improvement] refactor this code in order to make it more clear

            single_node_new_relationships = [
                [node_id, list(set(reachable_ids).difference(set(db_existing_nodes[node_id])))]
                for node_id, reachable_ids in existing_nodes_dict.items()
                if set(reachable_ids).difference(set(db_existing_nodes[node_id]))
            ]

            single_node_relationship_queries = [
                NodeRelationShip(
                    src_node_ids=[item[0]], dst_node_ids=item[1]
                ).create_single_node_relationships()
                for item in single_node_new_relationships
            ]
        else:
            new_nodes = data

        new_nodes_chunks = [
            new_nodes[i : i + chunk_size] for i in range(0, len(new_nodes), chunk_size)
        ]

        for chunk in new_nodes_chunks:
            # TODO [improvement] add resilient block here in case something wrong with an item
            nodes = [BusStationNode(**item) for item in chunk]
            graph = UnstructuredGraph(nodes)
            create_node_queries.append(graph.create_nodes_query)

            relationship = NodeRelationShip(src_node_ids=[item["id"] for item in chunk])
            multi_node_relationship_queries.append(
                relationship.create_multiple_node_relationships()
            )

        trace_uuid = str(uuid.uuid4())
        logger.info(f"[{trace_uuid}] Trying to load {len(new_nodes)} new nodes.")
        # TODO [improvement] propagate log trace uuid

        await asyncio.gather(*[conn.execute_query(query) for query in create_node_queries])
        await asyncio.gather(
            *[conn.execute_query(query) for query in multi_node_relationship_queries]
        )

        await asyncio.gather(
            *[conn.execute_query(query) for query in single_node_relationship_queries]
        )
