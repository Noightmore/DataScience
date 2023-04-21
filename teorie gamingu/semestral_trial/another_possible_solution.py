import heapq


class Vertex:
    def __init__(self, index):
        self.index = index
        self.min_distance_prob = float('inf')
        self.min_distance_all = float(1)
        self.previous = None

    def __lt__(self, other):
        return self.min_distance_prob/self.min_distance_all < other.min_distance_prob/other.min_distance_all


class Edge:
    def __init__(self, prob, all, start, end):
        self.prob = prob
        self.all = all
        self.start = start
        self.end = end


def dijkstra(connection_matrix, start_index):
    vertices = [Vertex(i) for i in range(len(connection_matrix))]
    vertices[start_index].min_distance_prob = 0
    vertices[start_index].min_distance_all = 1

    # Calculate d-ary heap size
    #num_edges = sum([len(row) for row in connection_matrix])
    #num_vertices = len(vertices)
    #d = math.ceil(num_edges / num_vertices)

    heap = []
    heapq.heappush(heap, vertices[start_index])

    while heap:
        current_vertex = heapq.heappop(heap)

        for neighbor_index, edge in enumerate(connection_matrix[current_vertex.index]):
            if edge is None:
                continue

            neighbor = vertices[neighbor_index]
            new_distance_prob = current_vertex.min_distance_prob + edge.prob
            new_distance_all = current_vertex.min_distance_all + edge.all

            if new_distance_prob/new_distance_all < neighbor.min_distance_prob/neighbor.min_distance_all:
                neighbor.min_distance_prob = new_distance_prob
                neighbor.min_distance_all = new_distance_all

                neighbor.previous = current_vertex.index

                # Update heap with new minimum distance
                if neighbor not in heap:
                    heapq.heappush(heap, neighbor)
                #else:
                #    heapq.heappush(heap, heap.index(neighbor))

    return vertices


def get_shortest_path(vertices, end_index):
    path = []
    current_vertex = vertices[end_index]

    while current_vertex.previous is not None:
        path.append(current_vertex.index)
        current_vertex = vertices[current_vertex.previous]

    if path:
        path.append(current_vertex.index)

    path.reverse()
    return path


if __name__ == '__main__':
    # Example usage:
    connection_matrix = [
        [None, Edge(2, 1, 0, 1), Edge(5, 1, 0, 2)], # 0
        [Edge(2, 1, 1, 0), None, Edge(3, 1, 1, 2)], # 1
        [Edge(5, 1, 2, 0), None, None] # 2
    ]
    start_index = 0
    end_index = 2

    # Calculate shortest path
    vertices = dijkstra(connection_matrix, start_index)
    shortest_path = get_shortest_path(vertices, end_index)

    # Output
    #print(len(shortest_path))
    print(*shortest_path)

