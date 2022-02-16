import os
from datetime import datetime

TIMESTAMP_SUFFIX = datetime.now().strftime("%Y%m%d-%H%M%S")
PROJECT_ROOT = os.path.dirname(os.path.dirname(__file__))

# Default for tensorboard logs, checkpoints and metrics
DEFAULT_KFP_LOG_DIR = os.path.join(PROJECT_ROOT, "kfp", TIMESTAMP_SUFFIX)

DEFAULT_KFP_UI_METADATA_FILENAME = "mlpipeline-ui-metadata.json"

DEFAULT_TENSORBOARD_LOG_DIR = os.path.join(PROJECT_ROOT, "runs", TIMESTAMP_SUFFIX)

DEFAULT_CHECKPOINT_DIR = os.path.join(PROJECT_ROOT, "checkpoints", TIMESTAMP_SUFFIX)

GCS_BUCKET = "dev"
GCS_BASE_STR = "gs://"
HTTP_URL_BASE_STR = "http://"
HTTPS_URL_BASE_STR = "https://"
LOCAL_FILE_BASE_STR = "file://"

# This is a hack on yacs config system, as it does not allow null values
# in configs. They are working on supporting null values in config
# https://github.com/rbgirshick/yacs/pull/18.
NULL_STRING = "None"

DEFAULT_DATA_ROOT = "data"
SYNTHETIC_SUBFOLDER = "synthetic"
CLASSES = ["dog"]

# Default Unity Project ID where USim jobs was executed
DEFAULT_PROJECT_ID = ""

# Default Timing text for codetiming.Timer decorator
TIMING_TEXT = "[{name}] elapsed time: {:0.4f} seconds."

# Click CLI context settings
CONTEXT_SETTINGS = {
    "help_option_names": ["-h", "--help"],
    "show_default": True,
    "ignore_unknown_options": True,
    "allow_extra_args": True,
}
DEFAULT_DATASET_VERSION = "latest"
