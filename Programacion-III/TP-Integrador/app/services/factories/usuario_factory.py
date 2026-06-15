from abc import ABC
from abc import abstractmethod


class UsuarioFactory(ABC):

    @abstractmethod
    def crear_usuario(
        self,
        id,
        nombre,
        email,
        password_hash
    ):
        pass