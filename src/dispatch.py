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


def make_pred_graph(network, distances):
    delete_edges = []
    num_tps = network.num_tps()
    predecessor_graph = STN()
    predecessor_graph.n = network.n
    predecessor_graph.names_list = network.names_list
    predecessor_graph.names_dict = network.names_dict
    
    for node_idx in range(num_tps):
        for successor_idx, weight in network.successor_edges[node_idx].items():
            if distances[successor_idx] == distances[node_idx] + weight:
                predecessor_graph.insert_new_edge(node_idx, successor_idx, weight)
    
    return predecessor_graph


def tarjan(network, potential_function):
    t = Tarjan(network)
    rigid_components = t.tarjan()
    rigid_components = sort_rigid_components(
        rigid_components, potential_function)
    distance_matrices = [[] for i in range(len(rigid_components))]
    for idx, RC in enumerate(rigid_components):
        distance_matrices[idx] = [[] for i in range(len(RC))]
        distance_matrices[idx] = Johnson.johnson()

    leader_to_node_distances = [{} for i in range(len(rigid_components))]
    node_to_leader_distances = [{} for i in range(len(rigid_components))]
    for idx, RC in enumerate(rigid_components):
        reverse_RC = RC[::-1]
        node_idx = RC[0]
        reverse_node_idx = reverse_RC[0]
        reverse_current_distance = network.successor_edges[reverse_node_idx][node_idx]
        current_distance = 0
        leader_to_node_distances[idx][node_idx] = current_distance
        node_to_leader_distances[idx][reverse_node_idx] = current_distance
        for reverse_successor_idx in reverse_RC[1:]:
            if reverse_successor_idx == node_idx:
                continue
            reverse_current_distance += network.successor_edges[reverse_successor_idx][reverse_node_idx]
            node_to_leader_distances[idx][reverse_node_idx] = reverse_current_distance
            reverse_node_idx = reverse_successor_idx
        for successor_idx in RC[1:]:
            current_distance += network.successor_edges[node_idx][successor_idx]
            leader_to_node_distances[idx][successor_idx] = current_distance
            node_idx = successor_idx


    return rigid_components, leader_to_node_distances, node_to_leader_distances


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


def get_doubly_linked_chain(rigid_components, APSP):
    doubly_linked_chain = []
    for rigid_component in rigid_components:
        for i in range(len(rigid_component) - 1):
            j = i + 1
            n1 = rigid_component[i]
            n2 = rigid_component[j]

            try:
                weight = APSP.successor_edges[n1][n2]
            except:
                bf = BellmanFord.bellman_ford_wrapper(APSP, n1)
                weight = bf[n2]

            doubly_linked_chain.append((n1, n2, weight))
    return doubly_linked_chain


def connect_leaders(network, list_of_leaders, rigid_components, leader_to_node_distances, node_to_leader_distances):
    # mapping nodes to their leaders
    node_to_leader_map = [None for i in range(network.num_tps())]
    for rigid_component in rigid_components:
        for node_idx in rigid_component:
            node_to_leader_map[node_idx] = rigid_component[0]

    contracted_graph = STN()
    for i in list_of_leaders:
        contracted_graph.insert_new_tp(network.names_list[i])

    for node_idx in range(len(list_of_leaders)):
        contracted_graph.successor_edges.append({})
    for node_idx, edge_dict in enumerate(network.successor_edges):
        for successor_idx, weight in edge_dict.items():
            if node_idx not in list_of_leaders:
                n1 = node_to_leader_map[node_idx]
                n2 = node_to_leader_map[successor_idx]
                # for each edge in the graph
                # U ---W--> V
                # L(U) ---W'--> L(V); W' = D(L(U), U) + W + D(V, L(V))
                # store distances when youre doing tarjan
                weight = leader_to_node_distances[list_of_leaders.index(n1)][node_idx] + \
                    network.successor_edges[node_idx][successor_idx] + \
                    network.successor_edges[successor_idx][n2]

                if weight != float("inf") and n1 != n2:
                    n1 = network.names_list[n1]
                    n2 = network.names_list[n2]
                    n1 = contracted_graph.names_dict[n1]
                    n2 = contracted_graph.names_dict[n2]
                    if n2 in contracted_graph.successor_edges[n1]:
                        if contracted_graph.successor_edges[n1][n2] > weight:
                            contracted_graph.successor_edges[n1][n2] = weight
                    else:
                        contracted_graph.insert_new_edge(n1, n2, weight)

    # Leader to leader edges with minimum weight
    for leader_1 in list_of_leaders:
        for leader_2 in list_of_leaders:
            CONTR_G_index_1 = network.names_list[leader_1]
            CONTR_G_index_2 = network.names_list[leader_2]
            n1 = contracted_graph.names_dict[CONTR_G_index_1]
            n2 = contracted_graph.names_dict[CONTR_G_index_2]
            if n1 == n2:
                continue
            if n2 in contracted_graph.successor_edges[n1]:
                weight = min(
                    network.successor_edges[n1][n2], contracted_graph.successor_edges[n1][n2])
                contracted_graph.successor_edges[n1][n2] = weight
            else:
                weight = network.successor_edges[n1][n2]
                if weight == float("inf"):
                    continue
                contracted_graph.insert_new_edge(
                    CONTR_G_index_1, CONTR_G_index_2, weight)

    return contracted_graph


