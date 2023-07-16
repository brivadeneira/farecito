"""
Implements pipeline classes for flixbus.
"""
import asyncio
from typing import Any

from pydantic.dataclasses import dataclass

from neo4j_graph import BusStationNode, Location, Neo4JConn, UnstructuredGraph
from pipelines import BaseDataLoader, BaseDataProcessor
from pipelines.settings import NEO4J_PASSWORD, NEO4J_URI, NEO4J_USERNAME


@dataclass
class FlixbusBusStationsDataProcessor(BaseDataProcessor):
    """
    Base class for cleaning and validate flixbus bus stations (cities)
    """

    ranking_size: int = 20  # determine the size of most searched stations ranking (cities)
    chunk_size: int = 100  # TODO research the best value for this

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

        for item in data:
            if self.mandatory_fields:
                if not all(item[field] for field in self.mandatory_fields):
                    # TODO log missing item data
                    continue

            reachable = item["reachable"]
            reachable_ids = [
                reach["id"] for reach in reachable if reach["id"] and isinstance(reach["id"], int)
            ]
            if not all(item["reachable"]):
                # TODO log not reachable city
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

        return processed_items


@dataclass
class FlixbusBusStationsDataLoader(BaseDataLoader):
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
        processed_data = self.processed_data
        chunk_size = self.chunk_size

        queries = []

        chunks = [
            processed_data[i : i + chunk_size] for i in range(0, len(processed_data), chunk_size)
        ]

        for chunk in chunks:
            nodes = [BusStationNode(**item) for item in chunk]
            graph = UnstructuredGraph(nodes)
            queries.append(graph.create_nodes_query)

        return queries

    async def load_items(self):
        """
        Stores items into a neo4j graph instance by chunks
        """
        conn = self.conn
        queries = self.build_cypher_queries()

        await asyncio.gather(*[conn.execute_query(query) for query in queries])
