from abc import ABC, abstractmethod

class Reporte:
    def __init__(self):
        self.titulo = " "
        self.encabezado = " "
        self.cuerpo = " "
        self.pie_pagina = " "

class ReporteBuilder (ABC):

    @abstractmethod
    def set_titulos(self,titulo):
        pass

    @abstractmethod
    def set_encabezado(self,encabezado):
        pass

    @abstractmethod
    def set_cuerpo(self,cuerpo):
        pass

    @abstractmethod
    def set_pie_pagina(self,pie_pagina):
        pass

    @abstractmethod
    def build(self):
        pass

class ReportePersonalizadoBuilder(ReporteBuilder):
    def __init__(self):
        self.reporte = Reporte()

    def set_titulo(self, titulo):
        self.reporte.titulo = titulo
        return self
    
    def set_cuerpo(self, cuerpo):
        self.reporte.cuerpo = cuerpo
        return self
    
    def set_pie_pagina(self, pie_pagina):
        self.reporte.pie_pagina = pie_pagina
        return self
    
    def build(self):
        return self.reporte
    
class Director:
    def construir_reporte_basico(self, builder: ReporteBuilder):
        return(
            builder
            .set_titulo("Reporte Basico")
            .set_cuerpo("Contenido del reporte")
            .build()
        )
