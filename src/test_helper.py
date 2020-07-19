from time import time


def time_test(test_function, test_parameters, return_string_function):
    start = time()
    test_function(test_parameters)
    end = time()
    test_duration = round(end - start, 2)
    print(return_string_function(test_duration))
