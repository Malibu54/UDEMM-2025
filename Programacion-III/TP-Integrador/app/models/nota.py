from datetime import datetime

class Nota:

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

        self.fecha_publicacion = datetime.now()

        self.revisada_por_gerente = False

    def editar(
        self,
        titulo,
        contenido
    ):
        self.titulo = titulo
        self.contenido = contenido

    def ocultar(self):
        self.visibilidad = "OCULTO"

    def marcar_deprecated(self):

        if not self.revisada_por_gerente:
            raise Exception(
                "La nota debe ser revisada por un gerente"
            )

        self.categoria = "DEPRECATED"

    def es_emergente(self):
        return self.categoria == "EMERGENTE"