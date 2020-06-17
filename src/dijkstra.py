import heapq
from copy import deepcopy


class Dijkstra:
    """
    A class to represent all variants of Dijkstra's algorithm.
    ...
    Methods
    -------
    dijkstra
    _dijkstra
    _pred_dijkstra
    _johnson_dijkstra
    """

    @staticmethod
    def dijkstra(network, src, succ_direction=True, potential_function=False, path=False, list_of_leaders=None, d=None):
        """
        A static method that calls one of the variants of Dikstra's algorithm
        depending on the inputs given.
        Parameters
        ----------
        network: STN, STNU
            The simple temporal network the algorithm will be run on.
        src: int, str
            An integer or string representing the index / name of a node. If
            not given the default is -1.
        succ_direction: bool
            If true succesor edge variant runs, if false predecessor edge
            variant runs. Default value is true.
        potential_function: int[]
            An array representing the shortest distances from the src to all
            nodes.
        Returns
        -------
        distances: int[]
            A list representing the shortest distances between the src and all
            the nodes.
        """

        if type(src) == str:
            src_idx = network.names_dict[src]
        else:
            src_idx = src

        distances = [float("inf") for i in range(network.length)]
        distances[src_idx] = 0

        if path:
            if not list_of_leaders:
                return False
            return Dijkstra._dispatch_dijkstra(network, src_idx, distances, potential_function, list_of_leaders, d)

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
        A static method that calls a variant of Dikstra's algorithm which
        calculates the shortest distances from the given src to all nodes by
        propagating successor edges.
        Parameters
        ----------
        network: STN, STNU
            The simple temporal network the algorithm will be run on.
        src_idx: int, str
            An integer representing the index of a node.
        distances: int[]
            A list representing the shortest distances between the src and all
            the nodes. Intialised to infinity besides the src to src intialised
            to 0.
        Returns
        -------
        distances: int[]
            A list representing the shortest distances between the src and all
            the nodes.
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
        """
        A static method that calls a variant of Dikstra's algorithm which
        calculates the shortest distances from the given src to all nodes by
        propagating predecessor edges.
        Parameters
        ----------
        network: STN, STNU
            The simple temporal network the algorithm will be run on.
        src_idx: int, str
            An integer representing the index of a node.
        distances: int[]
            A list representing the shortest distances between the src and all
            the nodes. Intialised to infinity besides the src to src intialised
            to 0.
        Returns
        -------
        distances: int[]
            A list representing the shortest distances between the src and all
            the nodes.
        """
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
        """
        A static method that calls a variant of Dikstra's algorithm used in
        Johnson's algorithm. It calculates the shortest distances from the
        given src to all nodes using a potential function.
        Parameters
        ----------
        network: STN, STNU
            The simple temporal network the algorithm will be run on.
        src_idx: int, str
            An integer representing the index of a node.
        distances: int[]
            A list representing the shortest distances between the src and all
            the nodes. Intialised to infinity besides the src to src intialised
            to 0.
        potential_function: int[]
            An array representing the shortest distances from the src to all
            nodes. For Johnsons it is generated using Bellman Ford's aribitrary
            node variant.
        Returns
        -------
        distances: int[]
            A list representing the shortest distances between the src and all
            the nodes.
        """
        reweighted_edges = deepcopy(network.successor_edges)

        for node_idx, dict_of_edges in enumerate(reweighted_edges):
            # do we not need tuple_idx?
            for _, (successor_idx, weight) in enumerate(dict_of_edges.items()):
                reweighted_edges[node_idx][successor_idx] = weight + \
                    potential_function[node_idx] - \
                    potential_function[successor_idx]

        min_heap = []
        in_queue = {}

        heapq.heappush(min_heap, (distances[src_idx], src_idx))
        in_queue[src_idx] = True

        while min_heap:
            _, u_idx = heapq.heappop(min_heap)
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

    @staticmethod
    def _dispatch_dijkstra(network, src_idx, distances, potential_function, list_of_leaders, d):
        predecessor_graphs = [[] for i in list_of_leaders]
        list_of_distances = [[] for i in list_of_leaders]
        print(src_idx)
        for idx, leader in enumerate(d):
            # print(leader)
            if leader == src_idx:
                continue
            reweighted_edges = deepcopy(network.successor_edges)

            for node_idx, dict_of_edges in enumerate(reweighted_edges):
                # do we not need tuple_idx?
                for _, (successor_idx, weight) in enumerate(dict_of_edges.items()):
                    reweighted_edges[node_idx][successor_idx] = weight + \
                        potential_function[node_idx] - \
                        potential_function[successor_idx]

            min_heap = []
            in_queue = {}
            previous = ["" for i in range(network.length)]

            heapq.heappush(min_heap, (distances[src_idx], src_idx))
            in_queue[src_idx] = True

            while min_heap:
                _, u_idx = heapq.heappop(min_heap)

                if leader == u_idx:
                    rtn = []
                    rtn.append(u_idx)
                    while previous[u_idx] != src_idx:
                        u_idx = previous[u_idx]
                        rtn.append(u_idx)
                    rtn.append(src_idx)
                    predecessor_graphs[idx] = rtn
                    list_of_distances[idx] = distances
                    break

                for successor_idx, weight in reweighted_edges[u_idx].items():

                    new_weight = weight + \
                        potential_function[successor_idx] - \
                        potential_function[u_idx]

                    if successor_idx not in in_queue:
                        heapq.heappush(min_heap, (new_weight, successor_idx))
                        previous[successor_idx] = u_idx
                        in_queue[successor_idx] = True
                    else:
                        if (new_weight < distances[successor_idx]):

                            distances[successor_idx] = new_weight
                            heapq.heappush(
                                min_heap, (distances[successor_idx], successor_idx))
                            previous[successor_idx] = u_idx
                            in_queue[successor_idx] = True

        return list_of_distances, predecessor_graphs
