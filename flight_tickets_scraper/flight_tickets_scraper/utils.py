from itertools import permutations

from scrapy.utils.project import get_project_settings

from json import load


settings = get_project_settings()


def get_json_key_value(json_file_path, key):
    json_file_handler = open(json_file_path)
    airports_city = load(json_file_handler)
    airports_codes = airports_city[key]

    json_file_handler.close()

    return airports_codes


def two_permutation_airports_codes():
    json_file_path = settings.get("SOURCES")["airport_city_codes_path"]
    json_key = "CityCodes"

    airports_city_codes_lst = get_json_key_value(json_file_path, json_key)
    
    airports_codes_lst = [airport_city_code_dict["id"]
                          for airport_city_code_dict in airports_city_codes_lst]
    
    two_permutation_codes = permutations(airports_codes_lst, 2)

    return two_permutation_codes


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
