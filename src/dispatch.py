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
        if network.dist_up_to_date and network.distance_matrix:
            pass
        else:
            Johnson.johnson(network)

        potential_function = BellmanFord.bellman_ford_wrapper(network)

        if potential_function == False:
            return False, False

        temp_network = deepcopy(network)

        # populating the successor edges making the network the APSP
        for node_idx, edge_list in enumerate(temp_network.distance_matrix):
            for successor_idx, weight in enumerate(edge_list):
                temp_network.successor_edges[node_idx][successor_idx] = weight

        # if network doesn't have predecessor edges, populate them
        if not temp_network.predecessor_edges:
            temp_network.populate_predecessor_edges()

        temp_network_num_tps = temp_network.num_tps()
        distance_matrix = [[] for _ in range(temp_network_num_tps)]

        # grabbing the source index
        src_idx = potential_function.index(min(potential_function))
        distance_matrix[src_idx] = Dijkstra.dijkstra_wrapper(
            temp_network, src_idx)

        # making predecessor graph for running tarjan on it
        def make_pred_graph(network):
            delete_edges = []
            num_tps = network.num_tps()
            for i in range(num_tps):
                for successor_idx, weight in network.successor_edges[i].items():
                    if distance_matrix[src_idx][successor_idx] != distance_matrix[src_idx][i] + weight:
                        delete_edges.append((i, successor_idx))

            predecessor_graph = deepcopy(network)
            for i, successor_idx in delete_edges:
                predecessor_graph.delete_edge(i, successor_idx)
            return predecessor_graph

        predecessor_graph = make_pred_graph(temp_network)

        # make the rigid components
        rigid_components = Dispatch._tarjan(predecessor_graph)

        # sorting rigid components w.r.t potential function, to get leaders later
        def sort_rigid_components(rigid_components, potential_function):
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
            return rigid_components

        rigid_components = sort_rigid_components(
            rigid_components, potential_function)
        counter = 0
        for rigid_component in rigid_components:
            if len(rigid_component) != 1:
                counter += len(rigid_component) - 1
        print(counter)
        list_of_leaders = []
        for i in range(len(rigid_components)):
            list_of_leaders.append(rigid_components[i][0])

        node_to_leader_map = [None for i in range(temp_network_num_tps)]
        for rigid_component in rigid_components:
            for node_idx in rigid_component:
                node_to_leader_map[node_idx] = rigid_component[0]

        def get_doubly_linked_chain(rigid_components):
            doubly_linked_chain = []
            for rigid_component in rigid_components:
                for i in range(len(rigid_component) - 1):
                    j = i + 1
                    n1 = rigid_component[i]
                    n2 = rigid_component[j]

                    try:
                        weight = temp_network.successor_edges[n1][n2]
                    except:
                        bf = BellmanFord.bellman_ford_wrapper(temp_network, n1)
                        weight = bf[n2]

                    doubly_linked_chain.append((n1, n2, weight))
            return doubly_linked_chain

        doubly_linked_chain = get_doubly_linked_chain(rigid_components)
        print(len(doubly_linked_chain))

        CONTR_G = STN()
        for i in list_of_leaders:
            CONTR_G.insert_new_tp(temp_network.names_list[i])

        for node_idx in range(len(list_of_leaders)):
            CONTR_G.successor_edges.append({})

        for node_idx, edge_dict in enumerate(temp_network.successor_edges):
            for successor_idx, weight in edge_dict.items():
                if node_idx not in list_of_leaders:
                    n1 = node_to_leader_map[node_idx]
                    n2 = node_to_leader_map[successor_idx]
                    weight = temp_network.successor_edges[n1][node_idx] + \
                        temp_network.successor_edges[node_idx][successor_idx] + \
                        temp_network.successor_edges[successor_idx][n2]

                    if weight != float("inf") and n1 != n2:
                        n1 = temp_network.names_list[n1]
                        n2 = temp_network.names_list[n2]
                        n1 = CONTR_G.names_dict[n1]
                        n2 = CONTR_G.names_dict[n2]
                        if n1 in CONTR_G.successor_edges and n2 in CONTR_G.successor_edges[n1]:
                            if CONTR_G.successor_edges[n1][n2] > weight:
                                CONTR_G.successor_edges[n1][n2] = weight
                        else:
                            CONTR_G.insert_new_edge(n1, n2, weight)

        for leader_1 in list_of_leaders:
            for leader_2 in list_of_leaders:
                CONTR_G_index_1 = temp_network.names_list[leader_1]
                CONTR_G_index_2 = temp_network.names_list[leader_2]
                n1 = CONTR_G.names_dict[CONTR_G_index_1]
                n2 = CONTR_G.names_dict[CONTR_G_index_2]
                if n1 == n2:
                    continue
                if n2 in CONTR_G.successor_edges[n1]:
                    weight = min(
                        temp_network.successor_edges[n1][n2], CONTR_G.successor_edges[n1][n2])
                    CONTR_G.successor_edges[n1][n2] = weight
                else:
                    weight = temp_network.successor_edges[n1][n2]
                    if weight == float("inf"):
                        continue
                    CONTR_G.insert_new_edge(
                        CONTR_G_index_1, CONTR_G_index_2, weight)

        distance_matrix = [[] for x in range(len(list_of_leaders))]

        delete_edges = set()
        for A in list_of_leaders:
            A = temp_network.names_list[A]
            A = CONTR_G.names_dict[A]
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
            if node_idx in CONTR_G.successor_edges and successor_idx in CONTR_G.successor_edges[node_idx]:
                CONTR_G.delete_edge(node_idx, successor_idx)

        DISPATCHABLE_STN = STN()
        for name in temp_network.names_list:
            DISPATCHABLE_STN.successor_edges.append({})
            DISPATCHABLE_STN.insert_new_tp(name)

        for node_idx, edge_dict in enumerate(CONTR_G.successor_edges):
            for successor_idx, weight in edge_dict.items():

                node_name = CONTR_G.names_list[node_idx]
                successor_name = CONTR_G.names_list[successor_idx]

                idx_1 = temp_network.names_dict[node_name]
                idx_2 = temp_network.names_dict[successor_name]

                if idx_1 == idx_2:
                    continue
                else:
                    DISPATCHABLE_STN.insert_new_edge(
                        idx_1, idx_2, weight)

        for node_idx, successor_idx, weight in doubly_linked_chain:
            if weight == float("inf"):
                continue
            DISPATCHABLE_STN.insert_new_edge(node_idx, successor_idx, weight)
            DISPATCHABLE_STN.insert_new_edge(successor_idx, node_idx, -weight)

        return DISPATCHABLE_STN, potential_function

    @ staticmethod
    def _tarjan(network):
        t = Tarjan(network)
        return t.tarjan()

    @staticmethod
    def slow_dispatch(network):
        # O(N^3) time, O(N^2) extra space
        if network.dist_up_to_date and network.distance_matrix:
            pass
        else:
            Johnson.johnson(network)

        distance_matrix = network.distance_matrix
        num_tps = network.num_tps()

        marked_edges = [[False for i in range(
            num_tps)] for i in range(num_tps)]

        for i in range(num_tps):
            for node_idx in range(num_tps):
                if i == node_idx:
                    continue
                for successor_idx in range(num_tps):
                    if i == successor_idx or node_idx == successor_idx:
                        continue
                    AC = distance_matrix[i][node_idx]
                    AB = distance_matrix[i][successor_idx]
                    BC = distance_matrix[successor_idx][node_idx]
                    CB = distance_matrix[node_idx][successor_idx]
                    if (AC < 0 and AB < 0 and AB + BC == AC) and (AB >= 0 and CB >= 0 and AC + CB == AB):
                        if not marked_edges[i][node_idx] and not marked_edges[i][successor_idx]:
                            if random() < 0.5:
                                marked_edges[i][node_idx] = True
                            else:
                                marked_edges[i][successor_idx] = True
                    elif (AC >= 0 and BC >= 0 and AB + BC == AC) and (AB < 0 and AC < 0 and AC + CB == AB):
                        if not marked_edges[i][node_idx] and not marked_edges[i][successor_idx]:
                            if random() < 0.5:
                                marked_edges[i][node_idx] = True
                            else:
                                marked_edges[i][successor_idx] = True
                    elif (AC < 0 and AB < 0) or (AC >= 0 and BC >= 0):
                        if not marked_edges[i][node_idx] and not marked_edges[i][successor_idx]:
                            if AB + BC == AC:
                                marked_edges[i][node_idx] = True
                    elif (AB < 0 and AC < 0) or (AB >= 0 and CB >= 0):
                        if not marked_edges[i][successor_idx] and not marked_edges[i][node_idx]:
                            if AC + CB == AB:
                                marked_edges[i][successor_idx] = True

        s = STN()
        s.n = num_tps
        s.names_dict = network.names_dict
        s.names_list = network.names_list

        for i in range(num_tps):
            s.successor_edges.append({})

        for i in range(num_tps):
            for j in range(num_tps):
                if not marked_edges[i][j] and distance_matrix[i][j] != 0 and distance_matrix[i][j] != float("inf"):
                    s.insert_new_edge(i, j, distance_matrix[i][j])

        return s

    @staticmethod
    def luke_dispatch(network):
        # O(N^3) time, O(N^2) extra space
        # compute distance matrix if not already computed and up-to-date
        if network.dist_up_to_date and network.distance_matrix:
            pass
        else:
            Johnson.johnson(network)
        # No need for copy of distance matrix -- it won't change!

        dm = network.distance_matrix
        n = network.num_tps()

        marked = [False]*n

        for i in range(n):
            marked[i] = [False]*n

        for a in range(n):
            for b in range(n):
                if a == b:
                    continue
                for c in range(b+1, n):
                    if a == c or b == c:
                        continue
                    AC = dm[a][c]
                    AB = dm[a][b]
                    BC = dm[b][c]
                    CB = dm[c][b]
                    # Checking triangle with A as source node of neg. edges
                    if not marked[a][c] and not marked[a][b]:
                        if AC < 0 and AB < 0:
                            if AC + CB == AB:
                                marked[a][b] = True
                            if AB + BC == AC:
                                marked[a][c] = True
                            if marked[a][b] and marked[a][c]:
                                if random() < 0.5:
                                    marked[a][b] = False
                                else:
                                    marked[a][c] = False
                    # Checking triangle with A as target of non neg. edges
                    BA = dm[b][a]
                    CA = dm[c][a]
                    if not marked[b][a] and not marked[c][a]:
                        if BA >= 0 and CA >= 0:
                            if BC + CA == BA:
                                marked[b][a] = True
                            if CB + BA == CA:
                                marked[c][a] = True
                            if marked[b][a] and marked[c][a]:
                                if random() < 0.5:
                                    marked[b][a] = False
                                else:
                                    marked[c][a] = False

        s = STN()
        s.n = n
        s.names_dict = network.names_dict
        s.names_list = network.names_list

        for i in range(n):
            s.successor_edges.append({})

        for i in range(n):
            for j in range(n):
                if not marked[i][j] and dm[i][j] != float("inf") and dm[i][j] != 0:
                    s.insert_new_edge(i, j, dm[i][j])

        return s
