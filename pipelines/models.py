"""
Implements base classes for pipelines.
"""

from typing import Any

from pydantic.dataclasses import dataclass


@dataclass
class BaseDataPipeline:
    """
    Base class for cleaning, validate and store items from scrapers
    """

    parsed_data: list[dict[str, Any]]
    mandatory_fields: list[str] = None

    def process_items(self):
        """
        Performs data processing tasks such as cleaning, validation for each item
        """
        return []

    async def store_items(self, processed_items):
        """
        Stores items into the correspondant data repository
        """
