from file_reader import FileReader
from stnu import STNU
from dc_checking import cairo_et_al_2018
from algorithms import dispatch, bellman_ford, johnson, greedy_execute, slow_dispatch, luke_dispatch, floyd_warshall
from dispatchability import Dispatchability
from copy import deepcopy

f = FileReader()
# stnu = f.read_file("../sample_stnus/controllable/dc-2.stnu")
# cairo_et_al_2018(stnu)
stn = f.read_file("../sample_stns/dc-hunsberger-0.stn")
floyd_warshall_dm = floyd_warshall(stn)
for node_idx, listy in enumerate(floyd_warshall_dm):
    for successor_idx, weight in enumerate(listy):
        if node_idx == successor_idx:
            continue
        stn.successor_edges[node_idx][successor_idx] = weight
print(stn)
stn1 = f.read_file("../sample_stns/dc-hunsberger-0.stn")
johnson_dm = johnson(stn)
for node_idx, listy in enumerate(johnson_dm):
    for successor_idx, weight in enumerate(listy):
        if node_idx == successor_idx:
            continue
        stn1.successor_edges[node_idx][successor_idx] = weight
print(stn1)

# stn.visualize()
# luke_dispatch = luke_dispatch(stn)
# print(luke_dispatch)
# result1 = greedy_execute(luke_dispatch)
# print(result1)

# slow_dispatch = slow_dispatch(stn)
# print(slow_dispatch)
# result2 = greedy_execute(slow_dispatch)
# print(result2)

# Fast_dispatch = dispatch(stn)
# print(Fast_dispatch)
# result = greedy_execute(Fast_dispatch)
# print(result)
