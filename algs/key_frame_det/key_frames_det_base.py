"""
Implements `Base Key Frames Detector` used as an interface for all key frames detection algorithms.
"""

from abc import ABC, abstractmethod
from typing import Final
import numpy as np
from miscellaneous.structures import Resolution


class KeyFrameDetBase(ABC):
    """
    Implements `Base Key Frames Detector` used as an interface for all key frames detection algorithms.
    Inherited classes entry points and the way of using:
    ```
    key_frame_det: KeyFrameDetBase = KeyFrameDetChild(...)
    key_frame_det.set_video_properties(**video1_properties)
    for frame in video1:
        key_frame_det(frame)
    key_frame_det.reset()

    key_frame_det.set_video_properties(**video2_properties)
    for frame in video2:
        key_frame_det(frame)
    key_frame_det.reset()
    ```

    Attributes:
        KEY_FRAMES_FOLDER (str): Subfolder name where key frames are stored.
    """

    KEY_FRAMES_FOLDER: Final[str] = "key_frames"

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
