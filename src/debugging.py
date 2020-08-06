from file_reader import FileReader
from stnu import STNU
from dc_checking import cairo_et_al_2018
from stn_algorithms import dispatch, bellman_ford, johnson, greedy_execute, slow_dispatch, luke_dispatch, floyd_warshall
from dispatchability import Dispatchability
from copy import deepcopy
from dispatch import Dispatch
import os
from write_stn import write_stn
from stnu_algorithms import dc_check_morris, dc_check_rul

f = FileReader()
stn = f.read_file("../sample_stnus/uncontrollable/notDC_200nodes_010ctgs_100maxWeight_20maxCtgWeight_4inDegree_4outDegree_000.plainstnu")
# print(dc_check_morris(stn))
print(dc_check_rul(stn))
# print(stn)
# potential_function = bellman_ford(stn)
# fast_dispatch = luke_dispatch(stn)
# # print(Dispatchability.greedy_execute(fast_dispatch, potential_function))
# try:
#     Dispatchability.greedy_execute(fast_dispatch, potential_function)
# except:
#     print("kkk")



