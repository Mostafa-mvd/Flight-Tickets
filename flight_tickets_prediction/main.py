import numpy as np
import pandas as pd

from hazm import Normalizer

from settings import (SOURCES, COLUMNS_NEED_TO_MOVE)

from required_data import (MONTH_DICT, AIRPORT_CITIES_NAME_EN_LOCALIZATION_DICT)

from airlines_tickets_prediction import (get_city_codes_dict,
                                         update_city_persian_name_fields,
                                         update_departure_date_YMD_format_fields,
                                         update_dependent_col,
                                         semi_space_correction,
                                         move_columns,
                                         replace_with,
                                         change_field_value_to_en)


city_codes_dict = get_city_codes_dict(SOURCES["json_file_path_from"])

text_normalizer = Normalizer(persian_numbers=False)

df = pd.read_csv(SOURCES["dataset_file_path_from"])

df = df.drop(["ticket_id"], axis=1)

df = df.drop_duplicates()

df["capacity"] = replace_with(df["capacity"], "موجود", np.nan, float)

df = update_dependent_col(
    df,
    update_city_persian_name_fields,
    "national_arrival_code",
    "arrival_city_name_persian",
    city_codes_dict)

df = update_dependent_col(
    df,
    update_city_persian_name_fields,
    "national_departure_code",
    "departure_city_name_persian",
    city_codes_dict)

df["departure_date"] = df["departure_date"].apply(func=semi_space_correction, args=(text_normalizer,))

df = update_dependent_col(
    df,
    update_departure_date_YMD_format_fields,
    "departure_date",
    "departure_date_YMD_format",
    MONTH_DICT)

df = df.sort_values(by=['departure_date_YMD_format', 'departure_time', 'arrival_time'], ascending=True)

df["arrival_city_name_persian"] = df["arrival_city_name_persian"].apply(
    func=change_field_value_to_en,
    args=(AIRPORT_CITIES_NAME_EN_LOCALIZATION_DICT, ))

df["departure_city_name_persian"] = df["departure_city_name_persian"].apply(
    func=change_field_value_to_en,
    args=(AIRPORT_CITIES_NAME_EN_LOCALIZATION_DICT, ))

df = move_columns(
    df,
    COLUMNS_NEED_TO_MOVE)

df.to_csv(SOURCES["dataset_file_path_to"], index=False)
