import heapq
from copy import deepcopy


class Dijkstra:
    """
    A class to represent all variants of Dijkstra's algorithm.
    ...
    Methods
    -------
    dijkstra_wrapper
    _dijkstra
    _pred_dijkstra
    _johnson_dijkstra
    """
    # How to deal with predecessor edges attribute? Does pred_dijkstra run when predecessor edges given or it always calculates them?

    @staticmethod
    def dijkstra_wrapper(network, src, succ_direction=True, potential_function=False, path=False, dispatch=False):
        """
        A static method that calls one of the variants of Dikstra's algorithm
        depending on the inputs given.
        Parameters
        ----------
        network: STN, STNU
            The simple temporal network the algorithm will be run on.
        src: int, str
            An integer or string representing the index / name of a node. 
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

        distances = [float("inf") for i in range(network.num_tps())]
        distances[src_idx] = 0

        if dispatch:
            if network.successor_edges is None or potential_function is None:
                return False
            return Dijkstra._dispatch_dijkstra(network, src_idx, distances, potential_function)

        if not potential_function:
            if succ_direction:
                return Dijkstra._dijkstra(network, src_idx, distances) if network.successor_edges is not None else False
            else:
                return Dijkstra._pred_dijkstra(network, src_idx, distances) if network.predecessor_edges is not None else False
        else:
            return Dijkstra._johnson_dijkstra(network, src_idx, distances, potential_function) if network.successor_edges is not None else False

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
        num_tps = network.num_tps()
        predecessor_edges = [{} for i in range(num_tps)]
        previous_visited = [False for i in range(num_tps)]

        min_heap = []

        for i in range(network.num_tps):
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
            for _, (successor_idx, weight) in enumerate(dict_of_edges.items()):
                reweighted_edges[node_idx][successor_idx] = weight + \
                    potential_function[node_idx] - \
                    potential_function[successor_idx]

        min_heap = []

        heapq.heappush(min_heap, (distances[src_idx], src_idx))

        while min_heap:
            _, u_idx = heapq.heappop(min_heap)
            for successor_idx, new_weight in reweighted_edges[u_idx].items():
                if (distances[u_idx] + new_weight < distances[successor_idx]):
                    distances[successor_idx] = new_weight + distances[u_idx]

                    heapq.heappush(
                        min_heap, (distances[successor_idx], successor_idx))

        return distances

    @staticmethod
    def _dispatch_dijkstra(network, src_idx, distances, potential_function):

        def reweight_edges(node_idx):
            weight = distances[node_idx] + \
                potential_function[src_idx] - potential_function[node_idx]
            return weight

        min_heap = []
        in_queue = {}
        for i in range(network.num_tps()):
            in_queue[i] = False

        previous = [None for i in range(network.num_tps())]

        heapq.heappush(min_heap, (reweight_edges(src_idx), src_idx))
        in_queue[src_idx] = True
        counter = 0

        while min_heap:
            _, u_idx = heapq.heappop(min_heap)
            for successor_idx, new_weight in network.successor_edges[u_idx].items():
                if (reweight_edges(u_idx) + new_weight < reweight_edges(successor_idx)) and in_queue[successor_idx] == False:
                    counter += 1
                    distances[successor_idx] = new_weight + \
                        reweight_edges(u_idx)
                    previous[successor_idx] = u_idx
                    heapq.heappush(
                        min_heap, (reweight_edges(successor_idx), successor_idx))
                    in_queue[successor_idx] = True

        return distances

    @staticmethod
    def dijkstra_(network, listy, src_idx):

        distances = [float("inf") for i in range(len(listy))]
        distances[src_idx] = 0

        min_heap = []
        heapq.heappush(min_heap, (distances[src_idx], src_idx))

        while min_heap:

            _, u_idx = heapq.heappop(min_heap)
            for successor_idx, weight in network.successor_edges[u_idx].items():
                if successor_idx in listy:
                    if (distances[u_idx] + weight < distances[successor_idx]):
                        distances[successor_idx] = distances[u_idx] + weight
                        heapq.heappush(
                            min_heap, (distances[successor_idx], successor_idx))

        return distances
