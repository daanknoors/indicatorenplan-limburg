import pytest
import numpy as np
import pandas as pd

from indicatorenplan_limburg.indicatoren.economie import mo7i


def test_categorize_company_size():
    """Test the conversion of categories."""
    # define the ranges
    ranges = ('0-9', '10-49', '50-99', '100-249', '250-9999')

    # test with different employee counts
    df = pd.DataFrame({
        'employee_count': [0, 5, 25, 75, 150, 300, 1000, 10000, -1],
        'expected': ['0-9', '0-9', '10-49', '50-99', '100-249', '250-9999', '250-9999', np.nan, np.nan]
    })

    # convert to categories
    df['dim_grootte'] = mo7i.categorize_company_size(df['employee_count'], ranges=ranges)

    # check if the conversion is correct
    for i, row in df.iterrows():
        # nan does not equal itself thus check for equality
        if pd.isna(row['expected']):
            assert pd.isna(row['dim_grootte']), f"Expected NaN but got {row['dim_grootte']} for employee count {row['employee_count']}"
        else:
            assert row['dim_grootte'] == row['expected'], f"Expected {row['expected']} but got {row['dim_grootte']} for employee count {row['employee_count']}"

def test_mo7i_main(years=(2023, 2024), n_rows=100):
    """Test the main function of the mo7i module."""
    # run the main function
    mo7i.main(years=years, n_rows=n_rows)

    print("Test passed: mo7i.main() with years:", years, "and n_rows:", n_rows)


def test_mo7i_output():
    """Test the output of the mo7i module."""

    # load output
    path_data = mo7i.get_path_data(name='vrl', state='processed')
    path_file = path_data / mo7i.OUTPUT_FILENAME

    # E   UnicodeDecodeError: 'utf-8' codec can't decode byte 0xa6 in position 10: invalid start byte
    df = pd.read_excel(path_file, engine='openpyxl')
    assert df is not None, f"Output file {path_file} is empty."

