from motron.data.repository.database.BaseRepository import BaseRepository
from motron.data.repository.database.DatabaseManager import DatabaseManager

class MongoRepository(BaseRepository):
    def __init__(self, entity_class):
        if not entity_class:
            raise ValueError("entity_class must not be None")
        self.entity_class = entity_class
        self._db = None
        self._collection = None

    @property
    def db(self):
        if self._db is None:
            self._db = DatabaseManager.get_db()
        return self._db

    @property
    def collection(self):
        if self._collection is None:
            self._collection = self.db[self.entity_class.__name__.lower()]
        return self._collection

    def _entity_to_filter(self, entity):
        return {
            key: value for key, value in entity.__dict__.items()
            if value is not None
        }

    def _strip_mongo_id(self, doc):
        doc.pop("_id", None)
        return doc

    def save(self, entity):
        result = self.collection.replace_one(
            {"id": entity.id},
            entity.__dict__,
            upsert=True
        )
        return {
            "id": str(result.upserted_id) if result.upserted_id else entity.id,
            "inserted": result.upserted_id is not None
        }

    def findById(self, id):
        doc = self.collection.find_one({"id": id})
        return self.entity_class(**self._strip_mongo_id(doc)) if doc else None

    def findAll(self, filter_entity=None):
        filter_dict = self._entity_to_filter(filter_entity) if filter_entity else {}
        return [
            self.entity_class(**self._strip_mongo_id(doc))
            for doc in self.collection.find(filter_dict)
        ]

    def findOne(self, filter_entity):
        filter_dict = self._entity_to_filter(filter_entity)
        doc = self.collection.find_one(filter_dict)
        return self.entity_class(**self._strip_mongo_id(doc)) if doc else None

    def delete(self, filter_entity):
        filter_dict = self._entity_to_filter(filter_entity)
        result = self.collection.delete_many(filter_dict)
        return {
            "deleted_count": result.deleted_count,
            "filter": filter_dict
        }

    def deleteById(self, id):
        self.collection.delete_one({"id": id})

    def existsById(self, id):
        return self.collection.find_one({"id": id}) is not None

    def count(self, filter_entity=None):
        filter_dict = self._entity_to_filter(filter_entity) if filter_entity else {}
        return self.collection.count_documents(filter_dict)
