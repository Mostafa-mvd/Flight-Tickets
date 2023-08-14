import json


def infinite_sequence():
    num = 0
    while num != 10:
        yield num
        num += 1
        yield num
        num += 1


def get_json_obj(json_file_path):
    with open(json_file_path) as json_file_handler:
        json_obj = json.load(json_file_handler)
    return json_obj


def extract_value_from_json_obj(data, nested_keys):
    if not nested_keys:
        return data
    
    if isinstance(data, dict):
        data_keys = data.keys()

        for key in nested_keys:
            if key in data_keys:
                return extract_value_from_json_obj(data[key], nested_keys[1:])
            else:
                return None
    elif isinstance(data, list):
        for dict_item in data:
            return extract_value_from_json_obj(dict_item, nested_keys)


nested_dict = get_json_obj("/home/magnus9102/Mostafa/Py/Github/data-science/scratch/nested.json")
result = extract_value_from_json_obj(nested_dict, ["data", "country_module", "global", "world_region"])
print(result)
