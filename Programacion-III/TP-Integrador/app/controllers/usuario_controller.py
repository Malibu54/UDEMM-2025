from dto.usuario_dto import (
    UsuarioDTO
)


class UsuarioController:

    def __init__(
        self,
        repository
    ):
        self.repository = repository

    def crear_usuario(
        self,
        usuario
    ):

        self.repository.guardar(
            usuario
        )

        return UsuarioDTO.from_usuario(
            usuario
        )

    def listar_usuarios(self):

        usuarios = self.repository.obtener_todos()

        return [
            UsuarioDTO.from_usuario(u)
            for u in usuarios
        ]