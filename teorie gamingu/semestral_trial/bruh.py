import sys
from heapq import heappush, heappop

# read the graph data from stdin as before
n, m = map(int, sys.stdin.readline().strip().split())
edges = {}
for i in range(m):
    u, v, w = map(float, sys.stdin.readline().strip().split())
    #w = 1000000 - w * 1000000
    w = 1 - w
    edges[(int(u), int(v))] = w
    edges[(int(v), int(u))] = w


# define a helper function to find the shortest path using Dijkstra's algorithm
def shortest_path(start, end):
    dist = {v: float('inf') for v in range(n)}
    dist[start] = 0
    prev = {}
    heap = [(0, start)]
    while heap:
        d, u = heappop(heap)
        if u == end:
            path = []
            while u in prev:
                path.append(u)
                u = prev[u]
            path.append(start)
            path.reverse()
            return path
        for v in range(n):
            if (u, v) in edges:
                w = edges[(u, v)]
                if dist[u] + w < dist[v]:
                    dist[v] = dist[u] + w
                    prev[v] = u
                    heappush(heap, (dist[v], v))
    return [start]


def solve():
    # read the queries and find the shortest path for each vertex duo
    q = int(sys.stdin.readline().strip())
    print("")
    for i in range(q):
        start, end = map(int, sys.stdin.readline().strip().split())
        path = shortest_path(start, end)
        if len(path) == 1:
            print(start)
        else:
            dist = sum(edges[(path[j], path[j+1])] for j in range(len(path)-1))
            #dist = dist / (len(path)-1) / 1000000
            print(" ".join(str(v) for v in path))


if __name__ == "__main__":
    solve()
