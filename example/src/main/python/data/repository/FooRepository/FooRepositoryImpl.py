from motron import Repository

from src.main.python.domain.repository.FooRepository import FooRepository


@Repository
class FooRepositoryImpl(FooRepository):
    def find_all(self):
        return ["foo1", "foo2", "foo3"]