"""
This file contains small domain-free functions specific to GRE2G.
"""


from os import path
import hydra
from commands.base_command import BaseCommand
from tools.databases.blob_database.base_blob_db import BaseBlobDB
from tools.config.gre2g_config_schema import GRE2GConfigSchema
from tools.config.hydra_config import GetHydraConfig
import tools.param_validators as param_val


@GetHydraConfig
def instantiate_run_command(hydra_config: GRE2GConfigSchema) -> BaseCommand:
    """
    Instantiates particular run command based on configuration provided by Hydra framework.

    Args:
        hydra_config (GRE2GConfigSchema): GRE2G configuration parameters provided by Hydra's config.

    Returns (BaseCommand): Instantiated run command.
    """
    return hydra.utils.instantiate(hydra_config.run)


@GetHydraConfig
def instantiate_blob_database_handler(hydra_config: GRE2GConfigSchema) -> BaseBlobDB:
    """
    Instantiates particular blob db handler based on configuration provided by Hydra framework.

    Args:
        hydra_config (GRE2GConfigSchema): GRE2G configuration parameters provided by Hydra's config.

    Returns (BaseBlobDB): Instantiated DB.
    """
    return hydra.utils.instantiate(hydra_config.settings.blob_database)


def append_file_ext_if_needed(file_path: str, file_ext: str) -> str:
    """
    Appends `file_ext` to `file_path` if not present. If the extension is present, `file_path` is returned without
    a change.

    Args:
        file_path (str): File path.
        file_ext (str): Extension to be added ot checked. It could be with or without leading '.'.

    Returns:
        str: File path with the extension.

    Exceptions:
        ValueError: If `file_path` contains a file extension, which doesn't match with `file_ext`.
    """
    param_val.type_check(file_path, str)
    param_val.type_check(file_ext, str)

    if file_ext[0] != ".":
        file_ext = "." + file_ext

    root, ext = path.splitext(file_path)
    if not ext:
        return path.join(root, file_ext)
    if ext not in [file_ext.lower(), file_ext.capitalize()]:
        raise ValueError(f"File path `{file_path}` doesn't have expected extension `{file_ext}`.")
    return file_path
