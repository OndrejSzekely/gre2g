"""
`init` run command class implementation.
"""


from os import path
from omegaconf import DictConfig
from tools.config.hydra_config import GetHydraConfig
from tools.databases.blob_database.base_blob_db import BaseBlobDB
from tools.io_handlers.fs_handler import FileSystemIOHandler as FSIOHandler
from .base_command import BaseCommand


class InitCommand(BaseCommand):  # pylint: disable=too-few-public-methods
    """
    `init` run command class implementation.

    Performs initialization of the databases and workdir folder. If the folders already exist, it will delete them and
    create empty ones. If the folders does not exist, it will create them.
    """

    def __init__(self) -> None:
        """"""

    @GetHydraConfig
    def __call__(self, hydra_config: DictConfig, blob_db_handler: BaseBlobDB) -> None:  # type: ignore
        """
        Performs initialization of the databases and workdir folder. If the folders already exist,
        it will delete them and create empty ones. If the folders does not exist, it will create them.

        Attributes:
            hydra_config (DictConfig): G2REG's config.
            blob_db_handler (BaseBlobDB): GRE2G's blob database handler.
        """
        with blob_db_handler:
            blob_db_handler.initialize()
            blob_db_handler.force_add_level(
                path.normpath(hydra_config.settings.blob_db_recordings_loc).split(blob_db_handler.PATH_SEPARATOR),
                use_hash=False,
            )
            FSIOHandler.create_folder(hydra_config.settings.blob_db_temp_loc)
