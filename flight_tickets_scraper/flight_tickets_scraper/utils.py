from itertools import combinations

from json import load
import pathlib


def get_airports_codes():
    parent_path = pathlib.Path(__file__).parent.parent.parent
    json_file_path = parent_path.joinpath(
        "source", "airport_city_codes.json")
    json_file_handler = open(json_file_path)
    airports_city = load(json_file_handler)
    airports_codes = airports_city["CityCodes"]
    json_file_handler.close()

    return airports_codes


def make_two_combinations_airports():
    def check_equal_constraint(airports_codes):
        if (airports_codes[0], airports_codes[1]) != ("THR", "IKA"):
            return True
        return False

    airports_city_codes_lst = get_airports_codes()
    airports_codes_lst = [airport_city_code_dict["id"]
                          for airport_city_code_dict in airports_city_codes_lst]
    two_combinations_codes = filter(
        check_equal_constraint, combinations(airports_codes_lst, 2))

    return two_combinations_codes
