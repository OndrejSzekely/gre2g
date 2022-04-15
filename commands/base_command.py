"""
Implements `BaseCommand` which is an abstract common interface for all commands.
"""


from abc import ABC, abstractmethod
from tools.databases.blob_database.base_blob_db import BaseBlobDB


class BaseCommand(ABC):
    """
    An abstract common interface for all commands.
    """

    @abstractmethod
    def __call__(self, blob_db_handler: BaseBlobDB) -> None:
        """
        With this magic function, a command is executed.

        Attributes:
            blob_db_handler (BaseBlobDB): GRE2G's blob database handler.
        """
