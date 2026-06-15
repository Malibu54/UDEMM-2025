from services.filtros.filtro_strategy import FiltroStrategy


class FiltroCategoria(FiltroStrategy):

    def __init__(self, categoria):
        self.categoria = categoria

    def aplicar(self, notas):

        return [
            nota
            for nota in notas
            if nota.categoria == self.categoria
        ]