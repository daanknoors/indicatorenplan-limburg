"""Indicatorenplan Limburg - MO-7i

Vestigingen per grootteklasse per sector
"""
import numpy as np
import pandas as pd
from pathlib import Path

from collections.abc import Sequence

from indicatorenplan_limburg.configs.paths import get_path_data
from indicatorenplan_limburg.data.load import load_data_vrl

# Constants
RANGES_GROOTTEKLASSE = ('0_9', '10_49', '50_99', '100_249', '250_9999')
OUTPUT_FILENAME = "MO_7i Vestigingen per grootteklasse per sector.xlsx"

# Mapping of SBI names to shorter name categories, easier to display
SBI_DICT = {
    'Industrie': 'industrie',
    'Bouwnijverheid': 'bouwnijverheid',
    'Advisering, onderzoek, special. zakelijke dienstverlening': 'onderzoek',
    'Openbaar bestuur, overheidsdiensten, sociale verzekeringen': 'overheid',
    'Logies-, maaltijd- en drankverstrekking': 'logies',
    'Onderwijs': 'onderwijs',
    'Gezondheids- en welzijnszorg': 'gezondheid',
    'Landbouw, bosbouw en visserij': 'landbouw',
    'Overige dienstverlening': 'overig',
    'Informatie en communicatie': 'ict',
    'Cultuur, sport en recreatie': 'csr',
    'Extraterritoriale organisaties en lichamen': 'extraterritoraal',
    'Financiële instellingen': 'financien',
    'Groot- en detailhandel; reparatie van auto’s': 'autoreparatie',
    'Huishoudens als werkgever': 'huishouden',
    'Productie, distributie, handel in elektriciteit en aardgas': 'productie',
    'Verhuur van en handel in onroerend goed': 'onroerend',
    'Verhuur van roerende goederen, overige zakel. dienstverl.': 'roerend',
    'Vervoer en opslag': 'vervoer',
    'Winning van delfstoffen': 'delfstoffen',
    'Winning/distributie van water; afval(water)beheer,sanering': 'afval'
}


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



def concat_data(list_df: Sequence[pd.DataFrame]) -> pd.DataFrame:
    """Concatenate the data from different years"""
    df = pd.concat(list_df, ignore_index=True)
    return df


def transform_data_vrl(df: pd.DataFrame) -> pd.DataFrame:
    """Transform the data to the desired format

    Args:
        df (pd.DataFrame): dataframe to transform

    Returns:
        pd.DataFrame: transformed dataframe
    """
    # retrieve the year from the PEILDATUM column
    year = pd.to_datetime(df['PEILDATUM']).dt.year

    # add grootteklassen and convert to category for easier ordering
    df['dim_grootte_1'] = categorize_company_size(employee_counts=df['WP_FPU_TOTAAL'], ranges=RANGES_GROOTTEKLASSE)
    
    # transform names SBI
    df['dim_sbi_1'] = df['SBI_1_NAAM'].replace(SBI_DICT)

    # count group by sbi naam and grootteklassen
    df_grouped = df.groupby(by=['dim_sbi_1', 'dim_grootte_1'], observed=False).size().reset_index(name='mo-7i')

    # add remaining columns
    df_grouped['period'] = year
    df_grouped['geolevel'] = 'prov_code'
    df_grouped['geoitem'] = 'pv31'

    # subset and order columns
    df_grouped = df_grouped[['period', 'geolevel', 'geoitem', 'dim_sbi_1', 'dim_grootte_1', 'mo-7i']]
    return df_grouped


