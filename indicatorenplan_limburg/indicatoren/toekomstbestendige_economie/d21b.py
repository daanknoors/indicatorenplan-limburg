"""Indicatorenplan Limburg

Aantal MKB bedrijven in innovatieve samenwerkingsverbanden
"""

from indicatorenplan_limburg.indicatoren.base_indicator import BaseIndicator
from indicatorenplan_limburg.metadata import metadata


class IndicatorD21b(BaseIndicator):
    """Indicator D.21b - Aantal MKB bedrijven in innovatieve samenwerkingsverbanden"""

    def compute(self, data=None):
        """Compute the indicator"""
        if data is None:
            data = self.load_data()

        df = data.copy()

        # select rows
        df = df[df['RegionName'] == 'Limburg']
        df = df[df['Indicator'] == "3.2.1 Innovative SMEs collaborating with others (Regional)"]

        # select and rename columns
        columns = {'Year': 'jaar',
                   'Value': 'index'}
        df = df[list(columns.keys())].rename(columns=columns)
        return df

    def get_metadata(self):
        """Get metadata for the indicator"""
        md = {
            'onderwerpen': metadata.metadata_onderwerpen(
                indicator_code=self.code,
                indicator_name=self.config['name'],
            )
        }
        return md
