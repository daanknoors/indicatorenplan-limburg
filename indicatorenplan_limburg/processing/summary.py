"""Create a summary of dataframes in a directory."""

import pandas as pd
from pathlib import Path

from indicatorenplan_limburg.configs import paths

def summarize_dataset(df: pd.DataFrame, n_rows: int, sheet_name=None) -> None:
    """Print summary of dataframe."""
    with pd.option_context('display.max_rows', 500, 'display.max_columns', 200):
        if sheet_name:
            print(f"\nSummary of sheet '{sheet_name}':")
        print(f"First {n_rows} rows:")
        print(df.head(n_rows))
        print("\nShape:")
        print(df.shape)
        print("\nColumns:")
        print(df.columns.tolist())
        print("\nDtypes:")
        print(df.dtypes)




def show_summary_data_in_dir(directory: Path | str, n_rows: int = 5) -> None:
    """Show a summary of dataframes in a directory, including first rows, shape, columns, and dtypes.
    Support excel and csv. Warn about other file types present in directory.

    Args:
        directory (Path | str): Directory containing the data files.
        n_rows (int): Number of rows to show in the summary.
    """


    if isinstance(directory, str):
        directory = Path(directory)


    directory = directory.expanduser()
    if not directory.exists():
        print(f"Directory {directory} does not exist.")
        return

    if not directory.is_dir():
        print(f"{directory} is not a directory.")
        return

    # Get all files in the directory
    files = list(directory.glob('*'))
    print(f"Found {len(files)} files in {directory}:")
    for file in files:
        print(f"- {file.code}")
    print(f"{'=' * 40}")

    # only process files with .csv, .xlsx, or .xls extensions
    supported_files = [file for file in files if file.suffix in ['.csv', '.xlsx', '.xls']]
    if not files:
        print(f"No supported files found in {directory}.")
        return
    else:
        print(f"Processing {len(supported_files)} supported files.\n")

    # Read each file and show summary
    for file in supported_files:
        print(f"Processing file: {file.code}")
        if file.suffix == '.csv':
            df = pd.read_csv(file)
            summarize_dataset(df, n_rows)
        elif (file.suffix == '.xlsx') or (file.suffix == '.xls'):
            # load all sheets in file
            engine = 'openpyxl' if file.suffix == '.xlsx' else 'xlrd'
            xls = pd.ExcelFile(file, engine=engine)
            for sheet_name in xls.sheet_names:
                df = pd.read_excel(file, sheet_name=sheet_name)
                summarize_dataset(df, n_rows, sheet_name=sheet_name)
        else:
            continue
        print(f"{'=' * 40}")
        del df

