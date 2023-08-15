from scrapy.utils.project import get_project_settings
from common_utils.utils import get_json_obj, extract_values_from_json_obj
from itertools import permutations


def two_permutation_airports_codes():
    settings = get_project_settings()
    json_file_path = settings.get("SOURCES")["airport_city_codes_path"]

    jsn_obj = get_json_obj(json_file_path)
    airports_codes_lst = extract_values_from_json_obj(jsn_obj, "id")
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
