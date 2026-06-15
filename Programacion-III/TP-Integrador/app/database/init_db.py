import sqlite3

conn = sqlite3.connect("betatrade.db")

cursor = conn.cursor()

cursor.execute(
    """
    CREATE TABLE IF NOT EXISTS usuarios
    (
        id INTEGER PRIMARY KEY AUTOINCREMENT,

        nombre TEXT NOT NULL,

        email TEXT NOT NULL,

        password_hash TEXT NOT NULL
    )
    """
)

cursor.execute(
    """
    CREATE TABLE IF NOT EXISTS notas
    (
        id INTEGER PRIMARY KEY AUTOINCREMENT,

        titulo TEXT NOT NULL,

        contenido TEXT NOT NULL,

        categoria TEXT NOT NULL,

        visibilidad TEXT NOT NULL
    )
    """
)

conn.commit()
conn.close()