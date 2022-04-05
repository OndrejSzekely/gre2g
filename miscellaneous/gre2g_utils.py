"""
This file contains small domain-free functions specific to GRE2G.
"""


import hydra
from commands.base_command import BaseCommand
from tools.database.base_db import BaseDB
from tools.config.gre2g_config_schema import GRE2GConfigSchema
from tools.config.hydra_config import GetHydraConfig


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
def instantiate_blob_database_handler(hydra_config: GRE2GConfigSchema) -> BaseDB:
    """
    Instantiates particular blob db handler based on configuration provided by Hydra framework.

    Args:
        hydra_config (GRE2GConfigSchema): GRE2G configuration parameters provided by Hydra's config.

    Returns (BaseDB): Instantiated DB.
    """
    return hydra.utils.instantiate(hydra_config.settings.blob_database)