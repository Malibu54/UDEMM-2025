from models.gerente import Gerente

from services.factories.usuario_factory import (
    UsuarioFactory
)


class GerenteFactory(
    UsuarioFactory
):

    def crear_usuario(
        self,
        id,
        nombre,
        email,
        password_hash
    ):

        return Gerente(
            id,
            nombre,
            email,
            password_hash
        )