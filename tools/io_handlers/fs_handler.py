"""
Stateless File System IO handler implementation.
"""


import os
from os import path
from shutil import rmtree
from tools import param_validators as param_val


class FileSystemIOHandler:
    """
    Stateless File System IO handler implementation.
    """

    @staticmethod
    def folder_force_create(folder_path: str) -> None:
        """
        Creates a folder given by `folder_path`. If there exists a folder on given path, it is deleated and created
        again. If there is a file on given path, an exception (OSError) is rised.

        Args:
            folder_path (str): Path of the folder which is created.

        Returns (None):
        """
        param_val.type_check(folder_path, str)

        if path.exists(folder_path):
            param_val.folder_existence_check(folder_path)
            rmtree(folder_path)
        os.mkdir(folder_path)

    @staticmethod
    def folder_create(folder_path: str) -> None:
        """
        Creates a folder given by `folder_path`. If there exists a folder on given path, then nothing happens.
        If there is a file on given path, an exception (OSError) is rised.

        Args:
            folder_path (str): Path of the folder which is created.

        Returns (None):
        """
        param_val.type_check(folder_path, str)

        if path.exists(folder_path):
            param_val.folder_existence_check(folder_path)
        else:
            os.mkdir(folder_path)
