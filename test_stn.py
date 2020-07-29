import sys
import os
from src.stn_algorithms import *
from src.file_reader import FileReader
from src.testing_all_pairs_shortest_path_algorithms import *
from src.testing_bellman_ford import *
from src.testing_dispatch import *
from src.testing_shortest_path import *
from src.test_helper import *

if __name__ == "__main__":
    args = sys.argv
    if len(args) == 1:
        # run all tests
        pass
