from functools import wraps
from flask import g, jsonify

def PreAuthorize(expression):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if not g.get("user"):
                return jsonify({"error": "Unauthorized"}), 401
            # example: hasRole('ADMIN')
            if "hasRole" in expression:
                role = expression.split("'")[1]
                if role not in g.user.get("roles", []):
                    return jsonify({"error": "Forbidden"}), 403
            return func(*args, **kwargs)
        return wrapper
    return decorator

def RolesAllowed(*allowed_roles):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            user = g.get("user")
            if not user:
                return jsonify({"error": "Unauthorized"}), 401
            if not any(role in user.get("roles", []) for role in allowed_roles):
                return jsonify({"error": "Forbidden"}), 403
            return func(*args, **kwargs)
        return wrapper
    return decorator
