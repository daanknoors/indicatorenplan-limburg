from pathlib import Path
from indicatorenplan_limburg.configs.settings import load_yaml_config
from indicatorenplan_limburg.system.registry import IndicatorRegistry
from indicatorenplan_limburg.system.logger import setup_logger


class IndicatorRunner:
    """Main class to run and instantiate the indicators based on the config file with
    indicator-specific settings."""

    def __init__(self, config: dict | None = None):
        """Initialize the runner with the config file."""
        self.logger = setup_logger(name=self.__class__.__name__,)
        self.logger.info("Initializing IndicatorRunner with config.")

        # automatically populate registry
        IndicatorRegistry.discover_indicators()

        # Load the config file
        self.config = config or load_yaml_config(config)


        # filter for included metrics based on category name
        self.included_indicators = {
            name: cls for name, cls in IndicatorRegistry.get_registry().items()
            if (cls.category in self.config['runner']['include_categories']) and (
                        name not in self.config['runner']['exclude_indicators'])
        }
        self.logger.info(f"Included indicators: {list(self.included_indicators.keys())}")

        self.indicators = self._init_indicators()

    def _init_indicators(self):
        # instantiate all included indicators with their specific config
        path_data = Path(self.config['paths']['data'])
        indicators = {
            name: cls(config=self.config['indicators'][cls.category][cls.code],
                      path_data=path_data / cls.category / cls.code)
            for name, cls in self.included_indicators.items()
        }
        return indicators

    def run(self):
        """Run all indicators."""
        self.logger.info("Running all indicators...")

        for name, indicator in self.indicators.items():
            self.logger.info(f"Running indicator: {name}")
            indicator.run()
