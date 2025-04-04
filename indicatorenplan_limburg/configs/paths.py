from pathlib import Path

# Data paths
PATH_DATA_DIR = Path('~/data')

PATH_DATA_SETS = {
    'vrl': PATH_DATA_DIR / 'vrl',
}


def get_path_data(name: str, state: str = 'raw') -> Path:
    """Get the path to a specific data set.
    
    Args:
        name (str): The name of the data set.
        state (str): The state of the data set. Default is 'raw'.
    """
    if name not in PATH_DATA_SETS:
        raise ValueError(f"Data set '{name}' not found.\nAvailable: {list(PATH_DATA_SETS.keys())}")
    return PATH_DATA_SETS[name] / state