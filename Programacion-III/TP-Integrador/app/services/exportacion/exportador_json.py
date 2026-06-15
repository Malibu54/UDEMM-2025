import json

from services.exportacion.exportador import (
    Exportador
)


class ExportadorJSON(
    Exportador
):

    def generar_salida(
        self,
        datos
    ):

        contenido = []

        for nota in datos:

            contenido.append(
                {
                    "titulo":
                        nota.titulo,

                    "categoria":
                        nota.categoria
                }
            )

        with open(
            "reporte.json",
            "w",
            encoding="utf-8"
        ) as archivo:

            json.dump(
                contenido,
                archivo,
                indent=4,
                ensure_ascii=False
            )

        return "reporte.json"