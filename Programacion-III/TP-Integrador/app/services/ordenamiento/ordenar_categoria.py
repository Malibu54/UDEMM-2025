from services.ordenamientos.ordenamiento_strategy import (
    OrdenamientoStrategy
)


class OrdenarCategoria(
    OrdenamientoStrategy
):

    def ordenar(self, notas):

        return sorted(
            notas,
            key=lambda n: n.categoria
        )