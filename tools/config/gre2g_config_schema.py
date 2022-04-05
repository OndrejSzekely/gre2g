"""
The module provides *Structured Config Schema* to validate Hydra configs - config parameters and their type.
It does not validate parameter values.
"""


from dataclasses import dataclass
from hydra.core.config_store import ConfigStore


@dataclass
class DatabaseSchema:
    """
    Hydra Config Schema parent for all database types. Serves as *Base Database* schema.
    """


@dataclass
class FileSystemDBSchema(DatabaseSchema):
    """
    File System database Hydra Schema.

    Attributes:
        database_path (str): Database FS path.
        _target_ (str): Path to `FileSystemDB` class.
    """
    database_path: str
    _target_: str = "tools.database.file_system_db.FileSystemDB"


@dataclass
class SettingsSchema:
    """
    Hydra config schema for Settings.

    Atributes:
        temp_path (str): Path of the GRE2G's temp folder.
        blob_database (str): GREG's blob database.
    """
    temp_path: str
    blob_database: FileSystemDBSchema


@dataclass
class RunSchema:
    """
    Hydra Config Schema parent for all `run` commands. Serves as *Base Command* schema.
    """


@dataclass
class RunInitSchema(RunSchema):
    """
    `init` run Hydra Schema.

    Attributes:
        _target_ (str): Path to `InitCommand` class.
    """
    _target_: str = "commands.init.InitCommand"


@dataclass
class GRE2GConfigSchema:
    """
    Main Hydra Config Schema for GRE2G.

    Attributes:
        settings (SettingsSchema): GRE2G's settings.
        run (RunSchema): GRE2G's run command.
    """
    settings: SettingsSchema
    run: RunSchema


def gre2g_config_schema_registration(cf_instance: ConfigStore) -> None:
    """
    Registers Hydra Config Schema for GRE2G.

    Args:
        cf_instance (ConfigStore): ConfigStore instance.

    Returns (None):
    """
    cf_instance.store(name="gre2g_config_schema", node=GRE2GConfigSchema)
    cf_instance.store(group="database", name="file_system_schema", node=FileSystemDBSchema)
    cf_instance.store(group="run", name="init_schema", node=RunInitSchema)
