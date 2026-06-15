from abc import ABC
from abc import abstractmethod


class Exportador(ABC):

    def exportar(
        self,
        notas
    ):

        datos = self.obtener_datos(
            notas
        )

        datos = self.filtrar_datos(
            datos
        )

        return self.generar_salida(
            datos
        )

    def obtener_datos(
        self,
        notas
    ):
        return notas

    def filtrar_datos(
        self,
        datos
    ):
        return datos

    @abstractmethod
    def generar_salida(
        self,
        datos
    ):
        pass