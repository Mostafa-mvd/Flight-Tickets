
from hazm import Normalizer
import pandas as pd
from airlines_tickets_prediction import (get_city_codes_dict,
                                         update_city_persian_name_fields,
                                         update_departure_date_YMD_format_fields,
                                         update_dependent_col,
                                         semi_space_correction)


dataset_file_path_from = "/home/magnus9102/Mostafa/Py/Github/data-science/source/final_flight_tickets_dataset.csv"
dataset_file_path_to = "/home/magnus9102/Mostafa/Py/Github/data-science/source/my_data.csv"
json_file_path_from = "/home/magnus9102/Mostafa/Py/Github/data-science/source/airport_city_codes.json"

month_dict = {
    "فروردین": "01",
    "اردیبهشت": "02",
    "خرداد": "03",
    "تیر": "04",
    "مرداد": "05",
    "شهریور": "06",
    "مهر": "07",
    "آبان": "08",
    "آذر": "09",
    "دی": "10",
    "بهمن": "11",
    "اسفند": "12",
}

df = pd.read_csv(dataset_file_path_from)

df = df.drop(["ticket_id"], axis=1)

city_codes_dict = get_city_codes_dict(json_file_path_from)

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

text_normalizer = Normalizer(persian_numbers=False)
df["departure_date"] = df["departure_date"].apply(func=semi_space_correction, args=(text_normalizer,))

df = update_dependent_col(
    df,
    update_departure_date_YMD_format_fields,
    "departure_date",
    "departure_date_YMD_format",
    month_dict)

df.to_csv(dataset_file_path_to, index=False)
