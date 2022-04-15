"""
Implements `BaseBlobDB` which is an abstract common interface for all blob databases.
"""


from abc import ABC, abstractmethod


class BaseBlobDB(ABC):
    """
    An abstract common interface for all database types.
    """

    @abstractmethod
    def initialize(self) -> None:
        """
        Initializes the database. If the database doesn't exist, it creates a new one. If the database already exists,
        it deletes the old one and creates a new one.
        """
