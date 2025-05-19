"""
Indicatorenplan Limburg - Indicator D.21a

Aantal MKB bedrijven in Limburg met proces- en productinnovaties
"""
import pandas as pd
import numpy as np

from indicatorenplan_limburg.indicatoren.base_indicator import BaseIndicator
from indicatorenplan_limburg.metadata import metadata


class IndicatorD21a(BaseIndicator):
    """Class for the D_21a indicator"""


    def compute(self, data):
        """Compute the indicator"""
        if data is None:
           data = self.load_data()

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