import sys


def read_input():
    # read the first line containing the number of vertices and edges
    n, m = map(int, sys.stdin.readline().strip().split())

    # create an empty hashtable to store the edges
    edges = {}

    # read the remaining lines containing the edge descriptions
    for i in range(m):
        u, v, w = map(float, sys.stdin.readline().strip().split())
        w = 1000000 - w * 1000000
        edges[(int(u), int(v))] = w
        edges[(int(v), int(u))] = w  # assuming graph is non-oriented

    # print the hashtable
    # print(edges)


if __name__ == "__main__":
    read_input()
