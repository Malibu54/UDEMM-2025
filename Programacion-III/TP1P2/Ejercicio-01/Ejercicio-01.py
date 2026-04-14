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
    