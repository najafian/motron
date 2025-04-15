from motron.data.repository.logger import MotronLogger
from motron import GetMapping, PostMapping, RequestMapping, RequestMethod, RestController
from motron.presentation.rest.response import ResponseEntity
from motron.presentation.rest.request import RequestBody, RequestParam


@RestController
class FooRestController:
    logger: MotronLogger

    def __init__(self):
        pass

    @GetMapping("/foo/<id>")
    def get_foo(self, id):
        self.logger.info(f"Fetching Foo with ID: {id}")
        return f"Foo ID: {id}"

    @PostMapping("/foo")
    def create_foo(self, body: RequestBody):
        name = body.get("name", "unknown")
        self.logger.info(f"Creating Foo with name: {name}")
        return ResponseEntity.created("/foo/123", {"name": name, "status": "created"})

    @GetMapping("/greet/<id>")
    def greet(self, id, name: RequestParam("name")):
        return ResponseEntity.ok(f"Hello, {name}! You are user #{id}")

    @RequestMapping(path="/foo", method=[RequestMethod.PUT, RequestMethod.DELETE])
    def update_or_delete(self):
        return "Handled PUT or DELETE for /foo"
