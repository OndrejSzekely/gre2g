"""
Contains various enumeration types.
"""

from enum import Enum


class PDDFFSFormat(Enum):
    """
    Pandas DataFrame file system saving formats.
    """

    PARQUET = ".parquet"
    CSV = ".csv"


class DebugLevel(Enum):
    """
    Debug level options.
    """

    NO_DEBUG = 0
    DEBUG_MAIN = 1
    DEBUG_ALL = 2
