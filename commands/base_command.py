"""
Implements `BaseCommand` which is an abstract common interface for all commands.
"""


from abc import ABC, abstractmethod
from tools.database.base_db import BaseDB


class BaseCommand(ABC):
    """
    An abstract common interface for all commands.
    """

    @abstractmethod
    def __call__(self, blob_db_handler: BaseDB) -> None:
        """
        With this magic function, a command is executed.

        Attributes:
            blob_db_handler (BaseDB): GRE2G's blob database handler.
        """
