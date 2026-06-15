from services.ordenamientos.ordenamiento_strategy import (
    OrdenamientoStrategy
)


class OrdenarFechaDesc(
    OrdenamientoStrategy
):

    def ordenar(self, notas):

        return sorted(
            notas,
            key=lambda n: n.fecha_publicacion,
            reverse=True
        )