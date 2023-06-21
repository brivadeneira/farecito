""" Contains misc neo4j utilities """
import datetime
from typing import Iterable


def date_time_to_cypher_conversion(date_time_object: datetime.datetime | datetime.timedelta) -> str:
    """
    Convert date/time python object into a str cypher type, according to:
    https://neo4j.com/developer/cypher/dates-datetimes-durations/
    - datetime.datetime:
        e.g. datetime("2019-06-01T18:40:32.142+0100")
    - datetime.timedelta: e.g. readingTime: {minutes: 3, seconds: 30}
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

    duration_str = f"{{ {duration_str} }}" if duration_str else "Null"

    return duration_str


def object_to_cypher_repr(_obj: any) -> str:
    """
    Convert a python object into a str cypher type,
    according to: https://neo4j.com/docs/api/python-driver/current/api.html#core-data-types
    ready to be included into a query as follows:
    - None: 'Null'
    - bool: 'false'/'true' for False and True
    - str: add double quotes
    - iterable: (except str) applies transformations below to each element
        (array with same type of objects in cypher)
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
        # TODO raise error for different types
        return f'[{", ".join(object_to_cypher_repr(item) for item in _obj)}]'
    if isinstance(_obj, (int, float)):
        return str(_obj)
    raise ValueError(f"No type compatible with neo4j API: {type(_obj)}")
