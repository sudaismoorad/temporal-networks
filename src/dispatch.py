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

# =============================
#  FILE:    dispatch.py
#  AUTHOR:  Sudais Moorad / Muhammad Furrukh Asif
#  DATE:    June 2020
# =============================

def make_pred_graph(network, distances):
    num_tps = network.num_tps()

    predecessor_graph = STN()
    predecessor_graph.n = network.n
    predecessor_graph.names_list = network.names_list
    predecessor_graph.names_dict = network.names_dict

    predecessor_graph.successor_edges = [{} for _ in range(num_tps)]

    for node_idx in range(num_tps):
        for successor_idx, weight in network.successor_edges[node_idx].items():
            if distances[successor_idx] == distances[node_idx] + weight:
                predecessor_graph.insert_new_edge(
                    node_idx, successor_idx, weight)

    return predecessor_graph


def tarjan(network, potential_function):
    t = Tarjan(network)
    unsorted_rigid_components = t.tarjan()

    rigid_components = sort_rigid_components(
        unsorted_rigid_components, potential_function)

    return rigid_components


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
    # print(rigid_components)
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


def connect_leaders(network, list_of_leaders, rigid_components, potential_function):
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
            n1 = node_to_leader_map[node_idx]
            n2 = node_to_leader_map[successor_idx]
            # U ---W--> V
            # L(U) ---W'--> L(V); W' = D(L(U), U) + W + D(V, L(V))
            D_U = potential_function[node_idx] - potential_function[n1]
            weight = network.successor_edges[node_idx][successor_idx]
            D_V = potential_function[n2] - \
                potential_function[successor_idx]

            weight = D_U + weight + D_V

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

    for node_idx in contracted_graph.successor_edges:
        for successor_idx in contracted_graph.successor_edges:
            pass
    
    return contracted_graph


def creating_dispatchable_stn(network, contracted_graph, doubly_linked_chain):
    DISPATCHABLE_STN = STN()
    for name in network.names_list:
        DISPATCHABLE_STN.successor_edges.append({})
        DISPATCHABLE_STN.insert_new_tp(name)

    # Adding all edges of the contracted graph
    for node_idx, edge_dict in enumerate(contracted_graph.successor_edges):
        for successor_idx, weight in edge_dict.items():

            node_name = contracted_graph.names_list[node_idx]
            successor_name = contracted_graph.names_list[successor_idx]

            idx_1 = network.names_dict[node_name]
            idx_2 = network.names_dict[successor_name]

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


def marker(stn, src, dist):

    n = stn.num_tps()
    mark = [False for _ in range(n)]
    visited = [False for _ in range(n)]
    pred_graph = make_pred_graph(stn, dist)
    # print(f"PredGraph: {pred_graph}\n")
    LOOKING_FOR_NEG = 0
    FOUND_NEG = 1
    queue = deque()
    for succ in pred_graph.successor_edges[src]:
        queue.append((succ, LOOKING_FOR_NEG, float("inf")))

    while queue:
        x, phase, min_so_far = queue.pop()
        # print("Popped: ", x, ", phase: ", phase, ", min: ", min_so_far)
        # case 1:  phase switch
        if phase == LOOKING_FOR_NEG and dist[x] < 0:
            phase = FOUND_NEG
            # print("Changed phase to found_neg!")
        # case 2:  lower dominated
        elif phase == FOUND_NEG and dist[x] < 0:
            mark[x] = True
            # print("Marked X (lower)!")
        # case 3:  upper dominated
        elif min_so_far <= dist[x] and dist[x] >= 0 and src != x:
            mark[x] = True
            # print("Marked X (upper)!")
        # all other cases do nothing, so ignore
        # Prepare for next iteration
        if visited[x] == False:
            # print("Changing visited X to False!")
            visited[x] = True
            for y in pred_graph.successor_edges[x]:
                queue.append((y, phase, min(dist[x], min_so_far)))
    # after the while loop
    # for x in range(n):
    #     if mark[x] == True:
    #         print(f"{x} is marked!\n")
    #     else:
    #         pass
    #         print(f"{x} is unmarked...\n")
    return mark


