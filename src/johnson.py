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

        potential_function = BellmanFord.bellman_ford(network)

        if not potential_function:
            return False

        for node_idx in range(network.length):
            distance_matrix[node_idx] = Dijkstra.dijkstra(
                network, node_idx, potential_function=potential_function)

        if network.flag:
            network.flag = False

        # network.distance_matrix = distance_matrix
        return distance_matrix
