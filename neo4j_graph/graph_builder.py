"""
Implements main code for creating a neo4j graph
"""

import itertools

from neo4j_graph import Node, format_node_type_label


def build_create_multiple_nodes_query(nodes_to_create: list[Node], label: str = None) -> str:
    """
    Builds the cypher query for create multiple nodes at once,
    ready for run.
    Nodes must have the same properties and 'node_type' attribute
    :param nodes_to_create: (list) of nodes to be created
    :param label: (str) if not given 'node_type' attribute will be use
    :return: (str) query ready to run.
    """
    label = nodes_to_create[0].node_type if not label else label

    if len(nodes_to_create) == 1:
        [node] = nodes_to_create
        return node.build_create_cypher_query(label)

    # check for all nodes properties that must be the same
    for a_node, another_node in itertools.combinations(nodes_to_create, 2):
        if not a_node.node_properties == another_node.node_properties:
            raise ValueError("Nodes must have the same properties")

    cypher_node_repr = [str(node) for node in nodes_to_create]
    cypher_node_properties = nodes_to_create[0].cypher_node_properties

    return (
        f"FOREACH (node IN [{{ {' }, { '.join(cypher_node_repr)} }}] "
        f"| MERGE (n: {format_node_type_label(label)} {{ {cypher_node_properties} }}))".strip()
    )
