# =============================
#  FILE:    stn.py
#  AUTHOR:  Sudais Moorad / Muhammad Furrukh Asif
#  DATE:    June 2020
# =============================


class STN:
    """
    -------------------------------------------------
    A class to represent a Simple Temporal Network
    -------------------------------------------------
    Attributes
    ----------
    names_dict : dict[name: index]
        A dictionary that maps the name of the node to its index
    names_list : List[Int]
        A list that maps the numerical index of a node to its name
    successor_edges : List[Dict[index:name]]
        A list of lists of successor edges. The list at index i of this attribute is
        the list of edges of the i-th node. Each edge is represented by a tuple - the
        first element of the tuple is the j-th node that the i-th node is connected to
        and the second element is the weight/distance between the i-th and j-th nodes
    n : int
        Number of nodes in the STN
    distance_matrix : List[List[int]]
        (optional) if used, holds the NxN all-pairs, shortest-paths (APSP) matrix
        for the STN.
    dist_up_to_date : boolean  
        True, if the distance_matrix is up-to-date; False, otherwise.
    ---------------------------------------------------
    """

    def __init__(self, successor_edges=True, predecessor_edges=False):
        """
        -----------------------------------------
        Constructor for a Simple Temporal Network
        -----------------------------------------
        Attributes
        ----------
        names_dict : dict[name: index]
            A dictionary that maps the name of the node to its index
        names_list : List[Int]
            A list that maps the numerical index of a node to its name
        successor_edges : List[Dictionary]
            A list of lists of successor edges. The list at index i of this attribute is
            the list of edges of the i-th node. Each edge is represented by a tuple - the
            first element of the tuple is the j-th node that the i-th node is connected to
            and the second element is the weight/distance between the i-th and j-th nodes
        length : int
            Number of nodes in the STN
        distance_matrix : List[List[int]]
            (optional) if used, holds the NxN all-pairs, shortest-paths (APSP) matrix
            for the STN.
        dist_up_to_date : boolean  
            True, if the distance_matrix is up-to-date; False, otherwise.
        -------
        Returns
        -------
        None
        -----------------------------------------
        """

        self.names_dict = {}
        self.names_list = []
        self.successor_edges = [] if successor_edges else None
        self.predecessor_edges = [] if predecessor_edges else None
        self.n = 0
        # need a flag for this? Why?
        self.distance_matrix = []
        self.dist_up_to_date = False

    def __str__(self):
        """
        ----------------------------------------
        Print method for an STN object
        ----------------------------------------
        Output:  String representation of the STN
        ----------------------------------------
        """
        stringy = "STN:\n"
        stringy += f"Number of nodes in network: {self.n}\n"
        stringy += f"Dictionary of names -> index: {self.names_dict}\n"
        if self.successor_edges:
            stringy += f"Successor edges of each node: {self.successor_edges}\n"
        if self.predecessor_edges:
            stringy += f"Predecessor edges of each node: {self.predecessor_edges}\n"
        # Display the distance_matrix if it is being used
        if self.distance_matrix:
            stringy += f"Distance matrix: {self.distance_matrix}\n"
            if self.dist_up_to_date:
                stringy += "Distance matrix might not be up to date"
        return stringy

    def num_tps(self):
        # should we make the length attribute private?
        return self.n

    def insert_new_edge(self, tp1, tp2, weight):
        """
        ----------------------------------------------
        Inserts a new edge into the STN object
        ----------------------------------------------
        Parameters:
        -----------
        tp1, either a numerical index or the name of a time-point
        tp2, ditto 
        weight, the numerical weight of the edge to be added
        -----------
        Returns:  none
        -----------
        Side Effect:
        -----------
        Inserts the edge, tp1 ----[weight]----> tp2 into the STN
        ---------------------------------------------------------
        """
        tp1_idx = self.names_dict[tp1] if type(tp1) == str else tp1
        tp2_idx = self.names_dict[tp2] if type(tp2) == str else tp2

        if self.successor_edges is not None:
            self.successor_edges[tp1_idx][tp2_idx] = int(weight)
        if self.predecessor_edges is not None:
            self.predecessor_edges[tp2_idx][tp1_idx] = int(weight)
        self.dist_up_to_date = False

    def delete_edge(self, tp1, tp2):
        """
        ----------------------------------------------
        Deletes an edge from the STN object
        ----------------------------------------------
        Parameters:
        -----------
        tp1, either a numerical index or the name of a time-point
        tp2, ditto 
        weight, the numerical weight of the edge to be added
        -----------
        Returns:  none
        -----------
        Side Effect:
        -----------
        Deletes the edge, tp1 ----[weight]----> tp2 from the STN
        ---------------------------------------------------------
        """
        tp1_idx = self.names_dict[tp1] if type(tp1) == str else tp1
        tp2_idx = self.names_dict[tp2] if type(tp2) == str else tp2

        if self.successor_edges:
            del self.successor_edges[tp1_idx][tp2_idx]
        if self.predecessor_edges:
            del self.predecessor_edges[tp2_idx][tp1_idx]

        self.dist_up_to_date = False

    def insert_new_tp(self, tp):
        """
        ----------------------------------------------
        Inserts a new time-point into the STN object
        ----------------------------------------------
        Parameters:
        -----------
        tp, the name of a time-point
        -----------
        Returns:  none
        -----------
        Side Effect:
        -----------
        Inserts the time-point, tp into the STN
        ---------------------------------------------------------
        """
        self.names_dict[tp] = self.n
        self.names_list.append(tp)
        self.n += 1

    # Discuss whether to keep this or no
    # should we make a generator for traversing through the stn
    def delete_tp(self, tp):
        if type(tp) == str:
            tp_idx = self.names_dict[tp]
        else:
            tp_idx = tp

        temp_names_dict = {}
        temp_names_list = []
        if self.successor_edges:
            temp_successor_edges = [{}
                                    for i in range(len(self.successor_edges))]
        if self.predecessor_edges:
            temp_predecessor_edges = [{}
                                      for i in range(len(self.predecessor_edges))]

        for i in range(self.n):
            if i == tp_idx:
                continue
            node_name = self.names_list[i]
            temp_names_dict[node_name] = i
            temp_names_list.append(node_name)
            for j, weight in self.successor_edges[i].items():
                if j == tp_idx:
                    continue
                if self.successor_edges:
                    temp_successor_edges[i][j] = weight
                if self.predecessor_edges:
                    temp_predecessor_edges[j][i] = weight

        self.names_list = temp_names_list
        self.names_dict = temp_names_dict
        if self.successor_edges:
            self.successor_edges = temp_successor_edges
        if self.predecessor_edges:
            self.predecessor_edges = temp_predecessor_edges
        self.n -= 1

    def check_solution(self, distances):
        """
        -----------------------------------------------------------------
        Method to check whether a solution works on the target STN or not
        ------------------------------------------------------------------
        Input:
            stn, the target STN
            distances, a list of integers representing the time at which each index is executed

        Output:
            works, a boolean that is true if the solution is valid and false otherwise.

        """
        for node_idx, distance in enumerate(distances):
            for successor_idx, edge_weight in self.successor_edges[node_idx].items():
                if distances[successor_idx] - distance > edge_weight:
                    return False
        return True

    def populate_predecessor_edges(self):
        if self.predecessor_edges is not None:
            return
        self.predecessor_edges = [{} for _ in range(self.n)]
        for node_idx, edge_dict in enumerate(self.successor_edges):
            for successor_idx, weight in edge_dict.items():
                self.predecessor_edges[successor_idx][node_idx] = weight
