"""
This module provides factories for generating fake data objects
used in Neo4J graph database operations.

The factories defined in this module use the 'factory' library to create instances of data models
used in the Neo4J graph database. The factories make use of the 'Faker' class to generate realistic
fake data for attributes of the models.

Classes:
- CompanyInfoFactory: Factory for generating fake CompanyInfo instances.
- LocationFactory: Factory for generating fake Location instances.
- Neo4JNodeFactory: Factory for generating fake Neo4JNode instances.
- Neo4JConnFactory: Factory for generating fake Neo4JConn instances.

Note: The factories rely on the 'factory' library
and the 'Faker' class from the 'factory.Faker' module.
Make sure to install the required dependencies before using the factories.
"""
import random

from factory import Factory, Faker, LazyAttribute, List, SubFactory

from neo4j_graph import CompanyInfo, Location, Neo4JConn, Neo4JNode


class LocationFactory(Factory):
    class Meta:
        model = Location

    latitude = LazyAttribute(lambda _: random.uniform(-90, 90))
    longitude = LazyAttribute(lambda _: random.uniform(-180, 180))


class CompanyInfoFactory(Factory):
    class Meta:
        model = CompanyInfo

    reachable_ids = List([1, 2, 3])
    id_from_company = LazyAttribute(lambda _: random.randint(0, 100))
    uuid_from_company = Faker("uuid4")


class Neo4JNodeFactory(Factory):
    class Meta:
        model = Neo4JNode

    name = Faker("city")
    region = Faker("city")
    location = SubFactory(LocationFactory)
    node_type = "city"
    companies_info = List([SubFactory(CompanyInfoFactory)])
    is_popular = False
    reachable_ids = List([1, 2, 3])


class Neo4JConnFactory(Factory):
    class Meta:
        model = Neo4JConn

    uri = "neo4j://127.0.0.1:9000"
    # Supported URI sch: 'bolt', 'bolt+ssc', 'bolt+s', 'neo4j', 'neo4j+ssc', 'neo4j+s'
    user_name = Faker("user_name")
    password = Faker("password")
    db_name = Faker("word")
