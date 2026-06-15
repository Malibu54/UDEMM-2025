from services.ordenamiento import ordenamiento_strategy


class OrdenarFechaDesc(
    ordenamiento_strategy
):

    def ordenar(self, notas):

        return sorted(
            notas,
            key=lambda n: n.fecha_publicacion,
            reverse=True
        )