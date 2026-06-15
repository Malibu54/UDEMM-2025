from models.usuario import Usuario


class Analista(Usuario):

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
            "crear_nota",
            "editar_nota",
            "ocultar_nota"
        ]