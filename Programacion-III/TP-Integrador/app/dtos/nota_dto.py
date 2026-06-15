class NotaDTO:

    def __init__(
        self,
        titulo,
        categoria,
        fecha_publicacion,
        autor
    ):
        self.titulo = titulo
        self.categoria = categoria
        self.fecha_publicacion = fecha_publicacion
        self.autor = autor

    @classmethod
    def from_nota(cls, nota):

        return cls(
            titulo=nota.titulo,
            categoria=nota.categoria,
            fecha_publicacion=nota.fecha_publicacion,
            autor=nota.autor.nombre
        )