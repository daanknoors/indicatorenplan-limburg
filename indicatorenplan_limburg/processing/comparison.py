"""Compare equivalence between two datasets. Handy for verifying whether the output is consistent
and spot differences between two datasets."""

import pandas as pd


def compare_datasets(df1: pd.DataFrame, df2: pd.DataFrame) -> pd.DataFrame:
    """Compare two datasets and return the differences.

    Args:
        df1 (pd.DataFrame): First dataset.
        df2 (pd.DataFrame): Second dataset.

    Returns:
        pd.DataFrame: DataFrame containing the differences between the two datasets.
    """
    # check same shape
    if df1.shape != df2.shape:
        raise ValueError("DataFrames have different shapes")

    # ensure both DataFrames have the same columns
    if set(df1.columns) != set(df2.columns):
        raise ValueError("DataFrames have different columns")

    # check whether all rows are equal
    df_diff = df1.compare(df2, keep_equal=False, keep_shape=False)
    return df_diff

