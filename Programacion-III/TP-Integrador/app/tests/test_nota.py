import unittest

from models.nota import Nota


class TestNota(unittest.TestCase):

    def test_no_deprecated_sin_revision(self):

        nota = Nota(
            "Titulo",
            "Contenido",
            "RELEVANTE",
            "VISIBLE",
            None
        )

        with self.assertRaises(
            Exception
        ):

            nota.marcar_deprecated()