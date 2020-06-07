class FloydWarshall:

    @staticmethod
    def floyd_warshall(network):
        length = network.length
        distance_matrix = [[float("inf") for i in range(length)]
                           for j in range(length)]

        for node_idx, edge_dict in enumerate(network.successor_edges):
            for successor_node_idx, weight in edge_dict.items():
                distance_matrix[node_idx][successor_node_idx] = weight
            distance_matrix[node_idx][node_idx] = 0

        for i in range(length):
            for j in range(length):
                for k in range(length):
                    distance_matrix[i][j] = min(
                        distance_matrix[i][j], distance_matrix[i][k] + distance_matrix[k][j])

        for node_idx in range(length):
            if distance_matrix[node_idx][node_idx] < 0:
                # raise Exception or return False?
                # raise Exception("Negative cycle found")
                return False

        network.distance_matrix = distance_matrix
        # should we return the distance matrix also?
        return distance_matrix
