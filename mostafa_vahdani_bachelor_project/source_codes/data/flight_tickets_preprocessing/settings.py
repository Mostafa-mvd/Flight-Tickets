
import os
import pathlib
from dotenv import load_dotenv

load_dotenv()

DATASET_BASE_PATH = pathlib.Path(__file__).parent.parent.parent.parent
PROJECT_BASE_PATH = pathlib.Path(__file__).parent.parent

SOURCES = {
    # datasets
    "dataset_file_path_from": DATASET_BASE_PATH.joinpath("data", "raw", "flight_tickets_dataset.csv"),
    "dataset_file_path_to": DATASET_BASE_PATH.joinpath("data", "processed", "flight_tickets_dataset.csv"),
    # statics
    "static_dir_path": PROJECT_BASE_PATH.joinpath("static"),
    "airport_codes_json_file_path": PROJECT_BASE_PATH.joinpath("static", "airport_city_codes.json"),
    "airports_info_json_file_path": PROJECT_BASE_PATH.joinpath("static", "airports_info.json"),
    "airports_geometry_json_file_path": PROJECT_BASE_PATH.joinpath("static", "airports_geometry.json"),
    "months_json_file_path": PROJECT_BASE_PATH.joinpath("static", "months.json"),
    "airlines_code_json_path": PROJECT_BASE_PATH.joinpath("static", "airlines_code.json"),
}

COLUMNS_NEED_TO_MOVE = {
    "arrival_city": 4,
    "national_arrival_code": 3,
    "departure_city": 1,
    "national_departure_code": 0,
    "departure_airport": 2,
    "arrival_airport": 5,
    "departure_date_YMD_format": 8,
    "local_departure_time": 9,
    "local_arrival_time": 10,
    "flight_number": 12,
    "ticket_price_T": 13,
    "company_name": 11,
    "orthodromic_distance_KM": 6,
    "flight_length_min": 7,
    "flight_sale_type": 14,
    "flight_class_type": 15,
    "flight_capacity": 16
}

OPENCAGEDATA_API_KEY = os.getenv("OPENCAGEDATA_API_KEY")
