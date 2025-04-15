import functools
from enum import Enum

from motron.core.boot_rest_server import rest_controllers, route_registry

from motron.data.repository.di.annotations import Component


def RestController(cls):
    rest_controllers.append(cls)
    setattr(cls, "_is_rest_controller", True)
    return Component(cls)

def GetMapping(path):
    return _mapping_decorator(path, [RequestMethod.GET])

def PostMapping(path):
    return _mapping_decorator(path, [RequestMethod.POST])

def RequestMapping(path=None, method=None):
    """
    A generic mapping that can handle multiple HTTP methods.
    e.g., @RequestMapping(path="/foo", method=[RequestMethod.PUT, RequestMethod.DELETE])
    """
    actual_path = path if path else "/"
    actual_methods = method if method else [RequestMethod.GET]
    return _mapping_decorator(actual_path, actual_methods)

def _mapping_decorator(path, methods):
    """
    The core logic for storing route info in route_registry.
    We register a dictionary: { 'path': ..., 'methods': [...], 'func': ... }.
    """
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            # Potential place for additional logic
            return func(*args, **kwargs)

        route_registry.append({
            "path": path,
            "methods": [m.value for m in methods],  # Convert Enum to string
            "func": func
        })
        return wrapper
    return decorator

class RequestMethod(str, Enum):
    GET = "GET"
    POST = "POST"
    PUT = "PUT"
    DELETE = "DELETE"