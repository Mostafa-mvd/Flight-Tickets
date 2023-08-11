import pandas as pd
import matplotlib.pyplot as plt


dataset_file_path_from = "/home/magnus9102/Mostafa/Py/Github/data-science/source/cleaned_flight_tickets_dataset.csv"
dataset_file_path_to = "/home/magnus9102/Mostafa/Py/Github/data-science/scratch/duplicated_flight_tickets_dataset.csv"

df = pd.read_csv(dataset_file_path_from)
cols_name = df.columns


def check_existence_of_null_values(df, cols_name):
    for col_name in cols_name:
        # if printed true then there is null value in your column
        print(f"{col_name}: {df[col_name].isnull().any()}")


def check_values_count(df, col_name):
    return df[col_name].value_counts()


def number_of_unique_values(df, col_name):
    print(df[col_name].nunique())


# check_existence_of_null_values(df, cols_name)
#‌ print(check_values_count(df, cols_name[-2]))
# number_of_unique_values(df, cols_name[-2])
# print(df.duplicated().sum())

# df_no_duplicates = df.drop_duplicates()
# print(df_no_duplicates.duplicated().sum())

# duplicate_rows = df[df.duplicated()]
# duplicate_rows.to_csv(dataset_file_path_to, index=False)
