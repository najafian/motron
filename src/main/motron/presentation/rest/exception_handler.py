from flask import jsonify

global_exception_handlers = {}

def ControllerAdvice(cls):
    for name in dir(cls):
        method = getattr(cls, name)
        if hasattr(method, "_handles_exception"):
            exc_type = getattr(method, "_handles_exception")
            global_exception_handlers[exc_type] = method
    return cls

def ExceptionHandler(exception_type):
    def decorator(func):
        func._handles_exception = exception_type
        return func
    return decorator
