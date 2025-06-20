from abc import ABC, abstractmethod

class Matriz(ABC):
    """
    Clase abstracta que define la interfaz para cualquier tipo de matriz.
    """

    @abstractmethod
    def construir(self):
        """
        Método abstracto para construir la matriz.
        """
        pass

    @abstractmethod
    def mostrar(self):
        """
        Método abstracto para mostrar la matriz.
        """
        pass


class MatrizIdentidad(Matriz):
    """
    Clase que implementa una matriz identidad de tamaño n x n.
    Hereda de la clase abstracta Matriz.
    """

    def __init__(self, n):
        """
        Constructor de la clase MatrizIdentidad.

        Parámetros:
        n (int): Tamaño de la matriz identidad (número de filas y columnas).
        """
        self.n = n
        self.matriz = []  # Inicialmente vacía

    def construir(self):
        """
        Construye la matriz identidad de tamaño n x n.
        """
        self.matriz = []  # Reiniciar matriz en cada construcción
        for i in range(self.n):
            fila = []
            for j in range(self.n):
                if i == j:
                    fila.append(1)
                else:
                    fila.append(0)
            self.matriz.append(fila)

    def mostrar(self):
        """
        Muestra la matriz identidad en forma de filas.
        """
        for fila in self.matriz:
            print(fila)


# Ejemplo de uso:
if __name__ == "__main__":
    tamaño = 4  # Puedes cambiar este valor
    matriz_identidad = MatrizIdentidad(tamaño)
    matriz_identidad.construir()
    matriz_identidad.mostrar()
