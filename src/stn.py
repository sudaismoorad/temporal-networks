import heapq


class STN:
    """
    A class to represent a Simple Temporal Network.
    ...
    Attributes
    ----------
    names_dict : dict[name: index]
        A dictionary that maps the name of the node to its index
    successor_edges : List[List[tuples]]
        A list of list of successor edges. The list at index i of this attribute is
        the list of edges of the i-th node. Each edge is represented by a tuple - the
        first element of the tuple is the j-th node that the i-th node is connected to
        and the second element is the weight/distance between the i-th and j-th nodes
    length : int
        number of nodes in the STN
    """

    def __init__(self):
        """
        Constructor for a Simple Temporal Network
        Parameters
        ----------
            names_dict : dict[name: index]
                A dictionary that maps the name of the node to its index
            successor_edges : List[dict[node: weight]]
                A list of list of successor edges. The list at index i of this attribute is
                the list of edges of the i-th node. Each edge is represented by a tuple - the
                first element of the tuple is the j-th node that the i-th node is connected to
                and the second element is the weight/distance between the i-th and j-th nodes
            length : int
                number of nodes in the STN
        Returns
        -------
        None
        """
        self.names_dict = {}
        self.names_list = []
        self.successor_edges = []
        self.length = 0
        self.distance_matrix = []
        self.flag = False

    def __str__(self):
        stringy = "STN:\n"
        stringy += f"Number of nodes in network: {self.length}\n"
        stringy += f"Dictionary of names -> index: {self.names_dict}\n"
        stringy += f"Successor edges of each node: {self.successor_edges}\n"
        if self.distance_matrix:
            stringy += f"Distance matrix: {self.distance_matrix}\n"
            if self.flag:
                stringy += "Distance matrix might not have a valid solution"
        return stringy

    def insert_new_edge(self, tp1, tp2, weight):

        tp1_idx = self.names_dict[tp1] if type(tp1) == str else tp1
        tp2_idx = self.names_dict[tp2] if type(tp2) == str else tp2

        self.successor_edges[tp1_idx][tp2_idx] = int(weight)
        self.flag = True

    def delete_edge(self, tp1, tp2):

        tp1_idx = self.names_dict[tp1] if type(tp1) == str else tp1
        tp2_idx = self.names_dict[tp2] if type(tp2) == str else tp2

        del self.successor_edges[tp1_idx][tp2_idx]

    def insert_new_tp(self, tp):
        self.names_dict[tp] = self.length
        self.names_list[self.length] = tp
        self.length += 1

    def delete_tp(self, tp):
        if type(tp) == str:
            tp_idx = self.names_dict[tp]
        else:
            tp_idx = tp

        del self.names_dict[self.names_list[tp_idx]]
        self.names_list.pop(tp_idx)
        self.length -= 1
