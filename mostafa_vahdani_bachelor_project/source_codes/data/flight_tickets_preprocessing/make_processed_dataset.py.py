import pandas as pd

from hazm import Normalizer

from tickets_preprocessing import (change_city_names_to_en, difference_drop,
                                   estimate_flight_length, estimate_arrival_time,
                                   orthodromic_distance, get_city_airport_names,
                                   update_city_persian_name_fields,
                                   update_departure_date_YMD_format_fields,
                                   update_dependent_col, semi_space_correction,
                                   move_columns, update_flight_sale_type, 
                                   change_company_name_specific_value,
                                   change_flight_class_type_specific_value,
                                   update_flight_number_col, extract_fare_class_code,
                                   fillna_capacity)

from common_utils.utils import (get_json_obj, create_flatten_dict,
                                extract_values_from_json_obj)

from utils import (filter_rows_by_values,
                   advance_mode,
                   fill_with_random)

from settings import (SOURCES, COLUMNS_NEED_TO_MOVE)


MONTH_DICT = get_json_obj(SOURCES["months_json_file_path"])
AIRPORT_CODES_DICT = get_json_obj(SOURCES["airport_codes_json_file_path"])
AIRPORTS_INFO_DICT = get_json_obj(SOURCES["airports_info_json_file_path"])
AIRPORTS_GEOMETRY_DICT = get_json_obj(SOURCES["airports_geometry_json_file_path"])
AIRLINE_CODES_DICT = get_json_obj(SOURCES["airlines_code_json_path"])

CITY_AIRPORT_CODES_LST = extract_values_from_json_obj(AIRPORT_CODES_DICT, "id")
CITY_AIRPORT_NAMES_FA_LST = extract_values_from_json_obj(AIRPORT_CODES_DICT, "city")
CITY_CODES_DICT = create_flatten_dict(CITY_AIRPORT_CODES_LST, CITY_AIRPORT_NAMES_FA_LST)

text_normalizer = Normalizer(persian_numbers=False)

df = pd.read_csv(SOURCES["dataset_file_path_from"])

# The prediction of the cheapest price of the plane ticket in a certain period of time is not a function of capacity and id.
df = df.drop(["ticket_id"], axis=1)

# Drop exact same rows.
df = df.drop_duplicates()

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

df = df.sort_values(by=['departure_date_YMD_format', 'local_departure_time', 'local_arrival_time'], ascending=True)

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
df = df.drop(["arrival_city_name_persian", 
              "departure_city_name_persian",
              "departure_date"], axis=1)

# Add orthodromic distance col based on kilometer
df2 = difference_drop(df, "national_departure_code", "national_arrival_code")

df["orthodromic_distance_KM"] = df2.apply(func=orthodromic_distance,
                                          args=(AIRPORTS_GEOMETRY_DICT,),
                                          axis=1)

# Add flight length col based on minutes
df2 = difference_drop(df, "orthodromic_distance_KM")
df["flight_length_min"] = df2.apply(func=estimate_flight_length, axis=1)

# Estimating arrival_time col
df["local_arrival_time"] = df.apply(func=estimate_arrival_time, axis=1)

# Changing specific values
df["company_name"] = df["company_name"].apply(func=change_company_name_specific_value)
df["flight_class_type"] = df["flight_class_type"].apply(func=change_flight_class_type_specific_value)

# Replacing space values
df["departure_city"] = df["departure_city"].replace(' ', '_', regex=True)
df["departure_airport"] = df["departure_airport"].replace(' ', '_', regex=True)
df["arrival_city"] = df["arrival_city"].replace(' ', '_', regex=True)
df["arrival_airport"] = df["arrival_airport"].replace(' ', '_', regex=True)
df["company_name"] = df["company_name"].replace(' ', '', regex=True)
df["flight_class_type"] = df["flight_class_type"].replace(' ', '', regex=True)


# Deleting 422 rows due to the absence of the mentioned company, its IATA, ICAO or call sign with specific ticket price in the collected data.
# (422 * 100) / 13972 = 3% -> It is just 3 percent of our main data so simply I removed it.
filter_rows_by_values(df, "company_name", ['J1', 'SR', 'RI', 'Flypersia', 'Asajet', 'Pouya', 'Pars'])

# Updating flight_number col
df2 = difference_drop(df, "flight_number", "company_name")

df["flight_number"] = df2.apply(func=update_flight_number_col,
                                args=(AIRLINE_CODES_DICT,),
                                axis=1)

# Extracting fare class code
df['fare_class_code'] = df["flight_class_type"].apply(func=extract_fare_class_code)
df = df.drop(["flight_class_type"], axis=1)

# Fill fare_class_code col with the most frequent value of fare class in each company group.
result = df.groupby('company_name')['fare_class_code'].apply(lambda group: group.fillna(group.mode().iloc[0]))
df['fare_class_code'] = result.droplevel(0)

# Changed to english
df['flight_sale_type'] = df["flight_sale_type"].apply(func=update_flight_sale_type)

# Fill flight_sale_type col with the most frequent value of sale type in each (company & fare_class_code) group.

# Be careful index of result in this situation is MultiIndex. (Hierarchical index)
# Our flight_sale_type in dataframe is Indexed not MultiIndexed. (Index -> one-dimensional labeled arrays)
# You can think of MultiIndex as an array of tuples where each tuple is unique.
result = df.groupby(["company_name", "fare_class_code"])['flight_sale_type'].apply(advance_mode)
# Convert MultiIndexed result to Indexed result then set label name for index with existence of current column.
indexed_result = result.reset_index().set_index('level_2')
# Drop the columns we don't want.
dropped_result = indexed_result.drop(["company_name", "fare_class_code"], axis=1)
# Now dropped_result and our df are in the same index size.
df['flight_sale_type'] = dropped_result["flight_sale_type"]

# Random Imputation of flight_sale_type
df = fill_with_random(df, "flight_sale_type")

# Fill Capacity
df["flight_capacity"] = df["flight_capacity"].replace('موجود', None, regex=True)

# df["flight_capacity"] = fillna_capacity(df[["flight_capacity"]])
df["flight_capacity"] = df["flight_capacity"].fillna(method='bfill')


# Move position of columns.
df = move_columns(
    df,
    COLUMNS_NEED_TO_MOVE)

# Save to csv file
df.to_csv(SOURCES["dataset_file_path_to"], index=False)
