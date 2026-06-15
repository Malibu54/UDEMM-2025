from services.notificaciones.observer import Observer


class EmailObserver(Observer):

    def actualizar(self, nota):

        print(
            f"[EMAIL] Nueva nota emergente: "
            f"{nota.titulo}"
        )