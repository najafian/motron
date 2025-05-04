from motron.data.repository.database.Entity import Entity

@Entity
class User:
    def __init__(self, id=None, name=None, email=None):
        self.id = id
        self.name = name
        self.email = email

