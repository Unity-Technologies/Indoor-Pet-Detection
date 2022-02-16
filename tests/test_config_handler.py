from unittest.mock import MagicMock, patch

import pytest
from yacs.config import CfgNode

from src.config_handler import load_config, override_config, prepare_config


@pytest.fixture
def config():
    """Prepare mock config"""
    with open("tests/configs/mock-config.yaml") as f:
        cfg = CfgNode.load_cfg(f)
    return cfg


def test_override_config(config):
    actual_value = True
    expected_value = False
    override = f"resume={expected_value}"
    config.resume = actual_value
    returned_config = override_config(override=override, config=config)
    assert returned_config["resume"] != actual_value
    assert returned_config["resume"] == expected_value


@patch("src.config_handler.CfgNode.load_cfg")
@patch("src.config_handler.open")
def test_load_config(mock_open, mock_config):
    mock_obj = MagicMock()
    mock_open.return_value = mock_obj
    config_url = "tests/configs/mock-config.yaml"
    load_config(config_url)
    mock_config.assert_called_with(mock_obj)


@patch("src.config_handler.override_config")
@patch("src.config_handler.load_config")
def test_prepare_config(mock_load, mock_override):
    mock_obj = MagicMock()
    mock_load.return_value = mock_obj
    config_url = "test.yaml"
    override = "test=test"
    prepare_config(path=config_url, override=override)
    mock_load.assert_called_with(config_url)
    mock_override.assert_called_with(override=override, config=mock_obj)
