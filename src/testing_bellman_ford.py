from file_reader import FileReader
from stn_algorithms import floyd_warshall
import sys

# =============================
#  FILE:    testing_bellman_ford.py
#  AUTHOR:  Sudais Moorad / Muhammad Furrukh Asif
#  DATE:    July 2020
# =============================



def testing_bellman_ford(file_name):
    f = FileReader()
    stn = f.read_file(file_name)
    return floyd_warshall(stn)


if __name__ == "__main__":
    args = sys.argv
    print(testing_bellman_ford(args[1]))


