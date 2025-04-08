"""Functions for loading datasets that are required to compute the indicators for Provicie Limburg."""
from pathlib import Path
import pandas as pd

from indicatorenplan_limburg.configs.paths import get_path_data


def load_data_vrl(year: int, usecols: int | list[str] | None = None, n_rows: int | None = None) -> pd.DataFrame:
    """Load Data Vestigingsregister Limburg (VRL) for a given year

    Args:
        year (int): year to load
        usecols (int, list, optional): columns to load. Defaults to None.
            If None, all columns are loaded.
        n_rows (int | None, optional): number of rows to load. Defaults to None.
    """
    # Load the processing
    path_data = get_path_data(name='vrl', subfolder='raw') / f"vrl{year}.xlsx"
    df = pd.read_excel(path_data, usecols=usecols, nrows=n_rows)
    return df
