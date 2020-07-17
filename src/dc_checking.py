from bellman_ford import BellmanFord
from collections import deque
from random import randint
from heapq import heappush, heappop, heapify
from copy import deepcopy


__all__ = ["morris_2014", "cairo_et_al_2018"]


def morris_2014():
    pass


def init_potential(ol_edges):
    N = len(ol_edges)
    potential_function = [0 for _ in range(N)]
    for _ in range(1, N):
        for V, edge_dict in enumerate(ol_edges):
            for W, w in edge_dict.items():
                potential_function[V] = max(
                    potential_function[V], potential_function[W] - w)

    return potential_function


def negative_cycle(network, potential_function):
    for V, edge_dict in enumerate(network.ol_edges):
        for W, w in edge_dict.items():
            if potential_function[V] < (potential_function[W] - w):
                return True
    return False


def apply_relax_lower(network, W, C):
    delta_W_C = network.successor_edges[W][C] if C in network.successor_edges[W] else float(
        "inf")
    edges = set()
    _, x, y, _ = network.contingent_links[C]
    if delta_W_C >= (y - x):
        pass
    elif network.contingent_links[W] != False:
        A_W, x_W, _, _ = network.contingent_links[W]
        edges.add((A_W, x_W + delta_W_C, C))
    else:
        for V, edge_dict in enumerate(network.ol_edges):
            for W, delta_V_W in edge_dict.items():
                if V == C:
                    continue
                edges.add((V, delta_V_W + delta_W_C, C))
    return edges


def close_relax_lower(network, potential_function, C):
    min_heap = []
    for W, edge_dict in enumerate(network.ol_edges):
        for C_prime, delta_W_C in edge_dict.items():
            if C_prime == C:
                heappush(min_heap, (potential_function[W] + delta_W_C, W))
    counter = 0
    while min_heap:
        counter += 1
        print(counter)
        _, W = heappop(min_heap)

        for (V, v, C) in apply_relax_lower(network, W, C):
            curr_VC = network.successor_edges[V][C] if C in network.successor_edges[V] else float(
                "inf")
            if v < curr_VC:
                network.insert_ordinary_edge(V, C, v)
            new_key = potential_function[V] + min(v, curr_VC)

            # use the in_queue trick here as well
            flag = False
            for i, (_, V_prime) in enumerate(min_heap):
                if V_prime == V:
                    flag = True
                    idx = i
                    node = min_heap[idx][1]
                    min_heap.pop(idx)
                    heappush(min_heap, (new_key, node))
                    heapify(min_heap)

            if not flag:
                heappush(min_heap, (new_key, V))
    return network


def apply_upper(network, C):
    A, x, y, C = network.contingent_links[C]
    insert_edges = []
    for V, edge_dict in enumerate(network.ol_edges):
        for C, v in edge_dict.items():
            if A in network.successor_edges[V]:
                original_weight = network.successor_edges[V][A]
            else:
                original_weight = float("inf")
            if v < (y - x):
                new_weight = min(original_weight, -x)
            else:
                new_weight = min(original_weight, v - y)
            insert_edges.append((V, A, new_weight))
    for (V, A, new_weight) in insert_edges:
        network.insert_ordinary_edge(V, A, new_weight)
    return network


def update_potential(network, potential_function, activation_point):
    updated_potential_function = deepcopy(potential_function)
    # do we not need to look at the POPPED_OFF case?
    NOT_YET_IN_QUEUE, IN_QUEUE, POPPED_OFF = 0, 1, 2
    in_queue = [NOT_YET_IN_QUEUE for i in range(len(potential_function))]

    min_heap = []
    heappush(
        min_heap, (updated_potential_function[activation_point], activation_point))
    in_queue[activation_point] = IN_QUEUE

    while min_heap:
        _, Q = heappop(min_heap)
        in_queue[Q] = POPPED_OFF
        for V, edge_dict in enumerate(network.ol_edges):
            for W, w in edge_dict.items():
                if W != Q:
                    continue
                if updated_potential_function[V] < updated_potential_function[W] - w:
                    updated_potential_function[V] = updated_potential_function[W] - w
                    new_key = potential_function[V] - \
                        updated_potential_function[V]
                    if in_queue[V] == IN_QUEUE:
                        for i, (_, node) in enumerate(min_heap):
                            if node == V:
                                idx = i
                        node = min_heap[idx][1]
                        min_heap.pop(idx)
                        heappush(min_heap, (new_key, node))
                        heapify(min_heap)
                    else:
                        heappush(
                            min_heap, (potential_function[V] - updated_potential_function[V], V))
                        in_queue[V] = IN_QUEUE

    return updated_potential_function


def cairo_et_al_2018(network):
    potential_function = init_potential(network.ol_edges)

    if negative_cycle(network, potential_function):
        return False
    contingent_links = network.contingent_links
    S = deque()
    # this idx could have a false, choose in a smarter way
    idx = randint(0, len(contingent_links) - 1)
    while contingent_links[idx] == False:
        idx = randint(0, len(contingent_links) - 1)
    S.append(contingent_links[idx])
    while S:
        # should it be S[0]?
        A, x, y, C = S[-1]
        print("wtf")
        network = close_relax_lower(network, potential_function, C)
        print("one")
        network = apply_upper(network, C)
        print("two")
        # fix the next line
        potential_function = update_potential(
            network, potential_function, A)
        print("wtf")
        if negative_cycle(network, potential_function):
            return False

        # use the in_queue strategy to make this constant time
        # instead of linear time
        flag = False
        for i in range(len(contingent_links)):
            if contingent_links[i] == False:
                continue
            A_prime, _, _, C_prime = contingent_links[i]
            if network.successor_edges[A_prime][C] < y - x:
                flag = True
            if flag:
                for C_alt in S:
                    if C_prime == C_alt:
                        return False

                S.append(contingent_links[C_prime])
        if not flag:
            contingent_links[C] = False
            S.pop()
            if contingent_links and not S:
                S.append(contingent_links[0])

    return True
