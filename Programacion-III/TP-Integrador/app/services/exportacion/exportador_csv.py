import csv

from services.exportacion.exportador import (
    Exportador
)


class ExportadorCSV(
    Exportador
):

    def generar_salida(
        self,
        datos
    ):

        with open(
            "reporte.csv",
            "w",
            newline="",
            encoding="utf-8"
        ) as archivo:

            writer = csv.writer(
                archivo
            )

            writer.writerow(
                [
                    "titulo",
                    "categoria"
                ]
            )

            for nota in datos:

                writer.writerow(
                    [
                        nota.titulo,
                        nota.categoria
                    ]
                )

        return "reporte.csv"