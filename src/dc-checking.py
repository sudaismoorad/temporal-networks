from bellman_ford import BellmanFord
from collections import deque


__all__ = ["morris_2014", "cairo_et_al_2018"]


def morris_2014():
    pass


def negative_cycle(network, potential_function):
    pass


def close_relax_lower(network, potential_function, R):
    return network


def apply_upper(network, R):
    return network


def update_potential(network, potential_function, activation_point):
    return network


def cairo_et_al_2018(network):
    potential_function = BellmanFord.bellman_ford_wrapper(network)
    if negative_cycle(network, potential_function) == False:
        return False, network
    contingent_links = network.contingent_links
    S = deque()
    # fix the next line
    Z = 0
    S.append(Z)
    while S:
        R = S.pop()
        network = close_relax_lower(network, potential_function, R)
        network = apply_upper(network, R)
        # fix the next line
        activation_point = network.activation_point[R]
        potential_function = update_potential(
            network, potential_function, activation_point)
        if negative_cycle(network, potential_function) == False:
            return False, network
        flag = False
        for R_prime, contingent_link_dict in enumerate(contingent_links):
            if network.successor_edges[activation_point[R_prime]][R] < contingent_link_dict[R][1] - contingent_link_dict[R][0]:
                flag = True
                if R_prime in S:
                    return False
                else:
                    # make enum for keeping track
                    S.append(R_prime)
        if not flag:
            contingent_links = contingent_links.pop(R)
            S.pop()
            if not contingent_links and not S:
                # how do you get top element of contingent_links though?!
                S.append(contingent_links[-1])
    return True, network
