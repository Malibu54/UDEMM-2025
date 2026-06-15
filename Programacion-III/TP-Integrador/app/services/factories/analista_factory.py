from models.analista import Analista

from services.factories.usuario_factory import (
    UsuarioFactory
)


class AnalistaFactory(
    UsuarioFactory
):

    def crear_usuario(
        self,
        id,
        nombre,
        email,
        password_hash
    ):

        return Analista(
            id,
            nombre,
            email,
            password_hash
        )