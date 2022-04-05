"""
Implements `FileSystemDB` which is a file system database.
"""


from tools.io_handlers.fs_handler import FileSystemIOHandler as FSIOHandler
from .base_db import BaseDB


class FileSystemDB(BaseDB):
    """
    File system database.
    """

    def __init__(self, database_path: str) -> None:
        """

        Args:
            database_path (str): Path of the database root folder location.
        """
        self.database_path = database_path

    def initialize(self) -> None:
        """
        Initializes the database. If the database doesn't exist, it creates a new one. If the database already exists,
        it deletes the old one and creates a new one.
        """
        FSIOHandler.folder_force_create(self.database_path)
