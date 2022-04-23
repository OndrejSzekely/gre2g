"""
Implements `BaseBlobDB` which is an abstract common interface for all blob databases.
"""


from __future__ import (
    annotations,
)  # allowing future references -> return class under which return value is returned
from typing import Any, List, Optional
from abc import ABC, abstractmethod


class BaseBlobDB(ABC):
    """
    An abstract common interface for all database types. It implements context manager magic methods interface.
    """

    @property
    def PATH_SEPARATOR(self) -> str:  # pylint: disable=invalid-name
        """
        Defines a path separator.

        Returns (str):
        """
        raise NotImplementedError

    @abstractmethod
    def __enter__(self) -> BaseBlobDB:
        """
        Context manager __entry__ method.

        Returns (BaseBlobDB): Itself.
        """

    @abstractmethod
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

    @abstractmethod
    def initialize(self) -> None:
        """
        Initializes the database. If the database doesn't exist, it creates a new one. If the database already exists,
        it deletes the old one and creates a new one.
        """

    @abstractmethod
    def get_level_content(self, level_path: List[str]) -> List[str]:
        """
        Returns a database content on `level_path` level.

        Returns:
            List[str]: Level content.
        """

    @abstractmethod
    def force_add_level(self, new_level_path: List[str], use_hash: bool = True) -> None:
        """
        Adds the new level, the last item in the `new_level_path`, into the database. If levels in the path don't exist
        it adds them too, so the last, new level can be added. If the path already exists, nothing happens.

        Args:
            new_level_path (List[str]): New level path to be added.
            use_hash (bool): Whether use item's name or generate a hash to create item's FS name. If set to `False`,
                item's first 32 characters are used.
        """
