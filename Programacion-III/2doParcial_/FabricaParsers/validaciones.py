from abc import ABC, abstractmethod

class Especificacion(ABC):

    @abstractmethod
    def es_satisfecha_por(self, documento):
        raise NotImplementedError

    def __and__(self, otra):
        return EspecificacionY(self, otra)

    def __or__(self, otra):
        return EspecificacionO(self, otra)

class EspecificacionY(Especificacion):

    def __init__(self, izquierda, derecha):
        self.__izquierda = izquierda
        self.__derecha = derecha

    def es_satisfecha_por(self, documento):
        return (self.__izquierda.es_satisfecha_por(documento)
                and self.__derecha.es_satisfecha_por(documento))

class EspecificacionO(Especificacion):

    def __init__(self, izquierda, derecha):
        self.__izquierda = izquierda
        self.__derecha = derecha

    def es_satisfecha_por(self, documento):
        return (self.__izquierda.es_satisfecha_por(documento)
                or self.__derecha.es_satisfecha_por(documento))

class EspecificacionDocumentoActivo(Especificacion):

    def es_satisfecha_por(self, documento):
        return documento.esta_activo()

class EspecificacionTipoSoportado(Especificacion):

    def __init__(self, tipos_soportados):
        self.__tipos_soportados = [
            tipo.lower() for tipo in tipos_soportados
        ]

    def es_satisfecha_por(self, documento):
        return documento.obtener_extension() in self.__tipos_soportados