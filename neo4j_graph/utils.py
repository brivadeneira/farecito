""" Contains misc neo4j utilities """
import datetime
import itertools
from typing import Iterable

from pydantic.utils import to_camel


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
        # TODO manage different time zones
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
        return "Null"
    if isinstance(_obj, bool):
        return str(_obj).lower()
    if isinstance(_obj, (datetime.datetime, datetime.timedelta)):
        return date_time_to_cypher_conversion(_obj)
    if isinstance(_obj, str):
        # Putting this block here avoid treating a str as iterable in next one
        return f'"{_obj}"'
    if isinstance(_obj, Iterable):
        # TODO test/improve the performance of next block
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


# TODO move next func to a more accurate place
def get_popular_nodes_cypher_query() -> str:
    """

    :return:
    """
