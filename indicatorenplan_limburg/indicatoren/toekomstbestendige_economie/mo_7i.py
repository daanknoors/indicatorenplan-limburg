"""Indicatorenplan Limburg - MO-7i

Vestigingen per grootteklasse per sector
"""
import numpy as np
import pandas as pd
from pathlib import Path

from collections.abc import Sequence

from indicatorenplan_limburg.indicatoren.base_indicator import BaseIndicator
from indicatorenplan_limburg.indicatoren.registry import register_indicator
from indicatorenplan_limburg.configs.paths import get_path_data
from indicatorenplan_limburg.processing.load import load_all_data_in_dir
from indicatorenplan_limburg.metadata import metadata


# Constants
RANGES_GROOTTEKLASSE = ('0_9', '10_49', '50_99', '100_249', '250_9999')
OUTPUT_FILENAME = "MO_7i Vestigingen per grootteklasse per sector.xlsx"



@register_indicator
class IndicatorMO7i(BaseIndicator):
    """Class for the MO-7i indicator"""


    def compute(self, data: dict[str, pd.DataFrame]) -> pd.DataFrame:
        """Compute the indicator"""
        if data is None:
           self.load_data(usecols=["PEILDATUM", "COROP_NAAM", "SBI_1_NAAM", "WP_FPU_TOTAAL"])

        output = []
        for name, df in data.items():
            df = df.copy()

            # Transform the data
            year = pd.to_datetime(df['PEILDATUM']).dt.year

            # add grootteklassen and convert to category for easier ordering
            df['dim_grootte_1'] = categorize_company_size(employee_counts=df['WP_FPU_TOTAAL'], ranges=RANGES_GROOTTEKLASSE)

            # transform names SBI
            df['dim_sbi_1'] = df['SBI_1_NAAM'].replace(metadata.SBI_DICT)

            # count group by sbi naam and grootteklassen
            df_grouped = df.groupby(by=['dim_sbi_1', 'dim_grootte_1'], observed=False).size().reset_index(name='mo-7i')

            # add remaining columns
            df_grouped['period'] = year
            df_grouped['geolevel'] = 'prov_code'
            df_grouped['geoitem'] = 'pv31'

            # subset and order columns
            df_grouped = df_grouped[['period', 'geolevel', 'geoitem', 'dim_sbi_1', 'dim_grootte_1', 'mo-7i']]

            # add to output list
            output.append(df_grouped)

        # Merge the output for multiple years
        df_output = pd.concat(output, ignore_index=True)

        # sort the output
        df_output = df_output.sort_values(by=['period', 'dim_sbi_1', 'dim_grootte_1'])

        return df_output

    def get_metadata(self) -> dict:
        """Get the metadata for the indicator"""
        metadata_dict = {
            'onderwerpen': metadata.metadata_onderwerpen(indicator_code='mo_7i', indicator_name='MO_7i Vestigingen per grootteklasse per sector', start_period=2023, end_period=2024)
            'dim_sbi': metadata.metadata_dim_sbi(dimension_dict=metadata.SBI_DICT),
            'dim_grootteklasse': metadata.metadata_dim_grootteklasse(RANGES_GROOTTEKLASSE),
            'dim_geoitem': metadata.metadata_geo_item()
        }
        return metadata_dict


def categorize_company_size(employee_counts: pd.Series, ranges: tuple):
    """Categorize the company size based on the number of employees (i.e. grootteklassen).

    Args:
        employee_counts (pd.Series): The number of employees.
        ranges (tuple): The range boundaries for categorization.
    Returns:
        pd.Series: The size class.
    """

    def _parse_ranges(_str_ranges: tuple) -> tuple:
        """
        Parse the ranges into a list of tuples.

        Args:
            _str_ranges (tuple): The range boundaries for categorization as strings

        Returns:
            tuple: The parsed ranges as integers.
        """
        _parsed_ranges = []
        for r in _str_ranges:
            # split the range into lower and upper bounds
            lb, ub = r.split('_')
            # convert to integers
            lb = int(lb)
            ub = int(ub)
            # add the range to the list
            _parsed_ranges.append((lb, ub))
        return tuple(_parsed_ranges)

    def _categorize_company_size(employee_count: int, _str_ranges: tuple , _parsed_ranges: tuple) -> str | float:
        """
        Categorize one row with company size based on the number of employees (i.e. grootteklassen).

        Args:
            employee_count (int): The number of employees.
            _str_ranges (tuple): The range boundaries for categorization as strings
            _parsed_ranges (tuple): The parsed ranges as integers.

        Returns:
            str: The size class.
        """
        for i, (lb, ub) in enumerate(_parsed_ranges):
            if lb <= employee_count <= ub:
                return _str_ranges[i]
        return np.nan

    # parse the ranges from string to integer bounds
    parsed_ranges = _parse_ranges(ranges)

    # categorize the company size
    employee_counts.copy()
    company_sizes = employee_counts.apply(_categorize_company_size, _str_ranges=ranges, _parsed_ranges=parsed_ranges)

    # check if there are any nan categories
    assert company_sizes.notna().all(), (f"Some company sizes could not be categorized as they fall outside of the defined ranges"
                                         f": rows {company_sizes[company_sizes.isna()].index.tolist()} with values {employee_counts[company_sizes.isna()].tolist()}")

    # convert to categorical for easier ordering
    company_sizes = pd.Categorical(company_sizes, categories=ranges, ordered=True)
    return company_sizes




def save_data(df_data: pd.DataFrame, metadata_dict: dict, save_path=None) -> None:


def main(years: Sequence[int] = (2023, 2024), n_rows: int | None = None, save_path: str | Path | None = None) -> None:
    """Main function to load, transform and save the processing
    Args:
        years (Sequence[int], optional): years to load. Defaults to (2023, 2024).
        n_rows (int | None, optional): number of rows to load. Mainly for testing. Defaults to None.
        save_path (str | Path | None, optional): path to save the processing. Defaults to None.

    Returns:
        None
    """
    # Load the processing
    list_df = []
    for year in years:
        # load only these columns
        subset_cols = ["PEILDATUM", "COROP_NAAM", "SBI_1_NAAM", "WP_FPU_TOTAAL"]
        df = load_data_vrl(year=year, usecols=subset_cols, n_rows=n_rows)
        df = transform_data_vrl(df)
        list_df.append(df)

    # Merge the processing for multiple years
    df_data = pd.concat(list_df, ignore_index=True)

    # sort the processing
    df_data = df_data.sort_values(by=['period', 'dim_sbi_1', 'dim_grootte_1'])

    # get metadata
    metadata_dict = get_metadata()

    # save the processing
    save_data(df_data, metadata_dict, save_path=save_path)


if __name__ == "__main__":
    main()
