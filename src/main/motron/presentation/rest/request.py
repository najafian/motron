# motron/web/annotations/request.py

class RequestParam:
    """
    Marker type for a query parameter.
    Used as a type annotation in route handlers.
    Example:
        def hello(name: RequestParam("name")):
    """
    def __init__(self, name: str):
        self.name = name

class RequestBody:
    """
    Marker type for body payload.
    Used like:
        def post(data: RequestBody): ...
    """
    pass
