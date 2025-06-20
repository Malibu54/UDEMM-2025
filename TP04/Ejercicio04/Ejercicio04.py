from abc import ABC, abstractmethod
from datetime import datetime
import random

# Clase abstracta que define la estructura básica de una venta
class VentaBase(ABC):
    @abstractmethod
    def obtener_valor(self):
        pass

    @abstractmethod
    def __str__(self):
        pass

# Clase concreta que representa una venta con id, valor y fecha
class Venta(VentaBase):
    def __init__(self, id_venta: int, valor: float, fecha: str):
        self.id_venta = id_venta
        self.valor = valor
        self.fecha = fecha  # formato: "YYYY-MM-DD"

    def obtener_valor(self):
        return self.valor

    def __str__(self):
        return f"Venta(ID: {self.id_venta}, Valor: {self.valor}, Fecha: {self.fecha})"

# Clase que representa la tabla de ventas de NxM
class TablaVentas:
    def __init__(self, filas: int, columnas: int):
        self.filas = filas
        self.columnas = columnas
        self.tabla = self._generar_tabla()

    def _generar_tabla(self):
        """Genera una tabla con objetos Venta, con datos aleatorios."""
        tabla = []
        id_counter = 1
        for i in range(self.filas):
            fila = []
            for j in range(self.columnas):
                valor = round(random.uniform(10, 1000), 2)
                fecha = datetime.now().strftime("%Y-%m-%d")
                venta = Venta(id_counter, valor, fecha)
                fila.append(venta)
                id_counter += 1
            tabla.append(fila)
        return tabla

    def obtener_ventas_por_fila(self, fila_idx: int):
        """Devuelve la lista de ventas en una fila específica."""
        if 0 <= fila_idx < self.filas:
            return self.tabla[fila_idx]
        else:
            raise IndexError("Índice de fila fuera de rango.")

# Clase que gestiona la clasificación de ventas en listas y top ten
class GestorVentas:
    def __init__(self, tabla_ventas: TablaVentas):
        self.tabla_ventas = tabla_ventas
        self.lista1 = []  # >=100 y <=150 ventas
        self.lista2 = []  # >=50 y <100
        self.lista3 = []  # >=0 y <50

    def clasificar_listas(self):
        """Clasifica cada fila en una de las tres listas según su número de ventas (columnas)."""
        for i in range(self.tabla_ventas.filas):
            fila_ventas = self.tabla_ventas.obtener_ventas_por_fila(i)
            cantidad_ventas = len(fila_ventas)

            if 100 <= cantidad_ventas <= 150:
                self.lista1.append(fila_ventas)
            elif 50 <= cantidad_ventas < 100:
                self.lista2.append(fila_ventas)
            elif 0 <= cantidad_ventas < 50:
                self.lista3.append(fila_ventas)

    def obtener_top_10(self):
        """Obtiene el top 10 de ventas con mayor valor de todas las listas."""
        todas_las_ventas = []

        for lista in [self.lista1, self.lista2, self.lista3]:
            for fila in lista:
                todas_las_ventas.extend(fila)

        # Ordenar por valor descendente
        todas_las_ventas.sort(key=lambda v: v.obtener_valor(), reverse=True)

        # Obtener top 10
        return todas_las_ventas[:10]

    def mostrar_top_10(self):
        top_ventas = self.obtener_top_10()
        print("\nTop 10 Ventas de Mayor Valor:")
        for venta in top_ventas:
            print(venta)

# Ejecución del programa
if __name__ == "__main__":
    N = 10  # Número de filas
    M = 120  # Número de columnas por fila (puede cambiar entre 0 y 150 para testear clasificación)

    tabla = TablaVentas(N, M)
    gestor = GestorVentas(tabla)
    gestor.clasificar_listas()
    gestor.mostrar_top_10()
