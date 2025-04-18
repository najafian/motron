# from motron.core.security.annotations import PreAuthorize, RolesAllowed
# from motron.data.repository.logger import MotronLogger
# from motron import GetMapping, PostMapping, RequestMapping, RequestMethod, RestController
# from motron.presentation.rest.response import ResponseEntity
# from motron.presentation.rest.request import RequestBody, RequestParam
#
# @RestController
# class FooControllerWithSecurity:
#     logger: MotronLogger
#
#     def __init__(self):
#         pass
#
#     @GetMapping("/foo/<id>")
#     @PreAuthorize('is_authenticated()')
#     def get_foo(self, id):
#         self.logger.info(f"Fetching Foo with ID: {id}")
#         return f"Foo ID: {id}"
#
#     @PostMapping("/foo")
#     @RolesAllowed(["admin", "manager"])
#     def create_foo(self, body: RequestBody):
#         name = body.get("name", "unknown")
#         self.logger.info(f"Creating Foo with name: {name}")
#         return ResponseEntity.created("/foo/123", {"name": name, "status": "created"})
#
#     @GetMapping("/greet/<id>")
#     @PreAuthorize("has_role('user')")
#     def greet(self, id, name: RequestParam("name")):
#         return ResponseEntity.ok(f"Hello, {name}! You are user #{id}")
