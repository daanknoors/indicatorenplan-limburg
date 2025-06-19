import logging
import pandas as pd
import inspect
from pathlib import Path

from indicatorenplan_limburg.configs import settings
from indicatorenplan_limburg.system.registry import IndicatorRegistry
from indicatorenplan_limburg.processing.load import load_all_data_in_dir
from indicatorenplan_limburg.system.logger import setup_logger


class BaseIndicator(metaclass=IndicatorRegistry):
    """Base class for all indicators.

    Automatically registers all subclasses in the IndicatorRegistry.
    """

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)

        # assign code and category based on the module path
        file_path = Path(inspect.getfile(cls)).resolve()
        cls.code = file_path.stem.replace('_', '')
        cls.category = file_path.parent.name

    def __init__(self, path_data=None, retain_input=False, retain_output=False, plot_results=False, config: dict | None = None):
        self.retain_input = retain_input
        self.retain_output = retain_output
        self.plot_results = plot_results
        self.path_data = Path(path_data).expanduser() if isinstance(path_data, str) else path_data

        self.config = self._load_config(config=config)

        self.logger = setup_logger(name=self.__class__.__name__)
        self.logger.info(f"Initializing {self.__class__.__name__} with config: {self.config}")

        # computed data attributes
        self.input_data_ = None  # to retain input data if needed
        self.output_data_ = None  # to retain output data if needed

    def _load_config(self, config: dict | None = None):
        """Load the configuration for the indicator."""
        if config is None:
            config = settings.load_yaml_config()
            # if path_data is not set, use the default path from config settings
            if self.path_data is None:
                self.path_data = Path(settings.load_yaml_config()['paths']['data']).expanduser() / self.category / self.code

            # focus config on the specific category and code
            config = config['indicators'][self.category][self.code]

        # check if config has name and metadata
        if 'name' not in config or 'metadata' not in config:
            raise ValueError(f"Config for {self.__class__.__name__} must contain 'name' and 'metadata' fields.")
        return config

    def load_data(self, usecols: list[str] | None = None, sheet_name: str | int | None = 0, **kwargs) -> pd.DataFrame | dict:
        path_input = self.path_data / 'input'
        self.logger.info(f"Loading data from {path_input}")
        data = load_all_data_in_dir(path_dir=path_input, file_extensions=['.xlsx', '.csv'], sheet_name=sheet_name, usecols=usecols, **kwargs)
        return data

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

        if isinstance(save_path, str):
            save_path = Path(save_path)

        # create missing directories and ensure the path exists
        path_file = (save_path / f"{self.config['name']}.xlsx").expanduser()
        path_file.parent.mkdir(parents=True, exist_ok=True)

        # save processing to excel with multiple sheets
        with pd.ExcelWriter(path_file, engine='openpyxl') as writer:
            df_output.to_excel(writer, sheet_name='data', index=False)
            for sheet_name, df_meta in metadata_dict.items():
                df_meta.to_excel(writer, sheet_name=sheet_name, index=False)

        self.logger.info(f"Saved results to {path_file}")

    def plot(self, output):
        """Optional: plot results if implemented and plot_results is True."""
        self.logger.info("Plotting not implemented for this metric.")

    def run(self):
        try:
            data = self.load_data()
            if self.retain_input:
                self.input_data_ = data
            output = self.compute(data=data)
            if self.retain_output:
                self.output_data_ = output
            md = self.get_metadata()
            self.save_results(output, metadata_dict=md)
            self.logger.info(f"Finished processing {self.__class__.__name__} - output saved to {self.path_data / 'output'}")
            if self.plot_results:
                self.plot(output)
        except Exception as e:
            self.logger.error(f"{self.__class__.__name__} failed: {e}", exc_info=True)