def get_metadata() -> dict:
    """Get the metadata for the indicator"""
    def _onderwerpen_metadata():
        """Get the 'onderwerpen' metadata for the indicator"""
        df_onderwerpen = pd.DataFrame({
            'Indicator code': ['mo_7i'],
            'Name': ['MO_7i Vestigingen per grootteklasse per sector'],
            'Data type': ['Numeric'],
            'Keywords': ['Indicatorenplan'],
            'Period type': ['Year'],
            'Formula': [np.nan],
            'Aggregation indicator': [np.nan],
            'Unit': ['aantal'],
            'Source': ['ETIL'],
            'Start period': [2023],
            'End period': [2024],
            'RoundOff': [1],
            'Description': [
                'Deze indicator maakt onderdeel uit van het Indicatorenplan Statenperiode 2023-2027 en is bedoeld om de maatschappelijke opgaven, doelstellingen of resultaten uit de beleidskaders te monitoren. Vestigingen per grootteklasse per sector.'],
            'More information': [np.nan]
        })
        return df_onderwerpen

    def _dim_sbi_metadata():
        """Get the 'sbi_dim' metadata for the indicator"""
        df_dim_sbi = pd.DataFrame({
            'itemcode': SBI_DICT.values(),
            'Name': SBI_DICT.keys()
        })
        return df_dim_sbi

    def _dim_grootteklasse_metadata():
        """Get the 'grootteklasse_dim' metadata for the indicator"""
        df_grooteklasse = pd.DataFrame({
            'itemcode': RANGES_GROOTTEKLASSE,
            'Name': [x.replace('_', '-') for x in RANGES_GROOTTEKLASSE]
        })
        return df_grooteklasse

    def _dim_geoitem_metadata():
        """Get the 'geoitem' metadata for the indicator"""
        df_dim_geoitem = pd.DataFrame({
            'itemcode': ['pv31'],
            'Name': ['Provincie Limburg']
        })
        return df_dim_geoitem

    metadata_dict = {
        'onderwerpen': _onderwerpen_metadata(),
        'dim_sbi': _dim_sbi_metadata(),
        'dim_grootteklasse': _dim_grootteklasse_metadata(),
        'dim_geoitem': _dim_geoitem_metadata()
    }
    return metadata_dict


def save_data(df_data: pd.DataFrame, metadata_dict: dict, save_path=None) -> None:
    """Save the data to a csv file

    Args:
        df_data (pd.DataFrame): dataframe to save
        metadata_dict (dict): metadata dictionary
        save_path (Path, optional): path to save the data. Defaults to None.
    """
    if not save_path:
        save_path = get_path_data(name='vrl', state='processed')
    path_file = save_path / OUTPUT_FILENAME

    # save data to excel with multiple sheets
    with pd.ExcelWriter(path_file, engine='openpyxl') as writer:
        # expand all cells

        df_data.to_excel(writer, sheet_name='data', index=False)
        for sheet_name, df_meta in metadata_dict.items():
            df_meta.to_excel(writer, sheet_name=sheet_name, index=False)

    print(f"Data saved to {path_file}")


def main(years: Sequence[int] = (2023, 2024), n_rows: int | None = None, save_path: str | Path | None = None) -> None:
    """Main function to load, transform and save the data
    Args:
        years (Sequence[int], optional): years to load. Defaults to (2023, 2024).
        n_rows (int | None, optional): number of rows to load. Mainly for testing. Defaults to None.
        save_path (str | Path | None, optional): path to save the data. Defaults to None.

    Returns:
        None
    """
    # Load the data
    list_df = []
    for year in years:
        # load only these columns
        subset_cols = ["PEILDATUM", "COROP_NAAM", "SBI_1_NAAM", "WP_FPU_TOTAAL"]
        df = load_data_vrl(year=year, usecols=subset_cols, n_rows=n_rows)
        df = transform_data_vrl(df)
        list_df.append(df)

    # Merge the data for multiple years
    df_data = concat_data(list_df)

    # sort the data
    df_data = df_data.sort_values(by=['period', 'dim_sbi_1', 'dim_grootte_1'])

    # get metadata
    metadata_dict = get_metadata()

    # save the data
    save_data(df_data, metadata_dict, save_path=save_path)


if __name__ == "__main__":
    main()
