"""
Implements `PandasDB` which is a Pandas DataFrame tabular database.

TODO: NOT NEEDED NOW
"""


from typing import Dict, Final
from miscellaneous.gre2g_utils import append_file_ext_if_needed
from tools.io_handlers.pandas_df_handler import PandasDFIOHandler as PDDFIOHandler
from .base_db import BaseDB


class PandasDB(BaseDB):
    """
    Pandas DataFrame tabular database.
    """

    PANDAS_DB_EXT: Final[str] = ".df"

    def __init__(self, database_path: str, header: Dict[str, str]) -> None:
        """

        Args:
            database_path (str): Path of the Pandas DB DataFrame.
            header (Dict[str, str]): Dictionary representing DF's column names and corresponding data types. Dictionary
                is defined in a "column_name": "type_string". For more info on type strings, take a look here -
                https://numpy.org/doc/stable/reference/arrays.dtypes.html, section `Array-protocol type strings`.
        """
        self.database_path = append_file_ext_if_needed(database_path, self.PANDAS_DB_EXT)
        self.database_header = header

    def initialize(self) -> None:
        """
        Initializes the database. If the database doesn't exist, it creates a new one. If the database already exists,
        it deletes the old one and creates a new one.
        """
        PDDFIOHandler.folder_force_create(self.database_path, self.database_header)
