from stn import STN
from stnu import STNU
from algorithms import *
from random_stn import RandomSTN
from dispatch import Dispatch
from dispatchability import Dispatchability
from write_stn import write_stn
from time import time


class FileReader:

    """
    A class to represent a read a file with the format of an stn/stnu.
    ...
    Attributes
    ----------
    file_path : str
        The path to the stn/stnu file
    network : STN, STNU
        The simple temporal network to be created
    Methods
    -------
    read_file
    """

    def __init__(self, successor_edges=True, predecessor_edges=False):
        """
        Constructor for the file reader
        Parameters
        ----------
        file_path : str
            The path to the stn/stnu file
        network : STN, STNU
            The simple temporal network to be created
        Returns
        -------
        None
        """
        self.predecessor_edges = predecessor_edges
        self.successor_edges = successor_edges

    def read_file(self, file_path):
        """
        Reads the file and decides whether to create an STN or an STNU
        Parameters
        ----------
        None
        Returns
        -------
        None
        """
        file = open(file_path, "r")
        state = ""
        for line in file:
            if "network" in line.lower():
                state = "NETWORK_TYPE"
                continue
            if state == "NETWORK_TYPE":
                if "u" not in line.lower():
                    return self._read_stn(file)
                elif "u" in line.lower():
                    return self._read_stnu(file)
                else:
                    raise Exception("Invalid Network Type")

    def _read_stn(self, file):
        network = STN(successor_edges=self.successor_edges,
                      predecessor_edges=self.predecessor_edges)
        state = ""
        for line in file:
            if line.startswith('#'):
                if "points" in line.lower() and "num" in line.lower():
                    state = "NO_POINTS"
                elif "edges" in line.lower() and "num" in line.lower():
                    state = "NO_EDGES"
                elif "links" in line.lower():
                    state = "NO_LINKS"
                elif "names" in line.lower():
                    state = "NAMES"
                elif "edges" in line.lower():
                    state = "EDGES"
                    edge_counter = 0
                elif "links" in line.lower():
                    state = "LINKS"
                else:
                    pass
            else:
                if state == 'NO_POINTS':
                    num_tps = int(line)
                    network.n = num_tps
                    if self.successor_edges:
                        network.successor_edges = [
                            {} for i in range(num_tps)]
                    if self.predecessor_edges:
                        network.predecessor_edges = [
                            {} for i in range(num_tps)]
                    network.names_list = ["0" for i in range(num_tps)]
                elif state == 'NO_EDGES':
                    num_edges = int(line)
                elif state == 'NO_LINKS':
                    # for testing, throw an error
                    raise Exception(
                        "Simple Temporal Networks do not have contingent links.")
                elif state == 'NAMES':
                    list_of_nodes = line.split()
                    if len(list_of_nodes) != num_tps:
                        raise Exception(
                            "Number of names does not match the number of nodes provided")
                    for idx, node_name in enumerate(list_of_nodes):
                        network.names_dict[node_name] = idx
                        network.names_list[idx] = node_name
                elif state == 'EDGES':
                    if num_edges == 0:
                        state = ''
                        continue
                    weights = line.split()
                    edge_counter += 1
                    # make a list of list of tuples
                    idx_node = network.names_dict[weights[0]]
                    idx_successor = network.names_dict[weights[2]]
                    if self.successor_edges:
                        network.successor_edges[idx_node][idx_successor] = int(
                            weights[1])
                    if self.predecessor_edges:
                        network.predecessor_edges[idx_successor][idx_node] = int(
                            weights[1])
                elif state == 'LINKS':
                    raise Exception(
                        "Simple Temporal Networks do not have contingent links.")
        if num_edges != edge_counter:
            raise Exception(
                "Number of edges does not match the number given above")
        return network

    def _read_stnu(self, file):
        network = STNU()
        state = ""
        for line in file:
            if line.startswith('#'):
                if "points" in line.lower() and "num" in line.lower():
                    state = "NO_POINTS"
                elif "edges" in line.lower() and "num" in line.lower():
                    state = "NO_EDGES"
                elif "links" in line.lower() and "num" in line.lower():
                    state = "NO_LINKS"
                elif "names" in line.lower():
                    state = "NAMES"
                elif "edges" in line.lower():
                    state = "EDGES"
                elif "links" in line.lower():
                    state = "LINKS"
                    network.contingent_links = [{} for i in range(num_points)]
                    network.activation_point = [False for i in range(num_points)]
                else:
                    raise Exception("Invalid Network Type")
            else:
                if state == 'NO_POINTS':
                    num_points = int(line)
                    network.n = num_points
                    network.successor_edges = [
                        {} for i in range(num_points)]
                    network.names_list = ["0" for i in range(num_points)]
                elif state == 'NO_EDGES':
                    num_edges = int(line)
                elif state == 'NO_LINKS':
                    no_links = int(line)
                elif state == 'NAMES':
                    list_of_nodes = line.split()
                    if len(list_of_nodes) != num_points:
                        raise Exception(
                            "Number of names does not match the number of nodes provided")
                    for idx, node_name in enumerate(list_of_nodes):
                        network.names_dict[node_name] = idx
                        network.names_list[idx] = node_name
                elif state == 'EDGES':
                    weights = line.split()
                    # make a list of list of tuples
                    idx_node = network.names_dict[weights[0]]
                    idx_successor = network.names_dict[weights[2]]
                    network.successor_edges[idx_node][idx_successor] = int(
                        weights[1])
                elif state == 'LINKS':
                    weights = line.split()
                    activation_time_point = network.names_dict[weights[0]]
                    duration = (int(weights[1]), int(weights[2]))
                    contingent_time_point = network.names_dict[weights[3]]
                    network.contingent_links[activation_time_point][contingent_time_point] = duration
                    network.activation_point[activation_time_point] = True
        return network


f = FileReader()

stnu = f.read_file("./sample_stnus/dc-2.stnu")
print(stnu)

# tim = time()
# fast_dispatch, _ = Dispatch.fast_dispatch(stn)

# print(fast_dispatch)
# potential_function = bellman_ford(stn)
# write_stn(fast_dispatch, "fast_dispatch_200")
# disp = Dispatchability.greedy_execute(fast_dispatch, potential_function)
# print(disp)


# print(f"Fast dispatch took {time() - tim} seconds")

# print("########### TESTING FLOYD WARSHALL ###########")
# floyd_warshall(stn)

# print(stn)

# print("########### TESTING BELLMAN FORD ###########")
# for i in range(1, 6):
#     print(bellman_ford(stn, i))
#     print(stn)

# print("########### TESTING BELLMAN FORD ###########")

# bellman_ford(stn)

# print(stn)


# print("########### TESTING DIJKSTRA ###########")
#
# for i in range(1, 5):
#     dijkstra(stn, i)
#     print(stn)
#
# print("########### TESTING JOHNSON ###########")

# johnson(stn)

# print(stn)

# dispatch(stn)


# R = RandomSTN()

# R.random_stns(5,5)
