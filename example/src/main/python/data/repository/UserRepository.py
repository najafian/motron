from example.src.main.python.domain.User import User
from motron.data.repository.database.MangoRepository import MongoRepository
from motron.data.repository.di.annotations import Repository


@Repository
class UserRepository(MongoRepository):
    def __init__(self):
        super().__init__(User)
