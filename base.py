from abc import ABC, abstractmethod
from typing import List, Any


class FieldABC(ABC):
    @abstractmethod
    def positive(self):
        pass

    @abstractmethod
    def negative(self):
        pass

    @abstractmethod
    def generate(self, length):  # Необходимо реализовывать только у итерируемых типов данных
        pass

    @abstractmethod
    def get_precision(self):  # Необходимо реализовывать только у числовых типов данных
        pass


class ValidatorABC:
    @abstractmethod
    def positive(self, data_type: FieldABC) -> List[Any]:
        pass

    @abstractmethod
    def negative(self, data_type: FieldABC) -> List[Any]:
        pass
