from services.exportacion.exportador import (
    Exportador
)


class ExportadorPDF(
    Exportador
):

    def generar_salida(
        self,
        datos
    ):

        with open(
            "reporte.pdf",
            "w",
            encoding="utf-8"
        ) as archivo:

            for nota in datos:

                archivo.write(
                    f"{nota.titulo}\n"
                )

        return "reporte.pdf"