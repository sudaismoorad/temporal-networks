import heapq
from copy import deepcopy


class Dijkstra:

    @staticmethod
    def dijkstra(network, src, succ_direction=True, potential_function=False):

        if type(src) == str:
            src_idx = network.names_dict[src]
        else:
            src_idx = src

        distances = [float("inf") for i in range(network.length)]
        distances[src_idx] = 0

        if not potential_function:
            if succ_direction:
                return Dijkstra._dijkstra(network, src_idx, distances)
            else:
                return Dijkstra._pred_dijkstra(network, src_idx, distances)
        else:
            return Dijkstra._johnson_dijkstra(network, src_idx, distances, potential_function)

    @staticmethod
    def _dijkstra(network, src_idx, distances):
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
        min_heap = []
        heapq.heappush(min_heap, (distances[src_idx], src_idx))

        while min_heap:
            _, u_idx = heapq.heappop(min_heap)
            for successor_idx, weight in network.successor_edges[u_idx].items():
                if (distances[u_idx] + weight < distances[successor_idx]):
                    distances[successor_idx] = distances[u_idx] + weight
                    heapq.heappush(
                        min_heap, (distances[successor_idx], successor_idx))

        return distances

    @staticmethod
    def _pred_dijkstra(network, src_idx, distances):

        predecessor_edges = [{} for i in range(network.length)]
        previous_visited = [False for i in range(network.length)]

        min_heap = []

        for i in range(network.length):
            if i == src_idx:
                continue
            heapq.heappush(min_heap, (distances[i], i))

        for node_idx, successor_idx, weight in enumerate(network.successor_edges.items()):
            predecessor_edges[successor_idx][node_idx] = weight

        while min_heap:
            _, u_idx = heapq.heappop(min_heap)
            for predecessor_idx, weight in predecessor_edges[u_idx].items() and not previous_visited[predecessor_idx]:
                previous_visited[predecessor_idx] = True
                if (distances[u_idx] + weight < distances[predecessor_idx]):
                    distances[predecessor_idx] = distances[u_idx] + weight
                    previous_visited[predecessor_idx] = u_idx
                    heapq.heappush(
                        min_heap, (distances[predecessor_idx], predecessor_idx))

        return distances

    # successor, predecessor both?!?!?!?!?!?!
    @staticmethod
    def _johnson_dijkstra(network, src_idx, distances, potential_function):

        reweighted_edges = deepcopy(network.successor_edges)

        for node_idx, dict_of_edges in enumerate(reweighted_edges):
            # do we not need tuple_idx
            for tuple_idx, (successor_idx, weight) in enumerate(dict_of_edges.items()):
                reweighted_edges[node_idx][successor_idx] = (
                    successor_idx, weight + potential_function[node_idx] - potential_function[successor_idx])

        min_heap = []
        in_queue = {}

        heapq.heappush(min_heap, (distances[src_idx], src_idx))
        in_queue[src_idx] = True

        # ok there is smth wrong here
        print(reweighted_edges)
        while min_heap:
            _, u_idx = heapq.heappop(min_heap)
            in_queue.pop(u_idx)
            for successor_idx, weight in reweighted_edges[u_idx].items():

                new_weight = weight + \
                    potential_function[successor_idx] - \
                    potential_function[u_idx]

                if successor_idx not in in_queue:
                    heapq.heappush(min_heap, (new_weight, successor_idx))
                    in_queue[successor_idx] = True
                else:
                    if (new_weight < distances[successor_idx]):
                        distances[successor_idx] = new_weight
                        heapq.heappush(
                            min_heap, (distances[successor_idx], successor_idx))
                        in_queue[successor_idx] = True

        return distances
