from abc import ABC, abstractmethod

# ──────────────────────────────────────────────
# ABSTRACCIÓN (interfaz de alto nivel)
# ──────────────────────────────────────────────

class EstrategiaPO (ABC):
    
    @abstractmethod
    def calcular(self, monto:float) -> float:
        ...

# ──────────────────────────────────────────────
# IMPLEMENTACIONES CONCRETAS
# ──────────────────────────────────────────────

class POEstandar (EstrategiaPO):

    TASA = 0.05

    def calcular(self, monto:float) -> float:
        return monto * self.TASA
    
class POImpuestoExterno(EstrategiaPO):

    UMBRAL_ALTO = 10_000_000
    UMBRAL_MEDIO = 1_000_000
    TASA_ALTA = 0.35
    TASA_MEDIA = 0.25
    TASA_BASE = 0.13

    def calcular(self, monto:float) -> float:
        if monto > self.UMBRAL_ALTO:
            return monto * self.TASA_ALTA
        if monto > self.UMBRAL_MEDIO:
            return monto * self.TASA_MEDIA
        return monto* self.TASA_BASE    

# Ejemplo de extensión futura sin tocar nada de lo anterior:

class POExentoONG(EstrategiaPO):

    def calcular (self,monto: float):
        return 0.0
    
class POImportacionLujo(EstrategiaPO):

    TASA = 0.42

    def calcular (self, monto: float) -> float:
        return monto * self.TASA
    
# ──────────────────────────────────────────────
# CLASE DE NEGOCIO (aislada de la economía)
# ──────────────────────────────────────────────

class Transaccion:

    def __init__(
            self,
            descripcion: str,
            motno: float,
            estrategia: EstrategiaPO,
    ) -> None:
        self.descripcion = descripcion
        self.monto = self.monto
        self._estrategia = estrategia
    
    def set_estrategia(self, estrategia:EstrategiaPO) -> None:
        self.estrategia = estrategia

    def calcular (self, monto:float) -> float:
        return self._estrategia.calcular (monto)
    
    def ejecutar(self) -> float:
        impuesto = self._estrategia.calcular(self.monto)
        total = self.monto + impuesto
        print(

            f"[{self.descripcion}]\n"
            f"  Monto base : {self.monto:>15,.2f}\n"
            f"  Impuesto   : {impuesto:>15,.2f}\n"
            f"  Total      : {total:>15,.2f}\n"

        )
        return total

