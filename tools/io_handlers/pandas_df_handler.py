"""
Stateless Pandas DataFrame IO handler implementation.
"""

import os
from os import path
from typing import Dict, Optional
import pandas as pd
from miscellaneous.enums import PDDFFSFormat
from tools import param_validators as param_val


class PandasDFIOHandler:
    """
    Stateless Pandas DataFrame IO handler implementation.
    """

    @staticmethod
    def df_fs_force_save_empty(df_base_path: str, df_format: PDDFFSFormat, header: Dict[str, str]) -> None:
        """
        Creates a new DataFrame with the header, given by <header> and saves it on <df_base_path> path in format
        <df_format> with corresponding extension. If file exists, it is overwritten.

        Args:
            df_base_path (str): Path of the newly created DataFrame without extension.
            df_format (PDDFFSFormat): Pandas DataFrame file system format.
            header (Dict[str, str]): Dictionary representing DF's column names and corresponding data types. Dictionary
                is defined in a "column_name": "type_string". For more info on type strings, take a look here -
                https://numpy.org/doc/stable/reference/arrays.dtypes.html, section `Array-protocol type strings`.

        Returns (None):
        """
        param_val.type_check(df_base_path, str)
        param_val.type_check(df_format, PDDFFSFormat)
        param_val.type_check(header, Dict[str, str])

        df_path = df_base_path + df_format.value

        if path.exists(df_path):
            param_val.file_existence_check(df_path)
            os.remove(df_path)
        df_db = pd.DataFrame(columns=list(header.keys()))
        df_db.astype(header, copy=False)
        if df_format == PDDFFSFormat.PARQUET:
            df_db.to_parquet(df_path, index=False)
        if df_format == PDDFFSFormat.CSV:
            df_db.to_csv(df_path, index=False)

    @staticmethod
    def df_fs_force_save(df_base_path: str, df_format: PDDFFSFormat, dataframe: pd.DataFrame) -> None:
        """
        Saves DataFrame <dataframe> on path <df_base_path> in format
        <df_format> with corresponding extension. If file exists, it is overwritten.

        Args:
            df_base_path (str): Path of the DataFrame FS path without extension.
            df_format (PDDFFSFormat): Pandas DataFrame file system format.
            dataframe (pd.DataFrame): DataFrame to be saved.

        Returns (None):
        """
        param_val.type_check(df_base_path, str)
        param_val.type_check(df_format, PDDFFSFormat)
        param_val.type_check(dataframe, pd.DataFrame)

        df_path = df_base_path + df_format.value

        if path.exists(df_path):
            param_val.file_existence_check(df_path)
            os.remove(df_path)
        if df_format == PDDFFSFormat.PARQUET:
            dataframe.to_parquet(df_path, index=False)
        if df_format == PDDFFSFormat.CSV:
            dataframe.to_csv(df_path, index=False)

    @staticmethod
    def load_df(df_base_path: str, df_format: PDDFFSFormat, dtype_header: Optional[Dict[str, str]]) -> pd.DataFrame:
        """
        Loads the DataFrame from FS located on path <df_base_path> without extension.
        Defines DataFrame's saved format and file's extension.
        Args:
            df_base_path (str): DataFrame's path without extension. The extension must be compliant with
                <df_format>.
            df_format (PDDFFSFormat): Pandas DataFrame file system format.
            dtype_header (Optional[Dict[str, str]]): Mapping table header with data types. In not passed, then data
                types are deduced.

        Returns:
            pd.DataFrame: Loaded Pandas DataFrame.
        """
        param_val.type_check(df_base_path, str)
        param_val.type_check(df_format, PDDFFSFormat)
        param_val.type_check(dtype_header, Optional[Dict[str, str]])

        df_path = df_base_path + df_format.value
        param_val.file_existence_check(df_path)

        loaded_df = pd.DataFrame()
        if df_format == PDDFFSFormat.PARQUET:
            loaded_df = pd.read_parquet(df_path)
        if df_format == PDDFFSFormat.CSV:
            loaded_df = pd.read_csv(df_path, header=0, dtype=dtype_header, engine="pyarrow")
        return loaded_df
