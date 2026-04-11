from abc import ABC, abstractmethod
from datetime import datetime

class Document (ABC):
    """Interfaz comun para todos los tipos de documento."""

    def __init__(self, title:str, content:str):
        self.title = title
        self.content = content
        self.created_at = datetime.now().strftime("%Y-%m-%d %H:%M")

    @abstractmethod
    def render(self) -> str:
        """Devuelve una representacion del documento listo para mostrar."""
        ...

    @abstractmethod
    def save(self, path:str) -> None:
        """Persiste el documento en el disco."""
        ...
    
    def __repr__(self):
        return f"<{self.__class__.__name__} title'{self.title}'>"