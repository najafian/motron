import inspect
from inspect import Parameter
from threading import Lock
from apscheduler.schedulers.background import BackgroundScheduler

from motron.data.repository.components.registry import component_registry
from motron.data.repository.logger import MotronLogger

scheduler = BackgroundScheduler()


def is_builtin_type(obj):
    return isinstance(obj, (dict, list, str, int, float, bool))


class ApplicationContext:
    _singleton = None
    _lock = Lock()
    _allow_init = False

    def __init__(self):
        if not ApplicationContext._allow_init:
            raise Exception("Use ApplicationContext.get_instance(), do not instantiate directly.")
        self._instances = {}

    @classmethod
    def get_instance(cls):
        with cls._lock:
            if cls._singleton is None:
                cls._allow_init = True
                cls._singleton = cls()
                cls._allow_init = False
                cls._singleton._initialize_components()
            return cls._singleton

    def _initialize_components(self):
        for name, obj in component_registry.items():
            if isinstance(obj, type):
                if name not in self._instances:
                    self._instances[name] = self.create_bean(obj)
            else:
                self._instances[name] = obj

        self._register_scheduled_methods()
        if scheduler.get_jobs():
            scheduler.start()

    def create_bean(self, cls):
        signature = inspect.signature(cls.__init__)
        init_args = {}

        for param_name, param in signature.parameters.items():
            if param_name == 'self':
                continue
            if param.kind in (Parameter.VAR_POSITIONAL, Parameter.VAR_KEYWORD):
                continue

            # Handle type-hinted injection
            if param.annotation is not Parameter.empty:
                bean_class = self._find_implementation(param.annotation)
                bean_name = bean_class.__name__

                if bean_name not in self._instances:
                    dependency_obj = component_registry.get(bean_name)
                    if isinstance(dependency_obj, type):
                        self._instances[bean_name] = self.create_bean(dependency_obj)
                    else:
                        self._instances[bean_name] = dependency_obj

                init_args[param_name] = self._instances[bean_name]
            else:
                # Fallback to name-based injection
                if param_name in component_registry:
                    dep_obj = component_registry[param_name]
                    if isinstance(dep_obj, type):
                        if param_name not in self._instances:
                            self._instances[param_name] = self.create_bean(dep_obj)
                        init_args[param_name] = self._instances[param_name]
                    else:
                        self._instances[param_name] = dep_obj
                        init_args[param_name] = dep_obj
                else:
                    init_args[param_name] = None

        instance = cls(**init_args)

        # Inject logger if it's not a primitive or dict
        if not is_builtin_type(instance):
            instance.logger = MotronLogger(cls.__name__)

        return instance

    @staticmethod
    def _find_implementation(param_type):
        import inspect
        print(f"Looking for implementation of: {param_type} ({id(param_type)})")

        for name, obj in component_registry.items():
            print(f"  -> registry[{name}] = {obj} ({'class' if isinstance(obj, type) else 'instance'}, id={id(obj)})")

        if not inspect.isabstract(param_type):
            return param_type

        matches = [
            obj for obj in component_registry.values()
            if isinstance(obj, type) and issubclass(obj, param_type) and obj is not param_type
        ]

        if len(matches) == 0:
            raise ValueError(f"No implementation found for ABC {param_type.__name__}")
        if len(matches) > 1:
            raise ValueError(f"Multiple implementations found for ABC {param_type.__name__}: " +
                             ", ".join(m.__name__ for m in matches))

        return matches[0]

    def _register_scheduled_methods(self):
        for bean in self._instances.values():
            for name, method in inspect.getmembers(bean, predicate=inspect.ismethod):
                if getattr(method, "_is_scheduled", False):
                    trigger = getattr(method, "_scheduled_trigger", None)
                    if trigger:
                        print(f"Registering scheduled method: {bean.__class__.__name__}.{name}")
                        scheduler.add_job(method, trigger)

    def getBean(self, name):
        return self._instances.get(name, None)
