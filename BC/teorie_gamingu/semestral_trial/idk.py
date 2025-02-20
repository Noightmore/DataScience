import sys
import heapq


def dijkstra_shortest_path(graph, start_node, end_node):
    # Initialize distance and previous node dictionaries
    dist = [(float('inf'), 1) for _ in range(len(graph))]
    dist[start_node] = (0, 1)
    prev = {}

    # Initialize heap with start node
    heap = [(0, start_node)]

    while heap:
        # Pop node with smallest distance
        curr_dist, curr_node = heapq.heappop(heap)

        # Check if current distance is outdated
        if curr_node == end_node:
            # End node found, return shortest path
            path = []
            while curr_node != start_node:
                path.append(curr_node)
                curr_node, _ = prev[curr_node]
            path.append(start_node)
            return list(reversed(path)), curr_dist / dist[end_node][1]

        if curr_dist > dist[curr_node][0] / dist[curr_node][1]:
            continue

        # Update distances for neighbors
        for neighbor, weight in range(len(graph[curr_node])):
            value, divisor = weight
            new_dist = (curr_dist + value, dist[curr_node][1] * divisor)
            if new_dist < dist[neighbor]:
                dist[neighbor] = new_dist
                prev[neighbor] = (curr_node, weight)
                heapq.heappush(heap, (new_dist[0] / new_dist[1], neighbor))

    # End node not found, return None
    return None


def read_input():
    # read the first line containing the number of vertices and edges
    n, m = map(int, input().strip().split())

    # create an empty dictionary to store the edges
    graph = {i: {} for i in range(n)}

    # read the remaining lines containing the edge descriptions
    for i in range(m):
        u, v, value = map(float, input().strip().split())
        if v not in graph[u]:
            graph[u][v] = (value, 1000000)
        if u not in graph[v]:
            graph[v][u] = (value, 1000000)

    return n, m, graph


    # print the hashtable
    # print(edges)


def main():
    # read the input graph
    graph = read_input()

    # read the starting and ending vertices for each query
    queries = []

    request_count = int(sys.stdin.readline().strip())
    for line in range(request_count):
        u, v = map(int, sys.stdin.readline().split())
        queries.append((u, v))

    # Compute shortest path for each query
    for u, v in queries:
        shortest_path = dijkstra_shortest_path(graph, u, v)
        if shortest_path is None:
            print(u)
        else:
            path, distance = shortest_path
            print(' '.join(str(node) for node in path) + ' ' + str(distance))


if __name__ == '__main__':
    main()

