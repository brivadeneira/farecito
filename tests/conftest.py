"""
This module contains fixtures and factories for testing Neo4j functionality.

Fixtures:
- dummy_location
- cypher_for_dummy_location
- dummy_company_info
- cypher_for_dummy_company_info
- dummy_node

Factories:
- LocationFactory
- CompanyInfoFactory
- Neo4JNodeFactory
"""
import datetime

import pytest

from tests.neo4j import BusStationNodeFactory, LocationFactory, NodeRelationshipFactory


@pytest.fixture
def dummy_location():
    return LocationFactory(latitude=0.0, longitude=0.0)


@pytest.fixture
def cypher_for_dummy_location():
    return "point({ longitude: 0.0, latitude: 0.0 })"


@pytest.fixture
def dummy_node(dummy_location):
    return BusStationNodeFactory(
        id=123,
        city_name="dummy-city",
        city_uuid="dummy-city-uuid",
        region="dummy-region",
        location=dummy_location,
        node_type="bus_station",
        service="flixbus",
        service_reachable_ids=[1, 2, 3],
        station_uuid="dummy-station-uuid",
    )


@pytest.fixture
def dummy_node_relationship():
    return NodeRelationshipFactory(
        relation_name="dummy-relation-name",
        service="dummy-service",
        schedules=[datetime.datetime(2023, 1, 1)],
        average_duration=datetime.timedelta(hours=1, minutes=15),
        average_price=0.0,
    )
