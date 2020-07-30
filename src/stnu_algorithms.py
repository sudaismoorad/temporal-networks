from dc_checking import cairo_et_al_2018, morris_2014

# =============================
#  FILE:    stnu_algorithms.py
#  AUTHOR:  Sudais Moorad / Muhammad Furrukh Asif
#  DATE:    June 2020
# =============================

def dc_check_rul(network):
    return cairo_et_al_2018(network)


def dc_check_morris(network):
    return morris_2014(network)
