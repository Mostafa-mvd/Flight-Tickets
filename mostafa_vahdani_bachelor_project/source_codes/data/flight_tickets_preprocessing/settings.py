
import pathlib

DATASET_BASE_PATH = pathlib.Path(__file__).parent.parent.parent.parent
PROJECT_BASE_PATH = pathlib.Path(__file__).parent.parent

SOURCES = {
    # datasets
    "dataset_file_path_from": DATASET_BASE_PATH.joinpath("data", "raw", "flight_tickets_dataset.csv"),
    "dataset_file_path_to": DATASET_BASE_PATH.joinpath("data", "processed", "flight_tickets_dataset.csv"),
    # statics
    "airport_codes_json_file_path": PROJECT_BASE_PATH.joinpath("static", "airport_city_codes.json"),
    "airports_info_json_file_path": PROJECT_BASE_PATH.joinpath("static", "airports_info.json"),
    "months_json_file_path": PROJECT_BASE_PATH.joinpath("static", "months.json"),
}

COLUMNS_NEED_TO_MOVE = {
    "arrival_city": 4,
    "national_arrival_code": 3,
    "departure_city": 1,
    "national_departure_code": 0,
    "departure_airport": 2,
    "arrival_airport": 5,
    "departure_date": 6,
    "departure_date_YMD_format": 7,
    "departure_time": 8,
    "arrival_time": 9,
    "capacity": 10,
}
