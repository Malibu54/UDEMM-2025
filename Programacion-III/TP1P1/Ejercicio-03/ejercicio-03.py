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
        ...

    @abstractmethod
    def save(self, path:str) -> None:
        ...
    
    def __repr__(self):
        return f"<{self.__class__.__name__} title'{self.title}'>"
    

class PDFDocument(Document):
    def __init__(self, title: str, content: str, compression: int = 5):
        super().__init__(title, content)
        self.compression = compression
        self.pages = max (1, len(content) // 500)

    def render(self) -> str:
        return(
            f"[PDF] {self.title}\n"
            f"Paginas:{self.pages} | Compresion: {self.compression}\n"
            f"Creado {self.created_at}\n"
            f"{'-' * 40}\n {self.content[:200]}\n"
        )
    
    def save (self, path: str) -> None:
        filename = f"{path}/{self.title.replace(' ', '_')}.pdf"
        print(f"GUardado PDF en: {filename}")


class DOCDocument(Document):
    def __init__(self, title: str, content: str, tenplate: str ="default"):
        super().__init__(title, content)
        self.template = self.templateself.styles = ["Normal", "Heading1","Heading2"]
    
    def render (self) -> str:
        return(
             f"[DOC] {self.title}\n"
            f"Plantillas:{self.template} | Estilos: {', '.jpin(self.styles)}\n"
            f"Creado {self.created_at}\n"
            f"{'-' * 40}\n {self.content[:200]}\n"
        )
    
    def save (self, path: str) -> None:
        filename = f"{path}/{self.title.replace(' ', '_')}.docx"
        print(f"GUardado DOC en: {filename}")


class TXTDocument(Document):
    def __init__(self, title: str, content: str, encoding: str ="utf-8"):
        super().__init__(title, content)
        self.encoding = encoding

    def render (self) -> str:
        return(
             f"[TXT] {self.title}\n"
            f"Enconding:{self.encoding}\n"
            f"Creado {self.created_at}\n"
            f"{'-' * 40}\n {self.content[:200]}\n"
        )
    
    def save (self, path: str) -> None:
        filename = f"{path}/{self.title.replace(' ', '_')}.txt"
        print(f"GUardado TXT en: {filename}")

class DocumentCreator(ABC):

    def __init__(self, office: str, author:str):
        self.office = office
        self.author = author

    @abstractmethod
    def create_document(self, title: str, content:str) -> Document:
        ...

    def generate_report(self, title: str, content:str, save_path:str = ".") -> None:
        print(f"\n{'='* 50 }")
        print(f"\Oficina:{self.office}")
        print(f"\Author:{self.author}")

        doc: Document = self.create_document(title, content)

        print(doc.render())
        doc.save(save_path)
        print(f"\n{'='* 50 }\n")



