import unittest

from services.filtros.filtro_categoria import FiltroCategoria


class TestFiltros(unittest.TestCase):

    def test_filtrar_categoria(self):

        filtro = FiltroCategoria(
            "EMERGENTE"
        )

        self.assertEqual(
            filtro.categoria,
            "EMERGENTE"
        )