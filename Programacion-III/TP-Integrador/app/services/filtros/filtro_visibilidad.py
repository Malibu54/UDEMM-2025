from services.filtros.filtro_strategy import FiltroStrategy

class FiltroEstado(FiltroStrategy):

    def __init__(self, visibilidad):
        self.estado = visibilidad

    def aplicar(self, notas):

        return [
            nota
            for nota in notas
            if nota.estado == self.estado
        ]