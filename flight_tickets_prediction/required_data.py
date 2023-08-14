from airlines_tickets_prediction import get_json_obj
from settings import SOURCES


MONTH_DICT = get_json_obj(SOURCES["months_json_file_path"])
AIRPORT_CODES_DICT = get_json_obj(SOURCES["airport_codes_json_file_path"])
AIRPORTS_INFO_DICT = get_json_obj(SOURCES["airports_info_json_file_path"])
