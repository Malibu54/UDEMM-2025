''' import oracledb

from repositories.nota_repository import (
    NotaRepository
)

class OracleNotaRepository(
    NotaRepository
):

    def __init__(
        self,
        user,
        password,
        host,
        port,
        service_name
    ):

        self.connection = oracledb.connect(
            user=user,
            password=password,
            host=host,
            port=port,
            service_name=service_name
        )

    def guardar(
        self,
        nota
    ):

        cursor = self.connection.cursor()

        cursor.execute(
            """
            INSERT INTO NOTAS
            (
                TITULO,
                CONTENIDO,
                CATEGORIA,
                VISIBILIDAD,
                FECHA_PUBLICACION
            )
            VALUES
            (
                :1,
                :2,
                :3,
                :4,
                :5
            )
            """,
            (
                nota.titulo,
                nota.contenido,
                nota.categoria,
                nota.visibilidad,
                nota.fecha_publicacion
            )
        )

        self.connection.commit()

    def actualizar(
        self,
        nota
    ):

        cursor = self.connection.cursor()

        cursor.execute(
            """
            UPDATE NOTAS
            SET
                TITULO = :1,
                CONTENIDO = :2,
                CATEGORIA = :3,
                VISIBILIDAD = :4
            WHERE ID = :5
            """,
            (
                nota.titulo,
                nota.contenido,
                nota.categoria,
                nota.visibilidad,
                nota.id
            )
        )

        self.connection.commit()

    def buscar_por_id(
        self,
        id
    ):

        cursor = self.connection.cursor()

        cursor.execute(
            """
            SELECT *
            FROM NOTAS
            WHERE ID = :1
            """,
            (id,)
        )

        return cursor.fetchone()

    def obtener_todas(
        self
    ):

        cursor = self.connection.cursor()

        cursor.execute(
            """
            SELECT *
            FROM NOTAS
            """
        )

        return cursor.fetchall()

    def eliminar(
        self,
        id
    ):

        cursor = self.connection.cursor()

        cursor.execute(
            """
            DELETE FROM NOTAS
            WHERE ID = :1
            """,
            (id,)
        )

        self.connection.commit()'''