"""
Implements tests for builder graph code
"""
import unittest

import pytest

from neo4j_graph.graph_builder import build_create_multiple_nodes_query


@pytest.mark.parametrize(
    "nodes,label,expected_query",
    [
        (["dummy_node"], None, "CREATE ( n:BusStation { cypher_for_dummy_node } )"),
        (["dummy_node"], "DummyNode", "CREATE ( n:DummyNode { cypher_for_dummy_node } )"),
        (
            ["dummy_node", "dummy_node"],
            None,
            "FOREACH (node IN [{ cypher_for_dummy_node }, { cypher_for_dummy_node }] "
            "| MERGE (n: BusStation { cypher_for_dummy_node_properties }))",
        ),
        (
            ["dummy_node", "dummy_node"],
            "DummyNode",
            "FOREACH (node IN [{ cypher_for_dummy_node }, { cypher_for_dummy_node }] "
            "| MERGE (n: DummyNode { cypher_for_dummy_node_properties }))",
        ),
    ],
    ids=[
        "single_node_without_label",
        "single_node_with_label",
        "multiple_nodes_without_label",
        "multiple_nodes_label",
    ],
)
def test_build_create_multiple_nodes_query(nodes, label, expected_query, request):
    cypher_for_dummy_node = request.getfixturevalue("cypher_for_dummy_node")
    cypher_for_dummy_node_properties = request.getfixturevalue("cypher_for_dummy_node_properties")

    nodes = [request.getfixturevalue(node) for node in nodes]

    expected_query = expected_query.replace(
        "cypher_for_dummy_node_properties", cypher_for_dummy_node_properties
    )
    expected_query = expected_query.replace("cypher_for_dummy_node", cypher_for_dummy_node)
    assert pytest.approx(expected_query) == pytest.approx(
        build_create_multiple_nodes_query(nodes, label)
    )


@pytest.mark.parametrize(
    "nodes,label",
    [
        (["dummy_node", "dummy_bus_station_node"], None),
        (["dummy_bus_station_node", "dummy_node"], "DummyNode"),
    ],
    ids=[
        "different_nodes_without_label",
        "different_nodes_with_label",
    ],
)
def test_build_create_multiple_wrong_nodes_query(nodes, label, request):
    nodes = [request.getfixturevalue(node) for node in nodes]
    with pytest.raises(ValueError):
        build_create_multiple_nodes_query(nodes, label)


if __name__ == "__main__":
    unittest.main()
