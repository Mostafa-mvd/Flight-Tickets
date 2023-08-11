import json
from matplotlib import pyplot as plt


def get_city_codes_dict(json_file_path):
    city_codes_dict = dict()

    with open(json_file_path) as json_file_handler:
        json_file = json.load(json_file_handler)
        city_codes_lst = json_file["CityCodes"]
    
    for city_code_dict in city_codes_lst:
        national_code, city_persian_name = city_code_dict.values()
        city_codes_dict[national_code] = city_persian_name
    
    return city_codes_dict


def correct_field(mail_col_field, secondary_col_field):
    if mail_col_field != secondary_col_field:
        return secondary_col_field
    return mail_col_field


def semi_space_correction(x, normalizer):
    return normalizer.normalize(x)


def update_city_persian_name_fields(data, x_col_name, y_col_name, city_codes_dict):
    national_code = data[x_col_name]
    city_name_persian_col_field = data[y_col_name]
    city_name_persian_dict_value = city_codes_dict[national_code]

    return correct_field(city_name_persian_col_field, city_name_persian_dict_value)


def update_departure_date_YMD_format_fields(data, x_col_name, y_col_name, months_dict):
    _, day_of_month, month = data[x_col_name].split()
    month_number_str = months_dict[month]
    created_departure_date_YMD_formats = f"1402/{month_number_str}/{day_of_month}"
    departure_date_YMD_formats_col_field = data[y_col_name]

    return correct_field(departure_date_YMD_formats_col_field, created_departure_date_YMD_formats)


def update_dependent_col(main_df, func, x_col_name, y_col_name, your_dict):
    secondary_df = main_df.drop(columns=main_df.columns.difference([x_col_name, y_col_name]), axis=1)
    # secondary_df = main_df[main_df.columns.intersection([x_col_name, y_col_name])]

    main_df[y_col_name] = secondary_df.apply(
        func=func,
        args=(x_col_name, y_col_name, your_dict),
        axis=1)

    return main_df


def move_columns(main_df, cols_name):
    for idx, col_name in enumerate(cols_name):
        column_to_move = main_df.pop(col_name)
        main_df.insert(idx, col_name, column_to_move)
    return main_df


def replace_with(col_df, origin_value, replacement_value, type_value=None):
    col_df = col_df.replace(origin_value, replacement_value)

    if type_value:
        col_df = col_df.astype(float)
    
    return col_df


def check_col_distribution(col_df):
    col_df.hist()
    plt.show()
