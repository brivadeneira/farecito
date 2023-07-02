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
import datetime
import random

import pytz
from factory import Factory, Faker, LazyAttribute, List, SubFactory
from factory.fuzzy import FuzzyDate, FuzzyDateTime

from neo4j_graph import BusStationNode, Currency, Location, Neo4JConn, Node, NodeRelationShip, Price


class LocationFactory(Factory):
    class Meta:
        model = Location

    latitude = LazyAttribute(lambda _: random.uniform(-90, 90))
    longitude = LazyAttribute(lambda _: random.uniform(-180, 180))


class NodeFactory(Factory):
    class Meta:
        model = Node

    id = LazyAttribute(lambda _: random.randint(0, 100))
    node_type = "node"
    reachable_ids = List([1, 2, 3])


class BusStationNodeFactory(Factory):
    class Meta:
        model = BusStationNode

    id = LazyAttribute(lambda _: random.randint(0, 100))
    # node_type = "BusStation"
    city_name = Faker("city")
    city_uuid = Faker("uuid4")
    region = Faker("country")
    location = SubFactory(LocationFactory)
    station_uuid = Faker("uuid4")
    # is_popular = False


def random_datetimes(cant: int = None):
    days = random.randint(0, 100)

    start_date = datetime.datetime.now()
    end_date = start_date + datetime.timedelta(days=days)
    start_date, end_date = pytz.utc.localize(start_date), pytz.utc.localize(end_date)

    fdt = FuzzyDateTime(start_date, end_date)
    computed_attr = cant if cant else random.randint(0, 9)
    return fdt.evaluate(computed_attr, None, None)


class PriceFactory(Factory):
    class Meta:
        model = Price

    amount = LazyAttribute(lambda _: round(random.random(), 2) * 100)
    currency = Currency.USD


class NodeRelationshipFactory(Factory):
    class Meta:
        model = NodeRelationShip

    # relation_name = "CAN_TRANSFER_TO"
    # service = "flixbus"
    schedules = List([random_datetimes() for _ in range(1, 3)])
    average_price = SubFactory(PriceFactory)


class Neo4JConnFactory(Factory):
    class Meta:
        model = Neo4JConn

    uri = "neo4j://127.0.0.1:9000"
    # Supported URI sch: 'bolt', 'bolt+ssc', 'bolt+s', 'neo4j', 'neo4j+ssc', 'neo4j+s'
    user_name = Faker("user_name")
    password = Faker("password")
    db_name = Faker("word")
