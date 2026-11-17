from abc import ABC, abstractmethod

class RepositorioResultados(ABC):

    @abstractmethod
    def guardar(self, resultado):
        raise NotImplementedError

    @abstractmethod
    def buscar_por_id_documento(self, id_documento):
        raise NotImplementedError

class RepositorioResultadosEnMemoria(RepositorioResultados):
    def __init__(self):
        self.__almacen = {}

    def guardar(self, resultado):
        self.__almacen[resultado.id_documento] = resultado

    def buscar_por_id_documento(self, id_documento):
        return self.__almacen.get(id_documento)

class RepositorioResultadosSQL(RepositorioResultados):

    def __init__(self, cadena_conexion):
        self.__cadena_conexion = cadena_conexion

    def guardar(self, resultado):

        raise NotImplementedError(
            "Persistencia SQL no implementada en este alcance.")

    def buscar_por_id_documento(self, id_documento):

        raise NotImplementedError(
            "Persistencia SQL no implementada en este alcance.")

class FabricaRepositorio:

    @staticmethod
    def crear(tipo_persistencia, cadena_conexion=None):
        tipo_normalizado = tipo_persistencia.lower().strip()
        if tipo_normalizado == "memoria":
            return RepositorioResultadosEnMemoria()
        if tipo_normalizado == "sql":
            return RepositorioResultadosSQL(cadena_conexion)
        raise ValueError(
            f"Tipo de persistencia no soportado: "
            f"'{tipo_persistencia}'.")