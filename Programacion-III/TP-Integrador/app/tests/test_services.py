import unittest

from services.nota_service import (
    NotaService
)


class FakeRepository:

    def guardar(
        self,
        nota
    ):
        return nota


class FakePublisher:

    def notificar(
        self,
        nota
    ):
        pass


class TestNotaService(
    unittest.TestCase
):

    def test_crear_nota(self):

        service = NotaService(
            FakeRepository(),
            FakePublisher()
        )

        self.assertIsNotNone(
            service
        )