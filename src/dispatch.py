from johnson import Johnson
from bellman_ford import BellmanFord
from tarjan import Tarjan
from dijkstra import Dijkstra
from collections import deque
from copy import deepcopy
from random import random


class Dispatch:

    @staticmethod
    def fast_dipsatch(network):
        # O(N^2 log N) time, O(N) extra space

        distance_matrix = [[] for x in range(network.length)]

        potential_function = BellmanFord.bellman_ford(network)

        if not potential_function:
            return False

        # [0, 0, 0, 3, 4, 4, 4, 3]

        rigid_components = Dispatch._tarjan(network)

        contracted_graphs = set(rigid_components)

        def _dfs(graph, idx):
            for succ in network.successor_edges[idx]:
                if not succ in visited:
                    _dfs(graph, succ)
            visited.add(idx)
            order.append(idx)

        for src_idx in contracted_graphs:
            predecessor_graph = Dijkstra.dijkstra(
                network, src_idx, potential_function=potential_function)
            visited = set()
            order = []
            _dfs(predecessor_graph, src_idx)
            order = order[::-1]

        return distance_matrix

    @staticmethod
    def _tarjan(network):
        t = Tarjan(network)
        return t.tarjan()

    @staticmethod
    def convert_to_dispatchable(network):
        # O(N^3) time, O(N^2) extra space
        if not network.flag and network.distance_matrix:
            pass
        else:
            Johnson.johnson(network)

        distance_matrix = deepcopy(network.distance_matrix)
        marked_edges = []

        intersecting_edges = Dispatch._get_intersecting_edges(network)

        for (src_idx, middle_idx), target_idx in intersecting_edges:
            D_A_B = distance_matrix[src_idx][middle_idx] + \
                distance_matrix[middle_idx][target_idx]
            D_C = distance_matrix[src_idx][target_idx]
            D_A = distance_matrix[src_idx][middle_idx]
            D_C_B = distance_matrix[src_idx][target_idx] + \
                distance_matrix[middle_idx][target_idx]
            if D_A_B == D_C and D_A == D_C_B:
                if (src_idx, target_idx) not in marked_edges and (src_idx, middle_idx) not in marked_edges:
                    if random() < 0.5:
                        marked_edges.append((src_idx, target_idx))
                    else:
                        marked_edges.append((src_idx, middle_idx))
            else:
                if D_A_B == D_C:
                    marked_edges.append((src_idx, target_idx))
                if D_A == D_C_B:
                    marked_edges.append((src_idx, middle_idx))

        for node_idx, succ_idx in marked_edges:
            network.delete_edge(node_idx, succ_idx)

        return marked_edges

    @staticmethod
    def _get_intersecting_edges(network):
        length = network.length
        intersecting_edges = []
        for i in range(length):
            for j in range(length):
                for k in range(length):
                    intersecting_edges.append((i, j), k)
        return intersecting_edges
