class ServicioConsultaNotas:

    def __init__(
        self,
        repository,
        filtro=None,
        ordenamiento=None
    ):
        self.repository = repository
        self.filtro = filtro
        self.ordenamiento = ordenamiento

    def obtener_notas(self):

        notas = self.repository.obtener_todas()

        if self.filtro:
            notas = self.filtro.aplicar(notas)

        if self.ordenamiento:
            notas = self.ordenamiento.ordenar(
                notas
            )

        return notas