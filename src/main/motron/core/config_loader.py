import os
import yaml
from functools import wraps

from motron.data.repository.components.registry import component_registry

_config = {}

def load_config(path: str):
    global _config
    with open(path, "r") as f:
        _config = yaml.safe_load(f)

def get_config():
    return _config or {}

def get_profile():
    return os.environ.get("APP_PROFILE", "default")
project_base = os.getcwd()
config_path = os.path.join(project_base,"..", "resources", "application.yml")
def ConfigurationProperties(prefix: str = "motron",path=config_path):
    def decorator(cls):
        load_config(path)
        config = get_config().get(prefix, {})
        for key, value in config.items():
            setattr(cls, key, value)
        return cls
    return decorator

def Profile(*accepted_profiles):
    def decorator(cls):
        current = get_profile()
        if current in accepted_profiles:
            component_registry[cls.__name__] = cls
            return cls
        else:
            return None  # Do not register this bean
    return decorator