"""
This module contains fixtures and factories for testing Neo4j functionality.

All "dummy" fixtures must have the next format in all their values attributes:
- str: "dummy_<attribute name>"
- int: 0
- float: 0.0
- list[int] = [1, 2, 3]
...

Fixtures:
- dummy_price
- dummy_node
- dummy_bus_station_node
- dummy_node_relationship

"""
import datetime

import pytest

from neo4j_graph import Currency
from tests.neo4j import (
    BusStationNodeFactory,
    LocationFactory,
    NodeFactory,
    NodeRelationshipFactory,
    PriceFactory,
    UnstructuredGraphFactory,
)


@pytest.fixture(scope="class")
def dummy_price():
    return PriceFactory(amount=0.0, currency=Currency.USD)


@pytest.fixture(scope="class")
def dummy_location():
    return LocationFactory(latitude=0.0, longitude=0.0)


@pytest.fixture(scope="class")
def dummy_node():
    return NodeFactory(
        id=123,
        node_type="dummy_node_type",
    )


@pytest.fixture
def dummy_bus_station_node(dummy_location):
    return BusStationNodeFactory(
        id=123,
        node_type="dummy_node_type",
        reachable_ids=[1, 2, 3],
        city_name="dummy_city",
        city_uuid="dummy_city_uuid",
        region="dummy_region",
        location=dummy_location,
        service="dummy_service",
        station_uuid="dummy_station_uuid",
    )


@pytest.fixture
def dummy_node_relationship(dummy_price):
    return NodeRelationshipFactory(
        relation_type="dummy_relation_type",
        schedules=[datetime.datetime(2023, 1, 1)],
        average_duration=datetime.timedelta(hours=1, minutes=12),
        average_price=dummy_price,
    )


@pytest.fixture
def dummy_graph(dummy_node_relationship):
    return UnstructuredGraphFactory(
        nodes=[
            NodeFactory(id=1, node_type="dummy_node_type", reachable_ids=[2, 3]),
            NodeFactory(id=2, node_type="dummy_node_type", reachable_ids=[1, 3]),
            NodeFactory(id=3, node_type="dummy_node_type", reachable_ids=[1, 2]),
        ],
        relationship=dummy_node_relationship,
    )
