# File: tests/test_summary.py

import pytest
from pathlib import Path
import pandas as pd
from indicatorenplan_limburg.processing.summary import show_summary_data_in_dir


def test_directory_with_csv_and_excel_files(tmp_path='~/tmp'):
    # initialize the directory with a csv and an excel file
    tmp_path = Path(tmp_path).expanduser()
    tmp_path.mkdir(parents=True, exist_ok=True)

    # create a csv
    csv_file = tmp_path / "data.csv"
    csv_file.write_text("col1,col2\n1,2\n3,4")

    # create excel with multiple sheets
    excel_file = tmp_path / "data.xlsx"

    df1 = pd.DataFrame({"col1": [1, 2], "col2": [3, 4]})
    df2 = pd.DataFrame({"col3": [5, 6], "col4": [7, 8]})
    with pd.ExcelWriter(excel_file, engine='openpyxl') as writer:
        df1.to_excel(writer, sheet_name='Sheet1', index=False)
        df2.to_excel(writer, sheet_name='Sheet2', index=False)

    # create an unsupported file
    unsupported_file = tmp_path / "unsupported.txt"
    unsupported_file.write_text("Unsupported content")

    # Call the function to show summary
    show_summary_data_in_dir(tmp_path)

