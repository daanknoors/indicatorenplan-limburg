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
    path_dir = Path(path_dir).expanduser()
    # check if directory exists
    if not path_dir.is_dir():
        raise FileNotFoundError(f"Directory {path_dir} does not exist")
    # check if directory is empty
    if not any(path_dir.iterdir()):
        raise FileNotFoundError(f"Directory {path_dir} is empty")

    # load all files with the given extensions
    data_dict = {}
    for ext in file_extensions:
        files = path_dir.glob(f"*{ext}")
        for file in files:
            try:
                df = pd.read_excel(file, usecols=usecols, engine='openpyxl') if ext == '.xlsx' else pd.read_csv(file, usecols=usecols)
                data_dict[file.stem] = df
            except Exception as e:
                raise ValueError(f"Failed to load {file}: {e.__class__.__name__} - {e}")

    # warn if no files are found
    if not data_dict:
        raise FileNotFoundError(f"No files found in {path_dir} with extensions {file_extensions}")
    return data_dict