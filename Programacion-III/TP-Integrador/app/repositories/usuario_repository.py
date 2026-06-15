from abc import ABC
from abc import abstractmethod

class UsuarioRepository(ABC):

    @abstractmethod
    def guardar(self, usuario):
        pass

    @abstractmethod
    def buscar_por_id(self, id):
        pass

    @abstractmethod
    def obtener_todos(self):
        pass