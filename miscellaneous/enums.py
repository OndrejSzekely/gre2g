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
