from abc import ABC
from abc import abstractmethod


class FiltroStrategy(ABC):

    @abstractmethod
    def aplicar(self, notas):
        pass