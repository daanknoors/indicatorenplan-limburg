"""Functions for loading datasets that are required to compute the indicators for Provicie Limburg."""
from pathlib import Path
import pandas as pd

from indicatorenplan_limburg.configs.paths import get_path_data


def load_data_vrl(year: int, usecols: None | list[str] = None) -> pd.DataFrame:
    """Load Data Vestigingsregister Limburg (VRL) for a given year

    Args:
        year (int): year to load
        usecols (None, optional): columns to load. Defaults to None.
            If None, all columns are loaded.
    """
    # Load the data
    path_data = get_path_data(name='vrl', state='raw') / f"vrl{year}.xlsx"
    df = pd.read_excel(path_data, usecols=usecols)
    return df
