import pytest

from indicatorenplan_limburg.data.load import load_data_vrl
from indicatorenplan_limburg.configs.paths import PATH_DATA_SETS


def test_load_data_vrl():
    years = [2024]
    n_rows = 100
    usecols = ["PEILDATUM", "COROP_NAAM", "SBI_1_NAAM", "WP_FPU_TOTAAL"]
    for year in years:
        df = load_data_vrl(year, usecols=usecols, n_rows=n_rows)

        assert df is not None, f"Data for year {year} could not be loaded."
        assert not df.empty, f"Data for year {year} is empty."
        assert set(usecols).issubset(df.columns), f"Data for year {year} does not contain the expected columns."
