import pandas as pd

from collections.abc import Sequence

from indicatorenplan_limburg.configs.paths import get_path_data
from indicatorenplan_limburg.data.load import load_data_vrl

# Constants
BOUNDS_GROOTTEKLASSE = [0, 10, 50, 100, 250, 10000]

# Mapping of SBI names to shorter name categories, easier to display
SBI_DICT = {
    'Bouwnijverheid': 'bouw',
    'Cultuur, sport en recreatie': 'csr',
    'Detailhandel': 'detailhandel',
    'Financiële instellingen': 'financien',
    'Gezondheids- en welzijnszorg': 'gezondheid',
    'Groot- en detailhandel; reparatie van auto’s': 'groothandel',
    'Horeca': 'horeca',
    'Industrie': 'industrie',
    'Informatie en communicatie': 'ict',
    'Landbouw, bosbouw en visserij': 'landbouw',
    'Onderwijs': 'onderwijs',
    'Overheid': 'overheid',
    'Openbaar bestuur, overheidsdiensten, sociale verzekeringen': 'overig',
    'Overige dienstverlening': 'overig',
    'Vervoer en opslag': 'vervoer',
    'Zakelijke diensten': 'zakelijk',
    'Advisering, onderzoek, special. zakelijke dienstverlening': 'onderzoek',
    'Logies-, maaltijd- en drankverstrekking': 'logies',
    'Winning/distributie van water; afval(water)beheer,sanering': 'afval',
    'Autoreparatie': 'autoreparatie',
    'Winning van delfstoffen': 'delfstoffen',
    'Extraterritoriale organisaties en lichamen': 'extraterritoraal',
    'Huishoudens als werkgever': 'huishouden',
    'Verhuur van en handel in onroerend goed': 'onroerend',
    'Productie, distributie, handel in elektriciteit en aardgas': 'productie',
    'Verhuur van roerende goederen, overige zakel. dienstverl.': 'roerend'
}


def categorize_company_size(company_sizes: pd.Series, bounds: list, fill_na: str | None ='outside_bounds'):
    """Categorize the company size based on the number of employees (i.e. grotteklassen).

    Args:
        company_sizes (pd.Series): The number of employees.
        bounds (list): The range boundaries for categorization.
        fill_na (str | None): The value to return if the employee count is outside the bounds.
            If None, the value will be NaN.
    Returns:
        pd.Series: The size class.
    """

    def _get_company_size_ranges(_bounds, _fill_na='outside_bounds') -> list:
        """Get the company size ranges for categorization.

        Example:
            bounds = [0, 10, 50, 100, 250, 10000]
            categories = ['0 - 9', '10 - 49', '50 - 99', '100 - 249', '250 - 9999']

        Args:
            _bounds (list): The range boundaries for categorization.
            _fill_na (str): The value to return if the employee count is outside the bounds.

        Returns:
            list: The range boundaries for categorization.
        """
        ranges = [f"{_bounds[i]} - {_bounds[i + 1] - 1}" for i in range(len(_bounds) - 1)]
        if _fill_na:
            ranges.append(_fill_na)
        return ranges

    def _categorize_company_size(employee_count, _bounds, _fill_na='outside_bounds'):
        """
        Categorize one row with company size based on the number of employees (i.e. grotteklassen).

        Args:
            employee_count (int): The number of employees.
            _bounds (list): The range boundaries for categorization.
            _fill_na (str): The value to return if the employee count is outside the bounds.
        Returns:
            str: The size class.
        """
        ranges = _get_company_size_ranges(_bounds)
        for i in range(len(_bounds) - 1):
            if _bounds[i] <= employee_count < _bounds[i + 1]:
                return ranges[i]
        return _fill_na

    # categorize the company size
    company_sizes = company_sizes.apply(_categorize_company_size, _bounds=bounds, _fill_na=fill_na)

    # convert to categorical for easier ordering
    ordered_ranges = _get_company_size_ranges(_bounds=bounds, _fill_na=fill_na)
    company_sizes = pd.Categorical(company_sizes, categories=ordered_ranges, ordered=True)
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
    df['dim_grootte'] = categorize_company_size(df['WP_FPU_TOTAAL'], bounds=BOUNDS_GROOTTEKLASSE, fill_na=None)
    
    # transform names SBI
    df['dim_sbi'] = df['SBI_1_NAAM'].replace(SBI_DICT)

    # count group by sbi naam and grootteklassen
    df_grouped = df.groupby(['dim_sbi', 'dim_grootte']).size().reset_index(name='mo-7i')

    # add year column
    df_grouped['period'] = year

    # subset and order columns
    df_grouped = df_grouped[['period', 'dim_sbi', 'dim_grootte', 'mo-7i']]
    return df_grouped


def save_data(df: pd.DataFrame, path_data=None) -> None:
    """Save the data to a csv file

    Args:
        df (pd.DataFrame): dataframe to save
        path_data (Path, optional): path to save the data. Defaults to None.
    """
    if not path_data:
        path_data = get_path_data(name='vrl', state='processed')
    path_file = path_data / "MO-7i.xlsx"
    df.to_excel(path_file, index=False)
    print(f"Data saved to {path_file}")


def main(years: Sequence[int] = (2023, 2024)) -> None:
    """Main function to load, transform and save the data"""
    # Load the data
    list_df = []
    for year in years:
        # load only these columns
        subset_cols = ["PEILDATUM", "COROP_NAAM", "SBI_1_NAAM", "WP_FPU_TOTAAL"]
        df = load_data_vrl(year=year, usecols=subset_cols)
        df = transform_data_vrl(df)
        list_df.append(df)

    # Merge the data for multiple years
    df = concat_data(list_df)

    # sort the data
    df = df.sort_values(by=['period', 'dim_sbi', 'dim_grootte'])

    # Save the data
    save_data(df)


if __name__ == "__main__":
    main()