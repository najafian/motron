# src/main/annotations.py

from functools import wraps
import time

# Mimicking Spring annotations
def EnableScheduling(func):
    """Decorator for enabling scheduling on functions"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        print(f"Scheduling enabled for {func.__name__}")
        return func(*args, **kwargs)
    return wrapper

def ConfigurationPropertiesScan(properties_prefix: str):
    """Decorator to simulate the configuration scanning"""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            print(f"Scanning configuration properties with prefix {properties_prefix}")
            return func(*args, **kwargs)
        return wrapper
    return decorator

def SpringBootApplication(func):
    """Marks the application entry point"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        print("Spring Boot Application initialized")
        return func(*args, **kwargs)
    return wrapper

def ComponentScan(base_package: str):
    """Decorator for component scanning"""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            print(f"Scanning components in package {base_package}")
            return func(*args, **kwargs)
        return wrapper
    return decorator

def Bean(func):
    """Marks a function as a bean in the DI container"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        print(f"Registering {func.__name__} as a Bean")
        return func(*args, **kwargs)
    return wrapper

def Service(func):
    """Marks a service function"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        print(f"Service {func.__name__} registered")
        return func(*args, **kwargs)
    return wrapper

def Component(func):
    """Marks a component function"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        print(f"Component {func.__name__} registered")
        return func(*args, **kwargs)
    return wrapper

def Controller(func):
    """Marks a controller function"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        print(f"Controller {func.__name__} registered")
        return func(*args, **kwargs)
    return wrapper

def RestController(func):
    """Marks a REST controller function"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        print(f"REST Controller {func.__name__} registered")
        return func(*args, **kwargs)
    return wrapper

def Scheduled(func):
    """Marks a function as scheduled"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        print(f"Scheduling task for {func.__name__}")
        return func(*args, **kwargs)
    return wrapper
