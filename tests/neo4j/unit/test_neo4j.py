"""
Implements tests for Neo4j-based data models.
"""
import datetime
import unittest

import pytest
from pydantic import ValidationError
from unittest_parametrize import ParametrizedTestCase, parametrize

from neo4j_graph import BusStationNode, Location, Neo4JConn, NodeRelationShip
from tests.neo4j import (
    BusStationNodeFactory,
    LocationFactory,
    Neo4JConnFactory,
    NodeFactory,
    NodeRelationshipFactory,
)

labels_for_parametrize = [
    ("FooLabel", "FooLabel"),
    ("spam_label", "SpamLabel"),
    ("foo", "Foo"),
    (None, "BusStation"),
]


class LocationTestCase(unittest.TestCase):
    """
    Test cases for Location model

    including type attr validation and cypher repr
    """

    @pytest.fixture(autouse=True)
    def __inject_fixtures(self, dummy_location, cypher_for_dummy_location):
        self.dummy_location = dummy_location
        self.cypher_for_dummy_location = cypher_for_dummy_location

    def test_valid_location(self):
        location = LocationFactory()
        self.assertIsInstance(location.latitude, float)
        self.assertIsInstance(location.longitude, float)
        self.assertTrue(-90 <= location.latitude <= 90)
        self.assertTrue(-180 <= location.longitude <= 180)

    def test_valid_cypher_repr(self):
        location = self.dummy_location
        cypher_point_repr = self.cypher_for_dummy_location
        # TODO: improve strings comparison
        assert pytest.approx(str(location)) == pytest.approx(cypher_point_repr)

    def test_invalid_latitude(self):
        with self.assertRaises(ValueError):
            LocationFactory(latitude=100)

    def test_invalid_longitude(self):
        with self.assertRaises(ValueError):
            LocationFactory(longitude=-200)

    def test_invalid_latitude_type(self):
        with self.assertRaises(TypeError):
            LocationFactory(latitude="90")

    def test_invalid_longitude_type(self):
        with self.assertRaises(TypeError):
            LocationFactory(longitude="180")


class NodeTestCase(ParametrizedTestCase):
    """
    Test cases for Node model

    including type attr validation and cypher repr
    """

    @pytest.fixture(autouse=True)
    def __inject_fixtures(
        self, dummy_node, cypher_for_dummy_node, cypher_for_dummy_node_properties
    ):
        self.dummy_node = dummy_node
        self.cypher_for_dummy_node = cypher_for_dummy_node
        self.cypher_for_dummy_node_properties = cypher_for_dummy_node_properties

    def test_valid_node(self):
        node = NodeFactory()
        self.assertIsInstance(node.id, int)
        self.assertIsInstance(node.node_type, (str, type(None)))

    def test_valid_cypher_repr(self):
        node = self.dummy_node
        cypher_node_repr = self.cypher_for_dummy_node
        assert pytest.approx(str(node)) == pytest.approx(cypher_node_repr)

    def test_invalid_int(self):
        with self.assertRaises(ValueError):
            NodeFactory(id={})

    def test_invalid_node_type(self):
        with self.assertRaises(ValueError):
            NodeFactory(node_type=3.14)

    def test_get_node_properties(self):
        node = self.dummy_node
        expected_properties = {"id", "node_type"}
        self.assertTrue(expected_properties == node.node_properties)

    def test_build_cypher_node_properties(self):
        node = self.dummy_node
        expected_cypher_properties = {"id: node.id", "node_type: node.node_type"}
        got_properties = node.build_cypher_node_properties()
        set_got_properties = set(got_properties.split(", "))
        self.assertTrue(expected_cypher_properties == set_got_properties)

    @parametrize("label,camel_label", labels_for_parametrize)
    def test_build_create_single_node(self, label, camel_label):
        node = self.dummy_node
        expected_create_query = (
            f'CREATE ( n:{camel_label} {{ id: 123, node_type: "bus_station" }} )'
        )

        got_create_query = (
            node.build_create_cypher_query(label) if label else node.build_create_cypher_query()
        )
        assert pytest.approx(expected_create_query) == pytest.approx(got_create_query)


