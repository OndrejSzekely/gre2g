"""
Implements `Pixels Dist` a key frames detection algorithms.
"""

from os import path
import numpy as np
import cv2 as cv
from .key_frames_det_base import KeyFrameDetBase
from miscellaneous.structures import Resolution
from miscellaneous.enums import DebugLevel
from miscellaneous import constants as consts
from tools.io_handlers.fs_handler import FileSystemIOHandler as FSIOHandler
from tools import param_validators as param_val


class KeyFrameDetPixelsDist(KeyFrameDetBase):
    """
    Implements `KeyFrameDetPixelsDist` a key frames detection algorithms.
    It compares pixels values distrubution of consecutive frames. The advantage of the the algorithm is that
    it does not rely on pixel positions, which is problematique when camera is shaking, but rather on pixel values
    distribution across whole frame.

    Attributes:
        KEY_FRAMES_FOLDER (str): Subfolder name where key frames are stored.
        prev_distribution (np.array): Proceeding frame distribution. Distrubution is stored for each HSV channel
            separatelly.
        debug_level (DebugLevel): Set 0 to disable debug mode. Set 1 to debug main parts and 2 to debug all relevant.
        debug_path (str): Temp FS path where to store alg's debug data.
        res (Resolution): Resolution of internal processing.
        frame_ind (int): Index of actual frame, staring with 0.
        kf_threshold (float): Frames ratio threshold in range (0.0, 1.0). If frames ratio is above
            the threshold, then the frame is a key frame.
        min_kf_distance (int): Minimal frames distance from consecutive key frames.
        kf_dist (int): Aux variable to store a distance from last key frame occurance.
    """

    def __init__(self, debug_level: int, debug_path: str, threshold: float, processing_res_width: int,
                 processing_res_height: int, min_kf_distance: int) -> None:
        """
        Init method.

        Args:
            debug_level (DebugLevel): Set 0 to disable debug mode. Set 1 to debug main parts and 2 to debug all
                relevant.
            debug_path (str): Temp FS path where to store alg's debug data.
            threshold (float): Frames difference threshold in range (0.0, 1.0). If frames difference is above
                the threshold, then the frame is a key frame.
            processing_res_width (int): Video resolution width during processing. Expected to be smaller than original.
            processing_res_height (int): Video resolution height during processing.
                Expected to be smaller than original.
            min_kf_distance (int): Minimal frames distance from consecutive key frames.
        """
        param_val.check_type(debug_level, int)
        param_val.check_type(debug_path, str)
        param_val.check_type(threshold, float)
        param_val.check_type(processing_res_width, int)
        param_val.check_type(processing_res_height, int)
        param_val.check_type(min_kf_distance, int)
        param_val.check_parameter_value_in_range(threshold, 1e-6, 1e10) # hardcoded value, KL-div is unbounded
        param_val.check_parameter_value_in_range(debug_level, DebugLevel.NO_DEBUG.value, DebugLevel.DEBUG_ALL.value)
        param_val.check_parameter_value_in_range(processing_res_width, 0, consts.MAX_RESOLUTION_WIDTH)
        param_val.check_parameter_value_in_range(processing_res_height, 0, consts.MAX_RESOLUTION_HEIGHT)
        param_val.check_parameter_value_in_range(min_kf_distance, 0, 5000)  # hardcoded value, no reason to go over 5k.

        self.prev_frames = None
        self.debug_level = DebugLevel(debug_level)
        self.debug_path = debug_path
        self.kf_threshold = threshold
        self.res = Resolution(processing_res_width, processing_res_height, 3)
        self.frame_ind = -1
        self.prev_distribution = np.zeros((3, 256), dtype=np.float32)
        self.min_kf_distance = min_kf_distance
        self.kf_dist = min_kf_distance  # to be able to detect very first frame

        FSIOHandler.create_whole_path(debug_path)
        FSIOHandler.create_whole_path(path.join(debug_path, self.KEY_FRAMES_FOLDER))

    def set_video_properties(self, res: Resolution) -> None:
        """
        Use metadata of the video.

        Args:
            res (Resolution): Video resolution.
        """
        self.res.channels = res.channels

    def reset(self) -> None:
        """
        Reset the key frame detection algorithm.

        Returns (None):
        """
        self.prev_distribution = np.zeros((3, 256), dtype=np.float32)
        self.frame_ind = -1
        self.kf_dist = self.min_kf_distance  # to be able to detect very first frame

    def __call__(self, new_frame: np.array) -> bool:
        """
        Current frame <new_frame> is passed in and `True` is returned if it's a key frame,
        otherwise `False` is returned.

        Args:
            new_frame (np.array): Current frame in BGR.

        Returns (bool): `True` is returned if it's a key frame, otherwise `False` is returned.
        """
        self.frame_ind += 1
        self.kf_dist += 1

        if self.kf_dist < self.min_kf_distance:
            return False

        frame_resized = cv.resize(new_frame, dsize=(self.res.width, self.res.height))
        hsv_frame = cv.split(cv.cvtColor(frame_resized, cv.COLOR_BGR2HSV))
        frame_hist = np.zeros((3, 256), dtype=np.float32)
        frame_hist[0] = np.squeeze(cv.calcHist(hsv_frame, [0], None, [256], (0, 256), accumulate=False)) / self.res.get_pixels_count()
        frame_hist[1] = np.squeeze(cv.calcHist(hsv_frame, [1], None, [256], (0, 256), accumulate=False)) / self.res.get_pixels_count()
        frame_hist[2] = np.squeeze(cv.calcHist(hsv_frame, [2], None, [256], (0, 256), accumulate=False)) / self.res.get_pixels_count()

        kl_div = np.abs(np.sum(frame_hist * np.nan_to_num(np.log(frame_hist / (self.prev_distribution + consts.MATH_EPS))), axis=1))
        kl_div_agg = np.sum(kl_div)
        is_key_frame = bool(kl_div_agg > self.kf_threshold)

        if is_key_frame:
            self.kf_dist = 0

        self.prev_distribution = frame_hist

        if self.debug_level is not DebugLevel.NO_DEBUG:
            if is_key_frame:
                cv.imwrite(path.join(self.debug_path, self.KEY_FRAMES_FOLDER,
                                     f"key_frame_{self.frame_ind:04}_kl_{kl_div_agg}.jpg"), new_frame)

        if self.debug_level == DebugLevel.DEBUG_ALL:
            ...

        return is_key_frame
