from collections import Counter
from itertools import combinations

import random
import json


def get_airports_codes():
    path = "/home/magnus9102/Mostafa/Py/Github/data-science/source/airport_city_codes.json"
    json_file_handler = open(path)
    airports_city = json.load(json_file_handler)
    airports_codes = airports_city["CityCodes"]
    json_file_handler.close()

    return airports_codes


def make_combination_airports():
    airports_city_codes_lst = get_airports_codes()
    airports_codes_lst = [airport_city_code_dict["id"] for airport_city_code_dict in airports_city_codes_lst]
    two_combination_lst = list(combinations(airports_codes_lst, 2))
    random.shuffle(two_combination_lst)
    return two_combination_lst


def check_for_duplicate_value(result):
    test_result = list()

    for item, count in Counter(result).items():
        if count == 1:
            test_result.append(item)
    return test_result


result = make_combination_airports()
test_result = check_for_duplicate_value(result)

print(len(test_result))
print(test_result == result)
