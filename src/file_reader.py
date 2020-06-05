from stn import STN
from stnu import STNU
from algorithms import *


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

    def __init__(self, file_path):
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
        self.file_path = file_path
        self.network = []

    def read_file(self):
        """
        Reads the file and decides whether to create an STN or an STNU
        Parameters
        ----------
        None
        Returns
        -------
        None
        """
        file = open(self.file_path, "r")
        state = ""
        for line in file:
            if "network" in line.lower():
                state = "NETWORK_TYPE"
                continue
            if state == "NETWORK_TYPE":
                if "u" not in line.lower():
                    self.network = STN()
                    return self._read_stn(file)
                elif "u" in line.lower():
                    self.network = STNU()
                    return self._read_stnu(file)
                else:
                    raise Exception("Invalid Network Type")

    def _read_stn(self, file):
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
                    num_points = int(line)
                    self.network.length = num_points
                    self.network.successor_edges = [
                        [] for i in range(num_points)]
                elif state == 'NO_EDGES':
                    num_edges = int(line)
                elif state == 'NO_LINKS':
                    # for testing, throw an error
                    raise Exception(
                        "Simple Temporal Networks do not have contingent links.")
                elif state == 'NAMES':
                    list_of_nodes = line.split()
                    if len(list_of_nodes) != num_points:
                        raise Exception(
                            "Number of names does not match the number of nodes provided")
                    for idx, node_name in enumerate(list_of_nodes):
                        self.network.names_dict[node_name] = idx
                elif state == 'EDGES':
                    weights = line.split()
                    edge_counter += 1
                    # make a list of list of tuples
                    idx_key = self.network.names_dict[weights[0]]
                    idx_value = self.network.names_dict[weights[2]]
                    tup = (idx_value, int(weights[1]))
                    self.network.successor_edges[idx_key].append(tup)
                elif state == 'LINKS':
                    raise Exception(
                        "Simple Temporal Networks do not have contingent links.")
                else:
                    pass
        if num_edges != edge_counter:
            raise Exception(
                "Number of edges does not match the number given above")

    def _read_stnu(self, file):
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
                elif "links" in line.lower():
                    state = "LINKS"
                else:
                    raise Exception("Invalid Network Type")
            else:
                if state == 'NO_POINTS':
                    num_points = int(line)
                    self.network.length = num_points
                    self.network.successor_edges = [
                        [] for i in range(num_points)]
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
                        self.network.names_dict[node_name] = idx
                elif state == 'EDGES':
                    weights = line.split()
                    # make a list of list of tuples
                    idx_key = self.network.names_dict[weights[0]]
                    idx_value = self.network.names_dict[weights[2]]
                    tup = (idx_value, weights[1])
                    self.network.successor_edges[idx_key].append(tup)
                elif state == 'LINKS':
                    # deal with contingent links later
                    pass
                else:
                    pass


f = FileReader("../sample_stns/dc-2.stn")

f.read_file()
print("########### TESTING FLOYD WARSHALL ###########")
floyd_warshall(f.network)

print(f.network)

print("########### TESTING BELLMAN FORD ###########")
for i in range(1, 6):
    bellman_ford(f.network, i)
    print(f.network)

print("########### TESTING BELLMAN FORD ###########")

bellman_ford(f.network)

print(f.network)

print("########### TESTING DIJKSTRA ###########")

for i in range(1, 5):
    dijkstra(f.network, i)
    print(f.network)

print("########### TESTING JOHNSON ###########")

johnson(f.network)

print(f.network)
