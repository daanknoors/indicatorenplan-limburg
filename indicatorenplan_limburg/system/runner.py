from indicatorenplan_limburg.configs.settings import load_yaml_config
from indicatorenplan_limburg.system.registry import IndicatorRegistry


class IndicatorRunner:
    """Main class to run and instantiate the indicators based on the config file with
    indicator-specific settings."""

    def __init__(self, config: str | None = None):
        """Initialize the runner with the config file."""


        # Load the config file
        self.config = config or load_yaml_config(config)
        self.included_categories = self.config['runner']['compute']

        # automatically populate registry
        IndicatorRegistry.discover_indicators(categories=self.included_categories)

        # filter for included metrics based on category name
        self.included_indicators = {
            name: cls for name, cls in IndicatorRegistry.get_registry().items()
            if cls.category in self.included_categories
        }

        # instantiate all included indicators
        self.indicators = {
            name: cls(config=config)
            for name, cls in self.included_indicators.items()
        }

    def run(self):
        """Run all indicators."""
        for name, indicator in self.indicators.items():
            indicator.run()


