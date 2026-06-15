from services.ordenamiento import ordenamiento_strategy


class OrdenarCategoria(
    ordenamiento_strategy
):

    def ordenar(self, notas):

        return sorted(
            notas,
            key=lambda n: n.categoria
        )