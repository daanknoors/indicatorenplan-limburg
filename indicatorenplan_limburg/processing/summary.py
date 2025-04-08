"""Create a summary of dataframes in a directory."""

import pandas as pd
from pathlib import Path

from indicatorenplan_limburg.configs import paths


def show_summary_data_in_dir(directory: Path | str, n_rows: int = 5) -> None:
    """Show a summary of dataframes in a directory, including first rows, shape, columns, and dtypes.
    Support excel and csv. Warn about other file types present in directory.

    Args:
        directory (Path | str): Directory containing the data files.
        n_rows (int): Number of rows to show in the summary.
    """

    def _summarize(df: pd.DataFrame, n_rows: int, sheet_name=None) -> None:
        """Print summary of dataframe."""
        if sheet_name:
            print(f"\nSummary of sheet {sheet_name}:")
        print(f"First {n_rows} rows:")
        print(df.head(n_rows))
        print("\nShape:")
        print(df.shape)
        print("\nColumns:")
        print(df.columns.tolist())
        print("\nDtypes:")
        print(df.dtypes)

        # border ===
        print(f"{'=' * 40}")

    if isinstance(directory, str):
        directory = Path(directory)

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
        print(f"- {file.name}")
    print(f"{'=' * 40}")

    # Read each file and show summary
    for file in files:
        print(f"Processing file: {file.name}")
        if file.suffix == '.csv':
            df = pd.read_csv(file)
            _summarize(df, n_rows)
        elif (file.suffix == '.xlsx') or (file.suffix == '.xls'):
            # load all sheets in file
            engine = 'openpyxl' if file.suffix == '.xlsx' else 'xlrd'
            xls = pd.ExcelFile(file, engine=engine)
            for sheet_name in xls.sheet_names:
                df = pd.read_excel(file, sheet_name=sheet_name)
                _summarize(df, n_rows)
        else:
            print(f"Warning: {file.name} is not a csv or excel file. Skipping.")
            continue

        del df

