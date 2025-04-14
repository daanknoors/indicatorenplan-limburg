import logging

import pandas as pd


def get_logger(name):
    pass

class BaseIndicator:
    def __init__(self, config, retain_data=False, plot_results=False):

        self.config = config
        self.retain_data = retain_data
        self.plot_results = plot_results
        # self.logger = get_logger(self.__class__.__name__)

    def load_data(self) -> pd.DataFrame | list | dict:
        raise NotImplementedError

    def compute(self, data: pd.DataFrame | list | dict):
        raise NotImplementedError

    def get_metadata(self):
        raise NotImplementedError

    def save_results(self):
        raise NotImplementedError

    def plot(self):
        """Optional: plot results if implemented and plot_results is True."""
        # warn if not implemented
        self.logger.warning("Plotting not implemented for this metric.")

    def run(self):
        try:
            data = self.load_data()
            self.compute(data=data)
            self.get_metadata()
            self.save_results()
            if self.plot_results:
                self.plot()
        except Exception as e:
            self.logger.error(f"Metric {self.__class__.__name__} failed: {e}")