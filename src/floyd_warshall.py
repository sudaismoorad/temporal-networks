# ==============================================
#  FILE:     bellman_ford.py
#  AUTHOR:   Sudais Moorad / Muhammad Furrukh Asif
#  DATE:     June 2020
# ==============================================


class FloydWarshall:
    """
    -------------------------------------------------
    A class to represent the FloydWarshall algorithm.
    -------------------------------------------------
    Methods
    -------
    floyd_warshall
    """

    @staticmethod
    def floyd_warshall(network):
        # If successor edges not given, should this run on predecessor edges?
        """
        -------------------------------------------------------------------------
        A static method that calculates the shortest distances between all nodes.
        -------------------------------------------------------------------------
        Parameters
        ----------
        network: STN
            The simple temporal network the algorithm is going to be run on.
        Returns
        -------
        distance_matrix: int[][]
            A NxN array representing the shortest distances between all nodes.
        """
        if network.successor_edges is None:
            return False
        num_tps = network.num_tps()
        distance_matrix = [[float("inf") for i in range(num_tps)]
                           for j in range(num_tps)]

        # ??
        # Initialize matrix entries to match the edges in the network
        for node_idx, edge_dict in enumerate(network.successor_edges):
            for successor_node_idx, weight in edge_dict.items():
                distance_matrix[node_idx][successor_node_idx] = weight

            # Note:  This is optional... it can be useful to have
            # values > 0 here (they would indicate that length of
            # shortest loop containing a given node)

            # we could run a bfs here to add the length of the shortest
            # loop... shouldnt affect time complexity.... if we are
            # worried about it we could run the dfs before the for loop
            # and store the results in an array
            distance_matrix[node_idx][node_idx] = 0

        for i in range(num_tps):
            for j in range(num_tps):
                for k in range(num_tps):
                    distance_matrix[i][j] = min(
                        distance_matrix[i][j], distance_matrix[i][k] + distance_matrix[k][j])

        for node_idx in range(num_tps):
            if distance_matrix[node_idx][node_idx] < 0:
                return False

        network.dist_up_to_date = True

        network.distance_matrix = distance_matrix
        return distance_matrix
