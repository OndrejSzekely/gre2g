"""
Implements `Frames Detector` a key frames detection algorithms.
"""

from os import path
import numpy as np
import cv2 as cv
from .key_frames_det_base import KeyFrameDetBase
from miscellaneous.structures import Resolution
from tools.io_handlers.fs_handler import FileSystemIOHandler as FSIOHandler


class KeyFrameDetFramesDiff(KeyFrameDetBase):
    """
    Implements `KeyFrameDetFramesDiff` a key frames detection algorithms. It does basic consecutive frame diff in abs.

    Attributes:
        prev_frame (np.array): Preceeding BGR image.
        debug (bool): Whether to run the algorithm in debug mode.
        debug_path (str): Temp FS path where to store alg's debug data.
    """

    def __init__(self, debug: bool, debug_path: str) -> None:
        """
        Init method.

        Args:
            debug (bool): Whether to run the algorithm in debug mode.
            debug_path (str): Temp FS path where to store alg's debug data.
        """
        self.prev_frame = None
        self.debug = debug
        self.debug_path = debug_path

        FSIOHandler.create_whole_path(debug_path)

    def set_video_properties(self, res: Resolution) -> None:
        """
        Usemetadata of the video to initialize empty previous frame.

        Args:
            res (Resolution): Video resolution.
        """
        self.prev_frame = np.zeros((res.height, res.width, res.channels), dtype=np.uint8)

    def reset(self) -> None:
        """
        Reset the key frame detection algorithm.

        Returns (None):
        """
        self.prev_frame = None

    def __call__(self, new_frame: np.array) -> bool:
        """
        Current frame <new_frame> is passed in and `True` is returned if it's a key frame,
        otherwise `False` is returned.

        Args:
            new_frame (np.array): Current frame in BGR.

        Returns (bool): `True` is returned if it's a key frame, otherwise `False` is returned.
        """
        frames_diff = np.abs(new_frame - self.prev_frame)
        self.prev_frame = new_frame

        if self.debug:
            cv.imwrite(path.join(self.debug_path, "frames_diff.png"), frames_diff)

        return True
