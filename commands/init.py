"""
`init` run command class implementation.
"""


from tools.config.hydra_config import GetHydraConfig
from .base_command import BaseCommand
from tools.databases.blob_database.base_blob_db import BaseBlobDB


class InitCommand(BaseCommand):
    """
    `init` run command class implementation.

    Performs initialization of the databases and temporary folder. If the folders already exist, it will delete them and
    create empty ones. If the folders does not exist, it will create them.
    """

    def __init__(self) -> None:
        """"""

    @GetHydraConfig
    def __call__(self, blob_db_handler: BaseBlobDB) -> None:
        """
        Performs initialization of the databases and temporary folder. If the folders already exist,
        it will delete them and create empty ones. If the folders does not exist, it will create them.

        Attributes:
            blob_db_handler (BaseBlobDB): GRE2G's blob database handler.
        """
        blob_db_handler.initialize()
