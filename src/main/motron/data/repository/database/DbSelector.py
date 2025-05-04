from motron.data.repository.database.BaseRepository import BaseRepository
from motron.data.repository.database.MangoRepository import MongoRepository


def get_repository(entity_class, config: dict) -> BaseRepository:
    db_type = config.get("database.type", "mongo")

    if db_type == "mongo":
        return MongoRepository(
            entity_class,
            mongo_uri=config.get("database.mongo.uri", "mongodb://localhost:27017"),
            db_name=config.get("database.mongo.name", "motron")
        )

    # Placeholder for future MySQL/MariaDB support
    raise NotImplementedError(f"DB type {db_type} not yet implemented")
