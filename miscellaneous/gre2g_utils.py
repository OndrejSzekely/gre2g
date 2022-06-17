"""
This file contains small domain-free functions specific to GRE2G.
"""


from typing import List
from os import path
import difflib
import hydra
from omegaconf import DictConfig
from commands.base_command import BaseCommand
from tools.databases.blob_database.base_blob_db import BaseBlobDB
from tools.config.hydra_config import GetHydraConfig
import tools.param_validators as param_val


@GetHydraConfig
def instantiate_run_command(hydra_config: DictConfig) -> BaseCommand:
    """
    Instantiates particular run command based on configuration provided by Hydra framework.

    Args:
        hydra_config (DictConfig): GRE2G configuration parameters provided by Hydra's config.

    Returns (BaseCommand): Instantiated run command.
    """
    return hydra.utils.instantiate(hydra_config.run)


@GetHydraConfig
def instantiate_blob_database_handler(hydra_config: DictConfig) -> BaseBlobDB:
    """
    Instantiates particular blob db handler based on configuration provided by Hydra framework.

    Args:
        hydra_config (DictConfig): GRE2G configuration parameters provided by Hydra's config.

    Returns (BaseBlobDB): Instantiated DB.
    """
    return hydra.utils.instantiate(hydra_config.settings.blob_database)


def append_file_ext_if_needed(file_path: str, file_ext: str) -> str:
    """
    Appends <file_ext> to <file_path> if not present. If the extension is present, <file_path> is returned without
    a change.

    Args:
        file_path (str): File path.
        file_ext (str): Extension to be added ot checked. It could be with or without leading `.`.

    Returns:
        str: File path with the extension.

    Exceptions:
        ValueError: If <file_path> contains a file extension, which doesn't match with <file_ext>.
    """
    param_val.check_type(file_path, str)
    param_val.check_type(file_ext, str)

    if file_ext[0] != ".":
        file_ext = "." + file_ext

    root, ext = path.splitext(file_path)
    if not ext:
        return path.join(root, file_ext)
    if ext not in [file_ext.lower(), file_ext.capitalize()]:
        raise ValueError(f"File path `{file_path}` doesn't have expected extension `{file_ext}`.")
    return file_path


def get_similar_items(
    item_names: List[str], queried_item_name: str, max_matches: int = 3, sim_thresh: float = 0.6
) -> List[str]:
    """
    Finds item names in <item_names> which are similar to queried name <queried_item_name>.

    Args:
        item_names (List[str]): List of item names.
        queried_item_name (str): Queried item name, for which similar names from <item_names> are searched.
        max_matches (int): Number of maximal returned matches.
        sim_thresh (float): Minimal similarity threshold.

    Returns (List[str]): A list of similar names from <item_names>.
    """
    return difflib.get_close_matches(queried_item_name, item_names, n=max_matches, cutoff=sim_thresh)


def print_selection_options(items: List[str], selection_indices: List[int]) -> None:
    """
    Displays <items> options with corresponding <selection_indices> indices in a pretty way. This is used when
    some options to pick up from are desired to be shown to a user, who afterwards selects an option from the list.

    Args:
        items (List[str]): Options to display.
        selection_indices (List[int]): Corresponding selection indices, for each option.

    Returns (None):
    """
    for item, selection_index in zip(items, selection_indices):
        print(f"{item:80}({selection_index})")


def get_recording_db_path(recording_db_path: List[str], blob_db_handler: BaseBlobDB) -> List[str]:
    """
    Convert's recording's DB path <recording_db_path> given by levels to actual recording file DB path with the
    filename.

    Args:
        recording_db_path (List[str]): Recording's DB path given by levels, without actual recoding file name.
        blob_db_handler (BaseBlobDB): Blob database handler.

    Returns (List[str]): Path to actual recording file. <recording_db_path> + recording's file name with extension.
    """
    param_val.check_type(recording_db_path, List[str])
    param_val.check_type(blob_db_handler, BaseBlobDB)

    recording_db_path_with_file = recording_db_path.copy()
    recording_db_path_with_file.append(blob_db_handler.get_level_content(recording_db_path_with_file)[0])
    return recording_db_path_with_file


@GetHydraConfig
def get_recordings_db_loc(hydra_config: DictConfig, blob_db_handler: BaseBlobDB) -> str:
    """
    Returns recordings DB normalized path.

    Args:
        hydra_config (DictConfig): GRE2G configuration parameters provided by Hydra's config.
        blob_db_handler (BaseBlobDB): DB handler of recordings DB.

    Returns:
        str: Recordings DB normalized path.
    """
    param_val.check_type(blob_db_handler, BaseBlobDB)

    return path.normpath(hydra_config.settings.blob_db_recordings_loc).split(blob_db_handler.PATH_SEPARATOR)
