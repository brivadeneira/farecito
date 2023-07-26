"""
Implements base classes for pipelines.
"""
from abc import ABC, abstractmethod
from typing import Any

from pydantic.dataclasses import dataclass


@dataclass
class BaseDataProcessor(ABC):
    """
    Base class for cleaning and validate from scrapers
    """

    parsed_data: list[dict[str, Any]]
    mandatory_fields: list[str] = None

    @abstractmethod
    def process_items(self):
        """
        Performs data processing tasks such as cleaning, validation for each item
        """


@dataclass
class BaseDataLoader(ABC):
    """
    Base class for store items after being clean and validated from scrapers
    """

    processed_data: list[Any]
    conn: Any = None

    @abstractmethod
    async def load_items(self):
        """
        Stores items into the correspondant data repository
        """


@dataclass
class BaseDataGetter(ABC):
    """
    Base class for store items after being clean and validated from scrapers
    """

    conn: Any = None

    @abstractmethod
    async def get_stored_data(self):
        """
        Stores items into the correspondant data repository
        """


@dataclass
class BaseDataTracker(ABC):
    """
    Base class for tracking items
    """

    @abstractmethod
    async def track_data_of_interest(self, processed_data: list[Any]):
        """
        Track data of interest of processed_data template method
        """
