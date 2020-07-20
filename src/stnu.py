import matplotlib.pyplot as plt
import networkx as nx


class STNU:

    def __init__(self, successor_edges=True, predecessor_edges=True):
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
        successor_edges : List[Dict[index:weight]]
            A list of dicts of ordinary edges. The list at index i of this attribute is
            the list of edges of the i-th node. Each edge is represented by a tuple - the
            first element of the tuple is the j-th node that the i-th node is connected to
            and the second element is the weight/distance between the i-th and j-th nodes
        n : int
            Number of nodes in the STN
        ou_edges : List[Dict[index:weight]]
            A list of dicts of ordinary and upper-case edges
        ol_edges : List[Dict[index:weight]]
            A list of dicts of ordinary and lower-case edges
        contingent_links: List[4-Tuple(A, x, y, C)]
            A list of contingent links. C is the contingent time point, A is its activation
            time point, x is the lower case edge weight and y is the upper case edge weight
        activation_point: List[List[Boolean]]
            activation_point[i][j] returns True if i is the activation point of j;
            otherwise it returns False
        ---------------------------------------------------
        """
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

    def visualize(self):
        # need to add contingent links
        G = nx.DiGraph()
        G.add_nodes_from(self.names_list)

        ordinary_edges, lower_edges, upper_edges = [], [], []
        for node_idx, edge_dict in enumerate(self.successor_edges):
            for successor_idx, weight in edge_dict.items():
                G.add_edge(
                    self.names_list[node_idx], self.names_list[successor_idx], weight=weight)
                ordinary_edges.append(
                    (self.names_list[node_idx], self.names_list[successor_idx]))

        for i in range(len(self.contingent_links)):
            if self.contingent_links[i] == False:
                continue
            activation_point, x, y, contingent_point = self.contingent_links[i]
            G.add_edge(self.names_list[activation_point],
                       self.names_list[contingent_point], weight=x)
            G.add_edge(self.names_list[contingent_point],
                       self.names_list[activation_point], weight=-y)
            lower_edges.append(
                (self.names_list[activation_point], self.names_list[contingent_point]))
            upper_edges.append(
                (self.names_list[contingent_point], self.names_list[activation_point]))

        pos = nx.shell_layout(G)
        nx.draw_networkx_nodes(G, pos, node_size=700)
        nx.draw_networkx_edges(G, pos, arrowstyle="->",
                               edgelist=ordinary_edges, connectionstyle='arc3, rad = 0.1', arrowsize=20, width=3, edge_color='r', alpha=0.5)
        nx.draw_networkx_edges(G, pos, arrowstyle="->",
                               edgelist=lower_edges, arrowsize=20, width=2, connectionstyle='arc3, rad = 0.1', edge_color='b', style="dashed", alpha=1)
        nx.draw_networkx_edges(G, pos, arrowstyle="->",
                               edgelist=upper_edges, arrowsize=20, width=2, connectionstyle='arc3, rad = 0.1', edge_color='g', style="dashed", alpha=1)
        labels = nx.get_edge_attributes(G, 'weight')
        nx.draw_networkx_edge_labels(G, pos, edge_labels=labels, label_pos=0.3)
        nx.draw_networkx_labels(G, pos, font_size=20, font_family='sans-serif')

        plt.axis('off')
        plt.show()
