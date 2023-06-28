"""
Implements tests for neo4j utils.
"""
import datetime
import unittest

import pytest

from neo4j_graph import format_node_type_label, object_to_cypher_repr

test_objects_to_cypher_with_ids = [
    [None, "Null", "none"],
    [True, "true", "bool_true"],
    [False, "false", "bool_false"],
    [
        datetime.datetime(2019, 6, 1, 18, 40, 32),
        'datetime("2019-06-01T18:40:32.000000")',
        "datetime",
    ],
    [
        datetime.timedelta(hours=1, minutes=20, seconds=5),
        "{ hours: 1, minutes: 20 }",
        "datetime_with_hours_and_min",
    ],
    [datetime.timedelta(seconds=3662), "{ hours: 1, minutes: 1 }", "datetime_just_with_seconds"],
    ["Turanga Leela", '"Turanga Leela"', "str"],
    [[1, 2, 3], str([1, 2, 3]), "list_of_ints"],
    [["1", "2", "3"], '["1", "2", "3"]', "list_of_strs"],
    [3.1416, str(3.1416), "float"],
]

test_objects_to_cypher = [(group[0], group[1]) for group in test_objects_to_cypher_with_ids]
test_objects_to_cypher_ids = [group[-1] for group in test_objects_to_cypher_with_ids]


@pytest.mark.parametrize("_obj,cypher_repr", test_objects_to_cypher, ids=test_objects_to_cypher_ids)
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


labels_for_parametrize = [
    ("FooLabel", "FooLabel"),
    ("spam_label", "SpamLabel"),
    ("foo", "Foo"),
    (None, ""),
]

labels_for_parametrize_ids = ["already_camel_case", "snake_case", "single_lower_word", "no_label"]


@pytest.mark.parametrize(
    "given_label,expected_label", labels_for_parametrize, ids=labels_for_parametrize_ids
)
def test_format_node_type_label(given_label, expected_label):
    assert expected_label == format_node_type_label(given_label)


if __name__ == "__main__":
    unittest.main()
