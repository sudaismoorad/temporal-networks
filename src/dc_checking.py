from bellman_ford import BellmanFord
from collections import deque
from random import randint
from heapq import heappush, heappop, heapify
from copy import deepcopy


__all__ = ["morris_2014", "cairo_et_al_2018"]


def morris_2014(graph, N):
    network = deepcopy(graph)
    N = network.num_tps()

    def is_negative(node):
        for _, w in network.predecessor_edges[node]:
            if w < 0:
                return True
        return False

    def is_unsuitable(node):
        pass

    def DC_backprop(src):
        if ancestor[src] == src:
            return False

        if prior[src]:
            return True

        distances[src] = 0
        for i in range(len(N)):
            if i != src:
                distances[i] = float("inf")

        min_heap = []
        for n1, e1 in network.predecessor_edges[src]:
            distances[n1] = e1
            heappush(min_heap, (e1, n1))

        while min_heap:
            _, u = heappop(min_heap)
            # might not need distances... first ele is distance
            if distances[u] >= 0:
                network.insert_ordinary_edge(u, src, distances[u])
                continue
            # cache the negative nodes
            if is_negative(u):
                # change global states here
                ancestor[u] = src
                # what do they mean by prior here?
                if DC_backprop(u) == False:
                    return False
            for v, e in network.predecessor_edges[src]:
                if e < 0:
                    continue
                # what does it mean for e to be unsuitable
                if negative_nodes(v):
                    continue
                new = distances[u] + e
                if new < distances[v]:
                    distances[v] = new
                    heappush(min_heap, (distances[v], v))
        prior[src] = True
        return True

    prior = [False for i in range(N)]
    for idx, state in negative_nodes:
        if state:
            distances = [float("inf") for i in range(N)]
            ancestor = [float("inf") for i in range(N)]
            negative_nodes = [is_negative(node) for node in range(N)]
            if DC_backprop(idx) == False:
                return False
    return True


def init_potential(ol_edges):
    """
    -------------------------------------------------------------------------
    A method that calculates the initial potential function for the LO-graph.
    -------------------------------------------------------------------------
    Parameters
    ----------
    ol_edges: List[Dictionary]
        A list of dictionaries representing the ordinary and lower-case edges.
    Returns
    -------
    potential_function: List[int]
        An array of length N representing the shortest distances from an external source.
        Involves N - 1 iterations of Bellman Ford.
    """
    N = len(ol_edges)
    potential_function = [0 for _ in range(N)]
    for _ in range(1, N):
        for V, edge_dict in enumerate(ol_edges):
            for W, w in edge_dict.items():
                potential_function[V] = max(
                    potential_function[V], potential_function[W] - w)

    return potential_function


def negative_cycle(network, potential_function):
    """
    -------------------------------------------------------------------------
    A method that checks if there is a negative cycle in the LO-graph.
    -------------------------------------------------------------------------
    Parameters
    ----------
    network: STNU
        A Simple Temporal Network with Uncertainity.
    potential_function: List[int]
        A candidate potential function for the LO-graph.
    Returns
    -------
    bool:
        True, if a negative cycle is found. False, if the potentail function is valid.
        Involves the Nth iteration of Bellman Ford.
    """
    for V, edge_dict in enumerate(network.ol_edges):
        for W, w in edge_dict.items():
            if potential_function[V] < potential_function[W] - w:
                return True
    return False


def apply_relax_lower(network, W, C):
    """
    -------------------------------------------------------------------------
    A method that generates the set of edges to be added to the network as a 
    reult of RELAX- and Lower- rules being applied.
    -------------------------------------------------------------------------
    Parameters
    ----------
    network: STNU
        A Simple Temporal Network with Uncertainity.
    W: int
        The index of a time-point in the STNU.
    C: int
        The index of a contingent time-point in the STNU.
    Returns
    -------
    edges => set((time-point, weight, time-point)): set((int, int, int))
        A set of edges to be added to the network.
    """
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
        for P, edge_dict in enumerate(network.ol_edges):
            for Q, delta_P_Q in edge_dict.items():
                if P == C:
                    continue
                if W == Q:
                    edges.add((P, delta_P_Q + delta_W_C, C))
    return edges


