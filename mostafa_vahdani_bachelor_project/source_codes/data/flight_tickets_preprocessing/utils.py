from matplotlib import pyplot as plt


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


def get_masked_df(df, col_name, specific_value):
    mask = (df[col_name] == specific_value)
    return mask, df[mask]


def apply_to_df_by_mask(main_df, mask, masked_df, col_name, your_func):
    main_df.loc[mask, col_name] = masked_df[col_name].apply(func=your_func)


def group_by_count(df, *args):
    """last column name on the args is the column you want to apply count() on it"""
    return df.groupby([*args])[args[-1]].count()


def count_duplicated(df):
    return df.duplicated().sum()


def check_col_distribution(col_df):
    col_df.hist()
    plt.show()


def filter_rows_by_values(df, col, values):
    df.drop(df[df[col].isin(values)].index, inplace=True)


if __name__ == '__main__':
    import pandas as pd
    from settings import SOURCES

    raw_dataset_file_path = SOURCES["dataset_file_path_from"]
    processed_dataset_file_path = SOURCES["dataset_file_path_to"]

    df = pd.read_csv(processed_dataset_file_path)
    col_names = df.columns


    #‌ print(count_unique_values(df, "flight_class_type"))
    # df2 = values_count(df, "flight_class_type")
    print(check_existence_of_null_values(df, col_names))

    # df2.to_csv("/home/magnus9102/Mostafa/Py/Github/data-science/mostafa_vahdani_bachelor_project/source_codes/data/scratch/f.csv")

