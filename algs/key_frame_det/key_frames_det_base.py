"""
Implements `Base Key Frames Detector` used as an interface for all key frames detection algorithms.
"""

from abc import ABC, abstractmethod
import numpy as np
from miscellaneous.structures import Resolution


class KeyFrameDetBase(ABC):
    """
    Implements `Base Key Frames Detector` used as an interface for all key frames detection algorithms.
    """

    @abstractmethod
    def __init__(self, debug: bool, debug_path: str) -> None:
        """
        N/A

        Args:
            debug (bool): Whether to run the algorithm in debug mode.
            debug_path (str): Temp FS path where to store alg's debug data.
        """
        ...

    @abstractmethod
    def set_video_properties(self, res: Resolution) -> None:
        """
        Used to store metadata of the video which is gonna be processed.

        Args:
            res (Resolution): Video resolution.
        """
        ...

    @abstractmethod
    def reset(self) -> None:
        """
        Reset the key frame detection algorithm.

        Returns (None):
        """
        ...

    @abstractmethod
    def __call__(self, new_frame: np.array) -> bool:
        """
        Current frame <new_frame> is passed in and `True` is returned if it's a key frame,
        otherwise `False` is returned.

        Args:
            new_frame (np.array): Current frame in BGR.

        Returns (bool): `True` is returned if it's a key frame, otherwise `False` is returned.
        """
        ...
