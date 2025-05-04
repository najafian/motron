from abc import ABC, abstractmethod

class BaseRepository(ABC):
    @abstractmethod
    def save(self, entity): pass

    @abstractmethod
    def findById(self, id): pass

    @abstractmethod
    def findAll(self, filter_entity=None): pass

    @abstractmethod
    def findOne(self, filter_entity): pass

    @abstractmethod
    def delete(self, filter_entity): pass

    @abstractmethod
    def deleteById(self, id): pass

    @abstractmethod
    def existsById(self, id): pass

    @abstractmethod
    def count(self, filter_entity=None): pass
