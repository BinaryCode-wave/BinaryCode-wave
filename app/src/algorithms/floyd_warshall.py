import math
def floyd_warshall(G):
    n = len(G)
    dist = [[math.inf] * n for _ in range(n)]
    for u, v, weight in G.edges.data('weight'):
        dist[u][v] = weight

    for i in range(n):
        dist[i][i] = 0

    for k in range(n):
        for i in range(n):
            for j in range(n):
                dist[i][j] = min(dist[i][j], dist[i][k] + dist[k][j])

    return dist