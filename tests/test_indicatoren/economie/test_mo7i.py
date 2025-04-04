import pytest
import pandas as pd

from indicatorenplan_limburg.indicatoren.economie import mo7i


def test_categorize_company_size():
    """Test the conversion of categories."""
    # fill values outside the bounds
    fill_na = 'outside_bounds'
    # test with different employee counts
    df = pd.DataFrame({
        'employee_count': [0, 5, 25, 75, 150, 300, 1000, 10000],
        'expected': ['0 - 9', '0 - 9', '10 - 49', '50 - 99', '100 - 249', '250 - 9999', '250 - 9999', fill_na]
    })

    bounds = [0, 10, 50, 100, 250, 10000]

    # convert to categories
    df['dim_grootte'] = mo7i.categorize_company_size(df['employee_count'], bounds=bounds, fill_na=fill_na)

    # check if the conversion is correct
    for i, row in df.iterrows():
        assert row['dim_grootte'] == row['expected'], f"Expected {row['expected']} but got {row['dim_grootte']} for employee count {row['employee_count']}"


def test_mo7i_main():
    """Test the main function of the mo7i module."""

    # run the main function
    years = [2023, 2024]
    mo7i.main(years=years)

def test_mo7i_output():
    """Test the output of the mo7i module."""

    # load output
    path_data = mo7i.get_path_data(name='vrl', state='processed')
    path_file = path_data / "MO-7i.xlsx"

    # E   UnicodeDecodeError: 'utf-8' codec can't decode byte 0xa6 in position 10: invalid start byte
    df = pd.read_excel(path_file, engine='openpyxl')
    assert df is not None, f"Output file {path_file} is empty."

