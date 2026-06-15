from dtos import nota_dto

class NotaController:

    def __init__(
        self,
        nota_service
    ):
        self.nota_service = nota_service

    def crear_nota(
        self,
        nota
    ):

        nota = self.nota_service.crear_nota(
            nota
        )

        return nota_dto.from_nota(
            nota
        )