def write_stn(network, stn_name):
        """
         write_stn: Writes a randomly generated STN to a file.
         -------------------------------------------------------------
         INPUTS:  network: A randomly generated STN.
                  stn_no: An integer representing a unique key for the STN to be
                          included in the file name.
         OUTPUT:  None
         SIDE EFFECTS:  Writes a randomly generated STN to a file.
         --------------------------------------------------------------
         """
        file = open("../sample_stns/" + str(stn_name) + '.stn', "w")
        edge_string = ""
        edge_counter = 0
        names_string = ""
        for name in network.names_list:
            names_string += name + " "
        for src_idx, dict in enumerate(network.successor_edges):
            for successor_idx, weight in dict.items():
                edge_string += str(network.names_list[src_idx]) + " " + str(
                    weight) + " " + str(network.names_list[successor_idx]) + "\n"
                edge_counter += 1
        L = ["# KIND OF NETWORK \n", "STN" + "\n", "# Num Time-Points \n",
             str(network.num_tps()) +
             "\n", "# Num Ordinary Edges \n", str(edge_counter) + "\n",
             "# Time-Point Names \n", names_string + "\n", "# Ordinary Edges \n", edge_string]
        file.writelines(L)