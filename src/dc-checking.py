from bellman_ford import BellmanFord
from collections import deque
from random import randint
from heapq import heappush, heappop, heapify
from copy import deepcopy


__all__ = ["morris_2014", "cairo_et_al_2018"]


def morris_2014():
    pass


def init_potential(network):
    N = network.num_tps()
    potential_function = [0 for _ in N]
    for _ in range(1, N):
        for V, w, W in network.lo.items():
            potential_function[V] = max(
                potential_function[V], potential_function[W] - w)
    return potential_function


def negative_cycle(network, potential_function):
    for V, w, W in network.lo:
        if potential_function[V] < (potential_function[W] - w):
            return True
    return False


def apply_relax_lower(network, W, C):
    delta_W_C = network.successor_edges[W][C] if C in network.successor_edges[W] else float(
        "inf")
    edges = set()
    _, x, y, _ = get_everything(C)
    if delta_W_C >= (y - x):
        return edges
    elif W in network.contingent_links:
        return edges
    else:
        return edges


def close_relax_lower(network, potential_function, C):
    heap = []
    for W, delta_W_C, C_prime in network.ordinary_edges:
        if C_prime == C:
            heappush(heap, (potential_function[W] + delta_W_C, W))
    while heap:
        _, W = heappop(heap)
        for V, v, C in apply_relax_lower(network, W, C):
            curr_VC = network.successor_edges[V][C] if C in network.successor_edges[V] else float(
                "inf")
            if v < curr_VC:
                network.insert_ordinary_edge(V, v, C)
            new_key = potential_function[V] + min(v, curr_VC)
            flag = False
            for _, V_prime in heap:
                if V_prime == V:
                    flag = True

                    idx = heap.index(V)
                    heap[idx][0] = new_key
                    heapify(heap)

                    break

            if not flag:
                heappush(new_key, V)
    return network


def apply_upper(network, C):
    A, x, y, C = get_everything(C)
    for V, v, C in network.ordinary_edges:
        original_weight = network.successor_edges[V][A]
        if v < (y - x):
            new_weight = min(original_weight, -x)
        else:
            new_weight = min(original_weight, v - y)

        network.insert_or_update_ordinary_edge(V, new_weight, A)
    return network


def update_potential(network, potential_function, activation_point):
    updated_potential_function = deepcopy(potential_function)

    min_heap = []
    heappush(
        min_heap, (activation_point, updated_potential_function[activation_point]))


def get_everything(S):
    return 0, 0, 0, 0


def cairo_et_al_2018(network):
    potential_function = init_potential(network.lo)
    if negative_cycle(network, potential_function) == False:
        return False
    contingent_links = network.contingent_links
    S = deque()
    S.append(contingent_links[randint(0, len(contingent_links) - 1)])
    while S:
        # should it be S[0]?
        A, x, y, C = get_everything(S[-1])
        network = close_relax_lower(network, potential_function, C)
        network = apply_upper(network, C)
        # fix the next line
        potential_function = update_potential(
            network.lo, potential_function, A)
        if negative_cycle(network, potential_function) == False:
            return False

        flag = False
        for C_prime in contingent_links:
            A_prime, _, _, _ = get_everything(C_prime)
            if network.successor_edges[A_prime][C] < y - x:
                flag = True
            if flag:
                for C_alt in S:
                    if C_prime == C_alt:
                        return False

                S.append(C_prime)
        if not flag:
            contingent_links = contingent_links.pop(C)
            S.pop()
            if contingent_links and not S:
                S.append(contingent_links[0])

    return True
