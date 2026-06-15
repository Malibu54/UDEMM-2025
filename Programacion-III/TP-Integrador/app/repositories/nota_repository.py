from abc import ABC
from abc import abstractmethod

class NotaRepository(ABC):

    @abstractmethod
    def guardar(self, nota):
        pass

    @abstractmethod
    def actualizar(self, nota):
        pass

    @abstractmethod
    def buscar_por_id(self, id):
        pass

    @abstractmethod
    def obtener_todas(self):
        pass

    @abstractmethod
    def eliminar(self, id):
        pass