from stn import STN
from random import random
# self.names_dict = {}
# self.names_list = []
# self.successor_edges = []
# self.length = 0
# self.distance_matrix = []
# self.flag = False


class RandomSTN:

    def random_stns(self, no_of_stns, max_no_of_nodes, max_weight=100):
        networks = []
        for i in range(no_of_stns):
            num = int(random() * max_no_of_nodes+1)
            num = max(3, num)
            networks.append(self.random_stn(num, max_weight))
        return networks



    def random_stn(self, no_of_nodes, max_weight=100, density_probability=None, node_names=None):
        network = STN()
        network.length = no_of_nodes
        if not node_names:
            node_names = [str(i) for i in range(network.length)]
        network.names_list = node_names
        for node_idx, node in enumerate(node_names):
            network.names_dict[node] = node_idx
        network.successor_edges = [{} for i in range(network.length)]
        self.random_edges(network, max_weight, density_probability)
        return network


    def random_edges(self, network, max_weight=100, density_probability=None):
        if not density_probability or density_probability > 1 or type(density_probability) != float:
            density_probability = random()
        for i in range(network.length):
            for j in range(network.length):
                if random() < density_probability:
                    network.successor_edges[i][j] = int(random() * max_weight)
