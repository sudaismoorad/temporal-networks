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


def mark_dominating_edges(contracted_graph, leader, distances, delete_edges, add_edges):
    
    predecessor_graph = make_pred_graph(contracted_graph, distances)
    print(leader, predecessor_graph)
    LOOKING_FOR_NEGATIVE = 0
    FOUND_NEGATIVE = 1
    num_tps = predecessor_graph.num_tps()
    visited = [False for _ in range(num_tps)]

    for successor_idx in predecessor_graph.successor_edges[leader]:
        phase = LOOKING_FOR_NEGATIVE
        stack = deque()
        for node_idx in predecessor_graph.successor_edges[successor_idx]:
            stack.append((node_idx, successor_idx))
        cur_dist = predecessor_graph.successor_edges[leader][successor_idx]
        min_dist = float("inf")
        prev_node_idx = successor_idx
        while stack:
            node_idx, prev_node_idx = stack.pop()
            cur_dist += predecessor_graph.successor_edges[prev_node_idx][node_idx]

            if phase == FOUND_NEGATIVE and cur_dist < 0:
                if node_idx in contracted_graph.successor_edges[leader]:
                    delete_edges.add(node_idx)
            elif min_dist <= cur_dist and cur_dist >= 0:
                if node_idx in contracted_graph.successor_edges[leader]:
                    delete_edges.add(node_idx)
            elif phase == LOOKING_FOR_NEGATIVE and cur_dist < 0:
                phase = FOUND_NEGATIVE
            # else:
            #     add_edges.add((leader, node_idx, cur_dist))

            min_dist = min(
                min_dist, predecessor_graph.successor_edges[prev_node_idx][node_idx])
            if visited[node_idx]:
                break
            visited[node_idx] = True
            for node_successor_idx in predecessor_graph.successor_edges[node_idx]:
                stack.append((node_successor_idx, node_idx))
    print("add", add_edges)
    print("mark", delete_edges)
    return delete_edges, add_edges


class Dispatch:

    @staticmethod
    def fast_dispatch(network):
        # O(N^2 log N) time, O(N) extra space

        potential_function = BellmanFord.bellman_ford_wrapper(network)

        if potential_function == False:
            return False, False

        # grabbing the source index
        # this does not need to be a matrix
        src_idx = potential_function.index(min(potential_function))
        
        distances = Dijkstra.dijkstra_wrapper(
            network, src_idx)
        

        # making predecessor graph for running tarjan on it
        predecessor_graph = make_pred_graph(
            network, distances)

        # tarjan returns sorted rigid components
        rigid_components = tarjan(
            predecessor_graph, potential_function)

        # making a list of leaders
        list_of_leaders = []
        for i in range(len(rigid_components)):
            list_of_leaders.append(rigid_components[i][0])

        # creating the doubly linked chain
        doubly_linked_chain = get_doubly_linked_chain(
            rigid_components, network)

        # Creating the contracted graph with the only time-points being the leader
        # For every edge going from an RC to another RC, an equivalent edge is
        # inserted from one leader to another
        CONTR_G = connect_leaders(
            network, list_of_leaders, rigid_components, potential_function)

        delete_edges = set()
        add_edges = set()
        # For every leader A
        for A in list_of_leaders:
            # Get the index of A in the contracted graph
            print("leader", A)
            A = network.names_list[A]
            A = CONTR_G.names_dict[A]

            # Run dijkstra to get the list of distances from the leader A
            distances = Dijkstra.dijkstra_wrapper(
                CONTR_G, A)

            for idx, val in CONTR_G.successor_edges[A].items():
                weight = min(distances[idx], val)
                CONTR_G.successor_edges[A][idx] = weight

            delete_edges, add_edges = mark_dominating_edges(
                CONTR_G, A, distances, delete_edges, add_edges)
        
        # Delete the marked dominating edges
        for i in range(CONTR_G.num_tps()):
            if i not in delete_edges:
                if distances[i] != float("inf"):
                    CONTR_G.insert_new_edge(A, i, distances[i])
            else:
                CONTR_G.delete_edge(A, i)

        for node_idx, successor_idx in delete_edges:
            CONTR_G.delete_edge(node_idx, successor_idx)

        # Creating the final dispatchable stn with original time-points
        DISPATCHABLE_STN = creating_dispatchable_stn(
            network, CONTR_G, doubly_linked_chain)

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
