import sqlite3

from repositories.usuario_repository import UsuarioRepository


class SQLiteUsuarioRepository(
    UsuarioRepository
):

    def __init__(self):

        self.conn = sqlite3.connect(
            "betatrade.db",
            check_same_thread=False
        )

    def guardar(self, usuario):

        cursor = self.conn.cursor()

        cursor.execute(
            """
            INSERT INTO usuarios
            (
                nombre,
                email,
                password_hash
            )
            VALUES
            (?, ?, ?)
            """,
            (
                usuario.nombre,
                usuario.email,
                usuario.password_hash
            )
        )

        self.conn.commit()

    def buscar_por_id(self, id):
        pass

    def obtener_todos(self):
        pass