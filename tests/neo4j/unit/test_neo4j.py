"""
Implements tests for Neo4j-based data models.
"""
import unittest

import pytest
from pydantic import ValidationError

from neo4j_graph import CompanyInfo, Location, Neo4JConn, Neo4JNode
from tests.neo4j import CompanyInfoFactory, LocationFactory, Neo4JConnFactory, Neo4JNodeFactory


class LocationTestCase(unittest.TestCase):
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

    def test_valid_cypher_repr(self):
        location = LocationFactory()
        cypher_point_repr = (
            f"location: point({{ longitude: {location.longitude}, "
            f"latitude: {location.longitude} }})"
        )

        assert pytest.approx(str(location)) == cypher_point_repr

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


class TestCompanyInfo(unittest.TestCase):
    def test_company_info(self):
        company_info = CompanyInfoFactory()
        self.assertIsInstance(company_info, CompanyInfo)

        self.assertIsInstance(company_info.company_name, str)
        self.assertIsInstance(company_info.id_from_company, (type(None), int))
        self.assertIsInstance(company_info.uuid_from_company, (type(None), str))

    def test_valid_cypher_repr(self):
        company_info = CompanyInfoFactory()

        cypher_repr = (
            f'{{ company_name: "{company_info.company_name}", '
            f"id_from_company: {company_info.id_from_company}, "
            f'uuid_from_company: "{company_info.uuid_from_company}" }}'
        )

        assert pytest.approx(str(company_info)) == cypher_repr

    def test_invalid_company_name_type(self):
        with self.assertRaises(ValidationError):
            CompanyInfo(company_name=3.14)

    def test_invalid_id_from_company(self):
        with self.assertRaises(ValidationError):
            CompanyInfo(id_from_company="3.141")

    def test_invalid_uuid_from_company(self):
        with self.assertRaises(ValidationError):
            CompanyInfo(uuid_from_company=3.14159)


class TestNeo4JNode(unittest.TestCase):
    def test_neo4j_node(self):
        node = Neo4JNodeFactory()
        self.assertIsInstance(node, Neo4JNode)

        self.assertIsInstance(node.name, str)
        self.assertIsInstance(node.region, str)
        self.assertIsInstance(node.location, Location)
        self.assertIsInstance(node.node_type, str)
        self.assertIsInstance(node.company_info, CompanyInfo)
        self.assertIsInstance(node.company_info.company_name, str)
        self.assertIsInstance(node.company_info.id_from_company, (type(None), int))
        self.assertIsInstance(node.company_info.uuid_from_company, (type(None), str))
        self.assertIsInstance(node.reachable_ids, (type(None), list))
        self.assertIsInstance(node.is_popular, bool)

    def test_valid_cypher_repr(self):
        node = Neo4JNodeFactory()

        cypher_node_repr = (
            f'{{ name: "{node.name}", region: "{node.region}", {str(node.location)}, '
            f"company_info: {str(node.company_info)}, "
            f'node_type: "{node.node_type}", is_popular: {node.is_popular}, '
            f"reachable_ids: {node.reachable_ids} }}"
        )
        assert pytest.approx(str(node)) == pytest.approx(cypher_node_repr)

    def test_invalid_name_type(self):
        with self.assertRaises(ValidationError):
            Neo4JNodeFactory(name=3.14)

    def test_invalid_region_type(self):
        with self.assertRaises(ValidationError):
            Neo4JNodeFactory(region=3.141)

    def test_invalid_node_type_type(self):
        with self.assertRaises(ValidationError):
            Neo4JNodeFactory(node_type=3.14159)


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
