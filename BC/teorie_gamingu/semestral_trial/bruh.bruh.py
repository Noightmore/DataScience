import sys
from heapq import heappush, heappop


def read_input() -> tuple:
    # read the first line containing the number of vertices and edges
    n, m = map(int, sys.stdin.readline().strip().split())

    # create an empty hashtable to store the edges
    edges = {}

    # read the remaining lines containing the edge descriptions
    for i in range(m):
        u, v, w = map(float, sys.stdin.readline().strip().split())
        w = 1000000 - w * 1000000
        edges[(int(u), int(v))] = edges[(int(v), int(u))] = (w, 1000000)

    return n, m, edges


def get_shortest_probability_path(edge_count: int, starting_vertex: int, ending_vertex: int, edges: dict) -> list:
    dist = {v: float('inf') for v in range(edge_count)}
    dist[starting_vertex] = 0
    prev = {}
    heap = [(0, starting_vertex)]

    while heap:
        d, u = heappop(heap)
        if u == ending_vertex:
            path = []
            while u in prev:
                path.append(u)
                u = prev[u]
            path.append(starting_vertex)
            path.reverse()
            return path
        for v in range(edge_count):
            if (u, v) in edges:
                w = edges[(u, v)]
                if dist[u] + w < dist[v]:
                    dist[v] = dist[u] + w
                    prev[v] = u
                    heappush(heap, (dist[v], v))


if __name__ == "__main__":
    _n, _m, _edges = read_input()
    print("")
    print(_edges)
