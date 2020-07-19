from file_reader import FileReader
from stnu import STNU
from dc_checking import cairo_et_al_2018
import os

f = FileReader()

controllable_file_names = [
    f for f in os.listdir("../sample_stnus/controllable/")]

for file_name in controllable_file_names:
    stnu = f.read_file("../sample_stnus/controllable/" + file_name)
    dc = cairo_et_al_2018(stnu)
    if dc != True:
        print(file_name)

uncontrollable_file_names = [
    f for f in os.listdir("../sample_stnus/uncontrollable/")]

for file_name in uncontrollable_file_names:
    stnu = f.read_file("../sample_stnus/uncontrollable/" + file_name)
    dc = cairo_et_al_2018(stnu)
    if dc != False:
        print(file_name)
