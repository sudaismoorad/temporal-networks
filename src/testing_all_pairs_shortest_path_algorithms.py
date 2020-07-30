from stn_algorithms import floyd_warshall, johnson
import os
import sys
from test_helper import time_test
from file_reader import FileReader

# =============================
#  FILE:    testing_all_pairs_shortest_path_algorithms.py
#  AUTHOR:  Sudais Moorad / Muhammad Furrukh Asif
#  DATE:    July 2020
# =============================


def test_all_pairs_shortest_path_algorithms(file_names):
    f = FileReader()
    FILE_PATH = "../sample_stns/"
    floyd_warshall_dict, johnson_dict = {}, {}

    def test_floyd_warshall(file_names):
        for file_name in file_names:
            stn = f.read_file(FILE_PATH + file_name)
            floyd_warshall_dm = floyd_warshall(stn)
            floyd_warshall_dict[file_name] = floyd_warshall_dm

    def test_floyd_warshall_return(time):
        return f"Testing Floyd Warshall took {time} seconds"

    def test_johnson(file_names):
        for file_name in file_names:
            stn = f.read_file(FILE_PATH + file_name)
            johnson_dm = johnson(stn)
            johnson_dict[file_name] = johnson_dm

    def test_johnson_return(time):
        return f"Testing Johnson took {time} seconds"

    def test_compare_dm(file_names):
        counter = 0
        for file_name in file_names:
            if floyd_warshall_dict[file_name] != johnson_dict[file_name]:
                print(file_name)
            else:
                counter += 1

        print(f"{counter}/{len(file_names)} tests passed!")

    def test_compare_dm_return(time):
        return f"Comparing Johnson and Floyd Warshall took {time} seconds"

    if file_names is None:
        file_names = [f for f in os.listdir(FILE_PATH)]

    time_test(test_floyd_warshall,
              file_names, test_floyd_warshall_return)

    time_test(test_johnson,
              file_names, test_johnson_return)

    time_test(test_compare_dm,
              file_names, test_compare_dm_return)


if __name__ == "__main__":
    args = sys.argv
    file_names = None
    if len(args) > 1:
        file_names = args[1:]

    test_all_pairs_shortest_path_algorithms(file_names)
