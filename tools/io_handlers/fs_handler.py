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
    def force_create_folder(folder_path: str) -> None:
        """
        Creates a folder given by <folder_path>. If there exists a folder on given path, it is deleated and created
        again. If there is a file on given path, an exception (OSError) is rised.

        Args:
            folder_path (str): Path of the folder which is created.

        Returns (None):
        """
        param_val.check_type(folder_path, str)

        if path.exists(folder_path):
            param_val.check_folder_existence(folder_path)
            rmtree(folder_path)
        os.mkdir(folder_path)

    @staticmethod
    def create_folder(folder_path: str) -> None:
        """
        Creates a folder given by <folder_path>. If there exists a folder on given path, then nothing happens.
        If there is a file on given path, an exception (OSError) is rised.

        Args:
            folder_path (str): Path of the folder which is created.

        Returns (None):
        """
        param_val.check_type(folder_path, str)

        if path.exists(folder_path):
            param_val.check_folder_existence(folder_path)
        else:
            os.mkdir(folder_path)

    @staticmethod
    def create_whole_path(folder_path: str) -> None:
        """
        Creates a folder given by <folder_path>. If there exists a folder on given path, it is deleated and created
        again. If there aren't existing path folders on the way, it creates ones.
        If there is a file on given path, an exception (OSError) is rised.

        Args:
            folder_path (str): Path of the folder which is created along missing path folders.

        Returns (None):
        """
        param_val.check_type(folder_path, str)

        folder_path_aux = folder_path + os.sep  # to handle also the last path folder in the loop
        sep_pos = -1
        while True:
            # sep_pos+1 because we want to move to next sep, not include in the substring previously found one
            sep_pos_next = folder_path_aux[sep_pos+1:].find(os.sep)
            if sep_pos_next == -1:
                break
            sep_pos = sep_pos_next + sep_pos + 1  # initial <sep_pos> is -1
            FileSystemIOHandler.create_folder(folder_path_aux[:sep_pos])

    @staticmethod
    def delete_file(file_path: str) -> None:
        """
        Deletes a file given by <file_path>. Raises an exception (OSError) if doesn't exist.

        Args:
            file_path (str): File path.

        Returns (None):
        """
        param_val.check_type(file_path, str)
        param_val.check_file_existence(file_path)

        os.remove(file_path)

    @staticmethod
    def get_file(file_path: str) -> bytes:
        """
        Reads file's bytes. File is given by its path <file_path>.

        Args:
            file_path (str): File path.

        Returns (bytes): File's bytes.
        """
        param_val.check_type(file_path, str)
        param_val.check_file_existence(file_path)

        with open(file_path, "rb") as file_reader:
            file_bytes = file_reader.read()
            file_reader.close()

        return file_bytes

    @staticmethod
    def delete_folder(folder_path: str) -> None:
        """
        Deletes a folder given by <folder_path>. Raises an exception (OSError) if doesn't exist.

        Args:
            folder_path (str): Folder path.

        Returns (None):
        """
        param_val.check_type(folder_path, str)
        param_val.check_folder_existence(folder_path)

        rmtree(folder_path)
