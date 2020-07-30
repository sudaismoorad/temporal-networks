from stn_algorithms import bellman_ford, dijkstra
import os
import sys
from test_helper import time_test
from file_reader import FileReader

# =============================
#  FILE:    testing_shortest_path.py
#  AUTHOR:  Sudais Moorad / Muhammad Furrukh Asif
#  DATE:    July 2020
# =============================




def test_shortest_path_algorithms(file_names):
    f = FileReader()
    FILE_PATH = "../sample_stns/"
    bellman_ford_dict, dijkstra_dict, pred_dijkstra_dict = {}, {}, {}

    def test_bellman_ford_existing_src(file_names):
        for file_name in file_names:
            stn = f.read_file(FILE_PATH + file_name)
            bellman_ford_dict[file_name] = [
                False for _ in range(stn.num_tps())]
            for i in range(stn.num_tps()):
                bellman_ford_d = bellman_ford(stn, i)
                bellman_ford_dict[file_name][i] = bellman_ford_d

    def test_bellman_ford_existing_src_return(time):
        return f"Testing Bellman Ford (existing src) took {time} seconds"

    def test_dijkstra(file_names):
        for file_name in file_names:
            stn = f.read_file(FILE_PATH + file_name)
            dijkstra_dict[file_name] = [False for _ in range(stn.num_tps())]
            for i in range(stn.num_tps()):
                dijkstra_d = dijkstra(stn, i)
                dijkstra_dict[file_name][i] = dijkstra_d

    def test_dijkstra_return(time):
        return f"Testing Dijkstra (forward propagation) took {time} seconds"

    def test_pred_dijkstra(file_names):
        for file_name in file_names:
            stn = f.read_file(FILE_PATH + file_name)
            pred_dijkstra_dict[file_name] = [
                False for _ in range(stn.num_tps())]
            for i in range(stn.num_tps()):
                dijkstra_d = dijkstra(stn, i, succ_direction=False)
                pred_dijkstra_dict[file_name][i] = dijkstra_d

    def test_pred_dijkstra_return(time):
        return f"Testing Dijkstra (backward propagation) took {time} seconds"

    def test_compare_d(file_names):
        counter = 0
        file_counter = 0
        for file_name in file_names:
            stn = f.read_file(FILE_PATH + file_name)
            for i in range(stn.num_tps()):
                if bellman_ford_dict[file_name][i] != dijkstra_dict[file_name][i] and dijkstra_dict[file_name][i] != pred_dijkstra_dict[file_name][i]:
                    print(file_name, i)
                else:
                    counter += 1
            file_counter += stn.num_tps()

        print(f"{counter}/{file_counter} tests passed!")

    def test_compare_d_return(time):
        return f"Comparing Bellman Ford (existing src) and Dijkstra (forward and backward propagation) took {time} seconds"

    if file_names is None:
        file_names = [f for f in os.listdir(FILE_PATH)]

    time_test(test_bellman_ford_existing_src,
              file_names, test_bellman_ford_existing_src_return)

    time_test(test_dijkstra,
              file_names, test_dijkstra_return)

    time_test(test_pred_dijkstra,
              file_names, test_pred_dijkstra_return)

    time_test(test_compare_d,
              file_names, test_compare_d_return)


if __name__ == "__main__":
    args = sys.argv
    file_names = None
    if len(args) > 1:
        file_names = args[1:]

    test_shortest_path_algorithms(file_names)
