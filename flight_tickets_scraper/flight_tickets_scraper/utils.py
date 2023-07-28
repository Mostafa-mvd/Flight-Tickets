from itertools import combinations

from json import load
import pathlib


def make_json_file_path(file_name):
    """create your json file path in source directory from your project parent folder"""
    parent_path = pathlib.Path(__file__).parent.parent.parent
    json_file_path = parent_path.joinpath("source", file_name)
    return json_file_path


def get_json_key_value(file_name, key):
    json_file_path = make_json_file_path(file_name)
    json_file_handler = open(json_file_path)
    airports_city = load(json_file_handler)
    airports_codes = airports_city[key]

    json_file_handler.close()

    return airports_codes


def make_two_combinations_airports():
    def check_equal_constraint(airports_codes):
        if (airports_codes[0], airports_codes[1]) != ("THR", "IKA"):
            return True
        return False

    airports_city_codes_lst = get_json_key_value("airport_city_codes.json", "CityCodes")
    airports_codes_lst = [airport_city_code_dict["id"]
                          for airport_city_code_dict in airports_city_codes_lst]
    two_combinations_codes = filter(
        check_equal_constraint, combinations(airports_codes_lst, 2))

    return two_combinations_codes


def list_odd_values(lst):
    return lst[1::2]


def list_even_values(lst):
    return lst[::2]


def merge_two_lists(list1, list2):
    for val1, val2 in zip(list1, list2):
        yield f"{val1} {val2}"


def filter_selectors(selectors, css_selector):
    for selector in selectors:
        if selector.css(css_selector):
            yield selector
