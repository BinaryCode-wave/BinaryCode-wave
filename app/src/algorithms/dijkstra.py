import math
import heapq as hq

def dijkstra(G, s):
    n = len(G)
    visited = [False] * n
    path = [-1] * n
    cost = [math.inf] * n

    cost[s] = 0
    pqueue = [(0, s)]
    while pqueue:
        g, u = hq.heappop(pqueue)
        if not visited[u]:
            visited[u] = True
            for v in range(n):
                if G[u][v] > 0 and not visited[v]:
                    f = g + G[u][v]
                    if f < cost[v]:
                        cost[v] = f
                        path[v] = u
                        hq.heappush(pqueue, (f, v))

    return path, cost