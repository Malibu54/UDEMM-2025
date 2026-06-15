class NotaPublisher:

    def __init__(self):

        self.observers = []

    def suscribir(
        self,
        observer
    ):
        self.observers.append(observer)

    def desuscribir(
        self,
        observer
    ):
        self.observers.remove(observer)

    def notificar(
        self,
        nota
    ):

        for observer in self.observers:
            observer.actualizar(nota)