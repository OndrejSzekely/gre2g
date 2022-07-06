"""
Implements `Frames Ratio` a key frames detection algorithms.
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


class KeyFrameDetFramesRatio(KeyFrameDetBase):
    """
    Implements `KeyFrameDetFramesRatio` a key frames detection algorithms.
    It does frame ratio. It takes actual frame and laged frames which are averaged into one. Then the ratio on a pixel
    level is computed which is averaged across pixels.

    Attributes:
        KEY_FRAMES_FOLDER (str): Subfolder name where key frames are stored.
        prev_frames (Optional[np.array]): Proceeding BGR images.
            Number of stored images is given by <max_temporal_lag> attribute. Untill <set_video_properties> method is
            called, `None` value is stored. When 
        debug_level (DebugLevel): Set 0 to disable debug mode. Set 1 to debug main parts and 2 to debug all relevant.
        debug_path (str): Temp FS path where to store alg's debug data.
        res (Resolution): Resolution of internal processing.
        frame_ind (int): Index of actual frame, staring with 0.
        kf_threshold (float): Frames ratio threshold in range (0.0, 1.0). If frames ratio is above
            the threshold, then the frame is a key frame.
        max_temporal_lag (int): Temporal smoothing of prevous image for subtraction. It controls how many preceeding
            images are taken. When <reset> method is called, it's set to `None` again. Minimal value is `1` which
            represents a previous frame.
        min_kf_distance (int): Minimal frames distance from consecutive key frames.
        kf_dist (int): Aux variable to store a distance from last key frame occurance.
    """

    def __init__(self, debug_level: int, debug_path: str, threshold: float, processing_res_width: int,
                 processing_res_height: int, max_temporal_lag: int, min_kf_distance: int) -> None:
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
            max_temporal_lag (int): Temporal smoothing of prevous image for subtraction. It controls how many preceeding
                images are taken. Minimal value is `1` which represents a previous frame.
            min_kf_distance (int): Minimal frames distance from consecutive key frames.
        """
        param_val.check_type(debug_level, int)
        param_val.check_type(debug_path, str)
        param_val.check_type(threshold, float)
        param_val.check_type(processing_res_width, int)
        param_val.check_type(processing_res_height, int)
        param_val.check_type(max_temporal_lag, int)
        param_val.check_type(min_kf_distance, int)
        param_val.check_parameter_value_in_range(threshold, 1e-6, 1-1e-6)
        param_val.check_parameter_value_in_range(debug_level, DebugLevel.NO_DEBUG.value, DebugLevel.DEBUG_ALL.value)
        param_val.check_parameter_value_in_range(processing_res_width, 0, consts.MAX_RESOLUTION_WIDTH)
        param_val.check_parameter_value_in_range(processing_res_height, 0, consts.MAX_RESOLUTION_HEIGHT)
        param_val.check_parameter_value_in_range(max_temporal_lag, 1, 100)  # hardcoded value, no reason to go over 100.
        param_val.check_parameter_value_in_range(min_kf_distance, 0, 5000)  # hardcoded value, no reason to go over 5k.

        self.max_temporal_lag = max_temporal_lag
        self.prev_frames = None
        self.debug_level = DebugLevel(debug_level)
        self.debug_path = debug_path
        self.kf_threshold = threshold
        self.res = Resolution(processing_res_width, processing_res_height, 3)
        self.frame_ind = -1
        self.min_kf_distance = min_kf_distance
        self.kf_dist = min_kf_distance  # to be able to detect very first frame

        FSIOHandler.create_whole_path(debug_path)
        FSIOHandler.create_whole_path(path.join(debug_path, self.KEY_FRAMES_FOLDER))

    def set_video_properties(self, res: Resolution) -> None:
        """
        Usemetadata of the video to initialize empty previous frame.

        Args:
            res (Resolution): Video resolution.
        """
        self.res.channels = res.channels
        self.prev_frames = np.zeros((self.max_temporal_lag, self.res.height, self.res.width, self.res.channels),
            dtype=np.uint8)

    def reset(self) -> None:
        """
        Reset the key frame detection algorithm.

        Returns (None):
        """
        self.prev_frames = None
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

        prev_frames_avg = np.mean(self.prev_frames, axis=0, dtype=np.uint16).astype(np.uint8)
        frames_diff = np.abs(frame_resized - prev_frames_avg)
        stacked_frames = np.stack((frame_resized, prev_frames_avg), axis=3)
        frames_min = stacked_frames.min(axis=-1).astype(np.float32)
        frames_max = stacked_frames.max(axis=-1).astype(np.float32)
        frames_diff_ratio = 1 - np.mean(frames_min / (frames_max + consts.MATH_EPS))
        is_key_frame = bool(frames_diff_ratio > self.kf_threshold)

        if is_key_frame:
            self.kf_dist = 0

        tem_lag_pos = self.frame_ind % self.max_temporal_lag
        self.prev_frames[tem_lag_pos] = frame_resized

        if self.debug_level is not DebugLevel.NO_DEBUG:
            if is_key_frame:
                cv.imwrite(path.join(self.debug_path, self.KEY_FRAMES_FOLDER,
                                     f"key_frame_{self.frame_ind:04}_ratio_{frames_diff_ratio}.png"), new_frame)

        if self.debug_level == DebugLevel.DEBUG_ALL:
            cv.imwrite(path.join(self.debug_path, "prev_frames_avg.png"), prev_frames_avg)
            cv.imwrite(path.join(self.debug_path, "frames_diff.png"), frames_diff)

        return is_key_frame
