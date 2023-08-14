import numpy as np
import pandas as pd

from hazm import Normalizer

from settings import (SOURCES, COLUMNS_NEED_TO_MOVE)

from required_data import MONTH_DICT, AIRPORT_CODES_DICT, AIRPORTS_INFO_DICT

from airlines_tickets_prediction import (extract_values_from_json_obj,
                                         change_city_names_to_en,
                                         get_city_airport_names,
                                         create_flatten_dict,
                                         update_city_persian_name_fields,
                                         update_departure_date_YMD_format_fields,
                                         update_dependent_col,
                                         semi_space_correction,
                                         move_columns,
                                         replace_with)


CITY_AIRPORT_CODES_LST = extract_values_from_json_obj(AIRPORT_CODES_DICT, "id")
CITY_AIRPORT_NAMES_FA_LST = extract_values_from_json_obj(AIRPORT_CODES_DICT, "city")
CITY_CODES_DICT = create_flatten_dict(CITY_AIRPORT_CODES_LST, CITY_AIRPORT_NAMES_FA_LST)

text_normalizer = Normalizer(persian_numbers=False)

df = pd.read_csv(SOURCES["dataset_file_path_from"])

df = df.drop(["ticket_id"], axis=1)

df = df.drop_duplicates()

df["capacity"] = replace_with(df["capacity"], "موجود", np.nan, float)

# Fill where fields of arrival_city_name_persian column are empty.
df = update_dependent_col(
    df,
    update_city_persian_name_fields,
    "national_arrival_code",
    "arrival_city_name_persian",
    CITY_CODES_DICT)

# Fill where fields of departure_city_name_persian column are empty.
df = update_dependent_col(
    df,
    update_city_persian_name_fields,
    "national_departure_code",
    "departure_city_name_persian",
    CITY_CODES_DICT)

df["departure_date"] = df["departure_date"].apply(func=semi_space_correction, args=(text_normalizer,))

# Fill where fields of departure_date_YMD_format column are empty.
df = update_dependent_col(
    df,
    update_departure_date_YMD_format_fields,
    "departure_date",
    "departure_date_YMD_format",
    MONTH_DICT)

df = df.sort_values(by=['departure_date_YMD_format', 'departure_time', 'arrival_time'], ascending=True)

# Change arrival city names from persian to english.
df["arrival_city"] = df["arrival_city_name_persian"].apply(
    func=change_city_names_to_en,
    args=(AIRPORTS_INFO_DICT,))

# Change departure city names from persian to english.
df["departure_city"] = df["departure_city_name_persian"].apply(
    func=change_city_names_to_en,
    args=(AIRPORTS_INFO_DICT,))

# Add arrival_airport column
df["arrival_airport"] = df["arrival_city_name_persian"].apply(
    func=get_city_airport_names,
    args=(AIRPORTS_INFO_DICT,))

# Add departure_airport column
df["departure_airport"] = df["departure_city_name_persian"].apply(
    func=get_city_airport_names,
    args=(AIRPORTS_INFO_DICT,))

# Deleting columns
df = df.drop(["arrival_city_name_persian", "departure_city_name_persian"], axis=1)

#Move position of columns.
df = move_columns(
    df,
    COLUMNS_NEED_TO_MOVE)

# Save to csv file
df.to_csv(SOURCES["dataset_file_path_to"], index=False)
