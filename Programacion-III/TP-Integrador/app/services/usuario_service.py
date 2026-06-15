class UsuarioService:

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

        return usuario

    def obtener_usuarios(self):

        return self.repository.obtener_todos()