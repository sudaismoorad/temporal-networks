from copy import deepcopy


class BellmanFord:

    @staticmethod
    def bellman_ford(network, src=-1):
        if src in network.names_dict.values():
            return BellmanFord._bellman_ford(network, src)
        else:
            return BellmanFord._bellman_ford_new(network)

    @staticmethod
    def _bellman_ford(network, src):
        # assuming src is always an idx
        length = network.length
        distances = [float("inf") for _ in range(length)]
        distances[src] = 0

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
