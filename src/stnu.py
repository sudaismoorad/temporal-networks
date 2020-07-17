class STNU:

    def __init__(self, successor_edges=True, predecessor_edges=True):
        self.names_dict = {}
        self.names_list = []
        self.successor_edges = [] if successor_edges else None
        self.predecessor_edges = [] if predecessor_edges else None
        self.ou_edges = []
        self.ol_edges = []
        self.contingent_links = []
        self.n = 0
        self.activation_point = []

    def __str__(self):
        """
        ----------------------------------------
        Print method for an STNU object
        ----------------------------------------
        Output:  String representation of the STNU
        ----------------------------------------
        """
        stringy = "STNU:\n"
        stringy += f"Number of nodes in network: {self.n}\n"
        stringy += f"Dictionary of names -> index: {self.names_dict}\n"
        if self.successor_edges:
            stringy += f"Successor edges of each node: {self.successor_edges}\n"
        if self.predecessor_edges:
            stringy += f"Predecessor edges of each node: {self.predecessor_edges}\n"
        stringy += f"Contingent Links: {self.contingent_links}\n"
        stringy += f"Ordinary Lower Edges: {self.ol_edges}\n"
        stringy += f"Ordinary Upper Edges: {self.ou_edges}\n"
        return stringy

    def num_tps(self):
        return self.n

    def insert_ordinary_edge(self, tp1, tp2, weight):
        tp1_idx = self.names_dict[tp1] if type(tp1) == str else tp1
        tp2_idx = self.names_dict[tp2] if type(tp2) == str else tp2

        if self.successor_edges is not None:
            self.successor_edges[tp1_idx][tp2_idx] = int(weight)
        if self.predecessor_edges is not None:
            self.predecessor_edges[tp2_idx][tp1_idx] = int(weight)
        self.ou_edges[tp1_idx][tp2_idx] = int(weight)
        self.ol_edges[tp1_idx][tp2_idx] = int(weight)

    # def insert_or_update_ordinary_edge(self, tp1, tp2, weight):
    #     tp1_idx = self.names_dict[tp1] if type(tp1) == str else tp1
    #     tp2_idx = self.names_dict[tp2] if type(tp2) == str else tp2

    #     if self.successor_edges is not None:
    #         if tp2_idx in self.successor_edges[tp1_idx]:
    #             self.successor_edges[tp1_idx][tp2_idx] = int(weight)
    #         else:
