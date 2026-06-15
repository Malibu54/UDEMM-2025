from services.filtros.filtro_strategy import (
    FiltroStrategy
)


class FiltroVisibilidad(FiltroStrategy):

    def __init__(self, visibilidad):
        self.visibilidad = visibilidad

    def aplicar(self, notas):

        return [
            nota
            for nota in notas
            if nota.visibilidad == self.visibilidad
        ]