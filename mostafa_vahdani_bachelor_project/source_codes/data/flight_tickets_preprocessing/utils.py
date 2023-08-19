import pandas as pd
from settings import SOURCES


def difference_drop(df, *args):
    """difference drop with column names that you will give on *args"""
    return df.drop(columns=df.columns.difference([*args]), axis=1)


def check_existence_of_null_values(df, cols_name):
    for col_name in cols_name:
        # if printed true then there is null value in your column
        print(f"{col_name}: {df[col_name].isnull().any()}")


def values_count(df, col_name):
    return df[col_name].value_counts()


def count_unique_values(df, col_name):
    return f"Length: {df[col_name].nunique()}"


def check_space_existence(df, cols_name):
    for col_name in cols_name:
        # if result is true then there is field that has space value.
        result = any(list(map(lambda x: True if str(x).find(' ') != -1 else False, df[col_name])))
        print(f"{col_name}: {result}")


raw_dataset_file_path = SOURCES["dataset_file_path_from"]
processed_dataset_file_path_ = SOURCES["dataset_file_path_to"]

df = pd.read_csv(processed_dataset_file_path_)
cols_name = df.columns


# print(count_unique_values(df, "company_name"))
# print("---")
# check_existence_of_null_values(df, ["flight_number"])
# print("---")
print(values_count(df, "company_name"))
# print("---")
# print(df.duplicated().sum())
# print("---")
# check_space_existence(df, ["flight_number"])
# print("---")


# df_no_duplicates = df.drop_duplicates()
# print(df_no_duplicates.duplicated().sum())

# duplicate_rows = df[df.duplicated()]
