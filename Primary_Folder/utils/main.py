import os
import sys

import dill
import numpy as np
import yaml
from pandas import DataFrame

from Primary_Folder.exceptions import final_except
from Primary_Folder.logger import logging


def read_yaml_file(file_path: str) -> dict:
    """
    Read a YAML file and return its content as a dictionary.

    Args:
        file_path (str): Path to the YAML file.

    Returns:
        dict: Content of the YAML file.
    """
    try:
        with open(file_path, "rb") as yaml_file:
            return yaml.safe_load(yaml_file)
    except Exception as e:
        raise final_except(e, sys) from e


def write_yaml_file(file_path: str, content: object, replace: bool = False) -> None:
    """
    Write content to a YAML file.

    Args:
        file_path (str): Path to the YAML file.
        content (object): Content to write to the file.
        replace (bool): Whether to replace the file if it exists. Default is False.
    """
    try:
        if replace and os.path.exists(file_path):
            os.remove(file_path)
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, "w") as file:
            yaml.dump(content, file)
    except Exception as e:
        raise final_except(e, sys) from e


def load_object(file_path: str) -> object:
    """
    Load an object from a file using dill.

    Args:
        file_path (str): Path to the file.

    Returns:
        object: Loaded object.
    """
    logging.info("Entered the load_object method of utils")

    try:
        with open(file_path, "rb") as file_obj:
            obj = dill.load(file_obj)

        logging.info("Exited the load_object method of utils")
        return obj
    except Exception as e:
        raise final_except(e, sys) from e


def save_numpy_array_data(file_path: str, array: np.array) -> None:
    """
    Save numpy array data to a file.

    Args:
        file_path (str): Location of the file to save.
        array (np.array): Data to save.
    """
    try:
        dir_path = os.path.dirname(file_path)
        os.makedirs(dir_path, exist_ok=True)
        with open(file_path, 'wb') as file_obj:
            np.save(file_obj, array)
    except Exception as e:
        raise final_except(e, sys) from e


def load_numpy_array_data(file_path: str) -> np.array:
    """
    Load numpy array data from a file.

    Args:
        file_path (str): Location of the file to load.

    Returns:
        np.array: Data loaded.
    """
    try:
        with open(file_path, 'rb') as file_obj:
            return np.load(file_obj, allow_pickle=True)  # Add allow_pickle=True
    except Exception as e:
        raise final_except(e, sys) from e


def save_object(file_path: str, obj: object) -> None:
    """
    Save an object to a file using dill.

    Args:
        file_path (str): Path to the file.
        obj (object): Object to save.
    """
    logging.info("Entered the save_object method of utils")

    try:
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, "wb") as file_obj:
            dill.dump(obj, file_obj)

        logging.info("Exited the save_object method of utils")
    except Exception as e:
        raise final_except(e, sys) from e


def drop_columns(df: DataFrame, cols: list) -> DataFrame:
    """
    Drop specified columns from a pandas DataFrame.

    Args:
        df (DataFrame): The DataFrame from which to drop columns.
        cols (list): List of columns to drop.

    Returns:
        DataFrame: DataFrame with the specified columns dropped.
    """
    logging.info("Entered drop_columns method of utils")

    try:
        df = df.drop(columns=cols, axis=1)

        logging.info("Exited the drop_columns method of utils")
        return df
    except Exception as e:
        raise final_except(e, sys) from e
