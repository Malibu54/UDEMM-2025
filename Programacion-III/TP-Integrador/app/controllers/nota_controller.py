from dtos.nota_dto import NotaDTO

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

        return NotaDTO.from_nota(
            nota
        )