"""
Indicatorenplan Limburg

Indicator D.21a - Aantal MKB bedrijven in Limburg met proces- en productinnovaties
"""
import matplotlib.pyplot as plt
import seaborn as sns

from indicatorenplan_limburg.indicatoren.base_indicator import BaseIndicator
from indicatorenplan_limburg.metadata import metadata
from indicatorenplan_limburg.configs.style import COLOR_PALETTE_LIST


class IndicatorD21a(BaseIndicator):

    """Class for the D_21a indicator"""

    def compute(self, data=None):
        """Compute the indicator"""
        if data is None:
            data = self.load_data()
        df = data.copy()

        # select rows
        categories = {
            '3.1.1 SMEs introducing product innovations (Regional)': 'product innovatie',
            '3.1.2 SMEs introducing business process innovations (Regional)': 'proces innovatie'
        }
        df = df[df['Indicator'].isin(categories.keys())]
        df = df[df['RegionName'] == 'Limburg']

        # rename values
        df['Indicator'] = df['Indicator'].replace(categories)

        # select and rename columns
        columns = {'Year': 'jaar',
                   'Indicator': 'type',
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

    def plot(self, output):
        """Plot the indicator results"""
        sns.set_style("whitegrid")

        fig, ax = plt.subplots(figsize=(7, 5))
        sns.lineplot(x='jaar', y='index', hue='type', data=output, palette=COLOR_PALETTE_LIST[:2])
        ax.set_ylim(0, 200)
        ax.set_title(self.config['name'])
        fig.savefig(self.path_data / 'output' / f"{self.code}_plot.png", bbox_inches='tight')
        plt.close(fig)


if __name__ == "__main__":
    # Example usage
    indicator = IndicatorD21a()
    data = indicator.load_data()  # Load data
    output = indicator.compute(data)  # Compute the indicator
    metadata = indicator.get_metadata()  # Get metadata
    print(output.head())  # Display the computed output
    indicator.plot(output)  # Plot the results
    print(metadata)  # Display metadata