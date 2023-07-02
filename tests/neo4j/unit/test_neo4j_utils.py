"""
Implements tests for neo4j utils.
"""
import datetime
import unittest

import pytest

from neo4j_graph import get_cypher_core_data_type, snake_to_upper_camel

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
        "duration({ hours: 1, minutes: 20 })",
        "datetime_with_hours_and_min",
    ],
    [
        datetime.timedelta(seconds=3662),
        "duration({ hours: 1, minutes: 1 })",
        "datetime_just_with_seconds",
    ],
    ["Turanga Leela", '"Turanga Leela"', "str"],
    [[1, 2, 3], str([1, 2, 3]), "list_of_ints"],
    [["1", "2", "3"], '["1", "2", "3"]', "list_of_strs"],
    [3.1416, str(3.1416), "float"],
]

test_objects_to_cypher = [(group[0], group[1]) for group in test_objects_to_cypher_with_ids]
test_objects_to_cypher_ids = [group[-1] for group in test_objects_to_cypher_with_ids]


@pytest.mark.parametrize(
    "_obj,expected_cypher_core_data", test_objects_to_cypher, ids=test_objects_to_cypher_ids
)
def test_object_to_cypher_repr(_obj, expected_cypher_core_data):
    assert pytest.approx(get_cypher_core_data_type(_obj)) == pytest.approx(
        expected_cypher_core_data
    )


@pytest.mark.parametrize(
    "_obj", [type(1), [1, "2", 3.0]], ids=["wrong_type", "array_of_different_types"]
)
def test_invalid_name_type(_obj):
    with pytest.raises(ValueError):
        get_cypher_core_data_type(_obj)


snake_str_for_parametrize = [
    ("FooLabel", "FooLabel"),
    ("spam_label", "SpamLabel"),
    ("foo", "Foo"),
    (None, ""),
]

snake_str_for_parametrize_ids = ["already_camel_case", "snake_case", "single_lower_word", "none"]


@pytest.mark.parametrize(
    "snake_str,expected_camel_str", snake_str_for_parametrize, ids=snake_str_for_parametrize_ids
)
def test_format_node_type_label(snake_str, expected_camel_str):
    assert pytest.approx(snake_to_upper_camel(snake_str)) == pytest.approx(expected_camel_str)


if __name__ == "__main__":
    unittest.main()
