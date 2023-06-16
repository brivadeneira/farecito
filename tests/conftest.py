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
from factory import List

from tests.neo4j import CompanyInfoFactory, LocationFactory, Neo4JNodeFactory


@pytest.fixture
def dummy_location():
    return LocationFactory(latitude=0.0, longitude=0.0)


@pytest.fixture
def cypher_for_dummy_location():
    return "location: point({{ longitude: 0.0, latitude: 0.0 }})"


@pytest.fixture
def dummy_company_info():
    return CompanyInfoFactory(
        company_name="company_name",
        reachable_ids=List([1, 2, 3]),
        reachable_id_name="reachable_id_name",
        id_from_company=1,
        uuid_from_company="uuid_from_company",
    )


@pytest.fixture
def cypher_for_dummy_company_info():
    return (
        'company_name: "company_name", '
        "reachable_ids: [1, 2, 3], "
        'reachable_id_name: "reachable_id_name", '
        "id_from_company: 1, "
        'uuid_from_company: "uuid_from_company"'
    )


@pytest.fixture
def dummy_node(dummy_location, dummy_company_info):
    return Neo4JNodeFactory(
        name="name",
        node_type="node_type",
        region="region",
        location=dummy_location,
        companies_info=List([dummy_company_info]),
    )
