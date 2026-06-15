class UsuarioDTO:

    def __init__(
        self,
        nombre,
        email,
        rol
    ):
        self.nombre = nombre
        self.email = email
        self.rol = rol

    @classmethod
    def from_usuario(cls, usuario):

        return cls(
            nombre=usuario.nombre,
            email=usuario.email,
            rol=usuario.__class__.__name__
        )