import functools
import yaml
import os
import importlib
import pathlib
from functools import wraps

from motron.core.application_context import ApplicationContext
from motron.core.boot_rest_server import setUpPort
from motron.data.repository.components.registry import component_registry
from motron.data.repository.logger import MotronLogger

globalLogger=MotronLogger("")

def _register(name, item):
    # Automatically inject logger if it's a class
    if isinstance(item, type):
        orig_init = item.__init__

        @functools.wraps(orig_init)
        def new_init(self, *args, **kwargs):
            full_name = f"{item.__module__}.{item.__name__}"
            self.logger = MotronLogger(full_name)
            orig_init(self, *args, **kwargs)

        item.__init__ = new_init

    component_registry[name] = item

def Component(cls):
    _register(cls.__name__, cls)
    return cls

def UseCase(cls):
    return _register_class(cls)

def _register_class(cls):
    _register(cls.__name__, cls)
    return cls

def Repository(cls):
    _register(cls.__name__, cls)
    return cls

def Bean(func):
    instance = func()
    _register(func.__name__, instance)
    return instance

def ConfigurationPropertiesScan(properties_prefix: str):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            globalLogger.info(f"Scanning configuration properties with prefix {properties_prefix}")
            return func(*args, **kwargs)
        return wrapper
    return decorator

def auto_import_modules(base_dir="."):
    for path in pathlib.Path(base_dir).rglob("*.py"):
        if "__init__" in path.name or path.name.startswith("__"):
            continue
        rel_path = path.with_suffix("").relative_to(base_dir)
        module_name = ".".join(rel_path.parts)
        try:
            importlib.import_module(module_name)
        except Exception as e:
            globalLogger.info(f"[Motron] Failed to import {module_name}: {e}")

def MotronApplication(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        config_path = os.path.join(os.getcwd(), "..", "resources", "application.yml")
        port = 5000

        if os.path.exists(config_path):
            with open(config_path, "r") as f:
                config = yaml.safe_load(f)
                motron_conf = config.get("motron", {})
                port = motron_conf.get("port", port)
                title = motron_conf.get("title", {})
                debug = motron_conf.get("debug", {})
                globalLogger.info(f" {title} Loaded port from application.yml: {port}")
                globalLogger.info(f" Debug mode: {debug}")
        else:
            globalLogger.info("[Motron] application.yml not found. Using default port 5000.")

        # Automatically scan and import all modules
        project_root = os.getcwd()
        auto_import_modules(project_root)

        context = ApplicationContext.get_instance()

        result = func(context, *args, **kwargs)
        setUpPort(port=port)
        return result

    return wrapper