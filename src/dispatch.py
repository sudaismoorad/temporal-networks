from johnson import Johnson
from bellman_ford import BellmanFord
from tarjan import Tarjan
from dijkstra import Dijkstra
from collections import deque, defaultdict
from copy import deepcopy
from random import random
from floyd_warshall import FloydWarshall


class Dispatch:

    @staticmethod
    def fast_dipsatch(network):
        # O(N^2 log N) time, O(N) extra space

        distance_matrix = [[] for x in range(network.num_tps())]

        potential_function = BellmanFord.bellman_ford_wrapper(network)

        if not potential_function:
            return False

        min_leaders = Dispatch._tarjan(network)

        list_of_leaders = set(min_leaders)

        dict_of_children = defaultdict(list)

        # min_leaders => [0,0,2,3,3]
        # list_of_leaders => [0,2,3]
        # dict_of_children => {0:[0,1], 2:[2], 3:[3,4]}
        for idx, i in enumerate(min_leaders):
            #if i in dict_of_children:
            dict_of_children[i].append(idx)
            #else:
            #   dict_of_children[i] = [idx]

        for src_idx in list_of_leaders:
            list_of_distances, predecessor_graph = Dijkstra.dijkstra_wrapper(
                network, src_idx, potential_function=potential_function, path=True, list_of_leaders=dict_of_children[src_idx])

            print(list_of_distances)

            for src_idx, distance_list in enumerate(list_of_distances):
                for successor_idx, weight in enumerate(distance_list):
                    list_of_distances[src_idx][successor_idx] = weight + \
                        potential_function[successor_idx] - \
                        potential_function[src_idx]
            
            # listy = [path from 3 to 0] = [3, 2, 1, 0]
            for listy in predecessor_graph:
                intersecting_edges = Dispatch._intersecting_edges(src_idx, dict_of_children[src_idx])
                print(dict_of_children)
                print(intersecting_edges)
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
                print(marked_edges)
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
        num_tps = network.num_tps()
        intersecting_edges = []
        arr = []
        for i in range(num_tps):
            for j in range(num_tps):
                if i == j:
                    continue
                for k in range(num_tps):
                    if k == i or k == j:
                        continue
                    if sorted([i, j]) in arr:
                        continue
                    arr.append(sorted([i, j]))
                    intersecting_edges.append(((i, j), k))
        return intersecting_edges

    @staticmethod
    def _intersecting_edges(leader, child_array):
        intersecting_edges = []
        for i in child_array:
            for j in child_array:
                if i == j or i == leader or j == leader:
                    continue
                intersecting_edges.append(((leader, i), j))
        return intersecting_edges