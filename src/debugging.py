from file_reader import FileReader
from stnu import STNU
from dc_checking import cairo_et_al_2018
from stn_algorithms import dispatch, bellman_ford, johnson, greedy_execute, slow_dispatch, luke_dispatch, floyd_warshall
from dispatchability import Dispatchability
from copy import deepcopy

f = FileReader()
stn = f.read_file("../sample_stns/dc-200-4.stnu")

Fast_dispatch = dispatch(stn)
# print(Fast_dispatch)
# result = greedy_execute(Fast_dispatch)
# print("fast", result)

# slow_dispatch = slow_dispatch(stn)
# print(slow_dispatch)
# result2 = greedy_execute(slow_dispatch)
# print(result2)


# luke_dispatch = luke_dispatch(stn)
# print(luke_dispatch)
# result1 = greedy_execute(luke_dispatch)
# print("luke", result1)
# counter = 0
# for i in range(stn.num_tps()):
#     counter += len(Fast_dispatch.successor_edges[i])
#     counter -= len(luke_dispatch.successor_edges[i])
#     if Fast_dispatch.successor_edges[i] != luke_dispatch.successor_edges[i]:
#         print(f"{i}th edge:")
#         print("fast ", Fast_dispatch.successor_edges[i])
#         print("luke", luke_dispatch.successor_edges[i])
# print(counter)
