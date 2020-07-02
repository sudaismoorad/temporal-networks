from bellman_ford import BellmanFord
from dijkstra import Dijkstra


class Johnson:

    @staticmethod
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
        if network.successor_edges is None:
            return False
        num_tps = network.num_tps()
        distance_matrix = [[] for x in range(num_tps)]

        potential_function = BellmanFord.bellman_ford_wrapper(network)

        if not potential_function:
            return False

        for node_idx in range(network.num_tps()):
            distance_matrix[node_idx] = Dijkstra.dijkstra_wrapper(
                network, node_idx, potential_function=potential_function)

        for src_idx, distance_list in enumerate(distance_matrix):
            for successor_idx, weight in enumerate(distance_list):
                distance_matrix[src_idx][successor_idx] = weight + \
                    potential_function[successor_idx] - \
                    potential_function[src_idx]

        network.dist_up_to_date = True

        network.distance_matrix = distance_matrix
        return distance_matrix
