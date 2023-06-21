"""
Implements tests for neo4j utils.
"""
import datetime
import unittest

import pytest

from neo4j_graph import object_to_cypher_repr

test_objects_to_cypher = [
    (None, "Null"),
    (True, "true"),
    (False, "false"),
    (datetime.datetime(2019, 6, 1, 18, 40, 32), 'datetime("2019-06-01T18:40:32.000000")'),
    (datetime.timedelta(hours=1, minutes=20, seconds=5), "{ hours: 1, minutes: 20 }"),
    (datetime.timedelta(seconds=3662), "{ hours: 1, minutes: 1 }"),
    ("Turanga Leela", '"Turanga Leela"'),
    ([1, 2, 3], str([1, 2, 3])),
    (["1", "2", "3"], '["1", "2", "3"]'),
    (3.1416, str(3.1416)),
]


@pytest.mark.parametrize("_obj,cypher_repr", test_objects_to_cypher)
def test_object_to_cypher_repr(_obj, cypher_repr):
    assert object_to_cypher_repr(_obj) == cypher_repr


@pytest.mark.parametrize(
    "_obj",
    [
        type(1),
        # TODO define other non standard or dataclass types
    ],
)
def test_invalid_name_type(_obj):
    with pytest.raises(ValueError):
        object_to_cypher_repr(_obj)


if __name__ == "__main__":
    unittest.main()
