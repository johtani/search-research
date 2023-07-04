import logging
from abc import ABC, abstractmethod
class IndexRepository(ABC):

    @abstractmethod
    def get_index_name(self):
        pass

    @abstractmethod
    def create_index(self):
        pass

    @abstractmethod
    def is_exist_index(self) -> bool:
        pass

    @abstractmethod
    def delete_index(self):
        pass

class Indexer:
    repository: IndexRepository
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)

    def __init__(self, repository: IndexRepository):
        self.repository = repository

    def create_index(self, delete_if_exists: bool = False) -> bool:
        error = False
        try:
            is_exists = self.repository.is_exist_index()
            if delete_if_exists:
                if is_exists:
                    self.logger.info(" Deleting existing %s" % self.repository.get_index_name())
                    self.repository.delete_index()
                is_exists = self.repository.is_exist_index()
            if not is_exists:
                self.logger.info(" Creating index %s" % self.repository.get_index_name())
                self.repository.create_index()
            else:
                self.logger.info(" Already exists %s, then skip to create the index" % self.repository.get_index_name())
        except Exception as err:
            self.logger.info(f"Error {err}")
            error = True
        return error
