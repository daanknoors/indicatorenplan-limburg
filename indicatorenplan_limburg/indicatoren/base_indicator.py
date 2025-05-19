import logging
import pandas as pd
from pathlib import Path

from indicatorenplan_limburg.configs import settings
from indicatorenplan_limburg.system.registry import IndicatorRegistry
from indicatorenplan_limburg.processing.load import load_all_data_in_dir


def get_logger(name):
    """Get a logger with the specified name."""
    logger = logging.getLogger(name)
    if not logger.handlers:
        handler = logging.StreamHandler()
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        logger.setLevel(logging.INFO)
    return logger


class BaseIndicator(metaclass=IndicatorRegistry):
    """Base class for all indicators.

    Automatically registers all subclasses in the IndicatorRegistry.
    """

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)

        # assign code based on class name and category based on folder name
        cls.code = cls.__class__.__name__.replace('Indicator', '')
        cls.category = cls.__module__.split('.')[-2]

    def __init__(self, config=None, retain_data=False, plot_results=False):
        self.retain_data = retain_data
        self.plot_results = plot_results

        self.config = config or settings.load_yaml_config()
        self.path_data = Path(self.config['paths']['data']) / self.category / self.code
        self.logger = get_logger(self.code)



    def load_data(self, usecols: list[str] | None = None) -> pd.DataFrame | list | dict:
        return load_all_data_in_dir(path_dir=self.path_data / 'input', file_extensions=['.xlsx', '.csv'], usecols=usecols)

    def compute(self, data: pd.DataFrame | list | dict):
        raise NotImplementedError

    def get_metadata(self):
        raise NotImplementedError

    def save_results(self, df_output, metadata_dict=None, save_path=None):
        """Save the processing to a csv file

        Args:
            df_output (pd.DataFrame): dataframe to save
            metadata_dict (dict): metadata dictionary
            save_path (Path, optional): path to save the output data. If None, the default path is used.
        """
        if save_path is None:
            save_path = self.path_data / 'output'
        path_file = save_path / f"{self.config['name']}.xlsx"

        # save processing to excel with multiple sheets
        with pd.ExcelWriter(path_file, engine='openpyxl') as writer:
            # expand all cells

            df_output.to_excel(writer, sheet_name='data', index=False)
            for sheet_name, df_meta in metadata_dict.items():
                df_meta.to_excel(writer, sheet_name=sheet_name, index=False)

        print(f"Data saved to {path_file}")

    def plot(self):
        """Optional: plot results if implemented and plot_results is True."""
        # warn if not implemented
        self.logger.warning("Plotting not implemented for this metric.")

    def run(self):
        try:
            data = self.load_data()
            output = self.compute(data=data)
            md = self.get_metadata()
            self.save_results(output)
            if self.plot_results:
                self.plot()
        except Exception as e:
            self.logger.error(f"{self.__class__.__name__} failed: {e}")