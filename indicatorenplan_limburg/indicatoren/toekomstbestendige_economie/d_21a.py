"""
Indicatorenplan Limburg - Indicator D.21a

Aantal MKB bedrijven in Limburg met proces- en productinnovaties
"""

import pandas as pd
import numpy as np

from indicatorenplan_limburg.configs.paths import get_path_data
from indicatorenplan_limburg.indicatoren.base_indicator import BaseIndicator
from indicatorenplan_limburg.indicatoren.registry import register_indicator

class IndicatorD21a(BaseIndicator):
    """Class for the D.21a indicator"""

    def load_data(self):
        """Load the data for the indicator"""
        # Load the data from the VRL
        df = pd.read_excel(get_path_data(name='vrl', subfolder='raw') / "vrl2023.xlsx")
        return df

    def compute(self, data):
        """Compute the indicator"""
        pass