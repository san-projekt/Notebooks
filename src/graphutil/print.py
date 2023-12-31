def print_edge_attribute_desc(G, attribute="weight", threshold=None, limit=-1):
    edges = list(G.edges(data=attribute))
    if threshold is not None:
        edges = [(s, t, a) for (s, t, a) in edges if a >= threshold]
    edges.sort(key=lambda x: x[2], reverse=True)
    to = len(edges) if limit == -1 else limit
    print(f"Edges descending order according {attribute} attribute (limit: {limit}):")
    print(*edges[:to], sep="\n")


def print_edges_with_attributes(G, limit=-1):
    to = len(G.edges) if limit == -1 else limit
    print(*list((G.edges(data=True)))[:to], sep='\n')


def print_network_information(G):
    print(f"Information for given Graph with name '{G.name}':")
    print(f"\tGraph is directed: {G.is_directed()}")
    print(f"\tNumber of nodes: {G.number_of_nodes()}")
    print(f"\tNumber of edges: {G.number_of_edges()}")
