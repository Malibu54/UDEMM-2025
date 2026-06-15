from services.ordenamiento import ordenamiento_strategy

class OrdenarFechaAsc(
    ordenamiento_strategy
):

    def ordenar(self, notas):

        return sorted(
            notas,
            key=lambda n: n.fecha_publicacion
        )