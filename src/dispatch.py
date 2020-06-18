from johnson import Johnson
from bellman_ford import BellmanFord
from tarjan import Tarjan
from dijkstra import Dijkstra
from collections import deque
from copy import deepcopy
from random import random
from floyd_warshall import FloydWarshall


class Dispatch:

    @staticmethod
    def fast_dipsatch(network):
        # O(N^2 log N) time, O(N) extra space

        distance_matrix = [[] for x in range(network.length)]

        potential_function = FloydWarshall.floyd_warshall(network)

        if not potential_function:
            return False

        min_leaders = Dispatch._tarjan(network)

        list_of_leaders = set(min_leaders)

        dict_of_children = {}

        for idx, i in enumerate(min_leaders):
            if i in list_of_leaders:
                if i in dict_of_children:
                    dict_of_children[i].append(idx)
                else:
                    dict_of_children[i] = [idx]

        for src_idx in list_of_leaders:
            list_of_distances, predecessor_graph = Dijkstra.dijkstra(
                network, src_idx, potential_function=potential_function, path=True, list_of_leaders=list_of_leaders)

            print(list_of_distances, predecessor_graph)

            # listy = [path from 3 to 0] = [3, 2, 1, 0]
            for listy in predecessor_graph:
                print(listy)
                intersecting_edges = []
                # get intersecting edges
                marked_edges = []
                for (src_idx, middle_idx), target_idx in intersecting_edges:
                    D_A_B = list_of_distances[src_idx][middle_idx] + \
                        list_of_distances[middle_idx][target_idx]
                    D_C = list_of_distances[src_idx][target_idx]
                    D_A = list_of_distances[src_idx][middle_idx]
                    D_C_B = list_of_distances[src_idx][target_idx] + \
                        list_of_distances[target_idx][middle_idx]
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
                    if succ_idx in network.successor_edges[node_idx]:
                        network.delete_edge(node_idx, succ_idx)

        return network

    @ staticmethod
    def _tarjan(network):
        t = Tarjan(network)
        return t.tarjan()

    @ staticmethod
    def convert_to_dispatchable(network):
        # O(N^3) time, O(N^2) extra space
        if not network.dist_up_to_date and network.distance_matrix:
            pass
        else:
            FloydWarshall.floyd_warshall(network)

        distance_matrix = deepcopy(network.distance_matrix)
        marked_edges = []

        intersecting_edges = Dispatch._get_intersecting_edges(network)
        print(intersecting_edges)
        # print(distance_matrix)
        for (src_idx, middle_idx), target_idx in intersecting_edges:
            D_A_B = distance_matrix[src_idx][middle_idx] + \
                distance_matrix[middle_idx][target_idx]
            D_C = distance_matrix[src_idx][target_idx]
            D_A = distance_matrix[src_idx][middle_idx]
            D_C_B = distance_matrix[src_idx][target_idx] + \
                distance_matrix[target_idx][middle_idx]
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
        print(marked_edges)
        for node_idx, succ_idx in marked_edges:
            if succ_idx in network.successor_edges[node_idx]:
                network.delete_edge(node_idx, succ_idx)

        return network

    @ staticmethod
    def _get_intersecting_edges(network):
        length = network.length
        intersecting_edges = []
        arr = []
        for i in range(length):
            for j in range(length):
                if i == j:
                    continue
                for k in range(length):
                    if k == i or k == j:
                        continue
                    if sorted([i, j]) in arr:
                        continue
                    arr.append(sorted([i, j]))
                    intersecting_edges.append(((i, j), k))
        return intersecting_edges
