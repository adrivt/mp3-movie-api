# data_loaders.py
from pathlib import Path

import logging
import pandas as pd
import json
import yaml


# Do not call logging.basicConfig() here.
# Use the logging configuration from Part 1.
logger = logging.getLogger(__name__)


def load_csv(filepath):
    """Load a CSV file into a DataFrame.
    filepath is a Path object.
    """
    df = pd.read_csv(filepath)
    logger.info("Loaded CSV file: %s. Rows: %d", filepath, len(df))
    return df


def load_json(filepath):
    """Load a JSON file into a Python object (dict or list).
    filepath is a Path object.
    """
    import json

    with open(filepath, "r") as f:
        data = json.load(f)
    logger.info("Loaded JSON file: %s", filepath)
    return data


def load_yaml(filepath):
    """Load a YAML file into a Python object.
    filepath is a Path object.
    """
    with open(filepath, "r") as f:
        config = yaml.safe_load(f)
    logger.info("Loaded YAML file: %s", filepath)
    return config


def load_data(filepath):
    """Load a file based on its extension.
    filepath is a string, such as 'fixtures/sample.csv'
    """
    extension = Path(filepath).suffix.lower()
    if extension == ".csv":
        return load_csv(filepath)
    elif extension == ".json":
        return load_json(filepath)
    elif extension in [".yaml", ".yml"]:
        return load_yaml(filepath)
    else:
        logger.error(f"Unsupported file extension: {extension}")
        return None
