class ConstructorPrompt:

    ENCABEZADO = "ANÁLISIS DE DOCUMENTO ACADÉMICO\n\n"
    INSTRUCCION_FINAL = "\nInstrucción: Analiza el resumen anterior.\n"

    def __init__(self):
        self.__partes = [self.ENCABEZADO]

    def con_titulo(self, titulo):
        self.__partes.append(f"TÍTULO: {titulo}\n")
        return self

    def con_id(self, id_documento):
        self.__partes.append(f"ID: {id_documento}\n")
        return self

    def con_likes(self, likes):
        self.__partes.append(f"LIKES: {likes}\n")
        return self

    def con_fecha_publicacion(self, fecha_publicacion):
        self.__partes.append(
            f"FECHA PUBLICACION: {fecha_publicacion}\n")
        return self

    def con_autores(self, autores):
        nombres = ", ".join(
            autor.nombre_completo() for autor in autores)
        self.__partes.append(f"AUTORES: {nombres}\n")
        return self

    def con_resumen(self, resumen):
        self.__partes.append(f"\n\nRESUMEN:\n{resumen}\n")
        return self

    def construir(self):
        self.__partes.append(self.INSTRUCCION_FINAL)
        return "".join(self.__partes)

    @staticmethod
    def desde_resultado(resultado):

        return (
            ConstructorPrompt()
            .con_titulo(resultado.titulo)
            .con_id(resultado.id_documento)
            .con_likes(resultado.likes)
            .con_fecha_publicacion(resultado.fecha_publicacion)
            .con_autores(resultado.autores)
            .con_resumen(resultado.resumen)
            .construir()
        )
