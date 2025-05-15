"""
Indicatorenplan Limburg - Indicator D.21a

Aantal MKB bedrijven in Limburg met proces- en productinnovaties
"""
import pandas as pd
import numpy as np

from indicatorenplan_limburg.configs.paths import get_path_data
from indicatorenplan_limburg.indicatoren.base_indicator import BaseIndicator
from indicatorenplan_limburg.indicatoren.registry import register_indicator
from indicatorenplan_limburg.metadata import metadata

class IndicatorD21a(BaseIndicator):
    """Class for the D_21a indicator"""

    def load_data(self):
        """Load the data for the indicator"""
        # Load the data
        df = pd.read_excel(get_path_data(name='toekomstbestendige_economie', subfolder='raw') / "Vestigingen van nieuw opgerichte bedrijven.xlsx")
        return df

    def compute(self, data):
        """Compute the indicator"""
        df = data.copy()
        print("Data loaded successfully")

        # select rows and columns
        df = df.iloc[1:13]
        df.columns = ['jaar' , 'totaal_campus', 'totaal_limburg']
        return df

    def get_metadata(self):
        """Get metadata for the indicator"""
        # todo: add other metadata
        md = {
            'onderwerpen': metadata.metadata_onderwerpen(
                indicator_code='D_21a',
                indicator_name='Aantal MKB bedrijven in Limburg met proces- en productinnovaties',
            )
        }
        return md



if __name__ == "__main__":
    # Example usage
    indicator = IndicatorD21a()
    indicator.run()