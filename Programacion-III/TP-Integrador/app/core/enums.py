from enum import Enum

class CategoriaNota(Enum):

    RELEVANTE = "RELEVANTE"

    NEUTRAL = "NEUTRAL"

    EMERGENTE = "EMERGENTE"

    DEPRECATED = "DEPRECATED"


class Visibilidad(Enum):

    VISIBLE = "VISIBLE"

    OCULTO = "OCULTO"