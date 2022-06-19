"""
`index_recording` run command class implementation.
"""


from typing import Final, Any
from os import path
import cv2 as cv
from omegaconf import DictConfig
from tools import param_validators as param_val
from tools.config.hydra_config import GetHydraConfig
from tools.databases.blob_database.base_blob_db import BaseBlobDB
from tools.io_handlers.fs_handler import FileSystemIOHandler as FSIOHandler
from miscellaneous import gre2g_utils
from .base_command import BaseCommand
from algs.key_frame_det.key_frames_det_base import KeyFrameDetBase
from miscellaneous.structures import Resolution

class IndexRecordingCommand(BaseCommand):
    """
    `index_recording` run command class implementation.

    Indexes a previously added recording (added by `add_recording` commands). This means, following operations are run:
        1) Key frames detection

    Attributes:
        TEMP_SUBFOLDER_NAME Final[str]: Command's name in the <blob_db_temp_loc> temp folder.
        TEMP_PULLED_RECORDING_NAME Final[str]: Temp name of the pulled recording which is saved
            in <blob_db_temp_loc> folder.
        TEMP_ALGS_SUBFOLDER_NAME Final[str]: Command's algorithms temp folder name.
        game_name (str): Name of the game to be registered.
        track_name (str): Track name of the recording to be registered. One game can store multiple game tracks.
        tech (str): Technology used for producing the video recording.
    """

    TEMP_SUBFOLDER_NAME: Final[str] = "index_recording_cmd"
    TEMP_PULLED_RECORDING_NAME: Final[str] = "recording"
    TEMP_ALGS_SUBFOLDER_NAME: Final[str] = "algs"

    def __init__(self, game_name: str, track_name: str, tech: str) -> None:
        """
        Args:
            game_name (str): Name of the game to be registered.
            track_name (str): Track name of the recording to be registered. One game can store multiple game tracks.
            tech (str): Technology used for producing the video recording.
        """
        param_val.check_type(game_name, str)
        param_val.check_type(track_name, str)
        param_val.check_type(tech, str)

        self.game_name = game_name
        self.track_name = track_name
        self.tech = tech

    @GetHydraConfig
    def __call__(self, hydra_config: DictConfig, blob_db_handler: BaseBlobDB) -> None:
        """
        Runs the indexing process.

        Args:
            hydra_config (DictConfig): GRE2G configuration parameters provided by Hydra's config.
            blob_db_handler (BaseDB): GRE2G's blob database handler.
        """
        param_val.check_type(blob_db_handler, BaseBlobDB)

        cmd_temp_path = path.join(hydra_config.settings.blob_db_temp_loc, self.TEMP_SUBFOLDER_NAME)
        FSIOHandler.force_create_folder(cmd_temp_path)

        # Save the recording into the temp folder
        recordings_db = gre2g_utils.get_recordings_db_loc(blob_db_handler)  # pylint: disable=no-value-for-parameter
        recording_db_path = recordings_db + [self.game_name, self.track_name, self.tech]
        recording_file_db_path = gre2g_utils.get_recording_db_path(recording_db_path, blob_db_handler)
        _, file_ext = path.splitext(recording_file_db_path[-1])
        temp_recording_path = path.join(cmd_temp_path, self.TEMP_PULLED_RECORDING_NAME + file_ext)
        recording_bytes = blob_db_handler.get_file(recording_file_db_path)
        with open(temp_recording_path, "wb") as file_handler:
            file_handler.write(recording_bytes)
            file_handler.close()

        key_frames_detector_partial: Any = gre2g_utils.instantiate_from_hydra_config(
            hydra_config.algorithms.key_frame_det
        )

        key_frames_detector_debug_path = path.join(cmd_temp_path, self.TEMP_ALGS_SUBFOLDER_NAME, "key_frame_det")
        key_frames_detector = key_frames_detector_partial(debug_path=key_frames_detector_debug_path)

        cap = cv.VideoCapture(temp_recording_path)  # BGR MODE
        res_height = int(cap.get(cv.CAP_PROP_FRAME_HEIGHT))
        res_width = int(cap.get(cv.CAP_PROP_FRAME_WIDTH))

        key_frames_detector.set_video_properties(
            Resolution(res_width, res_height, 3)  # assuming all recordings are RGB
            )

        while True:
            has_frame, frame = cap.read()

            if not has_frame:
                break

            key_frames_detector(frame)

        key_frames_detector.reset()
        cap.release()
