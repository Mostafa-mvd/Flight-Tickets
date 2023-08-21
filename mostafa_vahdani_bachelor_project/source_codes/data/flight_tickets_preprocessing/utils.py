import numpy as np
import pandas as pd

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


def count_null_values(df, col_name):
    return df[col_name].isnull().sum()


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


def count_specific_value_in_col(df, col_name, sp_value):
    return (df[col_name] == sp_value).sum()


def advance_mode(group):
    mode = group.mode()
    if not mode.empty:
        return group.fillna(group.mode().iloc[0])
    return group


def fill_with_random(df, column):
    df2 = df.copy()
    df2[column] = df2[column].apply(lambda x: np.random.choice(
        df2[column].dropna().values) if pd.isnull(x) else x)
    return df2
