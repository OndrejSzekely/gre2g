"""
The module provides *Structured Config Schema* to validate Hydra configs - config parameters and their type.
It does not validate parameter values.
"""


from dataclasses import dataclass
from hydra.core.config_store import ConfigStore
from miscellaneous.enums import PDDFFSFormat


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
        pd_df_fs_format (PDDFFSFormat): Underlying Pandas DF FS format.
        _target_ (str): Path to `FileSystemDB` class.
    """

    database_path: str
    pd_df_fs_format: PDDFFSFormat
    _target_: str = "tools.databases.blob_database.file_system_db.FileSystemDB"


@dataclass
class SettingsSchema:
    """
    Hydra config schema for Settings.

    Atributes:
        blob_db_recordings_loc (str): Location of recordings inside GRE2G's blob database.
        blob_db_temp_loc (str): Location of temp store inside GRE2G's blob database.
        blob_database (str): GREG's blob database.
    """

    blob_db_recordings_loc: str
    blob_db_temp_loc: str
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
class RunAddRecordingSchema(RunSchema):
    """
    `add_recording` run Hydra Schema.

    Attributes:
        game_name (str): Game name.
        track_name (str): Recording track name.
        tech (str): Technology used to produce the recording.
        recording_path (str): Recording path.
        start_offset (int): Video start offset, which doesn't contain a valid content to be compared.
        end_offset (int): Video end offset, which doesn't contain a valid content to be compared.
        _target_ (str): Path to `AddRecordingCommand` class.
    """

    game_name: str
    track_name: str
    tech: str
    recording_path: str
    start_offset: int
    end_offset: int
    _target_: str = "commands.add_recording.AddRecordingCommand"


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
    cf_instance.store(group="run", name="add_recording_schema", node=RunAddRecordingSchema)
