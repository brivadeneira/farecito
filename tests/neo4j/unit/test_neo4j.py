"""
Implements tests for Neo4j-based data models.
"""
import unittest

import pytest
from pydantic import ValidationError

from neo4j_graph import BusStationNode, Location, Neo4JConn
from tests.neo4j import BusStationNodeFactory, LocationFactory, Neo4JConnFactory


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


class TestBusStationNode(unittest.TestCase):
    @pytest.fixture(autouse=True)
    def __inject_fixtures(self, dummy_node, cypher_for_dummy_location):
        self.dummy_node = dummy_node
        self.cypher_for_dummy_location = cypher_for_dummy_location

    def test_neo4j_node(self):
        node = BusStationNodeFactory()
        self.assertIsInstance(node, BusStationNode)

        self.assertIsInstance(node.city, str)
        self.assertIsInstance(node.region, str)
        self.assertIsInstance(node.location, Location)
        self.assertIsInstance(node.node_type, str)
        self.assertIsInstance(node.is_popular, bool)

        self.assertIsInstance(node.station_id, int)
        self.assertIsInstance(node.id_for_reach, int)
        self.assertIsInstance(node.service, str)
        self.assertIsInstance(node.service_reachable_ids, (list, type(None)))
        if node.service_reachable_ids is not None:
            self.assertTrue(all(isinstance(i, int) for i in node.service_reachable_ids))
        self.assertIsInstance(node.uuid_from_service, (str, type(None)))

    def test_valid_cypher_repr(self):
        node = self.dummy_node
        cypher_for_dummy_location = self.cypher_for_dummy_location
        cypher_node_repr = (
            f"station_id: 123, "
            f'city: "Dummy City", '
            f'region: "Dummy Region", '
            f"{cypher_for_dummy_location}, "
            f"id_for_reach: 456, "
            f'node_type: "bus_station", '
            f'service: "flixbus", '
            f"service_reachable_ids: [789, 101112], "
            f'uuid_from_service: "dummy-uuid", '
            f"is_popular: False"
        )
        assert pytest.approx(str(node)) == pytest.approx(cypher_node_repr)

    def test_invalid_name_type(self):
        with self.assertRaises(ValidationError):
            BusStationNodeFactory(city=3.14)

    def test_invalid_region_type(self):
        with self.assertRaises(ValidationError):
            BusStationNodeFactory(region=3.141)

    def test_invalid_node_type_type(self):
        with self.assertRaises(ValidationError):
            BusStationNodeFactory(node_type=3.14159)


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
