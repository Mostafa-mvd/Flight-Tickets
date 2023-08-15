import json

from opencage.geocoder import OpenCageGeocode

from time import sleep
from common_utils.utils import get_json_obj

from settings import OPENCAGEDATA_API_KEY, SOURCES

max_recursive_depth = 0

def get_airport_geographic_coordinate(geo_coder, q, country_code, no_annotations=1, 
                                      no_dedupe=1, pretty_output=1, language='en', airport_name=None):
    """This function is just working on 'OpenCageGeocode web api' results for my specific task."""
    global max_recursive_depth

    if max_recursive_depth == 2:
        return None
    
    result_lst = geo_coder.geocode(query=q, countrycode=country_code, no_dedupe=no_dedupe,
                                   no_annotations=no_annotations, pretty=pretty_output,
                                   language=language)
    sleep(2)

    for result_dict in result_lst:
        components_dict = result_dict["components"]
        _category, _type = components_dict["_category"], components_dict["_type"]

        if (_category == "transportation" and 
            _type == "aeroway"):

            airport_name = components_dict["aeroway"]

            return {airport_name: result_dict["geometry"]}
        
    max_recursive_depth += 1
    return get_airport_geographic_coordinate(geo_coder,
                                             q=f"{airport_name} Airport",
                                             country_code=country_code,)


if __name__ == "__main__":
    airports_geometry_lst = list()
    airports_info_dict = get_json_obj(SOURCES["airports_info_json_file_path"])
    geo_coder = OpenCageGeocode(OPENCAGEDATA_API_KEY)

    for airport_val in airports_info_dict.values():
        airport_code = airport_val["airport_code"]
        country_code = airport_val["country_code"]
        airport_name = airport_val["airport_names"][-1]

        airport_geometry_dict = get_airport_geographic_coordinate(geo_coder, 
                                                                  airport_code,
                                                                  country_code,
                                                                  airport_name=airport_name)

        if airport_geometry_dict:
            airports_geometry_lst.append(airport_geometry_dict)
    
    with open(SOURCES["airports_geometry_json_file_path"], 'w') as fp:
        airports_geometry_lst.append({"Total Length": len(airports_geometry_lst)})
        json.dump(airports_geometry_lst, fp, indent=4)
