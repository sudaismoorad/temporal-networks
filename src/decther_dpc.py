class DPC:

    @staticmethod
    def DPC(network, ordering):
        def Relax(i, i_k_weight, k, k_j_weight, j):
            pass
        num_tps = network.num_tps()
        for k in ordering:
            for i in range(k):
                if k in network.successor_edges[i]:
                    i_k_weight = network.successor_edges[i][k]
                else:
                    continue
                for j in range(k, num_tps):
                    if j in network.successor_edges[k]:
                        k_j_weight = network.successor_edges[k][j]
                    else:
                        continue
                    Relax(i, i_k_weight, k, k_j_weight, j)
                    if i in network.successor_edges[j] and j in network.successor_edges[i] and network.successor_edges[i][j] + network.successor_edges[j][i] < 0:
                        return False

        return network
