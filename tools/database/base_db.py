"""
Implements `BaseDB` which is an abstract common interface for all databases.
"""


from abc import ABC, abstractmethod


class BaseDB(ABC):
    """
    An abstract common interface for all database types.
    """

    @abstractmethod
    def initialize(self) -> None:
        """
        Initializes the database. If the database doesn't exist, it creates a new one. If the database already exists,
        it deletes the old one and creates a new one.
        """
