from datetime import datetime


class Nota:

    def __init__(
        self,
        titulo,
        contenido,
        categoria,
        visibilidad,
        autor
    ):
        self.titulo = titulo
        self.contenido = contenido
        self.categoria = categoria
        self.visibilidad = visibilidad
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