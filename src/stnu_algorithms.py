from dc_checking import cairo_et_al_2018, morris_2014


def dc_check_rul(network):
    return cairo_et_al_2018(network)


def dc_check_morris(network):
    return morris_2014(network)
