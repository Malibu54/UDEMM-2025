from models.usuario import Usuario


class Gerente(Usuario):

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
            "ver_ocultas",
            "revisar_notas",
            "filtrar_notas"
        ]

    def revisar_nota(self, nota):
        nota.revisada_por_gerente = True