from johnson import Johnson
from copy import deepcopy
from random import random


class Dispatch:

    @staticmethod
    def convert_to_dispatchable(network):
        if not network.flag and network.distance_matrix:
            pass
        else:
            Johnson.johnson(network)

        distance_matrix = deepcopy(network.distance_matrix)
        marked_edges = []

        intersecting_edges = Dispatch._get_intersecting_edges(network)

        for (src_idx, middle_idx), target_idx in intersecting_edges:
            left_side_one = distance_matrix[src_idx][middle_idx] + \
                distance_matrix[middle_idx][target_idx]
            right_side_one = distance_matrix[src_idx][target_idx]
            left_side_two = distance_matrix[src_idx][middle_idx]
            right_side_two = distance_matrix[src_idx][target_idx] + \
                distance_matrix[middle_idx][target_idx]
            if left_side_one == right_side_one and left_side_two == right_side_two:
                if (src_idx, target_idx) not in marked_edges and (src_idx, middle_idx) not in marked_edges:
                    if random(1) < 0.5:
                        marked_edges.append((src_idx, target_idx))
                    else:
                        marked_edges.append((src_idx, middle_idx))
            else:
                if left_side_one == right_side_one:
                    marked_edges.append((src_idx, target_idx))
                if left_side_two == right_side_two:
                    marked_edges.append((src_idx, middle_idx))

        return marked_edges

    @staticmethod
    def _get_intersecting_edges(network):
        length = network.length
        intersecting_edges = []
        for i in range(length):
            for j in range(length):
                for k in range(length):
                    intersecting_edges.append((i, j), k)
        return intersecting_edges
