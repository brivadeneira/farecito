"""
Implements tests for Neo4j-based data models.
"""
import datetime
import unittest

import pytest
from pydantic import ValidationError

from neo4j_graph import (
    BusStationNode,
    Currency,
    Location,
    Neo4JConn,
    Node,
    NodeRelationShip,
    Price,
    UnstructuredGraph,
)
from tests.neo4j import (
    BusStationNodeFactory,
    LocationFactory,
    Neo4JConnFactory,
    NodeFactory,
    NodeRelationshipFactory,
    PriceFactory,
    UnstructuredGraphFactory,
)


class TestPrice(unittest.TestCase):
    @pytest.fixture(autouse=True)
    def __inject_fixtures(self, dummy_price):
        self.dummy_price = dummy_price

    def test_price(self):
        price = PriceFactory()
        self.assertIsInstance(price, Price)

        self.assertIsInstance(price.amount, (float, type(None)))
        self.assertIsInstance(price.currency, (Currency, type(None)))

    def test_valid_cypher_core_str(self):
        expected_cypher_core_str = '"0.0 USD"'
        assert pytest.approx(expected_cypher_core_str) == pytest.approx(str(self.dummy_price))

    def test_invalid_amount_value(self):
        with self.assertRaises(TypeError):
            PriceFactory(amount=-3.1416)

    def test_invalid_amount_type(self):
        with self.assertRaises(ValidationError):
            PriceFactory(amount="1,000")

    def test_invalid_currency_type(self):
        with self.assertRaises(ValidationError):
            PriceFactory(currency="USD")


class TestLocation(unittest.TestCase):
    """
    Test cases for Location model

    including type attr validation and cypher repr
    """

    def test_valid_location(self):
        location = LocationFactory()
        self.assertIsInstance(location.latitude, float)
        self.assertIsInstance(location.longitude, float)
        self.assertTrue(-90 <= location.latitude <= 90)
        self.assertTrue(-180 <= location.longitude <= 180)

    def test_valid_cypher_core_str(self):
        dummy_location = LocationFactory(latitude=0.0, longitude=0.0)
        expected_cypher_core_str = "point({ longitude: 0.0, latitude: 0.0 })"
        # TODO: improve strings comparison
        assert pytest.approx(expected_cypher_core_str) == pytest.approx(str(dummy_location))

    def test_invalid_latitude_value(self):
        with self.assertRaises(ValueError):
            LocationFactory(latitude=100)

    def test_invalid_longitude_value(self):
        with self.assertRaises(ValueError):
            LocationFactory(longitude=-200)

    def test_invalid_latitude_type(self):
        with self.assertRaises(ValidationError):
            LocationFactory(latitude="100")

    def test_invalid_longitude_type(self):
        with self.assertRaises(ValidationError):
            LocationFactory(longitude="-200")


class TestNode(unittest.TestCase):
    """
    Test cases for Node model

    including type attr validation and cypher repr
    """

    @pytest.fixture(autouse=True)
    def __inject_fixtures(self, dummy_node):
        self.dummy_node = dummy_node

    def test_valid_node(self):
        node = NodeFactory()
        self.assertIsInstance(node.id, int)
        self.assertIsInstance(node.node_type, (str, type(None)))
        self.assertIsInstance(node.reachable_ids, (list, type(None)))
        if node.reachable_ids is not None:
            self.assertTrue(all(isinstance(i, int) for i in node.reachable_ids))

    def test_valid_cypher_core_str(self):
        expected_cypher_core_str = 'Id: 123, NodeType: "dummy_node_type", ReachableIds: [1, 2, 3]'
        assert pytest.approx(expected_cypher_core_str) == pytest.approx(str(self.dummy_node))

    def test_invalid_int(self):
        with self.assertRaises(ValueError):
            NodeFactory(id={})

    def test_invalid_node_type(self):
        with self.assertRaises(ValueError):
            NodeFactory(node_type=3.14)

    def test_get_node_properties(self):
        expected_properties = {"Id", "NodeType", "ReachableIds"}
        self.assertTrue(expected_properties == self.dummy_node.node_properties)

    def test_get_cypher_node_properties(self):
        expected_properties = ["Id", "NodeType", "ReachableIds"]
        obtained_properties = self.dummy_node.cypher_node_properties
        assert set(expected_properties) == set(obtained_properties)

    def test_cypher_create_query(self):
        expected_create_query = (
            "CREATE ( n:DummyNodeType "
            '{ Id: 123, NodeType: "dummy_node_type", ReachableIds: [1, 2, 3] } )'
        )

        actual_create_query = self.dummy_node.cypher_create_query
        assert pytest.approx(expected_create_query) == pytest.approx(actual_create_query)


