"""
Implements `FileSystemDB` which is a file system database.
"""


from __future__ import (
    annotations,
)
import hashlib  # allowing future references -> return class under which return value is returned
from os import path
import os
from typing import Any, Dict, Final, List, Optional, Union

import pandas as pd
from miscellaneous.enums import PDDFFSFormat
from tools.io_handlers.fs_handler import FileSystemIOHandler as FSIOHandler
from tools.io_handlers.pandas_df_handler import PandasDFIOHandler as PDDFIOHandler
from tools import param_validators as param_val
from .base_blob_db import BaseBlobDB


class NullFSPath:
    """
    Represents a non-existing user facing path transformed into FS one. Represents Null Object design pattern.
    """

    def __str__(self) -> str:
        """
        Null FS string path representation.

        Returns:
            str: Null FS path.
        """
        return "Null FS Path"

    def __eq__(self, __o: object) -> bool:
        """
        Args:
            __o (object): Any object.

        Returns:
            bool: Return `False` if `__o` is not `NullFSPath`.
        """
        return isinstance(__o, NullFSPath)

    def __bool__(self) -> bool:
        """
        Used for `if object:` statement. Always false.

        Returns:
            bool: `False`.
        """
        return False


class FileSystemDB(BaseBlobDB):
    """
    File system database.

    Attributes:
        database_path (str): Path of the database root folder location.
        pd_df_fs_format (PDDFFSFormat): Pandas DataFrame file system format.
        MAPPING_TABLE (Final[str]): Name of Pandas DataFrame mapping table. It stores for each lavel mappings from
            user level/item name to file system id.
        PATH_SEPARATOR (str): Path separator.
    """

    MAPPING_TABLE: Final[str] = "mapping_table"
    PATH_SEPARATOR: Final[str] = os.sep
    MAPPING_TABLE_HEADER: Final[Dict[str, str]] = {"name": "U50", "fs_id": "U32"}
    HASH_LENGTH: Final[int] = 32

    def __init__(self, database_path: str, pd_df_fs_format: PDDFFSFormat) -> None:
        """

        Args:
            database_path (str): Path of the database root folder location.
            pd_df_fs_format (PDDFFSFormat): Pandas DataFrame file system format.

        Returns:
            None
        """
        self.database_path = database_path
        self.pd_df_fs_format = pd_df_fs_format

    def __enter__(self) -> FileSystemDB:
        """
        Context manager __entry__ method.

        Returns (FileSystemDB): Itself.
        """
        return self

    def __exit__(
        self,
        exc_type: Optional[Exception],
        exc_val: Optional[Any],
        exc_tb: Any,
    ) -> None:
        """
        Context manager __exit__ method.

        Args:
            exc_type (typing.Optional[Exception]): Exception type.
            exc_val (typing.Optional[typing.Any]): Exception value.
            exc_tb (typing.Any): Exception traceback.

        Returns (None):
        """

    def initialize(self) -> None:
        """
        Initializes the database. If the database doesn't exist, it creates a new one. If the database already exists,
        it deletes the old one and creates a new one.
        """
        FSIOHandler.folder_force_create(self.database_path)
        self._force_create_mapping_table([])

    def get_level_content(self, level_path: List[str]) -> List[str]:
        """
        Returns a database content on `level_path` level.

        Returns:
            List[str]: Level content.
        """
        ...

    def force_add_level(self, new_level_path: List[str], use_hash: bool = True) -> None:
        """
        Adds the new level, the last item in the `new_level_path`, into the database. If levels in the path don't exist
        it adds them too, so the last, new level can be added. If the path already exists, nothing happens.

        Args:
            new_level_path (List[str]): New level path to be added.
            use_hash (bool): Whether use item's name or generate a hash to create item's FS name. If set to `False`,
                item's first 32 characters are used.

        Returns:
            None
        """
        for path_level_ind in range(len(new_level_path)):
            level_path = new_level_path[: path_level_ind + 1]
            real_path = self._level_path_to_abs_fs_path_str(level_path)
            if not real_path:
                self._add_item_into_mapping_table(level_path[:-1], level_path[-1], use_hash)
                level_fs_path: List[str] = self._get_fs_path(level_path)  # type: ignore
                FSIOHandler.folder_create(self._get_absolute_fs_path_str(level_fs_path))
                self._force_create_mapping_table(level_path)

    def _get_fs_path(self, level_path: List[str]) -> Union[List[str], NullFSPath]:
        """
        Transforms a user facing path into actual FS one. If `level_path` does not exist, `None` is returned.

        Args:
            level_path (List[str]): User facing path.

        Returns:
            Union[List[str], NullFSPath]: Actual file system path. If path does not exist, NullFSPath is returned.
        """
        fs_path: List[str] = []
        for level in level_path:
            level_mapping_df = self._load_level_mapping_table(fs_path)
            level_mapping = level_mapping_df[level_mapping_df.name == level]
            if not level_mapping.empty:
                fs_path.append(level_mapping.fs_id.values[0])
            else:
                return NullFSPath()
        return fs_path

    def _get_absolute_fs_path_str(self, fs_path_list: List[str]) -> str:
        """
        Transforms a label path list `path_list` into FS path representation string with
        prepend absolute path of the database.

        Args:
            fs_path_list (List[str]): Path of a level/item given by path steps in a list.
                It is translated into FS path.

        Returns:
            str: String representation of the FS path with prepend absolute path of the database.
        """
        param_val.type_check(fs_path_list, List[str])

        return path.join(self.database_path, *fs_path_list)

    def _level_path_to_abs_fs_path_str(self, level_path: List[str]) -> Union[str, NullFSPath]:
        """
        Transforms a user facing path into FS path representation string with
        prepend absolute path of the database.

        Args:
            level_path (List[str]): User facing path in a list form.

        Returns:
            Union[str, NullFSPath]: String representation of the FS path with prepend absolute path of the database.
                If `level_path` isn't valid, `NullFSPath` is returned.
        """
        param_val.type_check(level_path, List[str])
        fs_path = self._get_fs_path(level_path)
        if not isinstance(fs_path, NullFSPath):  # `isinstance` is needed because of possible `[]` on a root level
            return self._get_absolute_fs_path_str(level_path)
        return NullFSPath()

    def _force_create_mapping_table(self, new_level_path: List[str]) -> None:
        """
        Creates a mapping table on the given level.

        Args:
            new_level_path (List[str]): Level path.

        Returns:
            None

        Exceptions:
            OSError: `new_level_path` is not a valid level path.
        """
        param_val.type_check(new_level_path, List[str])

        fs_new_level_path = self._get_fs_path(new_level_path)
        if isinstance(fs_new_level_path, NullFSPath):
            raise OSError(f"Given new level path `{fs_new_level_path}` does not exist.")
        mapping_table_base_path = path.join(self._get_absolute_fs_path_str(fs_new_level_path), self.MAPPING_TABLE)
        PDDFIOHandler.df_fs_force_save_empty(mapping_table_base_path, self.pd_df_fs_format, self.MAPPING_TABLE_HEADER)

    def _get_mapping_table_abs_path(self, level_fs_path: List[str]) -> str:
        """
        Composes a string representation of the mapping table FS path for given level `level_fs_path`.

        Args:
            level_fs_path (List[str]): Level File System path.

        Returns:
            str: Mapping table's absolute path.
        """
        return self._get_absolute_fs_path_str(level_fs_path + [self.MAPPING_TABLE])

    def _load_level_mapping_table(self, level_fs_path: List[str]) -> pd.DataFrame:
        """
        Loads level mapping DataFrame of the level given by `level_fs_path`. The path is a user facing path list.
        Args:
            level_fs_path (List[str]): User facing level path list.

        Returns:
            pd.DataFrame: Mapping table Pandas DataFrame.
        """
        param_val.type_check(level_fs_path, List[str])

        return PDDFIOHandler.load_df(self._get_mapping_table_abs_path(level_fs_path), self.pd_df_fs_format)

    def _add_item_into_mapping_table(self, level_path: List[str], item_name: str, use_hash: bool = True) -> str:
        """
        Adds item (folder/file) `item_name` into DataFrame's mapping table on a level `level_path`.

        Args:
            item_name (str): Item name. It can be level or actual file name with an extension.
            level_path (List[str]): Level path where `item_name` is added.
            use_hash (bool): Whether use item's name or generate a hash to create item's FS name. If set to `False`,
                item's first 32 characters are used.

        Returns (str): File System name of the item.
        """
        param_val.type_check(level_path, List[str])
        param_val.type_check(item_name, str)

        level_fs_path = self._get_fs_path(level_path)
        if isinstance(level_fs_path, NullFSPath):
            raise OSError(f"Given level path `{level_path}` does not exist.")
        mapping_table = self._load_level_mapping_table(level_fs_path)

        # check if item is a file, if not `ext` is empty
        base_item_name, ext = path.splitext(item_name)

        item_fs_id = None
        if use_hash:
            item_fs_id = hashlib.md5(base_item_name.encode("UTF-8")).hexdigest()  # nosec
        else:
            if len(item_name) - len(ext) > self.HASH_LENGTH:
                item_fs_id = item_name[: self.HASH_LENGTH]
            else:
                item_fs_id = base_item_name

        item_fs_id = item_fs_id + ext

        new_record = pd.DataFrame(data=[[item_name, item_fs_id]], columns=list(self.MAPPING_TABLE_HEADER.keys()))
        new_record.astype(self.MAPPING_TABLE_HEADER, copy=False)
        mapping_table = pd.concat([mapping_table, new_record])

        mapping_table_path = self._get_mapping_table_abs_path(level_fs_path)
        PDDFIOHandler.df_fs_force_save(mapping_table_path, self.pd_df_fs_format, mapping_table)

        return item_fs_id
