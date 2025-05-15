import pytest

from indicatorenplan_limburg.configs import paths, settings

def test_get_indicator_config():
    """Test the loading of indicator config."""
    config = settings.load_yaml_config()

    # Test with a valid indicator name
    indicator_name = 'MO_7i'
    indicator_config = settings.get_indicator_config(config, indicator_name)

    assert 'name' in indicator_config, f"Indicator config for {indicator_name} does not contain 'onderwerpen'."