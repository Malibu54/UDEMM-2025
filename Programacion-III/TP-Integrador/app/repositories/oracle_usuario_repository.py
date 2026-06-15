import oracledb

from repositories.usuario_repository import (
    UsuarioRepository
)


class OracleUsuarioRepository(
    UsuarioRepository
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
        usuario
    ):

        cursor = self.connection.cursor()

        cursor.execute(
            """
            INSERT INTO USUARIOS
            (
                NOMBRE,
                EMAIL,
                PASSWORD_HASH
            )
            VALUES
            (
                :1,
                :2,
                :3
            )
            """,
            (
                usuario.nombre,
                usuario.email,
                usuario.password_hash
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
            FROM USUARIOS
            WHERE ID = :1
            """,
            (id,)
        )

        return cursor.fetchone()

    def obtener_todos(
        self
    ):

        cursor = self.connection.cursor()

        cursor.execute(
            """
            SELECT *
            FROM USUARIOS
            """
        )

        return cursor.fetchall()