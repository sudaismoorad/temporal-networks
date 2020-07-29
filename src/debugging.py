from file_reader import FileReader
from stnu import STNU
from dc_checking import cairo_et_al_2018
from stn_algorithms import dispatch, bellman_ford, johnson, greedy_execute, slow_dispatch, luke_dispatch, floyd_warshall
from dispatchability import Dispatchability
from copy import deepcopy
from dispatch import Dispatch
import os

f = FileReader()
stn = f.read_file("../sample_stns/dc-hunsberger-0.stn")
dispatch(stn)
# FILE_PATH = "../sample_stns/"
# file_names = ['dc-1.stn', 'dc-3.stn', 'dc-5.stn', 'dc-APSP.stn',
#               'dc-dispatchable.stn', 'dc-hunsberger-0.stn', 'dc-hunsberger-1.stn', 'dc-hunsberger-2.stn', 'dc-original.stn']
# for file_name in file_names:
#     stn = f.read_file(FILE_PATH + file_name)
#     fast, luke = Dispatch.test_on_contracted(stn)
#     try:
#         print(fast)
#         greedy_execute(fast)
#         print(luke)
#         greedy_execute(luke)
#     except Exception as e:
#         print(e)
#         print(file_name)
#     print("#####################################")
# Fast_dispatch = dispatch(stn)
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
