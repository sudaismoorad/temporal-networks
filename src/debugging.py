from file_reader import FileReader
from stnu import STNU
from dc_checking import cairo_et_al_2018
from algorithms import dispatch, bellman_ford
from dispatchability import Dispatchability

f = FileReader()
# stnu = f.read_file("../sample_stnus/controllable/dc-2.stnu")
# cairo_et_al_2018(stnu)
stn = f.read_file("../sample_stns/dc-400.stn")
stn = dispatch(stn)
potential_function = bellman_ford(stn)
print(Dispatchability.greedy_execute(stn, potential_function))