class TestBusStationNode(ParametrizedTestCase):
    @pytest.fixture(autouse=True)
    def __inject_fixtures(self, dummy_bus_station_node, cypher_for_dummy_location):
        self.dummy_bus_station_node = dummy_bus_station_node
        self.cypher_for_dummy_location = cypher_for_dummy_location

    def test_neo4j_bus_station(self):
        node = BusStationNodeFactory()
        self.assertIsInstance(node, BusStationNode)

        self.assertIsInstance(node.city_name, str)
        self.assertIsInstance(node.region, str)
        self.assertIsInstance(node.location, Location)
        self.assertIsInstance(node.node_type, str)
        self.assertIsInstance(node.is_popular, bool)

        self.assertIsInstance(node.id, int)
        self.assertIsInstance(node.service, str)
        self.assertIsInstance(node.reachable_ids, (list, type(None)))
        if node.reachable_ids is not None:
            self.assertTrue(all(isinstance(i, int) for i in node.reachable_ids))

    def test_get_node_properties(self):
        node = self.dummy_bus_station_node
        expected_properties = {
            "is_popular",
            "region",
            "location",
            "reachable_ids",
            "city_uuid",
            "city_name",
            "node_type",
            "station_uuid",
            "service",
            "id",
        }
        self.assertTrue(expected_properties == node.node_properties)

    def test_build_cypher_node_properties(self):
        node = self.dummy_bus_station_node
        expected_cypher_properties = {
            "id: node.id",
            "node_type: node.node_type",
            "city_name: node.city_name",
            "city_uuid: node.city_uuid",
            "region: node.region",
            "location: node.location",
            "service: node.service",
            "reachable_ids: node.reachable_ids",
            "station_uuid: node.station_uuid",
            "is_popular: node.is_popular",
        }
        got_properties = node.build_cypher_node_properties()
        set_got_properties = set(got_properties.split(", "))
        self.assertTrue(expected_cypher_properties == set_got_properties)

    def test_valid_cypher_repr(self):
        node = self.dummy_bus_station_node
        cypher_for_dummy_location = self.cypher_for_dummy_location
        cypher_node_repr = (
            f"id: 123, "
            f'node_type: "BusStation", '
            f'city_name: "dummy-city", '
            f'city_uuid: "dummy-city-uuid", '
            f'region: "dummy-region", '
            f"location: {cypher_for_dummy_location}, "
            f'service: "flixbus", '
            f"reachable_ids: [1, 2, 3], "
            f'station_uuid: "dummy-station-uuid", '
            f"is_popular: false"
        )
        assert pytest.approx(str(node)) == pytest.approx(cypher_node_repr)

    def test_invalid_name_type(self):
        with self.assertRaises(ValidationError):
            BusStationNodeFactory(city_name=3.14)

    def test_invalid_region_type(self):
        with self.assertRaises(ValidationError):
            BusStationNodeFactory(region=3.141)

    @parametrize("label,camel_label", labels_for_parametrize)
    def test_build_create_single_node(self, label, camel_label):
        node = self.dummy_bus_station_node
        expected_create_query = (
            f'CREATE ( n:{camel_label} {{ id: 123, node_type: "BusStation", '
            f'city_name: "dummy-city", city_uuid: "dummy-city-uuid", '
            f'region: "dummy-region", location: point({{ longitude: 0.0, latitude: 0.0 }}), '
            f'service: "flixbus", reachable_ids: [1, 2, 3], '
            f'station_uuid: "dummy-station-uuid", is_popular: false }} )'
        )
        got_create_query = (
            node.build_create_cypher_query(label) if label else node.build_create_cypher_query()
        )
        assert pytest.approx(expected_create_query) == pytest.approx(got_create_query)


class TestNodeRelationShip(unittest.TestCase):
    @pytest.fixture(autouse=True)
    def __inject_fixtures(self, dummy_node_relationship):
        self.dummy_node_relationship = dummy_node_relationship

    def test_neo4j_relationship(self):
        relationship = NodeRelationshipFactory()
        self.assertIsInstance(relationship, NodeRelationShip)

        self.assertIsInstance(relationship.relation_name, str)
        self.assertIsInstance(relationship.travel_mode, str)
        self.assertIsInstance(relationship.schedules, (list, type(None)))
        if relationship.schedules is not None:
            self.assertTrue(all(isinstance(i, datetime.datetime) for i in relationship.schedules))
        self.assertIsInstance(relationship.average_price, float)

    def test_valid_cypher_repr(self):
        relationship = self.dummy_node_relationship
        cypher_relationship = (
            'relation_name: "dummy-relation-name", '
            'travel_mode: "bus", '
            'schedules: [datetime("2023-01-01T00:00:00.000000")], '
            "average_duration: { hours: 1, minutes: 15 }, "
            "average_price: 0.0"
        )
        assert pytest.approx(str(relationship)) == pytest.approx(cypher_relationship)

    def test_invalid_name_type(self):
        with self.assertRaises(ValidationError):
            BusStationNodeFactory(city_name=3.14)

    def test_invalid_region_type(self):
        with self.assertRaises(ValidationError):
            BusStationNodeFactory(region=3.141)


class TestNeo4JConn(unittest.TestCase):
    def test_neo4j_conn(self):
        neo4j_conn = Neo4JConnFactory()
        self.assertIsInstance(neo4j_conn, Neo4JConn)
        self.assertIsInstance(neo4j_conn.uri, str)
        self.assertIsInstance(neo4j_conn.user_name, str)
        self.assertIsInstance(neo4j_conn.password, str)
        self.assertIsInstance(neo4j_conn.db_name, str)

    def test_invalid_user_name_type(self):
        with self.assertRaises(ValidationError):
            Neo4JConnFactory(user_name=3.14)

    def test_invalid_password_type(self):
        with self.assertRaises(ValidationError):
            Neo4JConnFactory(password=3.141)

    def test_invalid_db_name_type(self):
        with self.assertRaises(ValidationError):
            Neo4JConnFactory(db_name=3.1416)


if __name__ == "__main__":
    unittest.main()
