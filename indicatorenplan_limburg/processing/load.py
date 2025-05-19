"""Functions for loading datasets that are required to compute the indicators for Provicie Limburg."""
from pathlib import Path
import pandas as pd


def load_all_data_in_dir(path_dir: Path,
                         file_extensions: list[str] = ('.xlsx', '.csv'),
                         usecols: list[str] | None = None) -> dict[str, pd.DataFrame]:
    """Load all data in a directory with the given file extensions

    Args:
        path_dir (Path): path to the directory
        file_extensions (list[str], optional): file extensions to load. Defaults to ['.xlsx', '.csv'].
        usecols (list[str], optional): columns to load. Can speed things up. Defaults to None.
            If None, all columns are loaded.

    Returns:
        dict[str, pd.DataFrame]: dictionary with the name of the file as key and the dataframe as value
    """
    data_dict = {}
    for ext in file_extensions:
        for file in path_dir.glob(f"*{ext}"):
            df = pd.read_excel(file, usecols=usecols) if ext == '.xlsx' else pd.read_csv(file, usecols=usecols)
            data_dict[file.stem] = df
    return data_dict