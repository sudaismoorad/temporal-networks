from johnson import Johnson
from bellman_ford import BellmanFord
from tarjan import Tarjan
from dijkstra import Dijkstra
from collections import deque
from copy import deepcopy
from random import random
from floyd_warshall import FloydWarshall
from stn import STN


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

        dict_of_children = {}

        # min_leaders => [0,0,2,3,3]
        # list_of_leaders => [0,2,3]
        # dict_of_children => {0:[1], 2:[], 3:[4]}
        for idx, i in enumerate(min_leaders):
            if idx == i:
                continue
            if i in dict_of_children:
                dict_of_children[i].append(idx)
            else:
                dict_of_children[i] = []

        intersecting_edges = [[] for i in dict_of_children]
        for i in dict_of_children:
            intersecting_edges[i] = Dispatch._intersecting_edges(
                i, dict_of_children[i])

        CONTR_G = STN()
        CONTR_G.n = network.num_tps()
        CONTR_G.successor_edges = []
        for _ in range(CONTR_G.num_tps()):
            CONTR_G.successor_edges.append({})
        # connecting all rigid components
        for leader_idx in dict_of_children:
            for successor_idx in dict_of_children[leader_idx]:
                CONTR_G.successor_edges[leader_idx][successor_idx] = network.successor_edges[leader_idx][successor_idx]
                for successor_idx_2 in dict_of_children[leader_idx]:
                    if successor_idx == successor_idx_2:
                        continue
                    elif successor_idx_2 in network.successor_edges[successor_idx].keys():
                        CONTR_G.successor_edges[successor_idx][successor_idx_2] = network.successor_edges[successor_idx][successor_idx_2]
        # connecting all leaders to one another
        for leader_idx_1 in dict_of_children:
            for leader_idx_2 in dict_of_children:
                if leader_idx_1 == leader_idx_2:
                    continue
                if leader_idx_2 not in network.successor_edges[leader_idx_1]:
                    continue
                CONTR_G.successor_edges[leader_idx_1][leader_idx_2] = network.successor_edges[leader_idx][leader_idx]

        print(f"CONTR_G {CONTR_G}")

        distance_matrix = [[] for x in range(len(list_of_leaders))]
        predecessor_graphs = [[] for _ in range(len(list_of_leaders))]
        print(list_of_leaders)
        for src_idx in list_of_leaders:
            distance_matrix[src_idx], predecessor_graphs[src_idx] = Dijkstra.dijkstra_wrapper(
                network, src_idx, potential_function=potential_function, dispatch=True, contr_g=CONTR_G)
            
            print("PG")
            print(predecessor_graphs[src_idx])
            for successor_idx, weight in enumerate(distance_matrix[src_idx]):
                distance_matrix[src_idx][successor_idx] = weight + \
                    potential_function[successor_idx] - \
                    potential_function[src_idx]

            marked_edges = []
            print("DM")
            print(distance_matrix)
            for successor_idx, weight in CONTR_G.successor_edges[src_idx].items():
                if weight >= 0:
                    if src_idx == successor_idx:
                        continue
                    for successor_idx_2, weight_2 in CONTR_G.successor_edges[src_idx].items():
                        if successor_idx_2 == successor_idx or successor_idx_2 == src_idx:
                            continue
                        else:
                            print(src_idx)
                            print(successor_idx)
                            print(successor_idx_2)
                            print("------")
                            if distance_matrix[src_idx][successor_idx_2] <= distance_matrix[src_idx][successor_idx]:
                                if distance_matrix[src_idx][successor_idx] == distance_matrix[src_idx][successor_idx_2] + network.successor_edges[successor_idx_2][successor_idx]:
                                    print("yes")
                                    marked_edges.append((src_idx, successor_idx))
                elif weight < 0:
                    if src_idx == successor_idx:
                        continue
                    for successor_idx_2, weight_2 in enumerate(distance_matrix[src_idx]):
                        if successor_idx_2 == successor_idx or successor_idx_2 == src_idx:
                            continue
                        else:
                            print(src_idx)
                            print(successor_idx)
                            print(successor_idx_2)
                            print("------")
                            if weight_2 < 0 and distance_matrix[src_idx][successor_idx] == distance_matrix[src_idx][successor_idx_2] + network.successor_edges[successor_idx_2][successor_idx]:
                                print("yes")
                                marked_edges.append((src_idx, successor_idx))


            # for (src_idx, middle_idx), target_idx in intersecting_edges[src_idx]:
            #     D_A_B = distance_matrix[src_idx][middle_idx] + \
            #         distance_matrix[middle_idx][target_idx]
            #     D_C = distance_matrix[src_idx][target_idx]
            #     D_A = distance_matrix[src_idx][middle_idx]
            #     D_C_B = distance_matrix[src_idx][target_idx] + \
            #         distance_matrix[target_idx][middle_idx]
            #     if D_A_B == D_C and D_A == D_C_B:
            #         if (src_idx, target_idx) not in marked_edges and (src_idx, middle_idx) not in marked_edges:
            #             if random() < 0.5:
            #                 marked_edges.append((src_idx, target_idx))
            #             else:
            #                 marked_edges.append((src_idx, middle_idx))
            #     else:
            #         if D_A_B == D_C:
            #             marked_edges.append((src_idx, target_idx))
            #         if D_A == D_C_B:
            #             marked_edges.append((src_idx, middle_idx))
            # print(marked_edges)
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
        # print(intersecting_edges)
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
        # print(marked_edges)
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
