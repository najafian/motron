from .logger import MotronLogger

def get_logger(class_or_name):
    name = class_or_name.__name__ if hasattr(class_or_name, '__name__') else str(class_or_name)
    return MotronLogger(name)
