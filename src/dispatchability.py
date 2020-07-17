# ===================================
##File: dispatchability.py
# Author: Merrick Chang
# Date: May 2020
# ===================================

from copy import deepcopy
import random
from johnson import Johnson

class Dispatchability:

    """
    The Dispatchibility class contains static methods relating to dispatchability.
    """


    @staticmethod
    def _get_predecessor_edges(stn, node_index):
        """
        Generator that finds precedessor edges of a given node
        Input:
            stn, the target stn
            node_index, index of the target node
        Output:
            edge, a tuple containing the start node of the edge and the weight of the edge
        """
        for u, edge_list in enumerate(stn.successor_edges[:node_index]):
            for v, delta in edge_list.items():
                if v == node_index:
                    yield (u, delta)
        for u, edge_list in enumerate(stn.successor_edges[node_index+1:], start=node_index+1):
            for v, delta in edge_list.items():
                if v == node_index:
                    yield (u, delta)



    @staticmethod
    def _find_point_in_time_window(A, bounds, time):
        """
        Find a point enabled within a given time window
        Inputs:
            A, the list of enabled points in the window
            bounds, a list of tuples representing the time contraints of each node
            time, the current time in the algorithm
        Outputs:
            node, an enabled point occuring within the time window
        Effects:
            Pops
        """
        for i, time_point in enumerate(A):
            lower_bound, upper_bound = bounds[time_point]
            if lower_bound <= time and time <= upper_bound:
                return A.pop(i)




    @staticmethod
    def _check_solution(stn, execution_times):
        """
        Method to check whether a solution works on the target STN or not
        Input:
            stn, the target STN
            execution_times, a list of integers representing the time at which each index is executed
        Output:
            works, a boolean that is true if the solution is valid and false otherwise.
        """
        for u, time in enumerate(execution_times):
            for v, delta in stn.successor_edges[u].items():
                if execution_times[v]-time > delta:
                    return False
        return True




    @staticmethod
    def greedy_execute(stn, potential_function):
        """
        Greedy executer for dispatchable STNs
        Input:
            stn, the target stn
            start, the start node
        Output:
            execution_times, a list of integers; execution_times[i] represents the time the ith node
                             (ordered as in stn.names_list) is executed
        Effects:
            Prints out execution sequence.
        """
        # minimum = float("inf")
        # for val in potential_function:
        #     minimum = min(minimum, val)
        # start = potential_function.index(minimum)
        # print(start, stn.successor_edges[start])
        start = -1
        for node_idx, edge_dict in enumerate(stn.successor_edges):
            flag = True
            if not edge_dict:
                continue
            for _, weight in edge_dict.items():
                if weight < 0:
                    flag = False
                    continue
            if flag:
                start = node_idx
                break
        print(start)
        if start == -1:
            return False
        # variable names lifted from Muscettola, Morris, and Tsamardinos
        p_inf = 2147483646
#        n_inf = -2147483648
        start_index = start
        time = 0
        length = len(stn.names_dict)
        n = range(length)
        if type(start) == str:
            start_index = stn.names_dict[start]
        A = [start_index]  # enabled time points
        A_min = 0  # minimum lower bound
        A_max = 0  # minimum upper bound
        S = []  # executed time points
        bounds = []
        execution_times = []
        for x in n:
            bounds.append([0, p_inf])
            execution_times.append(p_inf)
        bounds[start_index] = [0, 0]
        while len(S) < length:
            assert len(
                A) != 0, "There are no more enabled points. This STN is not dispatchable."
            A_min = min([bounds[l][0] for l in A])
            A_max = min([bounds[u][1] for u in A])
            assert A_min <= A_max, "The minimum time is more than the maximum time. This STN is not dispatchable."
            if time < A_min:
                time = random.randint(A_min, A_max)
            assert time <= A_max, "The time exceeds the maximum value in the enabled points. This STN is not dispatchable."
            time_point = Dispatchability._find_point_in_time_window(
                A, bounds, time)
            S.append(time_point)
            execution_times[time_point] = time
            for v, delta in stn.successor_edges[time_point].items():
                alt = time+delta
                if bounds[v][1] >= alt:
                    bounds[v][1] = alt
            for u, delta in Dispatchability._get_predecessor_edges(stn, time_point):
                alt = time-delta
                if alt >= bounds[u][0]:
                    bounds[u][0] = alt
            for u, edge_dict in enumerate(stn.successor_edges):
                if not (u in A or u in S):
                    neg_edges_lead_to_S = True
                    for v, delta in stn.successor_edges[u].items():
                        if delta < 0 and not v in S:
                            neg_edges_lead_to_S = False
                            break
                    if neg_edges_lead_to_S:
                        A.append(u)
        return execution_times