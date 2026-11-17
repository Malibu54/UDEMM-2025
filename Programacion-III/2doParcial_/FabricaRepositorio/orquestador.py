from output.scimeta.procesamiento import FabricaParsers
from prompt_builder import ConstructorPrompt

class ServicioOrquestacion:

    def __init__(self, repositorio_resultados, especificacion_validacion):
        self.__repositorio = repositorio_resultados
        self.__especificacion = especificacion_validacion

    def procesar_documento(self, documento):
        if not self.__especificacion.es_satisfecha_por(documento):
            raise ValueError(
                "El documento no cumple las condiciones necesarias "
                "para ser procesado (debe estar activo y ser de un "
                "tipo de archivo soportado).")

        extension = documento.obtener_extension()
        parser = FabricaParsers.obtener_parser(extension)

        resultado = parser.procesar(documento)

        self.__repositorio.guardar(resultado)
        return resultado

    def generar_prompt_para(self, id_documento):

        resultado = self.__repositorio.buscar_por_id_documento(
            id_documento)
        if resultado is None:
            raise ValueError(
                f"No existe un resultado procesado para el "
                f"documento {id_documento}.")
        return ConstructorPrompt.desde_resultado(resultado)