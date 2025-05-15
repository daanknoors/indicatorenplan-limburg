"""Get indicator settings from the config file."""
from pathlib import Path
import yaml

from indicatorenplan_limburg.configs.paths import PATH_REPO_DIR


def load_yaml_config(file_path: Path | None =None) -> dict:
    """Load a YAML config file."""
    # Define the path to the config file
    if file_path is None:
        file_path = PATH_REPO_DIR / 'configs' / 'indicators.yaml'

    # load config
    with open(file_path, 'r', encoding='utf-8') as file:
        config = yaml.safe_load(file)

    return config

def get_indicator_config(config: dict, indicator_name: str) -> dict:
    """Get the config for a specific indicator."""
    # Check if the indicator exists in the config
    config_indicators = config['indicators']

    if indicator_name not in config_indicators:
        raise ValueError(f"Indicator '{indicator_name}' not found in config file.")

    return config_indicators[indicator_name]
