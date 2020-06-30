from johnson import Johnson
from bellman_ford import BellmanFord
from tarjan import Tarjan
from dijkstra import Dijkstra
from collections import deque
from copy import deepcopy
from random import random, randint
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

        arbitrary_src = randint(0, network_num_tps - 1)
        distances = Dijkstra.dijkstra_wrapper(network, arbitrary_src)
        predecessor_graph = STN()
        predecessor_graph = deepcopy(network)
        
        delete_edges = []
        for node_idx, edge_dict in enumerate(predecessor_graph.successor_edges):
            for successor_idx, weight in edge_dict.items():
                if distances[successor_idx] != distances[node_idx] + weight:
                    delete_edges.append((node_idx, successor_idx))
        
        
        for node_idx, successor_idx in delete_edges:
            predecessor_graph.delete_edge(node_idx, successor_idx)


        
        rigid_components = Dispatch._tarjan(predecessor_graph)
        print("rigid", rigid_components)

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

                weight += potential_function[n1] - potential_function[n2]

                CONTR_G_EDGES.append((n1, n2, weight))

        CONTR_G = STN()
        for i in list_of_leaders:
            CONTR_G.insert_new_tp(str(i))

        for node_idx in range(len(list_of_leaders)):
            CONTR_G.successor_edges.append({})
            CONTR_G.insert_new_edge(node_idx, node_idx, 0)

        def reweight_edge(n1, n2):
            try:
                new_weight = network.successor_edges[n1][n2] + \
                    potential_function[n1] - potential_function[n2]
            except:
                new_weight = float("inf")
            return new_weight

        for node_idx, edge_dict in enumerate(network.successor_edges):
            for successor_idx, weight in edge_dict.items():
                if node_idx not in list_of_leaders:
                    n1 = str(node_to_leader_map[node_idx])
                    n2 = str(node_to_leader_map[successor_idx])
                    weight = reweight_edge(
                        n1, node_idx) + reweight_edge(node_idx, successor_idx) + reweight_edge(successor_idx, n2)
                    if weight != float("inf") and n1 != n2:
                        if n1 in CONTR_G.successor_edges and n2 in CONTR_G.successor_edges[n1]:
                            if CONTR_G.successor_edges[n1][n2] > weight:
                                CONTR_G.successor_edges[n1][n2] = weight
                        else:
                            print(type(n1), type(n2))
                            CONTR_G.insert_new_edge(n1, n2, weight)

        distance_matrix = [[] for x in range(len(list_of_leaders))]
        predecessor_graphs = [[] for _ in range(len(list_of_leaders))]
        CONTR_G = deepcopy(network)
        for leader_idx, leader in enumerate(list_of_leaders):
            distance_matrix[leader_idx], predecessor_graphs[leader_idx] = Dijkstra.dijkstra_wrapper(
                CONTR_G, leader, dispatch=True)
            print("PG", predecessor_graphs[leader_idx])
            marked_edges = []

            for successor_idx, weight in CONTR_G.successor_edges[leader_idx].items():
                if weight >= 0:
                    if leader_idx == successor_idx:
                        continue
                    for successor_idx_2, weight_2 in CONTR_G.successor_edges[leader_idx].items():
                        if successor_idx_2 == successor_idx or successor_idx_2 == leader_idx:
                            continue
                        else:
                            print("t", leader_idx, successor_idx)
                            if distance_matrix[leader_idx][successor_idx_2] <= distance_matrix[leader_idx][successor_idx]:
                                # predecessor_graphs = [3, 2, 1, 0] (3->0, 3->1, 3->2, 2->1, 2->0, 1->0)
                                if successor_idx_2 in predecessor_graphs[leader_idx] and successor_idx in predecessor_graphs[leader_idx] and predecessor_graphs[leader_idx].index(successor_idx) > predecessor_graphs[leader_idx].index(successor_idx_2):
                                    
                                    marked_edges.append(
                                        (leader_idx, successor_idx))
                elif weight < 0:
                    if leader_idx == successor_idx:
                        continue
                    for successor_idx_2, weight_2 in enumerate(distance_matrix[leader_idx]):
                        if successor_idx_2 == successor_idx or successor_idx_2 == leader_idx:
                            continue
                        else:
                            print("j", leader_idx, successor_idx)
                            if weight_2 < 0 and successor_idx_2 in predecessor_graphs[leader_idx] and successor_idx in predecessor_graphs[leader_idx] and predecessor_graphs[leader_idx].index(successor_idx) > predecessor_graphs[leader_idx].index(successor_idx_2):
                                
                                marked_edges.append(
                                    (leader_idx, successor_idx))
            print(marked_edges)    
            for leader_idx, succ_idx in marked_edges:
                # print("pppp", leader_idx, succ_idx)
                if succ_idx in CONTR_G.successor_edges[leader_idx]:
                    CONTR_G.delete_edge(leader_idx, succ_idx)

        print("fuck u", CONTR_G)
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
                for successor_idx, weight in edge_dict.items():
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
