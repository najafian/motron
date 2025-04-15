from functools import wraps


def Valid(model):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            body = kwargs.pop("body")
            validated = model(**body)
            return func(*args, **kwargs, body=validated)
        return wrapper
    return decorator
