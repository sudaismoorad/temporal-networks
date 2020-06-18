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
        distance_matrix = [[] for x in range(network.length)]

        potential_function = BellmanFord.bellman_ford_wrapper(network)
       
        if not potential_function:
            return False

        for node_idx in range(network.length):
            distance_matrix[node_idx] = Dijkstra.dijkstra(
                network, node_idx, potential_function=potential_function)

        for src_idx, distance_list in enumerate(distance_matrix):
            for successor_idx, weight in enumerate(distance_list):
                distance_matrix[src_idx][successor_idx] = weight + \
                    potential_function[successor_idx] - \
                    potential_function[src_idx]


        if network.dist_up_to_date:
            network.dist_up_to_date = False

        network.distance_matrix = distance_matrix
        return distance_matrix
