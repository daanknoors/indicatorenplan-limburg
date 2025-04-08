import pytest
import numpy as np
import pandas as pd

from indicatorenplan_limburg.indicatoren.toekomstbestendige_economie import mo_7i
from indicatorenplan_limburg.configs import paths


def test_categorize_company_size():
    """Test the conversion of categories."""
    # define the ranges
    ranges = ('0_9', '10_49', '50_99', '100_249', '250_9999')

    # test with different employee counts
    df = pd.DataFrame({
        'employee_count': [0, 5, 25, 75, 150, 300, 1000, 9999],
        'expected': ['0_9', '0_9', '10_49', '50_99', '100_249', '250_9999', '250_9999', '250_9999']
    })

    # convert to categories
    df['dim_grootte'] = mo_7i.categorize_company_size(df['employee_count'], ranges=ranges)

    # check if the conversion is correct
    for i, row in df.iterrows():
        # nan does not equal itself thus check for equality
        if pd.isna(row['expected']):
            assert pd.isna(row['dim_grootte']), f"Expected NaN but got {row['dim_grootte']} for employee count {row['employee_count']}"
        else:
            assert row['dim_grootte'] == row['expected'], f"Expected {row['expected']} but got {row['dim_grootte']} for employee count {row['employee_count']}"

    # check assertion error
    with pytest.raises(AssertionError):
        # test case outside the defined ranges
        df_outside = pd.DataFrame({
            'employee_count': [-1, 10000],
            'expected': [np.nan, np.nan]
        })
        mo_7i.categorize_company_size(df_outside['employee_count'], ranges=ranges)


def test_mo_7i_main(years=(2023, 2024), n_rows=100, state='test'):
    """Test the main function of the mo_7i module."""
    # run the main function
    save_path = paths.get_path_data(name='vrl', subfolder=state)

    mo_7i.main(years=years, n_rows=n_rows, save_path=save_path)

    print("Test passed: mo_7i.main() with years:", years, "and n_rows:", n_rows)


def test_mo_7i_output(state='test'):
    """Test the output of the mo_7i module."""

    # load output
    save_path = mo_7i.get_path_data(name='vrl', subfolder=state)
    path_file = save_path / mo_7i.OUTPUT_FILENAME

    # E   UnicodeDecodeError: 'utf-8' codec can't decode byte 0xa6 in position 10: invalid start byte
    df = pd.read_excel(path_file, engine='openpyxl')
    assert df is not None, f"Output file {path_file} is empty."

