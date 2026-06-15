class NotaDTO:

    def __init__(
        self,
        titulo,
        contenido,
        categoria,
        visibilidad,
        fecha_publicacion,
        hora_publicacion,
        autor
    ):
        self.titulo = titulo
        self.contenido = contenido
        self.categoria = categoria
        self.visibilidad = visibilidad
        self.fecha_publicacion = fecha_publicacion
        self.hora_publicacion = hora_publicacion
        self.autor = autor

    @classmethod
    def from_nota(cls, nota):

        return cls(
            titulo=nota.titulo,
            contenido=nota.contenido,
            categoria=nota.categoria,
            visibilidad=nota.visibilidad,
            fecha_publicacion=nota.fecha_publicacion,
            hora_publicacion=nota.hora_publicacion,
            autor=nota.autor.nombre
        )