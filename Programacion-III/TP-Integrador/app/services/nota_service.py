class NotaService:

    def __init__(
        self,
        repository,
        publisher
    ):

        self.repository = repository

        self.publisher = publisher

    def crear_nota(
        self,
        nota
    ):

        self.repository.guardar(
            nota
        )

        if nota.es_emergente():

            self.publisher.notificar(
                nota
            )

        return nota

    def obtener_notas(self):

        return self.repository.obtener_todas()