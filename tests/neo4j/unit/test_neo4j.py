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


class TestCompanyInfo(unittest.TestCase):
    @pytest.fixture(autouse=True)
    def __inject_fixtures(self, dummy_company_info, cypher_for_dummy_company_info):
        self.dummy_company_info = dummy_company_info
        self.cypher_for_dummy_company_info = cypher_for_dummy_company_info

    def test_company_info(self):
        company_info = CompanyInfoFactory()
        self.assertIsInstance(company_info, CompanyInfo)

        self.assertIsInstance(company_info.company_name, str)
        self.assertIsInstance(company_info.reachable_id_name, str)
        self.assertIsInstance(company_info.reachable_ids, list)
        self.assertIsInstance(company_info.reachable_ids[0], int)
        self.assertIsInstance(company_info.id_from_company, (type(None), int))
        self.assertIsInstance(company_info.uuid_from_company, (type(None), str))

    def test_valid_cypher_repr(self):
        company_info = self.dummy_company_info
        cypher_company_info_repr = self.cypher_for_dummy_company_info

        assert pytest.approx(str(company_info)) == pytest.approx(cypher_company_info_repr)

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
    @pytest.fixture(autouse=True)
    def __inject_fixtures(
        self, dummy_node, cypher_for_dummy_location, cypher_for_dummy_company_info
    ):
        self.dummy_node = dummy_node
        self.cypher_for_dummy_location = cypher_for_dummy_location
        self.cypher_for_dummy_company_info = cypher_for_dummy_company_info

    def test_neo4j_node(self):
        node = Neo4JNodeFactory()
        self.assertIsInstance(node, Neo4JNode)

        self.assertIsInstance(node.name, str)
        self.assertIsInstance(node.region, str)
        self.assertIsInstance(node.location, Location)
        self.assertIsInstance(node.node_type, str)
        self.assertIsInstance(node.companies_info, list)
        self.assertIsInstance(node.companies_info[0], CompanyInfo)
        self.assertIsInstance(node.is_popular, bool)

    def test_valid_cypher_repr(self):
        node = self.dummy_node

        cypher_node_repr = (
            f'name: "name", region: "region", '
            f"{self.cypher_for_dummy_location}, "
            f"companies_info: [{self.cypher_for_dummy_company_info}], "
            f'node_type: "node_type", is_popular: False'
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