class TestBusStationNode(unittest.TestCase):
    @pytest.fixture(autouse=True)
    def __inject_fixtures(self, dummy_bus_station_node):
        self.dummy_bus_station_node = dummy_bus_station_node

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

    def test_get_node_properties(self):
        expected_properties = {
            "IsPopular",
            "Region",
            "Location",
            "ReachableIds",
            "CityUuid",
            "CityName",
            "NodeType",
            "StationUuid",
            "Service",
            "Id",
        }
        actual_node_properties = self.dummy_bus_station_node.node_properties
        self.assertTrue(expected_properties == actual_node_properties)

    def test_valid_cypher_core_str(self):
        expected_cypher_core_str = (
            'Id: 123, NodeType: "DummyNodeType", '
            'ReachableIds: [1, 2, 3], CityName: "dummy_city", '
            'CityUuid: "dummy_city_uuid", Region: "dummy_region", '
            "Location: point({ longitude: 0.0, latitude: 0.0 }), "
            'Service: "dummy_service", StationUuid: "dummy_station_uuid", '
            "IsPopular: false"
        )

        obtained_cypher_str = str(self.dummy_bus_station_node)

        assert pytest.approx(expected_cypher_core_str) == pytest.approx(obtained_cypher_str)

    def test_invalid_name_type(self):
        with self.assertRaises(ValidationError):
            BusStationNodeFactory(city_name=3.14)

    def test_invalid_region_type(self):
        with self.assertRaises(ValidationError):
            BusStationNodeFactory(region=3.141)

    def test_cypher_create_query(self):
        expected_create_query = (
            'CREATE ( n:DummyNodeType { Id: 123, NodeType: "DummyNodeType", '
            'ReachableIds: [1, 2, 3], CityName: "dummy_city", CityUuid: "dummy_city_uuid", '
            'Region: "dummy_region", Location: point({ longitude: 0.0, latitude: 0.0 }), '
            'Service: "dummy_service", StationUuid: "dummy_station_uuid", IsPopular: false } )'
        )

        actual_create_query = self.dummy_bus_station_node.cypher_create_query
        assert pytest.approx(expected_create_query) == pytest.approx(actual_create_query)


class TestNodeRelationShip(unittest.TestCase):
    @pytest.fixture(autouse=True)
    def __inject_fixtures(self, dummy_node_relationship):
        self.dummy_node_relationship = dummy_node_relationship

    def test_neo4j_relationship(self):
        relationship = NodeRelationshipFactory()
        self.assertIsInstance(relationship, NodeRelationShip)

        self.assertIsInstance(relationship.relation_type, str)
        self.assertIsInstance(relationship.travel_mode, str)
        self.assertIsInstance(relationship.schedules, (list, type(None)))
        if relationship.schedules is not None:
            self.assertTrue(all(isinstance(i, datetime.datetime) for i in relationship.schedules))
        self.assertIsInstance(relationship.average_price, Price)

    def test_valid_cypher_core_str(self):
        relationship = self.dummy_node_relationship
        expected_relationship_cypher_str = (
            # 'relation_type: "DUMMY_RELATION_TYPE", '
            'TravelMode: "bus", '
            'Schedules: [datetime("2023-01-01T00:00:00.000000")], '
            "AverageDuration: duration({ hours: 1, minutes: 12 }), "
            'AveragePrice: "0.0 USD"'
        )
        assert pytest.approx(expected_relationship_cypher_str) == pytest.approx(str(relationship))

    def test_invalid_name_type(self):
        with self.assertRaises(ValidationError):
            BusStationNodeFactory(city_name=3.14)

    def test_invalid_region_type(self):
        with self.assertRaises(ValidationError):
            BusStationNodeFactory(region=3.141)


class TestUnstructuredGraph(unittest.TestCase):
    @pytest.fixture(autouse=True)
    def __inject_fixtures(
        self, dummy_graph, dummy_node_relationship, dummy_node, dummy_bus_station_node
    ):
        self.dummy_graph = dummy_graph
        self.dummy_node_relationship = dummy_node_relationship
        self.dummy_node = dummy_node
        self.dummy_bus_station_node = dummy_bus_station_node

    def test_neo4j_unstructured_graph(self):
        graph = UnstructuredGraphFactory()
        self.assertIsInstance(graph, UnstructuredGraph)

        self.assertTrue(all(issubclass(type(node), Node) for node in graph.nodes))
        if graph.relationship:
            self.assertIsInstance(graph.relationship, NodeRelationShip)

    def test_create_nodes_query(self):
        graph = self.dummy_graph
        expected_query = (
            "FOREACH (node IN ["
            '{ Id: 1, NodeType: "dummy_node_type", ReachableIds: [2, 3] }, '
            '{ Id: 2, NodeType: "dummy_node_type", ReachableIds: [1, 3] }, '
            '{ Id: 3, NodeType: "dummy_node_type", ReachableIds: [1, 2] }'
            "] | MERGE (n: DummyNodeType "
            "{ Id: node.Id, NodeType: node.NodeType, ReachableIds: node.ReachableIds }"
            "))"
        )

        assert pytest.approx(expected_query) == pytest.approx(graph.create_nodes_query)

    def test_different_nodes_class(self):
        with self.assertRaises(ValidationError):
            UnstructuredGraphFactory(nodes={}, relationship=self.dummy_node_relationship)

    def test_invalid_nodes_properties(self):
        with self.assertRaises(ValidationError):
            UnstructuredGraphFactory(
                nodes=[self.dummy_node, self.dummy_bus_station_node],
                relationship=self.dummy_node_relationship,
            )

    def test_invalid_node_type_value(self):
        with self.assertRaises(ValidationError):
            a_node = NodeFactory(id=1, node_type="dummy_node_type")
            another_node = NodeFactory(id=2, node_type="another_dummy_node_type")

            UnstructuredGraphFactory(
                nodes=[a_node, another_node], relationship=self.dummy_node_relationship
            )


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
