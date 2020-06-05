import heapq
from copy import deepcopy


__all__ = ['floyd_warshall', 'bellman_ford', 'dijkstra', 'johnson']


def floyd_warshall(network):
    length = network.length
    distance_matrix = [[float("inf") for i in range(length)]
                       for j in range(length)]

    for node_idx, edge_list in enumerate(network.successor_edges):
        for successor_node_idx, weight in edge_list:
            distance_matrix[node_idx][successor_node_idx] = weight
        distance_matrix[node_idx][node_idx] = 0

    for i in range(length):
        for j in range(length):
            for k in range(length):
                distance_matrix[i][j] = min(
                    distance_matrix[i][j], distance_matrix[i][k] + distance_matrix[k][j])

    for node_idx in range(length):
        if distance_matrix[node_idx][node_idx] < 0:
            # raise Exception or return False?
            # raise Exception("Negative cycle found")
            return False

    network.distance_matrix = distance_matrix
    # should we return the distance matrix also?
    return distance_matrix


def bellman_ford(network, src=-1):
    if src in network.names_dict.values():
        return _bellman_ford(network, src)
    else:
        return _bellman_ford_new(network)


def _bellman_ford(network, src):
    # assuming src is always an idx
    length = network.length
    distances = [float("inf") for _ in range(length)]
    distances[src] = 0

    for _ in range(length - 1):
        for node_idx in range(length):
            for successor_node_idx, weight in network.successor_edges[node_idx]:
                distances[successor_node_idx] = min(
                    distances[successor_node_idx], distances[node_idx] + weight)

    for node_idx in range(length):
        for successor_node_idx, weight in network.successor_edges[node_idx]:
            if distances[successor_node_idx] > distances[node_idx] + weight:
                # raise Exception("are we supposed to throw an error here?")
                return False

    network.distances = distances
    # should we return the distances also?
    return True


def _bellman_ford_new(network):
    length = network.length
    distances = [float("inf") for _ in range(length)]
    successor_edges = deepcopy(network.successor_edges)

    distances.append(0)
    successor_edges.append([(i, 0) for i in range(length)])

    for _ in range(length):
        for node_idx in range(length + 1):
            for successor_node_idx, weight in successor_edges[node_idx]:
                distances[successor_node_idx] = min(
                    distances[successor_node_idx], distances[node_idx] + weight)

    for node_idx in range(length + 1):
        for successor_node_idx, weight in successor_edges[node_idx]:
            if distances[successor_node_idx] > distances[node_idx] + weight:
                # raise Exception("are we supposed to throw an error here?")
                return False

    network.distances = distances[:-1]
    # should we return the distances also?
    return True


def dijkstra(network, src):
    """
    Calculates the shortest path using Dijkstra's algorithm
    Parameters
    ----------
    src : str, int
        The node dijkstra's algorithm uses to find the shortest path from.
        You could provide the index of the node or the name of the node and
        the algorithm should recognize which one you have entered
    Returns
    -------
    distances : List[int]
        A list representing the shortest distances to each node from the
        src node
    """
    distances = [float("inf") for i in range(network.length)]

    if type(src) == str:
        src_idx = network.names_dict[src]
    else:
        src_idx = src

    distances[src_idx] = 0
    min_heap = []
    heapq.heappush(min_heap, (distances[src_idx], src_idx))

    while min_heap:
        _, u_idx = heapq.heappop(min_heap)
        for successor_idx, weight in network.successor_edges[u_idx]:
            if (distances[u_idx] + weight < distances[successor_idx]):
                distances[successor_idx] = distances[u_idx] + weight
                heapq.heappush(
                    min_heap, (distances[successor_idx], successor_idx))

    network.distances = distances

    return distances


def johnson(network):
    """
    Calculates the shortest path using Johnson's algorithm
    Parameters
    ----------
    src : str, int
        An arbitrary node that does not exist in the STN.
    Returns
    -------
    distance_matrix : List[List[int]]
        A 2-D list representing the shortest distances between all the nodes
    """
    distance_matrix = [[] for x in range(network.length)]

    bellman_ford(network)
    successor_edges = deepcopy(network.successor_edges)
    for node_idx, list_of_edges in enumerate(successor_edges):
        for tuple_idx, (successor_idx, weight) in enumerate(list_of_edges):
            successor_edges[node_idx][tuple_idx] = (
                successor_idx, weight + network.distances[node_idx] - network.distances[successor_idx])

    for node_idx in range(network.length):
        distance_matrix[node_idx] = dijkstra(network, node_idx)

    network.distance_matrix = distance_matrix
    return distance_matrix
