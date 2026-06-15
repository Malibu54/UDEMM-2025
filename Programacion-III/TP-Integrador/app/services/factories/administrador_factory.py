from models.administrador import (
    Administrador
)

from services.factories.usuario_factory import (
    UsuarioFactory
)


class AdministradorFactory(
    UsuarioFactory
):

    def crear_usuario(
        self,
        id,
        nombre,
        email,
        password_hash
    ):

        return Administrador(
            id,
            nombre,
            email,
            password_hash
        )