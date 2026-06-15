from services.notificaciones.observer import (
    Observer
)


class TelegramObserver(Observer):

    def actualizar(self, nota):

        print(
            f"[TELEGRAM] Nueva nota emergente: "
            f"{nota.titulo}"
        )   