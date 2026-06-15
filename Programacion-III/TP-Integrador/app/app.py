from models.analista import Analista

from models.nota import Nota

from repositories.sqlite_nota_repository import (
    SQLiteNotaRepository
)

from controllers.nota_controller import (
    NotaController
)


repo = SQLiteNotaRepository()

controller = NotaController(
    repo
)

autor = Analista(
    1,
    "Ana",
    "ana@mail.com",
    "123"
)

nota = Nota(
    "Dólar en alza",
    "Contenido...",
    "EMERGENTE",
    "VISIBLE",
    autor
)

controller.crear_nota(
    nota
)