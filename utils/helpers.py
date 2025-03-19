import yaml

def load_config(config_path):
    """Load configuration from a YAML file."""
    with open(config_path, 'r') as f:
        return yaml.safe_load(f)