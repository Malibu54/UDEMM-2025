import json
import os
from abc import ABC, abstractmethod

class Persistencia(ABC):
    """
    Interfaz abstracta para mecanismos de persistencia.
    """

    @abstractmethod
    def guardar(self, datos):
        """
        Guarda los datos proporcionados en un medio persistente.
        """
        pass

    @abstractmethod
    def cargar(self):
        """
        Recupera los datos desde el medio persistente.
        """
        pass


class ArchivoPersistencia(Persistencia):
    """
    Implementación de persistencia usando archivos JSON.
    """

    def __init__(self, nombre_archivo='matriz_data.json'):
        self.nombre_archivo = nombre_archivo

    def guardar(self, datos):
        """
        Guarda los datos en un archivo JSON.
        """
        with open(self.nombre_archivo, 'w') as f:
            json.dump(datos, f)

    def cargar(self):
        """
        Carga los datos desde un archivo JSON si existe.
        """
        if os.path.exists(self.nombre_archivo):
            with open(self.nombre_archivo, 'r') as f:
                return json.load(f)
        return None


class Matriz:
    """
    Clase que representa una matriz de nxm con operaciones básicas y persistencia.
    """

    def __init__(self, n, m):
        """
        Crea una matriz de tamaño n x m inicializada con None.
        """
        self.n = n
        self.m = m
        self.data = [[None for _ in range(m)] for _ in range(n)]
        self.persistencia = ArchivoPersistencia()
        self._persistir()

    def _persistir(self):
        """
        Guarda el estado actual de la matriz en un archivo.
        """
        self.persistencia.guardar({
            'n': self.n,
            'm': self.m,
            'data': self.data
        })

    def recuperar(self):
        """
        Recupera el estado de la matriz desde el archivo de persistencia.
        """
        datos = self.persistencia.cargar()
        if datos:
            self.n = datos['n']
            self.m = datos['m']
            self.data = datos['data']

    def add(self, i, j, item):
        """
        Agrega o reemplaza un elemento en la posición (i, j).
        """
        self.data[i][j] = item
        self._persistir()

    def update(self, i, j, item):
        """
        Actualiza el valor en la posición (i, j).
        """
        self.data[i][j] = item
        self._persistir()

    def get_columna(self, j):
        """
        Retorna todos los valores de la columna j.
        """
        return [self.data[i][j] for i in range(self.n)]

    def get_fila(self, i):
        """
        Retorna todos los valores de la fila i.
        """
        return self.data[i]

    def buscar(self, elemento):
        """
        Busca un elemento en la matriz. Devuelve una tupla (fila, columna) si lo encuentra.
        """
        for i in range(self.n):
            for j in range(self.m):
                if self.data[i][j] == elemento:
                    return (i, j)
        return None

    def replace(self, tipo, index, valores):
        """
        Reemplaza completamente una fila o columna por una lista de nuevos valores.
        tipo: 'fila' o 'columna'
        index: índice de la fila o columna
        valores: lista de nuevos valores
        """
        if tipo == 'fila':
            if len(valores) != self.m:
                raise ValueError("La longitud no coincide con el número de columnas")
            self.data[index] = valores
        elif tipo == 'columna':
            if len(valores) != self.n:
                raise ValueError("La longitud no coincide con el número de filas")
            for i in range(self.n):
                self.data[i][index] = valores[i]
        else:
            raise ValueError("Tipo debe ser 'fila' o 'columna'")
        self._persistir()

    def dim(self):
        """
        Retorna la dimensión de la matriz como una tupla (n, m).
        """
        return (self.n, self.m)

    def sum(self, otra):
        """
        Suma elemento a elemento otra matriz del mismo tamaño.
        Devuelve una nueva matriz con los resultados.
        """
        if self.n != otra.n or self.m != otra.m:
            raise ValueError("Las matrices deben tener las mismas dimensiones")
        resultado = Matriz(self.n, self.m)
        for i in range(self.n):
            for j in range(self.m):
                resultado.add(i, j, self.data[i][j] + otra.data[i][j])
        return resultado

    def producto_scalar(self, escalar):
        """
        Multiplica todos los elementos de la matriz por un escalar.
        Devuelve una nueva matriz con el resultado.
        """
        resultado = Matriz(self.n, self.m)
        for i in range(self.n):
            for j in range(self.m):
                resultado.add(i, j, self.data[i][j] * escalar)
        return resultado

    def exportar(self, nombre_archivo):
        """
        Exporta el contenido de la matriz a un archivo CSV (texto plano con comas).
        """
        with open(nombre_archivo, 'w') as f:
            for fila in self.data:
                f.write(','.join(str(x) for x in fila) + '\n')
