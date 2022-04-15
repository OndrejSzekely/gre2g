"""
Implements `FileSystemDB` which is a file system database.
"""


from miscellaneous.enums import PDDFFSFormat
from tools.io_handlers.fs_handler import FileSystemIOHandler as FSIOHandler
from .base_blob_db import BaseBlobDB


class FileSystemDB(BaseBlobDB):
    """
    File system database.

    Attributes:
        database_path (str): Path of the database root folder location.
        pd_df_fs_format (PDDFFSFormat): Pandas DataFrame file system format.
    """

    def __init__(self, database_path: str, pd_df_fs_format: PDDFFSFormat) -> None:
        """

        Args:
            database_path (str): Path of the database root folder location.
            pd_df_fs_format (PDDFFSFormat): Pandas DataFrame file system format.
        """
        self.database_path = database_path
        self.pd_df_fs_format = pd_df_fs_format

    def initialize(self) -> None:
        """
        Initializes the database. If the database doesn't exist, it creates a new one. If the database already exists,
        it deletes the old one and creates a new one.
        """
        FSIOHandler.folder_force_create(self.database_path)
