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
    def fast_dispatch(network):
        # O(N^2 log N) time, O(N) extra space
        potential_function = BellmanFord.bellman_ford_wrapper(network)
        if not potential_function:
            return False

        if not network.predecessor_edges:
            network.populate_predecessor_edges()

        network_num_tps = network.num_tps()
        distance_matrix = [[] for _ in range(network_num_tps)]

        rigid_components = Dispatch._tarjan(network)

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

        CONTR_G_EDGES = []
        for rigid_component in rigid_components:
            for i in range(len(rigid_component) - 1):
                j = i + 1
                n1 = rigid_component[i]
                n2 = rigid_component[j]
                # weight..... do we need reweighted edges for this???
                weight = network.successor_edges[n1][n2] + \
                    potential_function[n1] - potential_function[n2]
                CONTR_G_EDGES.append((n1, n2, weight))
        print(CONTR_G_EDGES)

        CONTR_G = STN()
        for i in list_of_leaders:
            CONTR_G.insert_new_tp(i)
        print(CONTR_G)

        for node_idx, edge_dict in enumerate(network.successor_edges):
            for successor_idx, weight in edge_dict:
                if node_idx not in list_of_leaders:
                    pass

    @staticmethod
    def old_fast_dispatch(network):
        # O(N^2 log N) time, O(N) extra space

        potential_function = BellmanFord.bellman_ford_wrapper(network)
        if not potential_function:
            return False
        else:
            # \hat{w}, not network.successor_edges -- use this in dijkstra as well
            for node_idx, dict_of_edges in enumerate(network.successor_edges):
                for _, (successor_idx, weight) in enumerate(dict_of_edges.items()):
                    network.successor_edges[node_idx][successor_idx] = weight + \
                        potential_function[node_idx] - \
                        potential_function[successor_idx]
        if not network.predecessor_edges:
            network.populate_predecessor_edges()

        distance_matrix = [[] for x in range(network.num_tps())]

        rigid_components = Dispatch._tarjan(network)
        # rigid_components = [0, 0, 2, 3, 3, 3]

        list_of_leaders = set(rigid_components)
        # list_of_leaders = [0, 2, 3]

        dict_of_children = {}

        for idx, i in enumerate(rigid_components):
            if i in dict_of_children:
                dict_of_children[i].append(idx)
            else:
                dict_of_children[i] = [i]
        # replacing edges from children to nodes outside RC with edges from leader
        # to the outisde nodes
        marked_edges = []
        insert_edges = []
        for i in range(network.num_tps()):
            leader = rigid_components[i]
            if leader == i:
                continue
            for j in network.successor_edges[i]:
                if j not in dict_of_children[leader] and leader != j:
                    weight = network.successor_edges[i][leader] + \
                        network.successor_edges[leader][j]
                    if j in network.successor_edges[leader]:
                        network.successor_edges[leader][j] = weight
                    else:
                        insert_edges.append((leader, j, weight))
                    if (i, j) not in marked_edges:
                        marked_edges.append((i, j))
            for j in network.predecessor_edges[i]:
                if i not in dict_of_children[leader] and leader != i:
                    weight = network.predecessor_edges[j][leader] + \
                        network.predecessor_edges[leader][i]
                    if i in network.predecessor_edges[leader]:
                        network.predecessor_edges[leader][i] = weight
                    else:
                        insert_edges.append((leader, i, weight))
                    if (j, i) not in marked_edges:
                        marked_edges.append((j, i))

        for node_idx, successor_idx, weight in insert_edges:
            network.insert_new_edge(node_idx, successor_idx, weight)
        for child, successor_idx in marked_edges:
            network.delete_edge(child, successor_idx)

        temp_network = deepcopy(network)
        for node_idx in range(network.num_tps()):
            if node_idx not in list_of_leaders:
                for successor_idx in network.successor_edges[node_idx]:
                    temp_network.delete_edge(node_idx, successor_idx)

        for leader in list_of_leaders:
            # dict_of_children[leader] would give us the RC
            # run dijksra on this to find the shortest path
            RC_distances = Dijkstra.dijkstra_(
                network, dict_of_children[leader], leader)

            RC_order = []
            for idx, distance in enumerate(RC_distances):
                RC_order.append((distance, idx))
            RC_order.sort()

            for i in range(len(RC_order)):
                length = len(RC_order)
                j = (i + 1) % length

                weight = RC_order[j][0] - RC_order[i][0]
                node_1 = RC_order[i][1]
                node_2 = RC_order[j][1]
                temp_network.insert_new_edge(node_1, node_2, weight)
                temp_network.insert_new_edge(node_2, node_1, -weight)

        network = temp_network
        num_tps = network.num_tps()
        distance_matrix = [[] for x in range(num_tps)]
        predecessor_graphs = [[] for _ in range(num_tps)]
        for node_idx in range(network.num_tps()):
            distance_matrix[node_idx], predecessor_graphs[node_idx] = Dijkstra.dijkstra_wrapper(
                network, node_idx, dispatch=True)

        # for node_idx in range(network.num_tps()):
            for successor_idx, weight in network.successor_edges[node_idx].items():
                # we have not populated distance_matrix[successor_idx] yet so we can not
                # modify the predecessor edges, took care of this at the end of this algorithm
                # an alternative to this would be to populate distance matrix first and then
                # running this part of the algorithm (just uncomment line 112, and comment out last 2 lines)
                # the alternative is definitely faster
                network.successor_edges[node_idx][successor_idx] = weight + \
                    distance_matrix[node_idx][successor_idx] - \
                    distance_matrix[node_idx][node_idx]

            marked_edges = []

            for successor_idx, weight in network.successor_edges[node_idx].items():
                if weight >= 0:
                    if node_idx == successor_idx:
                        continue
                    for successor_idx_2, weight_2 in network.successor_edges[node_idx].items():
                        if successor_idx_2 == successor_idx or successor_idx_2 == node_idx:
                            continue
                        else:
                            if distance_matrix[node_idx][successor_idx_2] <= distance_matrix[node_idx][successor_idx]:
                                # predecessor_graphs = [3, 2, 1, 0] (3->0, 3->1, 3->2, 2->1, 2->0, 1->0)
                                if successor_idx_2 in predecessor_graphs[node_idx] and successor_idx in predecessor_graphs[node_idx] and predecessor_graphs[node_idx].index(successor_idx) < predecessor_graphs[node_idx].index(successor_idx_2):
                                    marked_edges.append(
                                        (node_idx, successor_idx))
                elif weight < 0:
                    if node_idx == successor_idx:
                        continue
                    for successor_idx_2, weight_2 in enumerate(distance_matrix[node_idx]):
                        if successor_idx_2 == successor_idx or successor_idx_2 == node_idx:
                            continue
                        else:
                            if weight_2 < 0 and successor_idx_2 in predecessor_graphs[node_idx] and successor_idx in predecessor_graphs[node_idx] and predecessor_graphs[node_idx].index(successor_idx) < predecessor_graphs[node_idx].index(successor_idx_2):
                                marked_edges.append((node_idx, successor_idx))

            for node_idx, succ_idx in marked_edges:
                if succ_idx in network.successor_edges[node_idx]:
                    network.delete_edge(node_idx, succ_idx)

        # predecessor edges recalculated (if you uncomment line 122, commment out the next 2 lines)
        network.predecessor_edges = None
        network.populate_predecessor_edges()

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
