
import pathlib

BASE_PATH = pathlib.Path(__file__).parent.parent

SOURCES = {
    "dataset_file_path_from": BASE_PATH.joinpath("source", "final_flight_tickets_dataset.csv"),
    "dataset_file_path_to": BASE_PATH.joinpath("source", "cleaned_flight_tickets_dataset.csv"),
    "json_file_path_from": BASE_PATH.joinpath("source", "airport_city_codes.json"),
}

COLUMNS_NEED_TO_MOVE = {
    "arrival_city_name_persian": 0,
    "national_arrival_code": 1,
    "departure_city_name_persian": 2,
    "national_departure_code": 3,
    "departure_date": 4,
    "departure_date_YMD_format": 5,
    "departure_time": 6,
    "arrival_time": 7,
    "capacity": 8,
}
