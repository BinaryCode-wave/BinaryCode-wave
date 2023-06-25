import networkx as nx
def kruskal(G):
    mst = nx.Graph()
    edges = list(G.edges(data='weight'))
    edges.sort(key=lambda x: x[2])  # Ordenar aristas por peso
    uf = nx.utils.UnionFind()
    for u, v, weight in edges:
        if uf[u] != uf[v]:
            mst.add_edge(u, v, weight=weight)
            uf.union(u, v)
    return mst