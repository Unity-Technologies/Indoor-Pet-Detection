import logging
import re

from yacs.config import CfgNode

import src.constants as const

logger = logging.getLogger(__name__)
_REMOTE_PATTERN = r"://"
_EQUAL_STR = "="
""" This module handles YAML config related operations such as
    locating config from local or remote locations.
"""


def prepare_config(path=None, override=None):
    """load and override config from local or remote locations .

    Args:
        path: config location
        override: key-value pairs to override config
    Returns:
        config object of type yacs.config.CfgNode
    """
    config = load_config(path)
    logger.info(f"config loading from {path} completed")
    if override:
        logger.info(f"overriding config params= {override}")
        override_config(override=override, config=config)
    return config


def load_config(path):
    """ Load config file from local or remote locations.

    Args:
        path (str): This is the file-uri that indicates where
                          the YAML config should be loaded from.
        Examples:
            >>> path = "file:///root/config.yaml" # absolute path
            >>> path = "/root/config.yaml" # absolute path
            >>> path = "dev/config.yaml" # relative path

    Returns:
        config object of type yacs.config.CfgNode
    """
    logger.info(f"loading config from {path}")
    if path.startswith(const.LOCAL_FILE_BASE_STR):
        path = path[len(const.LOCAL_FILE_BASE_STR) :]
    if re.search(_REMOTE_PATTERN, path):
        # TODO: Implement remote GCS, S3, HTTP config backends
        raise NotImplementedError("Remote configs are not supported yet.")

    return CfgNode.load_cfg(open(path, "r"))


def override_config(override=None, config=None):
    """ Override params of config YAML. if override key doesn't exist
        it will throw Non-existent key.

    Args:
        override (str): String of key-value pairs.

        config: config object of type yacs.config.CfgNode

        Examples:
            >>> override = "optimizer.args.lr=0.00005 pretrained=False"

    """
    logger.debug(f" config before overriding {config}")
    tokens = override.split()
    merge_list = []
    for token in tokens:
        merge_list.extend(token.split(_EQUAL_STR))
    logger.info(f" overriding key-values {merge_list}")
    config.merge_from_list(merge_list)
    logger.info(f" overriding completed, config after override{config}")

    return config
