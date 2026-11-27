import os
import yaml

def load_config (path=None):
    path = path or os.environ.get ("CONFIG_PATH", "config/config.yaml")

    with open(path) as f:
        config = yaml.safe_load(f)

    return (config)

def data_path(config):
    """Return the training data path, respecting environment overrides."""
    return os.environ.get("DATA_PATH", config["data_path"])
