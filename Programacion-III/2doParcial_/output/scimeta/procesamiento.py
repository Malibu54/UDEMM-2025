from abc import ABC, abstractmethod

class ResultadoProcesamiento:
 
    def __init__(self, id_documento, titulo, resumen, likes,
                 fecha_publicacion, autores):
        self.id_documento = id_documento
        self.titulo = titulo
        self.resumen = resumen
        self.likes = likes
        self.fecha_publicacion = fecha_publicacion
        self.autores = list(autores)

    def __repr__(self):
        return (f"ResultadoProcesamiento(id={self.id_documento}, "
                f"titulo={self.titulo!r})")

class ParserDocumento(ABC):

    @abstractmethod
    def procesar(self, documento):
        raise NotImplementedError

class ParserPDF(ParserDocumento):
    def procesar(self, documento):
        resumen_extraido = (
            documento.resumen
            or "Resumen simulado extraido de archivo PDF."
        )
        return ResultadoProcesamiento(
            id_documento=documento.id,
            titulo=documento.titulo,
            resumen=resumen_extraido,
            likes=documento.likes,
            fecha_publicacion=documento.fecha_publicacion,
            autores=documento.autores,
        )

class ParserDOC(ParserDocumento):

    def procesar(self, documento):
        resumen_extraido = (
            documento.resumen
            or "Resumen simulado extraido de archivo DOC."
        )
        return ResultadoProcesamiento(
            id_documento=documento.id,
            titulo=documento.titulo,
            resumen=resumen_extraido,
            likes=documento.likes,
            fecha_publicacion=documento.fecha_publicacion,
            autores=documento.autores,
        )

class ParserTXT(ParserDocumento):

    def procesar(self, documento):
        resumen_extraido = (
            documento.resumen
            or "Resumen simulado extraido de archivo TXT."
        )
        return ResultadoProcesamiento(
            id_documento=documento.id,
            titulo=documento.titulo,
            resumen=resumen_extraido,
            likes=documento.likes,
            fecha_publicacion=documento.fecha_publicacion,
            autores=documento.autores,
        )

class FabricaParsers:

    __parsers_registrados = {}

    @classmethod
    def registrar(cls, extension, clase_parser):
        cls.__parsers_registrados[extension.lower()] = clase_parser

    @classmethod
    def tipos_soportados(cls):
        return list(cls.__parsers_registrados.keys())

    @classmethod
    def obtener_parser(cls, extension):
        clase_parser = cls.__parsers_registrados.get(
            extension.lower())
        if clase_parser is None:
            raise ValueError(
                f"No existe parser registrado para '{extension}'.")
        return clase_parser()

FabricaParsers.registrar(".pdf", ParserPDF)
FabricaParsers.registrar(".doc", ParserDOC)
FabricaParsers.registrar(".txt", ParserTXT)