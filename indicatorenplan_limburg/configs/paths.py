from pathlib import Path

# Data path
PATH_REPO_DIR = Path(__file__).resolve().parent.parent
PATH_DATA_DIR = Path('~/data/Indicatorenplan').expanduser()


def get_path_data(name: str, subfolder: str | None = None) -> Path:
    """Get the path to a specific processing set.
    
    Args:
        name (str): The name of the processing set.
        subfolder (str): The subfolder of the processing set. Default is None.
    """
    path_data = PATH_DATA_DIR / name
    if not subfolder:
        return path_data

    return path_data / subfolder