def postorder(stn, root):
    visited = set()
    order = []

    def dfs_walk(node):
        visited.add(node)
        for successor_idx in stn.successor_edges[node]:
            if successor_idx not in visited:
                dfs_walk(successor_idx)
        order.append(node)
    dfs_walk(root)
    order.reverse()

    return order


def creating_dispatchable_stn(APSP, contracted_graph, doubly_linked_chain):
    DISPATCHABLE_STN = STN()
    for name in APSP.names_list:
        DISPATCHABLE_STN.successor_edges.append({})
        DISPATCHABLE_STN.insert_new_tp(name)

    # Adding all edges of the contracted graph
    for node_idx, edge_dict in enumerate(contracted_graph.successor_edges):
        for successor_idx, weight in edge_dict.items():

            node_name = contracted_graph.names_list[node_idx]
            successor_name = contracted_graph.names_list[successor_idx]

            idx_1 = APSP.names_dict[node_name]
            idx_2 = APSP.names_dict[successor_name]

            if idx_1 == idx_2:
                continue
            else:
                DISPATCHABLE_STN.insert_new_edge(
                    idx_1, idx_2, weight)

    # Adding all the doubly-linked chains
    for node_idx, successor_idx, weight in doubly_linked_chain:
        if weight == float("inf"):
            continue
        DISPATCHABLE_STN.insert_new_edge(node_idx, successor_idx, weight)
        DISPATCHABLE_STN.insert_new_edge(successor_idx, node_idx, -weight)
    return DISPATCHABLE_STN


def leader_pred_graph(CONTR_G, distances):
    predecessor_graph = deepcopy(CONTR_G)
    marked_edges = []
    for node_idx, edge_dict in enumerate(predecessor_graph.successor_edges):
        for successor_idx, weight in edge_dict.items():
            if distances[successor_idx] != distances[node_idx] + weight:
                marked_edges.append((node_idx, successor_idx))
    for node_idx, successor_idx in marked_edges:
        predecessor_graph.delete_edge(node_idx, successor_idx)
    return predecessor_graph


##################################
# pretty sure the problem is here#
##################################
def mark_dominating_edges(leader, APSP, reverse_postorder, distances, delete_edges):
    # check if you have to change indices
    min_dist = float("inf")
    neg_dist_node = False
    for C in reverse_postorder:
        if C == leader:
            continue
        AC = distances[C]
        if AC < 0:
            neg_dist_node = True
        for B in reverse_postorder:
            if B == C:
                break
            if leader == B:
                continue
            AB = distances[B]
            BC = APSP.successor_edges[B][C]
            if neg_dist_node:
                if AB < 0:
                    if AB + BC == AC:
                        delete_edges.add((leader, C))
            else:
                if B == C:
                    continue
                if min_dist <= AC:
                    if AB + BC == AC:
                        delete_edges.add((leader, C))
        min_dist = min(min_dist, AC)
        neg_dist_node = False
    return delete_edges


