import json


def get_json_obj(json_file_path):
    with open(json_file_path) as json_file_handler:
        json_obj = json.load(json_file_handler)
    return json_obj


def extract_values_from_json_obj(obj, key):
    arr = []

    def extract(obj, arr, key):
        if isinstance(obj, dict):
            for k, v in obj.items():
                if isinstance(v, (dict, list)):
                    extract(v, arr, key)
                elif k == key:
                    arr.append(v)
        elif isinstance(obj, list):
            for item in obj:
                extract(item, arr, key)
        return arr

    results = extract(obj, arr, key)
    return results


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


def create_flatten_dict(keys, values):
    return {key: value for key, value in zip(keys, values)}
