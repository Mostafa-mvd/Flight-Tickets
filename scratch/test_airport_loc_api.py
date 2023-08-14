from opencage.geocoder import OpenCageGeocode
from time import sleep


key = 'a46dbe3457cf42bcab87bc5a69dbd008'
geocoder = OpenCageGeocode(key)

airports_geometry = dict()

airports = [
    {
        "airport_code": "DEF",
        "airport_name": "Dezful",
        "country_code": "IR"
    },
    {
        "airport_code": "SHJ",
        "airport_name": "Sharjah",
        "country_code": "AE"
    },
    {
        "airport_code": "SAW",
        "airport_name": "Sabiha Gokcen",
        "country_code": "TR"
    }
]

no_annotations = 1
no_dedupe = 1
pretty = 1


for airport in airports:
    query = airport["airport_name"] + " Airport"
    # query = airport["airport_code"]
    countrycode = airport["country_code"]
    result_lst = geocoder.geocode(query=query, 
                                countrycode=countrycode,
                                no_annotations=no_annotations,
                                no_dedupe=no_dedupe,
                                pretty=pretty)
    sleep(1)

    if result_lst:
        for result_dict in result_lst:
            components_dict = result_dict["components"]
            _category, _type = components_dict["_category"], components_dict["_type"]

            if _category == "transportation" and _type == "aeroway":
                airport_name = components_dict["aeroway"]
                airport_road_name = components_dict["road"]
                
                if ("Airport" in airport_name or
                    "Airport" in airport_road_name):

                    airports_geometry[airport_name] = result_dict["geometry"]
    else:
        print("There is no result.")

print(airports_geometry)