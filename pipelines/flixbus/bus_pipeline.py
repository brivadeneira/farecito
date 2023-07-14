"""
Implements pipeline classes for flixbus.
"""
import asyncio
from typing import Any

from pydantic.dataclasses import dataclass

from neo4j_graph import BusStationNode, Location, Neo4JConn, UnstructuredGraph
from pipelines.models import BaseDataPipeline
from pipelines.settings import NEO4J_DB, NEO4J_PASSWORD, NEO4J_URI, NEO4J_USERNAME


@dataclass
class FlixbusBusStationsDataPipeline(BaseDataPipeline):
    """
    Base class for cleaning, validate and store items from scrapers
    """

    ranking_size: int = 20  # determine the size of most searched stations ranking (cities)
    chunk_size: int = 100  # TODO research the best value for this

    def __post_init__(self):
        self.mandatory_fields = ["id", "name", "uuid", "location", "search_volume", "reachable"]

    @property
    def neo4j_conn(self):
        return Neo4JConn(
            uri=NEO4J_URI, user_name=NEO4J_USERNAME, password=NEO4J_PASSWORD, db_name=NEO4J_DB
        )

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

    async def store_items(self, processed_items: list[dict[str, Any]]):
        """
        Stores items into the correspondant data repository
        """
        queries = []
        chunk_size = self.chunk_size
        conn = self.neo4j_conn

        chunks = [
            processed_items[i : i + chunk_size] for i in range(0, len(processed_items), chunk_size)
        ]
        for chunk in chunks:
            nodes = [BusStationNode(**item) for item in chunk]
            graph = UnstructuredGraph(nodes)
            queries.append(graph.create_nodes_query)

        await asyncio.gather(*[conn.run_query(query) for query in queries])
