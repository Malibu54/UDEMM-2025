import unittest

from services.factories.gerente_factory import (
    GerenteFactory
)


class TestFactory(unittest.TestCase):

    def test_crear_gerente(self):

        factory = GerenteFactory()

        gerente = factory.crear_usuario(
            1,
            "Juan",
            "juan@mail.com",
            "123"
        )

        self.assertEqual(
            gerente.__class__.__name__,
            "Gerente"
        )