""" Contains misc neo4j utilities """
import datetime
import itertools
from typing import Iterable

from pydantic.utils import to_camel

from neo4j_graph.settings import POPULAR_DST, POPULAR_SRC


def date_time_to_cypher_conversion(date_time_object: datetime.datetime | datetime.timedelta) -> str:
    """
    Convert date/time python object into a str cypher type, according to:
    https://neo4j.com/developer/cypher/dates-datetimes-durations/
    - datetime.datetime:
        e.g. datetime("2019-06-01T18:40:32.142+0100")
    - datetime.timedelta: e.g. duration(minutes: 3, seconds: 30)
        without seconds (it is not useful for bus trips)
    :param date_time_object: datetime or timedelta
    :return: the (str) cypher representation
    """
    if isinstance(date_time_object, datetime.datetime):
        formatted_date = date_time_object.strftime("%Y-%m-%dT%H:%M:%S.%f%z")
        # TODO [feature] manage different time zones
        return f'datetime("{formatted_date}")'
    # timedelta
    duration_str = ""

    duration_str += f"days: {date_time_object.days}, " if date_time_object.days else ""
    hours = date_time_object.seconds // 3600
    duration_str += f"hours: {hours}, " if hours else duration_str
    minutes = (date_time_object.seconds // 60) % 60
    duration_str += f"minutes: {minutes}" if hours else duration_str

    duration_str = f"duration({{ {duration_str} }})" if duration_str else "Null"

    return duration_str


def get_cypher_core_data_type(_obj: any) -> str:
    """
    Convert a python object into a str cypher type,
    according to: https://neo4j.com/docs/api/python-driver/current/api.html#core-data-types
    ready to be included into a query as follows:
    - None: 'Null'
    - bool: 'false'/'true' for False and True
    - str: add double quotes
    - iterable: (except str) applies transformations below to each element
        (array with same type of objects in cypher)
        and if its items are not primitive ones, an array of arrays will be created
    - others: their str repr
    :param _obj: (any) to be transformed
    :return: (str) with the cypher representation of the object
    """
    if _obj is None:
        return "''"
        # "Null", for avoiding cypher error when creating multiple nodes
        # TODO [improvement] fix this!
    if isinstance(_obj, bool):
        return str(_obj).lower()
    if isinstance(_obj, (datetime.datetime, datetime.timedelta)):
        return date_time_to_cypher_conversion(_obj)
    if isinstance(_obj, str):
        # Putting this block here avoid treating a str as iterable in next one
        return f'"{_obj}"'
    if isinstance(_obj, Iterable):
        # TODO [improvement] (and test) the performance of next block
        for an_item, another_item in itertools.combinations(_obj, 2):
            if not isinstance(an_item, type(another_item)):
                raise ValueError("Cypher arrays must contain the same type of objects")
        items_as_cypher = [get_cypher_core_data_type(item) for item in _obj]
        return f'[{", ".join(items_as_cypher)}]'
    if isinstance(_obj, (int, float)):
        return str(_obj)
    raise ValueError(f"No type compatible with neo4j API: {type(_obj)}")


def snake_to_upper_camel(snake_str: str) -> str:
    """
    Tt is useful for cypher queries building
    e.g. 'bus_station' -> 'BusStation'
    e.g. 'foo' -> 'Foo'
    :param snake_str: (str) any format string
    :return: (str) a camel case label (with uppercase at the beginning)
    """
    if not snake_str:
        return ""
    if "_" not in snake_str:
        return f"{snake_str[0].upper()}{snake_str[1:]}"
    return to_camel(snake_str)


# TODO [refactor] move next func to a more accurate place
def get_cities_cypher_query(region: str = "EU") -> str:
    """
    Query for look for all city_uuid for a set of cities,
    and its reachable cities uuids,
    useful for popular trips discounts scraper

    :param region: (str) The region to filter nodes by. Default is 'EU' (Europe).
    :return: (str) The cypher query ready to run.
    """

    popular_src_substring = "AND n.IsPopular" if POPULAR_SRC else ""
    popular_dst_substring = "AND m.IsPopular" if POPULAR_DST else ""

    return f"""
    MATCH (n:BusStation)
    WHERE n.Region='{region}' {popular_src_substring}
    WITH n.CityUuid AS from_city_uuid, n.ReachableIds AS reachableIds
    MATCH (m:BusStation)
    WHERE m.CityUuid <> from_city_uuid {popular_dst_substring} AND m.Id IN reachableIds
    RETURN from_city_uuid, COLLECT(DISTINCT m.CityUuid) AS to_city_uuids
    """.strip()


def get_nodes_cypher_query(region: str = "EU", properties: list[str] = None) -> str:
    """
    Generate a Cypher query to retrieve nodes based on specified properties and region.

    This function constructs a Cypher query to match nodes
    in the databasethat belong to the given region.
    It also allows for filtering the properties to be returned for each matched node.

    :param region: (str) The region to filter nodes by. Default is 'EU' (Europe).
    :param properties: (list[str]) A list of property names to be returned for each matched node.
                       If None, all properties of the matched nodes will be returned.
                       Default is None.
    :return: (str) A Cypher query to fetch nodes based on the given region and properties.
    :raises: ValueError: If 'properties' is not a list of strings or contains non-string elements.

    Example:
        get_nodes_cypher_query(region='South America', properties=['name', 'age'])
        Output: "MATCH(n) WHERE n.Region='South America' RETURN n.Name, n.Age"
    """
    # TODO [missing tests]
    if not isinstance(properties, list):
        raise ValueError(f"properties must be a list of str, not {type(properties)}")
    if not all((isinstance(prop, str) for prop in properties)):
        raise ValueError("properties must be str")

    upper_properties = [f"n.{snake_to_upper_camel(prop)}" for prop in properties]

    return_prop = ", ".join(upper_properties)
    return f"MATCH(n) WHERE n.Region='{region}' RETURN {return_prop}".strip()
