from example.src.main.python.domain.repository.FooRepository import FooRepository
print(f"[Impl] FooRepository id: {id(FooRepository)}")
from motron import Repository




@Repository
class FooRepositoryImpl(FooRepository):
    def find_all(self):
        return ["foo1", "foo2", "foo3"]