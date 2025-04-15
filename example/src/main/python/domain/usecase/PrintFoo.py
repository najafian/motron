from motron import UseCase, Bean
from motron.data.repository.logger import MotronLogger

from src.main.python.domain.repository.FooRepository import FooRepository


@UseCase
class FooService:
    def __init__(self, fooRepository: FooRepository, appInfo: dict):
        self.repo = fooRepository
        self.bean = appInfo
        self.logger = MotronLogger(self.__class__.__name__)
        self.logger.info("FooService initialized")

    def print_data(self):
        items = self.repo.find_all()
        self.logger.info(f"Items from repo: {items}")
        self.logger.debug(f"Custom bean: {self.bean}")
