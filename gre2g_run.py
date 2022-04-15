"""
Run script for GRE2G.
"""

import os
import hydra
from tools.config.gre2g_config_schema import gre2g_config_schema_registration, GRE2GConfigSchema
from tools.config.hydra_config import set_hydra_config
from tools.config.config_schema import create_structured_config_schema
from miscellaneous.gre2g_utils import instantiate_run_command, instantiate_blob_database_handler


@create_structured_config_schema(gre2g_config_schema_registration)
@hydra.main(config_path=f"{os.path.join(os.getcwd(), 'conf')}", config_name="gre2g_config")  # type: ignore[misc]
@set_hydra_config
def main(hydra_config: GRE2GConfigSchema) -> None:  # pylint: disable=unused-argument
    """
    Main function of GRE2G.

    Args:
        hydra_config (GRE2GConfigSchema): GRE2G configuration parameters provided by Hydra's config.

    Returns (None):
    """
    blob_database = instantiate_blob_database_handler()  # pylint: disable=no-value-for-parameter
    run_command = instantiate_run_command()  # pylint: disable=no-value-for-parameter
    run_command(blob_database)


if __name__ == "__main__":
    main()  # pylint: disable=no-value-for-parameter
