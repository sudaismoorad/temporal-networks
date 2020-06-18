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
        length = network.length
        distance_matrix = [[float("inf") for i in range(length)]
                           for j in range(length)]

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

        for i in range(length):
            for j in range(length):
                for k in range(length):
                    distance_matrix[i][j] = min(
                        distance_matrix[i][j], distance_matrix[i][k] + distance_matrix[k][j])

        for node_idx in range(length):
            if distance_matrix[node_idx][node_idx] < 0:
                return False

        if network.dist_up_to_date:
            network.dist_up_to_date = False

        network.distance_matrix = distance_matrix
        return distance_matrix
