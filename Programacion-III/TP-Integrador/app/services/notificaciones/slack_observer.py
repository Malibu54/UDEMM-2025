from services.notificaciones.observer import (
    Observer
)


class SlackObserver(Observer):

    def actualizar(self, nota):

        print(
            f"[SLACK] Nueva nota emergente: "
            f"{nota.titulo}"
        )