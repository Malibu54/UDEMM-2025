from models.usuario import Usuario


class Administrador(Usuario):

    def __init__(
        self,
        id,
        nombre,
        email,
        password_hash
    ):
        super().__init__(
            id,
            nombre,
            email,
            password_hash
        )

        self.permisos = [
            "gestionar_usuarios",
            "cambiar_categoria"
        ]