def close_relax_lower(network, potential_function, C):
    """
    -------------------------------------------------------------------------
    A method that adds all the edges terminating at the contingent time-point 
    as a result of the Relax- and Lower- rules being applied.
    -------------------------------------------------------------------------
    Parameters
    ----------
    network: STNU
        A Simple Temporal Network with Uncertainity.
    potential_function: List[int]
        A potential function for the LO-graph.
    C: int
        The index of a contingent time-point in the STNU.
    Returns
    -------
    network: STNU
        A modified network with all incoming edges to the contingent 
        time-point being added.
    """
    min_heap = []
    NOT_YET_IN_QUEUE, IN_QUEUE, POPPED_OFF = 0, 1, 2
    in_queue = [NOT_YET_IN_QUEUE for i in range(len(potential_function))]

    for W, edge_dict in enumerate(network.ol_edges):
        for C_prime, delta_W_C in edge_dict.items():
            if C_prime == C:
                in_queue[W] = IN_QUEUE
                heappush(min_heap, (potential_function[W] + delta_W_C, W))

    while min_heap:
        _, W = heappop(min_heap)
        in_queue[W] = POPPED_OFF
        result = apply_relax_lower(network, W, C)
        for (V, v, C) in result:
            curr_VC = network.successor_edges[V][C] if C in network.successor_edges[V] else float(
                "inf")
            if v < curr_VC:
                network.insert_ordinary_edge(V, C, v)
            new_key = potential_function[V] + min(v, curr_VC)

            if in_queue[V] == IN_QUEUE:
                for i, (_, node) in enumerate(min_heap):
                    if node == V:
                        idx = i
                node = min_heap[idx][1]
                min_heap.pop(idx)
                heappush(min_heap, (new_key, node))
                heapify(min_heap)
            elif in_queue[V] == NOT_YET_IN_QUEUE:
                heappush(min_heap, (new_key, V))
                in_queue[V] = IN_QUEUE
    return network


def apply_upper(network, C):
    """
    -------------------------------------------------------------------------
    A method that generates and adds all the edges terminating at the 
    activation time-point as a result of the Upper- rule being applied.
    -------------------------------------------------------------------------
    Parameters
    ----------
    network: STNU
        A Simple Temporal Network with Uncertainity.
    C: int
        The index of a contingent time-point in the STNU.
    Returns
    -------
    network: STNU
        A modified network with all incoming edges to the activation 
        time-point being added.
    """
    A, x, y, C = network.contingent_links[C]
    insert_edges = []
    for V, edge_dict in enumerate(network.successor_edges):
        for D, v in edge_dict.items():
            if D != C:
                continue
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
    """
    -------------------------------------------------------------------------
    A method that updates the potential function to reflect the new_edges.
    -------------------------------------------------------------------------
    Parameters
    ----------
    network: STNU
        A Simple Temporal Network with Uncertainity.
    potential_function: List[int]
        A potential function for the LO-graph.
    C: int
        The index of a contingent time-point in the STNU.
    Returns
    -------
    updated_potentail_function: List[int]
        An updated potential function for the LO-graph. Involves N - 1 
        iterations of Bellman Ford.
    """
    updated_potential_function = deepcopy(potential_function)

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
                        min_heap[idx] = (new_key, V)
                        heapify(min_heap)
                    elif in_queue[V] == NOT_YET_IN_QUEUE:
                        heappush(
                            min_heap, (new_key, V))
                        in_queue[V] = IN_QUEUE
                    # else:
                    #     return False

    return updated_potential_function


def cairo_et_al_2018(network):
    """
    -------------------------------------------------------------------------
    The main method for the RUL- DC-checking algorithm. Checks if a given STNU
    is dynamically controllable.
    -------------------------------------------------------------------------
    Parameters
    ----------
    network: STNU
        A Simple Temporal Network with Uncertainity.
    Returns
 -------
    bool:
        True, if the network is dynamically controlled and False otherwise.
    """
    potential_function = init_potential(network.ol_edges)
    if negative_cycle(network, potential_function):
        return False

    contingent_links = network.contingent_links
    stack = deque()

    idx = randint(0, len(contingent_links) - 1)
    while contingent_links[idx] == False:
        idx = randint(0, len(contingent_links) - 1)
    stack.append(contingent_links[idx])
    # for i in range(len(contingent_links)):
    #     if contingent_links[i]:
    #         print(i, end=" ")
    # print("")
    while stack:

        A, x, y, C = stack[-1]
        # print(C, end=" ")
        network = close_relax_lower(network, potential_function, C)
        network = apply_upper(network, C)

        potential_function = update_potential(
            network, potential_function, A)

        # print(True if init_potential(network.ol_edges) else False)

        if negative_cycle(network, potential_function):
            return False

        # use the in_queue strategy to make this constant time
        # instead of linear time
        flag = False
        for i in range(len(contingent_links)):
            if contingent_links[i] == False:
                continue
            A_prime, _, _, C_prime = contingent_links[i]
            weight = network.successor_edges[A_prime][C] if C in network.successor_edges[A_prime] else float(
                "inf")
            if weight < y - x:
                flag = True
                break
        if flag:
            for _, _, _, C_alt in stack:
                if C_prime == C_alt:
                    return False
            stack.append(contingent_links[i])
        else:
            contingent_links[C] = False
            stack.pop()
            if not stack:
                for i in range(len(contingent_links)):
                    if contingent_links[i] != False:
                        stack.append(contingent_links[i])
                        break

    return True
