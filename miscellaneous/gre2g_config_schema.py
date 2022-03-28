"""
The module provides *Structured Config Schema* to validate Hydra configs - config parameters and their type.
It does not validate parameter values.
"""


from dataclasses import dataclass
from hydra.core.config_store import ConfigStore


@dataclass
class SettingsSchema:
    """
    Hydra config schema for Settings.

    Atributes:
        temp_path (str): Path of the GRE2G's temp folder.
        database_path (str): Path of the GREG's database path.
    """
    temp_path: str
    database_path: str


@dataclass
class GRE2GConfigSchema:
    """
    Main Hydra Config Schema for GRE2G.

    Attributes:
        settings (SettingsSchema): GRE2G's settings.
    """
    settings: SettingsSchema


def gre2g_config_schema_registration(cf_instance: ConfigStore) -> None:
    """
    Registers Hydra Config Schema for GRE2G.

    Args:
        cf_instance (ConfigStore): ConfigStore instance.

    Returns (None):
    """
    cf_instance.store(name="gre2g_config_schema", node=GRE2GConfigSchema)
