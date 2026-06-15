from abc import ABC
from abc import abstractmethod


class OrdenamientoStrategy(ABC):

    @abstractmethod
    def ordenar(self, notas):
        pass