from services.filtros.filtro_strategy import (
    FiltroStrategy
)


class FiltroFecha(FiltroStrategy):

    def __init__(
        self,
        fecha_inicio,
        fecha_fin
    ):
        self.fecha_inicio = fecha_inicio
        self.fecha_fin = fecha_fin

    def aplicar(self, notas):

        return [
            nota
            for nota in notas
            if self.fecha_inicio
            <= nota.fecha_publicacion
            <= self.fecha_fin
        ]