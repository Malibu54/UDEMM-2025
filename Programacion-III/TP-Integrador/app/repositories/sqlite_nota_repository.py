import sqlite3

from repositories.nota_repository import NotaRepository


class SQLiteNotaRepository(NotaRepository):

    def __init__(self):

        self.conn = sqlite3.connect(
            "betatrade.db",
            check_same_thread=False
        )

    def guardar(self, nota):

        cursor = self.conn.cursor()

        cursor.execute(
            """
            INSERT INTO notas
            (
                titulo,
                contenido,
                categoria,
                visibilidad,
                fecha,
                hora,
                autor
            )
            VALUES
            (?, ?, ?, ?)
            """,
            (
                nota.titulo,
                nota.contenido,
                nota.categoria,
                nota.visibilidad,
                nota.fecha,
                nota.hora,
                nota.autor
            )
        )

        self.conn.commit()

    def actualizar(self, nota):
        pass

    def buscar_por_id(self, id):
        pass

    def obtener_todas(self):
        pass

    def eliminar(self, id):
        pass