class Dispatch:

    @staticmethod
    def test_on_contracted(network):
        potential_function = BellmanFord.bellman_ford_wrapper(network)

        if potential_function == False:
            return False

        # grabbing the source index
        # this does not need to be a matrix
        src_idx = potential_function.index(min(potential_function))

        distances = Dijkstra.dijkstra_wrapper(
            network, src_idx)
       
        # making predecessor graph for running tarjan on it
        predecessor_graph = make_pred_graph(
            network, distances)
        # print("predecessor_graph: ", predecessor_graph)
        # tarjan returns sorted rigid components
        rigid_components = tarjan(
            predecessor_graph, potential_function)
       
        # making a list of leaders
        list_of_leaders = []
        for i in range(len(rigid_components)):
            list_of_leaders.append(rigid_components[i][0])
        # Creating the contracted graph with the only time-points being the leader
        # For every edge going from an RC to another RC, an equivalent edge is
        # inserted from one leader to another
        CONTR_G = connect_leaders(
            network, list_of_leaders, rigid_components, potential_function)

        stn1 = deepcopy(CONTR_G)
        stn2 = deepcopy(CONTR_G)

        fast = Dispatch.fast_dispatch(stn1)
        luke = Dispatch.luke_dispatch(stn2)

        return fast, luke

    @staticmethod
    def fast_dispatch(network):
        # O(N^2 log N) time, O(N) extra space

        potential_function = BellmanFord.bellman_ford_wrapper(network)

        if potential_function == False:
            return False

        # grabbing the source index
        # this does not need to be a matrix
        src_idx = potential_function.index(min(potential_function))
        # print("pf: ", potential_function)
        # print(src_idx)
        distances = Dijkstra.dijkstra_wrapper(
            network, src_idx)
        # print("d: ", distances)
        # making predecessor graph for running tarjan on it
        predecessor_graph = make_pred_graph(
            network, distances)
        # print("pg: ", predecessor_graph)
        # print("predecessor_graph: ", predecessor_graph)
        # tarjan returns sorted rigid components
        rigid_components = tarjan(
            predecessor_graph, potential_function)
        # print("rigid: ", rigid_components)
        # making a list of leaders
        list_of_leaders = []
        for i in range(len(rigid_components)):
            list_of_leaders.append(rigid_components[i][0])
        # print("list_of_leaders: ", list_of_leaders)
        # creating the doubly linked chain
        doubly_linked_chain = get_doubly_linked_chain(
            rigid_components, network)
        # print("doubly_linked_chain: ", doubly_linked_chain)
        # Creating the contracted graph with the only time-points being the leader
        # For every edge going from an RC to another RC, an equivalent edge is
        # inserted from one leader to another
        CONTR_G = connect_leaders(
            network, list_of_leaders, rigid_components, potential_function)
        # print("yay: ", CONTR_G)
        # For every leader A
        for A in list_of_leaders:
            # Get the index of A in the contracted graph
            A = network.names_list[A]
            A = CONTR_G.names_dict[A]

            # Run dijkstra to get the list of distances from the leader A
            distances = Dijkstra.dijkstra_wrapper(
                CONTR_G, A)

            for idx, val in CONTR_G.successor_edges[A].items():
                weight = min(distances[idx], val)
                CONTR_G.successor_edges[A][idx] = weight

            mark = marker(
                CONTR_G, A, distances)
            # print(A, delete_edges)
            # Delete the marked dominating edges
            for i in range(CONTR_G.num_tps()):
                if i == A or distances[i] == float("inf"):
                    continue
                    # need more information here
                if mark[i] == False:
                    CONTR_G.insert_new_edge(A, i, distances[i])
                elif i in CONTR_G.successor_edges[A]:
                    CONTR_G.delete_edge(A, i)

        # Creating the final dispatchable stn with original time-points
        DISPATCHABLE_STN = creating_dispatchable_stn(
            network, CONTR_G, doubly_linked_chain)

        return DISPATCHABLE_STN

    @ staticmethod
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
                    BA = distance_matrix[B][A]
                    if not marked_edges[A][C] and not marked_edges[B][C]:
                        if AC >= 0 and BC >= 0 and AB + BC == AC and BA + AC == BC:
                            if random() < 0.5:
                                marked_edges[A][C] = True
                            else:
                                marked_edges[B][C] = True
                        elif AC >= 0 and BC >= 0 and AB + BC == AC:
                            marked_edges[A][C] = True
                        elif AC >= 0 and BC >= 0 and BA + AC == BC:
                            marked_edges[B][C] = True
                    if not marked_edges[A][C] and not marked_edges[A][B]:
                        if AC < 0 and AB < 0 and AB + BC == AC and AC + CB == AB:
                            if random() < 0.5:
                                marked_edges[A][C] = True
                            else:
                                marked_edges[A][B] = True
                        elif AC < 0 and AB < 0 and AB + BC == AC:
                            marked_edges[A][C] = True
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

    @ staticmethod
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
