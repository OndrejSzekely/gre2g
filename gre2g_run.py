"""
Run script for GRE2G.
"""

import os
import hydra
from omegaconf import DictConfig
from tools.config.hydra_config import set_hydra_config
from miscellaneous.gre2g_utils import instantiate_run_command, instantiate_blob_database_handler


@hydra.main(config_path=f"{os.path.join(os.getcwd(), 'conf')}", config_name="gre2g_config")  # type: ignore[misc]
@set_hydra_config
def main(hydra_config: DictConfig) -> None:  # pylint: disable=unused-argument
    """
    Main function of GRE2G.

    Args:
        hydra_config (DictConfig): GRE2G configuration parameters provided by Hydra's config.

    Returns (None):
    """
    blob_database = instantiate_blob_database_handler()  # pylint: disable=no-value-for-parameter
    run_command = instantiate_run_command()  # pylint: disable=no-value-for-parameter
    run_command(blob_database)


if __name__ == "__main__":
    main()  # pylint: disable=no-value-for-parameter
