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

import pytest

from tests.neo4j import BusStationNodeFactory, LocationFactory


@pytest.fixture
def dummy_location():
    return LocationFactory(latitude=0.0, longitude=0.0)


@pytest.fixture
def cypher_for_dummy_location():
    return "location: point({ longitude: 0.0, latitude: 0.0 })"


@pytest.fixture
def dummy_node(dummy_location):
    return BusStationNodeFactory(
        station_id=123,
        city="Dummy City",
        region="Dummy Region",
        location=dummy_location,
        id_for_reach=456,
        service_reachable_ids=[789, 101112],
        uuid_from_service="dummy-uuid",
    )
