"""
Indicatorenplan Limburg - Indicator D.23a

Aantal startende innovatieve bedrijven vanuit: (i) Brightlands ecosystemen en (ii) acquisitie van de Provincie
"""

from indicatorenplan_limburg.indicatoren.base_indicator import BaseIndicator
from indicatorenplan_limburg.metadata import metadata


class IndicatorD23a(BaseIndicator):
    """Class for the D_23a indicator"""

    def compute(self, data=None):
        """Compute the indicator"""
        if data is None:
            data = self.load_data()

        df = data.copy()

        # select rows and columns
        df = df.iloc[1:13]
        df.columns = ['jaar', 'totaal_campus', 'totaal_limburg']
        return df

    def get_metadata(self):
        """Get metadata for the indicator"""
        # todo: add other metadata
        md = {
            'onderwerpen': metadata.metadata_onderwerpen(
                indicator_code=self.code,
                indicator_name=self.config['name'],
            )
        }
        return md

