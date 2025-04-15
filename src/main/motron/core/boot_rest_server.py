from flask import Flask, request
import inspect
from motron.core.security.jwt_authentication import jwt_authentication_middleware
from motron.presentation.rest.request import RequestParam, RequestBody  # Your custom types

app = Flask(__name__)
route_registry = []    # From @GetMapping, etc.
rest_controllers = []  # From @RestController

def setUpPort(port=5000):
    controller_instances = {}
    for ctrl_class in rest_controllers:
        instance = ctrl_class()
        controller_instances[ctrl_class.__name__] = instance

    for route_def in route_registry:
        path = route_def["path"]
        methods = route_def["methods"]
        func = route_def["func"]

        qual_name_parts = func.__qualname__.split(".")
        ctrl_class_name = qual_name_parts[0] if len(qual_name_parts) > 1 else None
        instance = controller_instances.get(ctrl_class_name)

        def route_handler(*args, __instance=instance, __func=func, **kwargs):
            sig = inspect.signature(__func)
            bound_args = {}

            for name, param in sig.parameters.items():
                annotation = param.annotation

                if isinstance(annotation, RequestParam):
                    bound_args[name] = request.args.get(annotation.name)
                elif annotation is RequestBody:
                    bound_args[name] = request.get_json(force=True)
                elif name == 'self' and __instance:
                    bound_args[name] = __instance
                elif name in kwargs:
                    bound_args[name] = kwargs[name]

            return __func(**bound_args)

        endpoint_name = func.__module__ + "." + func.__qualname__
        app.add_url_rule(
            path,
            endpoint=endpoint_name,
            view_func=route_handler,
            methods=methods
        )

    print(f"Starting Flask server on port {port}")
    jwt_authentication_middleware(app)
    app.run(port=port)
