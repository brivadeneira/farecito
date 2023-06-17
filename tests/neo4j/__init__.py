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

from neo4j_graph import BusStationNode, Location, Neo4JConn


class LocationFactory(Factory):
    class Meta:
        model = Location

    latitude = LazyAttribute(lambda _: random.uniform(-90, 90))
    longitude = LazyAttribute(lambda _: random.uniform(-180, 180))


class BusStationNodeFactory(Factory):
    class Meta:
        model = BusStationNode

    node_type = "bus_station"
    station_id = LazyAttribute(lambda _: random.randint(0, 100))
    city = Faker("city")
    region = Faker("country")
    location = SubFactory(LocationFactory)
    service = "flixbus"
    service_reachable_ids = List([1, 2, 3])
    id_for_reach = LazyAttribute(lambda _: random.randint(0, 100))
    uuid_from_service = Faker("uuid4")
    is_popular = False


class Neo4JConnFactory(Factory):
    class Meta:
        model = Neo4JConn

    uri = "neo4j://127.0.0.1:9000"
    # Supported URI sch: 'bolt', 'bolt+ssc', 'bolt+s', 'neo4j', 'neo4j+ssc', 'neo4j+s'
    user_name = Faker("user_name")
    password = Faker("password")
    db_name = Faker("word")
