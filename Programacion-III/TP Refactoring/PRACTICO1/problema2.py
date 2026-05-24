from abc import ABC, abstractmethod


class Elemento(ABC):

    def __init__(self):
        self._encendido = False

    @abstractmethod
    def on(self):
        pass

    @abstractmethod
    def status(self) -> bool:
        pass


class ElementoSimple(Elemento):

    def on(self):
        self._encendido = True

    def status(self) -> bool:
        return self._encendido

class ElementoCompuesto(Elemento):

    def __init__(self):
        super().__init__()
        self._hijos: list[Elemento] = []

    def add(self, elemento: Elemento):
        self._hijos.append(elemento)

    def on(self):
        self._encendido = True
        for hijo in self._hijos:
            if not hijo.status():
                hijo.on()

    def status(self) -> bool:
        if not self._hijos:
            return self._encendido
        return all(hijo.status() for hijo in self._hijos)

class Problema2:
    def status(self, elemento: Elemento) -> bool:
        return elemento.status()