class Dispatch:

    @staticmethod
    def fast_dispatch(network):
        # O(N^2 log N) time, O(N) extra space

        potential_function = BellmanFord.bellman_ford_wrapper(network)

        if potential_function == False:
            return False, False

        # creating the APSP
        temp_network = network
        num_tps = temp_network.num_tps()

        

        # grabbing the source index
        # this does not need to be a matrix
        src_idx = potential_function.index(min(potential_function))
        distances = Dijkstra.dijkstra_wrapper(
            temp_network, src_idx)

        # making predecessor graph for running tarjan on it
        predecessor_graph = make_pred_graph(
            temp_network, distances)

        # tarjan returns sorted rigid components
        rigid_components, leader_to_node_distances = tarjan(predecessor_graph, potential_function)

        

        # making a list of leaders
        list_of_leaders = []
        for i in range(len(rigid_components)):
            list_of_leaders.append(rigid_components[i][0])

        # creating the doubly linked chain
        doubly_linked_chain = get_doubly_linked_chain(
            rigid_components, temp_network)

        # Creating the contracted graph with the only time-points being the leader
        # For every edge going from an RC to another RC, an equivalent edge is
        # inserted from one leader to another
        CONTR_G = connect_leaders(
            temp_network, list_of_leaders, rigid_components, leader_to_node_distances)

        distance_matrix = [[] for x in range(len(list_of_leaders))]

        delete_edges = set()
        # For every leader A
        for A in list_of_leaders:
            # Get the index of A in the contracted graph
            A = temp_network.names_list[A]
            A = CONTR_G.names_dict[A]

            # Run dijkstra to get the list of distances from the leader A
            distance_matrix[A] = Dijkstra.dijkstra_wrapper(
                CONTR_G, A, potential_function=potential_function, dispatch=True)

            for idx, val in CONTR_G.successor_edges[A].items():
                weight = min(distance_matrix[A][idx], val)
                CONTR_G.successor_edges[A][idx] = weight

            # Creating the predecessor graph
            predecessor_graph = leader_pred_graph(CONTR_G, distance_matrix[A])

            # convert the graph into reverse post-order form
            reverse_postorder = postorder(predecessor_graph, A)

            # add new dominating edges
            delete_edges = mark_dominating_edges(
                A, temp_network, reverse_postorder, distance_matrix[A], delete_edges)

        # Delete the marked dominating edges
        for node_idx, successor_idx in delete_edges:
            CONTR_G.delete_edge(node_idx, successor_idx)

        # Creating the final dispatchable stn with original time-points
        DISPATCHABLE_STN = creating_dispatchable_stn(
            temp_network, CONTR_G, doubly_linked_chain)

        return DISPATCHABLE_STN, potential_function

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

        for A in range(num_tps):
            for C in range(num_tps):
                if A == C:
                    continue
                for B in range(num_tps):
                    if A == B or C == B:
                        continue
                    AC = distance_matrix[A][C]
                    AB = distance_matrix[A][B]
                    BC = distance_matrix[B][C]
                    CB = distance_matrix[C][B]
                    if not marked_edges[A][C] and not marked_edges[A][B]:
                        if AC >= 0 and BC >= 0 and AB + BC == AC and AB >= 0 and CB >= 0 and AC + CB == AB:
                            if random < 0.5:
                                marked_edges[A][C] = True
                            else:
                                marked_edges[A][B] = True
                        elif AC < 0 and AB < 0 and AB + BC == AC and AC + CB == AB:
                            if random() < 0.5:
                                marked_edges[A][C] = True
                            else:
                                marked_edges[A][B] = True
                        elif AC >= 0 and BC >= 0 and AB + BC == AC:
                            marked_edges[A][C] = True
                        elif AC < 0 and AB < 0 and AB + BC == AC:
                            marked_edges[A][C] = True
                        elif AB >= 0 and CB >= 0 and AC + CB == AB:
                            marked_edges[A][B] = True
                        elif AB < 0 and AC < 0 and AC + CB == AB:
                            marked_edges[A][B] = True

        s = STN()
        s.n = num_tps
        s.names_dict = network.names_dict
        s.names_list = network.names_list

        for i in range(num_tps):
            s.successor_edges.append({})

        for i in range(num_tps):
            for j in range(num_tps):
                if not marked_edges[i][j] and i != j and distance_matrix[i][j] != float("inf"):
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
                if not marked[i][j] and dm[i][j] != float("inf") and i != j:
                    s.insert_new_edge(i, j, dm[i][j])

        return s
