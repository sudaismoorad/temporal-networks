from file_reader import FileReader
from stnu import STNU
from stnu_algorithms import dc_check_rul, dc_check_morris
import os
import sys
from test_helper import time_test

# =============================
#  FILE:    testing_controllability.py
#  AUTHOR:  Sudais Moorad / Muhammad Furrukh Asif
#  DATE:    July 2020
# =============================



def test_morris_2014(test_controllable, test_uncontrollable):
    f = FileReader()

    def test_controllable_STNUs(controllable_file_names):

        counter = 0
        for file_name in controllable_file_names:
            stnu = f.read_file("../sample_stnus/controllable/" + file_name)
            dc = dc_check_morris(stnu)
            if dc != True:
                print(file_name)
            if dc == True:
                counter += 1

        print(f"{counter}/{len(controllable_file_names)} tests passed!")

    def test_controllable_STNUs_return(time):
        return f"Testing controllable STNUs took {time} seconds"

    def test_uncontrollable_STNUs(uncontrollable_file_names):

        counter = 0
        for file_name in uncontrollable_file_names:
            stnu = f.read_file("../sample_stnus/uncontrollable/" + file_name)
            dc = dc_check_morris(stnu)
            if dc != False:
                print(file_name)
            if dc == False:
                counter += 1

        print(f"{counter}/{len(uncontrollable_file_names)} tests passed!")

    def test_uncontrollable_STNUs_return(time):
        return f"Testing uncontrollable STNUs took {time} seconds"

    if test_controllable:
        controllable_file_names = [
            f for f in os.listdir("../sample_stnus/controllable/")]
        time_test(test_controllable_STNUs,
                  controllable_file_names, test_controllable_STNUs_return)

    if test_uncontrollable:
        uncontrollable_file_names = [
            f for f in os.listdir("../sample_stnus/uncontrollable/")]
        time_test(test_uncontrollable_STNUs,
                  uncontrollable_file_names, test_uncontrollable_STNUs_return)


def test_cormen_et_al_2018(test_controllable, test_uncontrollable):
    f = FileReader()

    def test_controllable_STNUs(controllable_file_names):

        counter = 0
        for file_name in controllable_file_names:
            stnu = f.read_file("../sample_stnus/controllable/" + file_name)
            dc = dc_check_rul(stnu)
            if dc != True:
                print(file_name)
            if dc == True:
                counter += 1

        print(f"{counter}/{len(controllable_file_names)} tests passed!")

    def test_controllable_STNUs_return(time):
        return f"Testing controllable STNUs took {time} seconds"

    def test_uncontrollable_STNUs(uncontrollable_file_names):

        counter = 0
        for file_name in uncontrollable_file_names:
            stnu = f.read_file("../sample_stnus/uncontrollable/" + file_name)
            dc = dc_check_rul(stnu)
            if dc != False:
                print(file_name)
            if dc == False:
                counter += 1

        print(f"{counter}/{len(uncontrollable_file_names)} tests passed!")

    def test_uncontrollable_STNUs_return(time):
        return f"Testing uncontrollable STNUs took {time} seconds"

    if test_controllable:
        controllable_file_names = [
            f for f in os.listdir("../sample_stnus/controllable/")]
        time_test(test_controllable_STNUs,
                  controllable_file_names, test_controllable_STNUs_return)

    if test_uncontrollable:
        uncontrollable_file_names = [
            f for f in os.listdir("../sample_stnus/uncontrollable/")]
        time_test(test_uncontrollable_STNUs,
                  uncontrollable_file_names, test_uncontrollable_STNUs_return)


if __name__ == "__main__":
    args = sys.argv
    controllable, uncontrollable = True, True
    if len(sys.argv) > 2:
        raise Exception("Upto 2 system arguments expected")
    if len(sys.argv) == 2:
        if sys.argv[1].lower() == "controllable":
            uncontrollable = False
        elif sys.argv[1].lower() == "uncontrollable":
            controllable = False
        else:
            raise Exception(
                "System argument expected to be either 'controllable' or 'uncontrollable'")

    test_cormen_et_al_2018(controllable, uncontrollable)
