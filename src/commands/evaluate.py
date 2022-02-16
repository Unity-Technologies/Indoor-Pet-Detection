import logging

import click

import src.constants as const
from src.commands.train import OverrideKey
from src.config_handler import prepare_config
from src.estimators.detectron import DetectronEstimator

logger = logging.getLogger(__name__)


@click.command(
    help="Start model evaluation tasks for a pre-trained model.",
    context_settings=const.CONTEXT_SETTINGS,
)
@click.option(
    "-c",
    "--config",
    type=click.STRING,
    required=True,
    help="Path to the config estimator yaml file.",
)
@click.option(
    "-p",
    "--checkpoint-file",
    type=click.STRING,
    required=True,
    help="URI to a checkpoint file.",
)
@click.option(
    "-t",
    "--test-data",
    type=click.Path(exists=True, file_okay=False),
    required=True,
    help="Directory on localhost where test dataset is located.",
)
@click.option(
    "-l",
    "--tb-log-dir",
    type=click.STRING,
    default=const.DEFAULT_TENSORBOARD_LOG_DIR,
    help=(
        "Path to the directory where tensorboard events should be stored. "
        "This Path can be GCS URI (e.g. gs://<bucket>/runs) or full path "
        "to a local directory."
    ),
)
@click.option(
    "-w",
    "--workers",
    type=click.INT,
    default=0,
    help=(
        "Number of multiprocessing workers for loading datasets. "
        "Set this argument to 0 will disable multiprocessing which is "
        "recommended when running inside a docker container."
    ),
)
@click.option(
    "--override",
    default=None,
    type=OverrideKey(),
    required=False,
    help=(
        "String of key-value pairs."
        f"Supported override key {OverrideKey.OVERRIDE_PTRN}"
    ),
)
def cli(
    config, checkpoint_file, test_data, tb_log_dir, workers, override,
):
    ctx = click.get_current_context()
    logger.debug(f"Called evaluate command with parameters: {ctx.params}")
    logger.debug(f"Override estimator config with args: {ctx.args}")

    config = prepare_config(path=config, override=override)

    estimator = DetectronEstimator(
        config=config,
        name=config.estimator,
        checkpoint_file=checkpoint_file,
        tb_log_dir=tb_log_dir,
        workers=workers,
        test_data=test_data,
    )

    estimator.run(eval_only=True)
