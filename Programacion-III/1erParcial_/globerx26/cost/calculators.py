"""
cost/calculators.py
====================
Patrón: TEMPLATE METHOD (GoF - Behavioral)

Problema que resuelve:
    El algoritmo de cálculo de costo es idéntico para todas las regiones
    (base → factor regional → payload), pero el factor específico varía.
    Sin este patrón, habría condicionales (if region == "latam": ...) en
    el algoritmo, violando OCP: agregar "zona oriente" requeriría modificar
    el código existente.

Solución:
    CostCalculator define el algoritmo en calculate() (método template).
    La parte que varía (regional_factor) es abstracta: cada subclase
    la implementa con su valor específico.

    Para agregar "zona oriente" solo se crea OrienteCalculator con su factor.
    El algoritmo de calculate() no se toca jamás.

Nota sobre get_sizeoff:
    Se usa la función externa del módulo prize_by_payload.
    El payload_bytes ya viene precalculado en MonitoringReport,
    por lo que CostCalculator solo lo usa como entrada, sin
    recalcularlo (Single Responsibility).
"""

from __future__ import annotations

from abc import ABC, abstractmethod

from domain.entities import MonitoringReport, OperationCost

BASE_RATE = 120       # valor base por cada 10 peticiones
REQUESTS_PER_UNIT = 10


class CostCalculator(ABC):
    """
    Calculadora de costos de operación.

    Define el algoritmo estándar en calculate() (Template Method).
    Las subclases implementan únicamente regional_factor().

    Algoritmo:
        1. base_price     = (requests / 10) × 120
        2. regional_extra = base_price × regional_factor()
        3. payload_cost   = payload_bytes (peso del payload en bytes)
        4. total          = base_price + regional_extra + payload_cost
    """

    @property
    @abstractmethod
    def region_name(self) -> str:
        """Nombre de la región (para el reporte)."""
        ...

    @abstractmethod
    def regional_factor(self) -> float:
        """
        Factor multiplicador regional sobre el precio base.
        Ej: 0.35 para LATAM, 0.26 para Europa.
        """
        ...

    def calculate(self, report: MonitoringReport) -> OperationCost:
        """
        Método template: ejecuta el algoritmo completo de cálculo.

        Este método NO debe ser sobreescrito por las subclases.
        Solo regional_factor() y region_name varían.
        """
        base_price = (report.request_count / REQUESTS_PER_UNIT) * BASE_RATE
        regional_extra = base_price * self.regional_factor()
        payload_cost = float(report.payload_bytes)

        return OperationCost(
            region=self.region_name,
            base_price=round(base_price, 2),
            regional_extra=round(regional_extra, 2),
            payload_cost=round(payload_cost, 2),
        )


# ──────────────────────────────────────────────────────────────────────────────
# Implementaciones concretas — cada una solo define su factor y nombre
# ──────────────────────────────────────────────────────────────────────────────

class LatamCostCalculator(CostCalculator):
    """
    Calculadora para la región Latinoamérica.
    Factor: 35% adicional sobre el precio base.
    """

    @property
    def region_name(self) -> str:
        return "LATAM"

    def regional_factor(self) -> float:
        return 0.35


class EuropeCostCalculator(CostCalculator):
    """
    Calculadora para la región Europa.
    Factor: 26% adicional sobre el precio base.
    """

    @property
    def region_name(self) -> str:
        return "Europa"

    def regional_factor(self) -> float:
        return 0.27


# ──────────────────────────────────────────────────────────────────────────────
# Agregar "Zona Oriente" en el futuro es tan simple como esto:
# ──────────────────────────────────────────────────────────────────────────────
# class OrienteCostCalculator(CostCalculator):
#     @property
#     def region_name(self) -> str:
#         return "Zona Oriente"
#
#     def regional_factor(self) -> float:
#         return 0.18   # factor a definir por el negocio


# Registro de calculadoras por nombre de región
# Permite instanciar la calculadora correcta en tiempo de ejecución
CALCULATORS: dict[str, type[CostCalculator]] = {
    "latam": LatamCostCalculator,
    "europa": EuropeCostCalculator,
}


def get_calculator(region: str) -> CostCalculator:
    """
    Retorna la calculadora de costo para la región indicada.

    Args:
        region: Nombre de la región (case-insensitive).

    Raises:
        KeyError: Si la región no está registrada.
    """
    key = region.strip().lower()
    calculator_class = CALCULATORS.get(key)
    if calculator_class is None:
        available = list(CALCULATORS.keys())
        raise KeyError(
            f"Región no registrada: '{region}'. Disponibles: {available}"
        )
    return calculator_class()