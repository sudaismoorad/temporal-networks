from file_reader import FileReader
from stnu import STNU
from dc_checking import cairo_et_al_2018
from algorithms import dispatch, bellman_ford, johnson, greedy_execute, slow_dispatch, luke_dispatch
from dispatchability import Dispatchability

f = FileReader()
# stnu = f.read_file("../sample_stnus/controllable/dc-2.stnu")
# cairo_et_al_2018(stnu)
stn = f.read_file("../sample_stns/controllable/dc-2.stnu")
stn.visualize()
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
