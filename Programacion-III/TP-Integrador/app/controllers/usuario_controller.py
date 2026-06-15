from dtos import usuario_dto


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

        return usuario_dto.from_usuario(
            usuario
        )

    def listar_usuarios(self):

        usuarios = self.repository.obtener_todos()

        return [
            usuario_dto.from_usuario(u)
            for u in usuarios
        ]