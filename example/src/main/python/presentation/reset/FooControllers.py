from example.src.main.python.data.repository.UserRepository import UserRepository
from example.src.main.python.domain.User import User
from example.src.main.python.domain.usecase.PrintFoo import FooService
from motron.data.repository.database.DatabaseManager import DatabaseManager
from motron.data.repository.logger import MotronLogger
from motron import GetMapping, PostMapping, RequestMapping, RequestMethod, RestController
from motron.presentation.rest.response import ResponseEntity
from motron.presentation.rest.request import RequestBody, RequestParam


@RestController
class FooRestController:
    logger: MotronLogger

    def __init__(self, fooService1:FooService,userRepository:UserRepository):
        self.fooService1= fooService1
        self.repo = userRepository
        pass

    @GetMapping("/foo1/<id>")
    def get_foo1(self, id):
        self.repo.save(User("u1", "Alice", "a@example.com"))

        # Find by ID
        self.repo.findById("u1")

        # Find all users named Alice
        self.repo.findAll(User(name="Alice"))

        # Delete all users with given name and email
        self.repo.delete(User(name="David", email="test@example.com"))

        # Check existence
        self.repo.existsById("u1")

        # Count all users with given email
        return str(self.repo.count(User(email="x@example.com")))


    @GetMapping("/foo/<id>")
    def get_foo(self, id):
        db = DatabaseManager.get_db()
        collection = db["users"]
        collection.insert_one({"name": "Saeid"})
        self.fooService1.print_data()
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
