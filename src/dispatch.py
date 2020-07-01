from johnson import Johnson
from bellman_ford import BellmanFord
from tarjan import Tarjan
from dijkstra import Dijkstra
from collections import deque
from copy import deepcopy
from random import random, randint
from floyd_warshall import FloydWarshall
from stn import STN
import heapq


class Dispatch:

    @staticmethod
    def fast_dispatch(network):
        # O(N^2 log N) time, O(N) extra space
        potential_function = BellmanFord.bellman_ford_wrapper(network)

        if not potential_function:
            return False

        if not network.predecessor_edges:
            network.populate_predecessor_edges()

        network_num_tps = network.num_tps()
        distance_matrix = [[] for _ in range(network_num_tps)]

        delete_edges = []
        src_idx = potential_function.index(min(potential_function))
        distance_matrix[src_idx] = Dijkstra.dijkstra_wrapper(
            network, src_idx)

        for i in range(network_num_tps):
            for successor_idx, weight in network.successor_edges[i].items():
                if distance_matrix[src_idx][successor_idx] != distance_matrix[src_idx][i] + weight:
                    delete_edges.append((i, successor_idx))

        stn = deepcopy(network)
        for i, successor_idx in delete_edges:
            stn.delete_edge(i, successor_idx)

        rigid_components = Dispatch._tarjan(stn)
        temp_rigid_components = [[] for i in range(len(rigid_components))]
        for idx, rigid_component in enumerate(rigid_components):
            for node in rigid_component:
                temp_rigid_components[idx].append(
                    (potential_function[node], node))
            temp_rigid_components[idx].sort()
        rigid_components = []
        for i in range(len(temp_rigid_components)):
            rigid_components.append([])
            for j in range(len(temp_rigid_components[i])):
                rigid_components[i].append(temp_rigid_components[i][j][1])

        list_of_leaders = []
        for i in range(len(rigid_components)):
            list_of_leaders.append(rigid_components[i][0])

        node_to_leader_map = [None for i in range(network_num_tps)]
        for rigid_component in rigid_components:
            for node_idx in rigid_component:
                node_to_leader_map[node_idx] = rigid_component[0]
        CONTR_G_EDGES = []
        for rigid_component in rigid_components:
            for i in range(len(rigid_component) - 1):
                j = i + 1
                n1 = rigid_component[i]
                n2 = rigid_component[j]

                try:
                    weight = network.successor_edges[n1][n2]
                except:
                    bf = BellmanFord.bellman_ford_wrapper(network, n1)
                    weight = bf[n2]

                CONTR_G_EDGES.append((n1, n2, weight))

        CONTR_G = STN()
        for i in list_of_leaders:
            CONTR_G.insert_new_tp(str(i))

        for node_idx in range(len(list_of_leaders)):
            CONTR_G.successor_edges.append({})
            for successor_idx in range(len(list_of_leaders)):
                if successor_idx == node_idx:
                    continue
                try:
                    if successor_idx in CONTR_G.successor_edges[node_idx]:
                        if CONTR_G.successor_edges[node_idx][successor_idx] < network.successor_edges[node_idx][successor_idx]:
                            continue
                    weight = network.successor_edges[node_idx][successor_idx]
                    # weight = reweight_edge(node_idx, successor_idx)
                    CONTR_G.insert_new_edge(
                        node_idx, successor_idx, weight)
                except:
                    pass

        for node_idx, edge_dict in enumerate(network.successor_edges):
            for successor_idx, weight in edge_dict.items():
                if node_idx not in list_of_leaders:
                    n1 = node_to_leader_map[node_idx]
                    n2 = node_to_leader_map[successor_idx]
                    weight = network.successor_edges[n1][node_idx] + \
                        network.successor_edges[node_idx][successor_idx] + \
                        network.successor_edges[successor_idx][n2]
                    # weight = reweight_edge(
                    #     n1, node_idx) + reweight_edge(node_idx, successor_idx) + reweight_edge(successor_idx, n2)
                    if weight != float("inf") and n1 != n2:
                        if n1 in CONTR_G.successor_edges and n2 in CONTR_G.successor_edges[n1]:
                            if CONTR_G.successor_edges[n1][n2] > weight:
                                CONTR_G.successor_edges[n1][n2] = weight
                        else:
                            CONTR_G.insert_new_edge(n1, n2, weight)

        distance_matrix = [[] for x in range(len(list_of_leaders))]

        delete_edges = set()
        for A in list_of_leaders:
            distance_matrix[A] = Dijkstra.dijkstra_wrapper(
                CONTR_G, A, potential_function=potential_function, dispatch=True)
            listy = []
            for idx, val in CONTR_G.successor_edges[A].items():
                weight = min(distance_matrix[A][idx], val)
                CONTR_G.successor_edges[A][idx] = weight
                listy.append((weight, idx))
            listy.sort(reverse=True)
            for i, (_, node_idx) in enumerate(listy):
                listy[i] = node_idx
            stn = deepcopy(CONTR_G)
            marked_edges = []
            for node_idx, edge_dict in enumerate(stn.successor_edges):
                for successor_idx, weight in edge_dict.items():
                    if distance_matrix[A][successor_idx] != distance_matrix[A][node_idx] + weight:
                        marked_edges.append((node_idx, successor_idx))
            for node_idx, successor_idx in marked_edges:
                stn.delete_edge(node_idx, successor_idx)
            stn.populate_predecessor_edges()
            marked_edges = []
            for node_idx, edge_dict in enumerate(stn.predecessor_edges):
                if A == node_idx:
                    continue
                for successor_idx, weight in edge_dict.items():
                    if successor_idx == A or successor_idx == node_idx:
                        continue
                    AC = distance_matrix[A][node_idx]
                    AB = distance_matrix[A][successor_idx]
                    BC = CONTR_G.successor_edges[successor_idx][node_idx]
                    if (AC < 0 and AB < 0) or (AC >= 0 and BC >= 0):
                        if AB + BC == AC:
                            delete_edges.add((A, node_idx))

        for node_idx, successor_idx in delete_edges:
            CONTR_G.delete_edge(node_idx, successor_idx)

        DISPATCHABLE_STN = STN()
        for name in network.names_list:
            DISPATCHABLE_STN.successor_edges.append({})
            DISPATCHABLE_STN.insert_new_tp(name)

        for node_idx, edge_dict in enumerate(CONTR_G.successor_edges):
            for successor_idx, weight in edge_dict.items():
                if node_idx == successor_idx:
                    continue
                else:
                    DISPATCHABLE_STN.insert_new_edge(
                        node_idx, successor_idx, weight)

        for node_idx, successor_idx, weight in CONTR_G_EDGES:
            DISPATCHABLE_STN.insert_new_edge(node_idx, successor_idx, weight)
            DISPATCHABLE_STN.insert_new_edge(successor_idx, node_idx, -weight)

        return DISPATCHABLE_STN

    @ staticmethod
    def _tarjan(network):
        t = Tarjan(network)
        return t.tarjan()

    @staticmethod
    def slow_dispatch(network):
        # O(N^3) time, O(N^2) extra space
        if not network.dist_up_to_date and network.distance_matrix:
            pass
        else:
            FloydWarshall.floyd_warshall(network)

        distance_matrix = deepcopy(network.distance_matrix)
        marked_edges = []

        for i in range(network.num_tps()):
            for node_idx, edge_dict in enumerate(network.successor_edges):
                if i == node_idx:
                    continue
                for successor_idx in edge_dict:
                    if i == successor_idx or node_idx == successor_idx:
                        continue
                    AC = distance_matrix[i][node_idx]
                    AB = distance_matrix[i][successor_idx]
                    BC = distance_matrix[successor_idx][node_idx]
                    CB = distance_matrix[node_idx][successor_idx]
                    if (AC < 0 and AB < 0) and (AB >= 0 and CB >= 0):
                        if (i, node_idx) not in marked_edges and (i, successor_idx) not in marked_edges:
                            if random() < 0.5:
                                marked_edges.append((i, node_idx))
                            else:
                                marked_edges.append((i, successor_idx))
                    if (AC >= 0 and BC >= 0) and (AB < 0 and AC < 0):
                        if (i, node_idx) not in marked_edges and (i, successor_idx) not in marked_edges:
                            if random() < 0.5:
                                marked_edges.append((i, node_idx))
                            else:
                                marked_edges.append((i, successor_idx))
                    elif (AC < 0 and AB < 0) or (AC >= 0 and BC >= 0):
                        if (i, node_idx) not in marked_edges and (i, successor_idx) not in marked_edges:
                            if AB + BC == AC:
                                marked_edges.append((i, node_idx))
                    elif (AB < 0 and AC < 0) or (AB >= 0 and CB >= 0):
                        if (i, node_idx) not in marked_edges and (i, successor_idx) not in marked_edges:
                            if AC + CB == AB:
                                marked_edges.append((i, successor_idx))
        print(marked_edges)
        for node_idx, succ_idx in marked_edges:
            if succ_idx in network.successor_edges[node_idx]:
                network.delete_edge(node_idx, succ_idx)

        return network

    @ staticmethod
    def _intersecting_edges(leader, child_array):
        intersecting_edges = []
        for i in child_array:
            for j in child_array:
                if i == j or i == leader or j == leader:
                    continue
                intersecting_edges.append(((leader, i), j))
        return intersecting_edges
