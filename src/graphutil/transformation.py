import networkx as nx

"""
Creates a global view graph view by merging all nodes with the same attribute value in order to create a nice overall 
view.

Simple version: It only creates a weighted graph with nodes and edges of the given attribute. An extended version would 
also aggregate other nodes attributes. It does not consider edge direction which could be improved later.
"""


def global_view(G: nx.Graph, attribute_to_collapse: str, ignore_edge_weight=False) -> nx.Graph:
    if attribute_to_collapse is None:
        raise ValueError("attribute to collapse must be given")
    collapsed = dict()

    for edge in G.edges(data=True):
        source = edge[0]
        target = edge[1]
        weight = edge[2].get("weight", 1)

        source_node_attribute = G.nodes().get(source).get(attribute_to_collapse)
        target_node_attribute = G.nodes().get(target).get(attribute_to_collapse)

        if source_node_attribute is None or target_node_attribute is None:
            print("Edge will be ignored: At least one of the nodes does not have the collapse attribute: " + str((source, target)))
            continue

        source = source_node_attribute
        target = target_node_attribute

        if source > target:
            source, target = target, source

        existing_weight:int = collapsed.get((source, target), 0)
        updated_weight = existing_weight
        if (ignore_edge_weight):
            updated_weight += 1
        else:
            updated_weight += weight

        collapsed[(source, target)] = updated_weight

    print(collapsed)
    collapsed_graph = nx.Graph()
    for (e, w) in collapsed.items():
        collapsed_graph.add_edge(e[0], e[1], weight=w)

    return collapsed_graph



if __name__ == '__main__':
    graph = nx.read_graphml("kooperationshuereden wo isolates.graphml")
    print(nx.info(graph))

    collapsed = global_view(graph, attribute_to_collapse="sektor")
    print(nx.info(collapsed))
    nx.write_gexf(collapsed, "kh_collapsed_by_sector.gexf")

    """
    G = nx.DiGraph()
    G.add_node("1", sector="wirtschaft", gender="male")
    G.add_node("2", sector="bildung", gender="male")
    G.add_node("3", sector="kultur", gender="male")
    G.add_node("4", sector="verwaltung", gender="male")

    G.add_node("5", sector="wirtschaft", gender="male")
    G.add_node("6", sector="bildung", gender="male")

    G.add_edge("1", "2", weight=3)
    G.add_edge("1", "6", weight=2)
    G.add_edge("5", "2", weight=4)

    new_g = global_view(G, "sector")
    print("----------- new graph -------------")
    print(nx.info(new_g))
    print(new_g.nodes(data=True))
    print(new_g.edges(data=True))
    """
