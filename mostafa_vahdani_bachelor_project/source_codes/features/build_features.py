# Python scripts or Jupyter notebooks that contain code to generate, transform, or manipulate features from raw data. These scripts might involve tasks like encoding categorical variables, scaling numeric features, feature selection,creating interaction terms, etc.

import pandas as pd

from jdatetime import datetime


def flight_dep_time(X):
    if int(X[:2]) >= 0 and int(X[:2]) < 6:
        return 'mid_night'
    elif int(X[:2]) >= 6 and int(X[:2]) < 12:
        return 'morning'
    elif int(X[:2]) >= 12 and int(X[:2]) < 18:
        return 'afternoon'
    elif int(X[:2]) >= 18 and int(X[:2]) < 20:
        return 'evening'
    elif int(X[:2]) >= 20 and int(X[:2]) < 24:
        return 'night'


def flight_duration_sec(X):
    return int(X) * 60


processed_dataset_path = "/home/magnus9102/Mostafa/Py/Github/data-science/mostafa_vahdani_bachelor_project/data/processed/flight_tickets_dataset.csv"

df = pd.read_csv(processed_dataset_path)

# Converting flight departure_date_YMD_format type from string to jdatatime
df['departure_date_YMD_format'] = df['departure_date_YMD_format'].apply(lambda d: datetime.strptime(d, '%Y-%m-%d'))

# Splitting the departure_date_YMD_format into day, month and year.
df["year"] = df['departure_date_YMD_format'].map(lambda x: x.year)
df["month"] = df['departure_date_YMD_format'].map(lambda x: x.month)
df["day"] = df['departure_date_YMD_format'].map(lambda x: x.day)

# ‌Converting the flight local_departure_time into proper time
df['dep_flight_time'] = df['local_departure_time'].apply(flight_dep_time)

# Converting the flight duration to seconds
df['duration_sec'] = df['flight_length_min'].apply(flight_duration_sec)

# Removing the unused features
df.drop(["national_departure_code",
         "departure_airport",
         "national_arrival_code",
         "arrival_airport",
         "orthodromic_distance_KM",
         "flight_length_min",
         "departure_date_YMD_format",
         "local_departure_time",
         "local_arrival_time",
         "flight_number"],
        inplace=True,
        axis=1)

df.to_csv("/home/magnus9102/Mostafa/Py/Github/data-science/mostafa_vahdani_bachelor_project/data/interim/build_features_flight_tickets_dataset.csv", index=False)