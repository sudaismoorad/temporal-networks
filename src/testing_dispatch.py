from algorithms import dispatch, slow_dispatch, luke_dispatch, greedy_execute, johnson
import os
import sys
from test_helper import time_test
from file_reader import FileReader


def test_dispatch(test_fast, test_slow, test_luke):
    f = FileReader()
    FILE_PATH = "../sample_stns/"

    def test_fast_dispatch(file_names):
        counter = 0
        for file_name in file_names:
            stn = f.read_file(FILE_PATH + file_name)
            dispatchable_stn = dispatch(stn)
            try:
                greedy_execute(dispatchable_stn)
                counter += 1
            except:
                print(file_name)

        print(f"{counter}/{len(file_names)} tests passed!")

    def test_fast_dispatch_return(time):
        return f"Testing Fast Dispatch took {time} seconds"

    def test_slow_dispatch(file_names):
        counter = 0
        for file_name in file_names:
            stn = f.read_file(FILE_PATH + file_name)
            dispatchable_stn = slow_dispatch(stn)
            try:
                greedy_execute(dispatchable_stn)
                counter += 1
            except:
                pass

        print(f"{counter}/{len(file_names)} tests passed!")

    def test_slow_dispatch_return(time):
        return f"Testing Slow Dispatch took {time} seconds"

    def test_luke_dispatch(file_names):
        counter = 0
        for file_name in file_names:
            stn = f.read_file(FILE_PATH + file_name)
            dispatchable_stn = luke_dispatch(stn)
            try:
                greedy_execute(dispatchable_stn)
                counter += 1
            except:
                print(file_name)

        print(f"{counter}/{len(file_names)} tests passed!")

    def test_luke_dispatch_return(time):
        return f"Testing Luke Dispatch took {time} seconds"

    dispatch_file_names = [f for f in os.listdir(FILE_PATH)]

    if test_fast:
        time_test(test_fast_dispatch,
                  dispatch_file_names, test_fast_dispatch_return)
    if test_slow:
        time_test(test_slow_dispatch,
                  dispatch_file_names, test_slow_dispatch_return)
    if test_luke:
        time_test(test_luke_dispatch,
                  dispatch_file_names, test_luke_dispatch_return)


if __name__ == "__main__":
    args = sys.argv
    fast, slow, luke = True, True, True
    if len(args) > 3:
        raise Exception("Upto 3 system arguments expected")
    if len(args) == 2:
        if args[1].lower() == "fast":
            slow, luke = False, False
        elif args[1].lower() == "slow":
            fast, luke = False, False
        elif args[1].lower() == "luke":
            fast, slow = False, False
        else:
            raise Exception(
                "System argument expected to be either 'fast', 'slow' or 'luke'")
    if len(args) == 3:
        listy = [arg.lower() for arg in args[1:]]
        if "fast" not in listy:
            fast = False
        elif "slow" not in listy:
            slow = False
        elif "luke" not in listy:
            luke = False
        # this needs to be changed
        else:
            raise Exception(
                "System argument expected to be either 'fast', 'slow' or 'luke'")

    test_dispatch(fast, slow, luke)
