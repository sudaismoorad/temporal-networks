from copy import deepcopy


class BellmanFord:
    """
    A class to represent all variants of the Bellman Ford algorithm.
    ...
    Methods
    -------
    bellman_ford
    _bellman_ford
    _bellman_ford_new
    """

    @staticmethod
    def bellman_ford(network, src=-1):
        """
        A static method that calls one of the Bellman Ford variants depending on
        if the source is in the network or no.
        Parameters
        ----------
        network: STN, STNU
            The simple temporal network the algorithm will be run on.
        src: int, str
            An integer or string representing the index / name of a node. If
            not given the default is -1.
        Returns
        -------
        distances: int[]
            A list representing the shortest distances between the src and all
            the nodes.
        """
        if src in network.names_dict.values():
            return BellmanFord._bellman_ford(network, src)
        else:
            return BellmanFord._bellman_ford_new(network)

    @staticmethod
    def _bellman_ford(network, src):
        """
        A static method that executes a variant of Bellman Ford where the given
        src exists in the network.
        Parameters
        ----------
        network: STN, STNU
            The simple temporal network the algorithm will be run on.
        src: int, str
            An integer or string representing the index / name of a node in
            the network.
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
        length = network.length
        distances = [float("inf") for _ in range(length)]
        distances[src_idx] = 0

        for _ in range(length - 1):
            for node_idx in range(length):
                for successor_node_idx, weight in network.successor_edges[node_idx].items():
                    distances[successor_node_idx] = min(
                        distances[successor_node_idx], distances[node_idx] + weight)

        for node_idx in range(length):
            for successor_node_idx, weight in network.successor_edges[node_idx].items():
                if distances[successor_node_idx] > distances[node_idx] + weight:
                    # raise Exception("are we supposed to throw an error here?")
                    return False

        return distances

    @staticmethod
    def _bellman_ford_new(network):
        """
        A static method that executes a variant of Bellman Ford where the source
        is not given rather its an arbitrary node.
        Parameters
        ----------
        network: STN, STNU
            The simple temporal network the algorithm will be run on.
        Returns
        -------
        distances: int[]
            A list representing the shortest distances between an aribitrary
            node and all the nodes.
        """
        length = network.length
        distances = [float("inf") for _ in range(length)]
        successor_edges = deepcopy(network.successor_edges)

        distances.append(0)
        successor_edges.append({})
        for i in range(length):
            successor_edges[length][i] = 0

        for _ in range(length):
            for node_idx in range(length + 1):
                for successor_node_idx, weight in successor_edges[node_idx].items():
                    distances[successor_node_idx] = min(
                        distances[successor_node_idx], distances[node_idx] + weight)

        for node_idx in range(length + 1):
            for successor_node_idx, weight in successor_edges[node_idx].items():
                if distances[successor_node_idx] > distances[node_idx] + weight:
                    # raise Exception("are we supposed to throw an error here?")
                    return False

        return distances[:-1]
