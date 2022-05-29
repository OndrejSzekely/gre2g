"""
`add_recording` run command class implementation.
"""


from os import path
from miscellaneous import gre2g_utils
import tools.param_validators as param_val
from tools.config.hydra_config import GetHydraConfig
from tools.config.gre2g_config_schema import GRE2GConfigSchema
from tools.databases.blob_database.base_blob_db import BaseBlobDB
from .base_command import BaseCommand


class AddRecordingCommand(BaseCommand):
    """
    `add_recording` run command class implementation.

    Adds the recording into the database.

    Attributes:
        game_name (str): Name of the game to be registered.
        track_name (str): Track name of the recording to be registered. One game can store multiple game tracks.
        tech (str): Technology used for producing the video recording.
        recording_path (str): Recording path.
        start_offset (int): Track starting offset (seconds) which are skipped - doesn't contain a valid content.
        end_offset (int): Track ending offset (seconds) which are skipped - doesn't contain a valid content.
    """

    def __init__(
        self, game_name: str, track_name: str, tech: str, recording_path: str, start_offset: int, end_offset: int
    ) -> None:
        """
        Args:
            game_name (str): Name of the game to be registered.
            track_name (str): Track name of the recording to be registered. One game can store multiple game tracks.
            tech (str): Technology used for producing the video recording.
            recording_path (str): Recording path.
            start_offset (int): Track starting offset (seconds) which are skipped - doesn't contain a valid content.
            end_offset (int): Track ending offset (seconds) which are skipped - doesn't contain a valid content.
        """
        param_val.check_type(game_name, str)
        param_val.check_type(track_name, str)
        param_val.check_type(tech, str)
        param_val.check_type(recording_path, str)
        param_val.check_type(start_offset, int)
        param_val.check_type(end_offset, int)
        param_val.check_file_existence(recording_path)

        self.game_name = game_name
        self.track_name = track_name
        self.tech = tech
        self.recording_path = recording_path
        self.start_offset = start_offset
        self.end_offset = end_offset

    @GetHydraConfig
    def __call__(self, blob_db_handler: BaseBlobDB) -> None:
        """
        Adds the recording into the database and indexes it.

        Args:
            blob_db_handler (BaseDB): GRE2G's blob database handler.
        """
        recording_path = gre2g_utils.get_recordings_db_loc(blob_db_handler)  # pylint: disable=no-value-for-parameter
        for level in [self.game_name, self.track_name, self.tech]:
            existing_levels = blob_db_handler.get_level_content(recording_path)
            existing_similar_levels = gre2g_utils.get_similar_items(existing_levels, level, 6, 0.4)
            if level in existing_similar_levels:
                existing_similar_levels.remove(level)

            if existing_similar_levels:
                print("_____________________________________________________________________________________________")
                print("There are existing items with similar names:")
                display_options = existing_similar_levels + [f"Your option: {level}"]
                num_of_options = len(display_options)
                gre2g_utils.print_selection_options(display_options, range(num_of_options-1, -1, -1))  # starts with 0
                print("#############################################################################################")
                print("HINT: Just press ENTER to keep (0) option.")
                selection = input("Select an option:") or 0
                selection = int(selection)
                print("_____________________________________________________________________________________________")

                param_val.check_parameter_value_in_range(selection, 0, num_of_options - 1)  # selection starts from 0

                selected_level = (
                    level if selection == 0 else existing_similar_levels[num_of_options - 1 - selection]
                )  # `num_of_options - 1 - selection` sim levels have reverse indices + user defined
                recording_path.append(selected_level)
            else:
                recording_path.append(level)
            blob_db_handler.force_add_level(recording_path)

        _, file_name = path.split(self.recording_path)
        with open(self.recording_path, 'rb') as file_reader:
            blob_db_handler.add_file(recording_path, file_reader.read(), file_name, use_hash=True)
            file_reader.close()
