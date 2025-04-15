from abc import ABC, abstractmethod

class FooRepository(ABC):
    @abstractmethod
    def find_all(self):
        pass