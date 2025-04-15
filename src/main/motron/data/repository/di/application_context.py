import inspect
from inspect import Parameter
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from apscheduler.triggers.interval import IntervalTrigger
from apscheduler.triggers.date import DateTrigger
from datetime import datetime, timedelta
import functools

# Global component registry for classes and beans
component_registry = {}

# Global scheduler
scheduler = BackgroundScheduler()

# ApplicationContext Class
class ApplicationContext:
    """
    A simple application context that:
    1) Collects all annotated classes/functions from component_registry.
    2) Instantiates classes (recursively) by examining constructor parameters.
    3) If a constructor parameter is typed as an ABC, it finds exactly one implementation in the registry.
    4) If multiple or no implementations exist, it raises an error.
    5) Automatically registers and starts scheduled tasks.
    """

    def __init__(self):
        # Stores class name -> instance
        self._instances = {}

    def initialize(self):
        """
        Go through everything in the registry. If it's a class, instantiate it.
        If it's already an instance (from @Bean), store it directly.
        Additionally, register scheduled methods.
        """
        for name, obj in component_registry.items():
            if isinstance(obj, type):  # It's a class
                if name not in self._instances:
                    self._instances[name] = self._create_bean(obj)
            else:
                # It's already a pre-created object (e.g., from @Bean)
                self._instances[name] = obj

        # Automatically register scheduled methods
        self._register_scheduled_methods()

        # Start scheduler if there is at least one job
        if scheduler.get_jobs():
            scheduler.start()

    def _create_bean(self, cls):
        """
        Recursively instantiate `cls`, injecting dependencies based on type hints.
        ABC -> automatically find one implementing class.
        Non-abstract type -> use param_type.__name__ to find a match.
        """
        signature = inspect.signature(cls.__init__)
        init_args = {}

        # Skip 'self' by ignoring the first parameter if it's named self
        for param_name, param in signature.parameters.items():
            if param_name == 'self':
                continue

            # 2. Skip *args and **kwargs
            if param.kind in (Parameter.VAR_POSITIONAL, Parameter.VAR_KEYWORD):
                continue

            # Check if there's a type annotation
            if param.annotation is not Parameter.empty:
                # If it's an ABC, find exactly one implementer in the registry
                bean_class = self._find_implementation(param.annotation)
                bean_name = bean_class.__name__

                # If not already instantiated, create it
                if bean_name not in self._instances:
                    dependency_obj = component_registry.get(bean_name)
                    if isinstance(dependency_obj, type):
                        # Recursively create
                        self._instances[bean_name] = self._create_bean(dependency_obj)
                    else:
                        # It's already an instance (from @Bean)
                        self._instances[bean_name] = dependency_obj

                # Assign the instance to this parameter
                init_args[param_name] = self._instances[bean_name]
            else:
                # No type annotation => optionally do name-based fallback
                if param_name in component_registry:
                    dep_obj = component_registry[param_name]
                    if isinstance(dep_obj, type):
                        # Not yet instantiated
                        if param_name not in self._instances:
                            self._instances[param_name] = self._create_bean(dep_obj)
                        init_args[param_name] = self._instances[param_name]
                    else:
                        # It's an instance
                        self._instances[param_name] = dep_obj
                        init_args[param_name] = dep_obj
                else:
                    init_args[param_name] = None

        # Now instantiate the class with the gathered args
        return cls(**init_args)

    def _find_implementation(self, param_type):
        """
        If param_type is an ABC, find exactly one class in the registry that implements it.
        If param_type is not abstract, just return it directly.
        """
        import inspect
        if not inspect.isabstract(param_type):
            # It's a normal class, just return it
            return param_type

        # It's an ABC -> search for exactly one matching subclass in the registry
        matches = []
        for name, obj in component_registry.items():
            if isinstance(obj, type) and issubclass(obj, param_type) and obj is not param_type:
                matches.append(obj)

        if len(matches) == 0:
            raise ValueError(f"No implementation found for ABC {param_type.__name__}")
        elif len(matches) > 1:
            raise ValueError(
                f"Multiple implementations found for ABC {param_type.__name__}: "
                + ", ".join(m.__name__ for m in matches)
            )
        return matches[0]

    def _register_scheduled_methods(self):
        """
        Scan all beans for scheduled methods and register them with the scheduler.
        """
        for bean in self._instances.values():
            for name, method in inspect.getmembers(bean, predicate=inspect.ismethod):
                if getattr(method, "_is_scheduled", False):
                    trigger = getattr(method, "_scheduled_trigger", None)
                    if trigger:
                        print(f"Registering scheduled method: {bean.__class__.__name__}.{name}")
                        scheduler.add_job(method, trigger)

    def getBean(self, name):
        """Retrieve an instantiated bean by name."""
        return self._instances.get(name, None)
