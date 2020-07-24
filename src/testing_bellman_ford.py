from file_reader import FileReader
from stn_algorithms import floyd_warshall
import sys


def testing_bellman_ford(file_name):
    f = FileReader()
    stn = f.read_file(file_name)
    return floyd_warshall(stn)


if __name__ == "__main__":
    args = sys.argv
    print(testing_bellman_ford(args[1]))

# for file in ./../sample_stns/random_stns/*.stn; do python3 testing_bellman_ford.py $file; done
