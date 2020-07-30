from stn import STN
from random import random, randrange

# =============================
#  FILE:    random_stn.py
#  AUTHOR:  Sudais Moorad / Muhammad Furrukh Asif
#  DATE:    June 2020
# =============================


class RandomSTN:

    def random_stns(self, no_of_stns, max_no_of_nodes, max_weight=100, min_weight=-100):
        """
         random_stns: Generates and writes to files as many STNs as the user
                      wants.
         -------------------------------------------------------------
         INPUTS:  no_of_stns: An integer representing the number of STNs to be
                              generated
                  max_no_of_nodes: An integer representing the max no of nodes
                                   a STN generated can have
                  max_weight: An integer representing the max weight to be
                              assigned to any edge in a STN. Assigned a default
                              value of 100.
         OUTPUT:  networks: An array of STNs
         SIDE EFFECTS:  Writes the genrated STNs to individual files.
         --------------------------------------------------------------
         """
        networks = []
        for _ in range(no_of_stns):
            num = int(random() * max_no_of_nodes + 1)
            num = max(3, num)
            network = self.random_stn(num, max_weight, min_weight)
            networks.append(network)
            self.write_stn(network, _)
        return networks

    def random_stn(self, no_of_nodes, max_weight=100, min_weight=-100, density_probability=None, node_names=None):
        """
         random_stn: Generates a random STN.
         -------------------------------------------------------------
         INPUTS:  no_of_nodes: An integer representing the number of nodes the
                  STN is going to have.
                  max_weight: An integer representing the max weight to be
                              assigned to any edge in the STN.
                  density_probability: A float representing the density of
                                       edges in the STN. Default value is None.
                  node_names: A list representing the node names of the STN.
                              Default value is None.
         OUTPUT:  network: A randomly genrated STN.
         --------------------------------------------------------------
         """
        network = STN()
        network.length = no_of_nodes
        if not node_names:
            node_names = [str(i) for i in range(network.length)]
        network.names_list = node_names
        for node_idx, node in enumerate(node_names):
            network.names_dict[node] = node_idx
        network.successor_edges = [{} for i in range(network.length)]
        self.random_edges(network, max_weight, min_weight, density_probability)
        return network

    def random_edges(self, network, max_weight=100, min_weight=-100, density_probability=None):
        """
         random_edges: Randomly populates the successor_edges of a randomly
                       generated STN.
         -------------------------------------------------------------
         INPUTS:  network: A randomly generated STN.
                  max_weight: An integer representing the max weight to be
                              assigned to any edge in the STN. Assigned a
                              default value of 100.
                  density_probability: A float representing the density of
                                       edges in the STN. Random if not given.
         OUTPUT:  None
         SIDE EFFECTS:  Randomly populates the successor_edges of a STN.
         --------------------------------------------------------------
         """
        if not density_probability or density_probability > 1 or type(density_probability) != float:
            density_probability = random()
        counter = 0
        for i in range(network.length):
            for j in range(network.length):
                rand = random()
                if rand < 0.5 * density_probability:
                    network.successor_edges[i][j] = int(
                        randrange(1, max_weight, 1))
                    counter += 1
                elif rand < density_probability:
                    network.successor_edges[i][j] = int(
                        randrange(min_weight, -1, 1))
                    counter += 1
        if counter == 0:
            network.successor_edges[randrange(
                0, network.length, 1)][randrange(0, network.length, 1)] = int(
                randrange(min_weight, -1, 1))

    def write_stn(self, network, stn_no):
        """
         write_stn: Writes a randomly generated STN to a file.
         -------------------------------------------------------------
         INPUTS:  network: A randomly generated STN.
                  stn_no: An integer representing a unique key for the STN to be
                          included in the file name.
         OUTPUT:  None
         SIDE EFFECTS:  Writes a randomly generated STN to a file.
         --------------------------------------------------------------
         """
        file = open('myfile' + str(stn_no) + '.txt', "w")
        edge_string = ""
        edge_counter = 0
        names_string = ""
        for name in network.names_list:
            names_string += name + " "
        for src_idx, dict in enumerate(network.successor_edges):
            for successor_idx, weight in dict.items():
                edge_string += str(network.names_list[src_idx]) + " " + str(
                    weight) + " " + str(network.names_list[successor_idx]) + "\n"
                edge_counter += 1
        L = ["# KIND OF NETWORK \n", "STN" + "\n", "# Num Time-Points \n",
             str(network.length) +
             "\n", "# Num Ordinary Edges \n", str(edge_counter) + "\n",
             "# Time-Point Names \n", names_string + "\n", "# Ordinary Edges \n", edge_string]
        file.writelines(L)

        # alpha => the grid ratio (P/T)
        # beta => grid density (no_grid_points : no_of_nodes => |V|)
        # s_min, s_max => real and non-negative, control the amplitude of the
        #                 interval between two nodes
        # u => the number of units per each grid interval
        def ntm(self, no_of_nodes, alpha, beta, edge_density, s_min, s_max, u):
            pass

        def random_mappping(self, alpha, beta):
            pass
