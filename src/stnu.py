class STNU:

    def __init__(self, successor_edges=True, predecessor_edges=False):
        self.names_dict = {}
        self.names_list = []
        self.successor_edges = [] if successor_edges else None
        self.predecessor_edges = [] if predecessor_edges else None
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
        return stringy

    
