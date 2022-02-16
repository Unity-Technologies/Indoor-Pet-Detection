import logging

import click

import src.constants as const
from src.commands import Entrypoint

logging.basicConfig(
    level=logging.INFO,
    format=("%(levelname)s | %(asctime)s | %(name)s | %(threadName)s | " "%(message)s"),
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger(__name__)


@click.command(
    cls=Entrypoint, help="unity-cv.", context_settings=const.CONTEXT_SETTINGS,
)
@click.option(
    "-v", "--verbose", is_flag=True, default=False, help="Enables verbose mode.",
)
def entrypoint(verbose):
    if verbose:
        root_logger = logging.getLogger()
        root_logger.setLevel(logging.DEBUG)


if __name__ == "__main__":
    entrypoint()
