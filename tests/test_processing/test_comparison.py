import pytest
import pandas as pd

from indicatorenplan_limburg.processing.comparison import compare_datasets


def test_raises_error_for_different_columns():
    df1 = pd.DataFrame({'A': [1, 2], 'B': [3, 4]})
    df2 = pd.DataFrame({'A': [1, 2], 'C': [3, 4]})
    with pytest.raises(ValueError, match="DataFrames have different columns"):
        compare_datasets(df1, df2)

def test_returns_empty_dataframe_for_identical_data():
    df1 = pd.DataFrame({'A': [1, 2], 'B': [3, 4]})
    df2 = pd.DataFrame({'A': [1, 2], 'B': [3, 4]})
    result = compare_datasets(df1, df2)
    assert result.empty

def test_returns_differences_for_mismatched_data():
    df1 = pd.DataFrame({'A': [1, 2], 'B': [3, 4]})
    df2 = pd.DataFrame({'A': [1, 3], 'B': [3, 5]})
    result = compare_datasets(df1, df2)
    assert not result.empty
    assert result.loc[1, ('A', 'self')] == 2
    assert result.loc[1, ('A', 'other')] == 3
    assert result.loc[1, ('B', 'self')] == 4
    assert result.loc[1, ('B', 'other')] == 5

def handles_empty_dataframes_correctly():
    df1 = pd.DataFrame(columns=['A', 'B'])
    df2 = pd.DataFrame(columns=['A', 'B'])
    result = compare_datasets(df1, df2)
    assert result.empty