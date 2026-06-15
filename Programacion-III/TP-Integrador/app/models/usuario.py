from abc import ABC


class Usuario(ABC):

    def __init__(
        self,
        id,
        nombre,
        email,
        password_hash
    ):
        self.id = id
        self.nombre = nombre
        self.email = email
        self.password_hash = password_hash

    def autenticar(self):
        return True