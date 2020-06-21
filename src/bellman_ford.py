# ==============================================
#  FILE:     bellman_ford.py
#  AUTHOR:   Sudais Moorad / Muhammad Furrukh Asif
#  DATE:     June 2020
# ==============================================


class BellmanFord:
    """
    -----------------------------------------------------------------
    A class to hold several variants of the Bellman Ford 
    algorithm, each implemented as a static method.
    -----------------------------------------------------------------
    Methods
    -------
    bellman_ford_wrapper   
    bellman_ford_existing_src
    bellman_ford_external_source
    """

    # =================================================================
    @staticmethod
    def bellman_ford_wrapper(network, src=-1):
        """
        ------------------------------------------------------------------------
        A static method that calls one of the Bellman Ford variants depending on
        if the source is in the network or no.
        ------------------------------------------------------------------------
        Parameters
        ----------
        network: STN
            The simple temporal network the algorithm will be run on.
        src: int, str
            An integer or string representing the index / name of a node. If 
            src not given, then a new source node is used that does not belong 
            to the given STN.
        Returns
        -------
        distances: int[]
            A list representing the shortest distances between the src and all
            the nodes.
        """
        if network.successor_edges is None:
            return False
        if src in network.names_dict.values():
            return BellmanFord.bellman_ford_existing_src(network, src)
        else:
            return BellmanFord.bellman_ford_external_source(network)

    @staticmethod
    def bellman_ford_existing_src(network, src):
        """
        ------------------------------------------------------------------------
        A static method that executes a variant of Bellman Ford where the given
        src exists in the network.
        ------------------------------------------------------------------------
        Parameters
        ----------
        network: STN  
            The simple temporal network the algorithm will be run on.
        src: int, str
            An integer or string representing the index / name of a node in
            the network.
        Returns
        -------
        distances: int[]
            A list representing the shortest distances from the src to
            every node in the network
        --------------------------------------------------------------------------
        """
        if type(src) == str:
            src_idx = network.names_dict[src]
        else:
            src_idx = src
        num_tps = network.num_tps()
        distances = [float("inf") for _ in range(num_tps)]
        distances[src_idx] = 0

        # First N-1 passes of bellman ford
        for _ in range(num_tps - 1):
            for node_idx in range(num_tps):
                # Consider every edge emanating from NODE_IDX
                for successor_node_idx, weight in network.successor_edges[node_idx].items():
                    # Update distance if SRC -> NODE_IDX -> SUCCESSOR_NODE_IDX is shorter path
                    distances[successor_node_idx] = min(
                        distances[successor_node_idx], distances[node_idx] + weight)

        # Last pass of bellman ford (checks for negative cycle)
        for node_idx in range(num_tps):
            for successor_node_idx, weight in network.successor_edges[node_idx].items():
                if distances[successor_node_idx] > distances[node_idx] + weight:
                    return False

        return distances

    @staticmethod
    def bellman_ford_external_source(network):
        """
        -------------------------------------------------------------------------
        A static method that executes a variant of Bellman Ford where a new
        node, not belonging to the network, is used as a source node
        -------------------------------------------------------------------------
        Parameters
        ----------
        network: STN  *** only STN for now ***
            The simple temporal network the algorithm will be run on.
        Returns
        -------
        distances: int[]
            A list representing the shortest distances from the new 
            source node and all the nodes in the network
        --------------------------------------------------------------------------
        """
        num_tps = network.num_tps()
        distances = [0 for _ in range(num_tps)]

        for _ in range(num_tps - 1):
            for node_idx in range(num_tps):
                for successor_node_idx, weight in network.successor_edges[node_idx].items():
                    distances[successor_node_idx] = min(
                        distances[successor_node_idx], distances[node_idx] + weight)

        for node_idx in range(num_tps):
            for successor_node_idx, weight in network.successor_edges[node_idx].items():
                if distances[successor_node_idx] > distances[node_idx] + weight:
                    return False

        return distances
