"""
domain/entities.py
==================
Entidades del dominio de GloberX26.

Las entidades son objetos de valor puro (value objects / dataclasses).
No tienen dependencias externas ni conocen cómo se obtienen o persisten los datos.
Esto respeta el principio de separación de responsabilidades y permite que el dominio
sea estable ante cambios en infraestructura, formatos o proveedores.
"""

from __future__ import annotations
from dataclasses import dataclass, field
from datetime import date, datetime
from typing import List


@dataclass(frozen=True)
class ServiceStatus:
    """
    Estado puntual de un servicio en un instante dado.

    Es inmutable (frozen=True) porque un estado ya registrado no debe cambiar.
    Representa el resultado normalizado que cualquier adaptador debe producir,
    independientemente del proveedor origen.

    Atributos:
        provider    -- nombre del proveedor que originó el dato (ej: "WebAPI")
        available   -- True si el servicio respondió correctamente
        latency_ms  -- latencia de respuesta en milisegundos
        timestamp   -- momento en que se capturó el estado
        error       -- mensaje de error si el proveedor falló (None si todo OK)
    """
    provider: str
    available: bool
    latency_ms: float
    timestamp: datetime
    error: str | None = None

    @property
    def is_healthy(self) -> bool:
        """Conveniente para condicionales de negocio."""
        return self.available and self.error is None


@dataclass
class MonitoringReport:
    """
    Reporte diario que agrega los estados de todos los proveedores activos.

    Es mutable porque se construye incrementalmente a medida que llegan
    los resultados de cada adaptador.

    Atributos:
        report_date    -- fecha del reporte
        statuses       -- lista de ServiceStatus recolectados
        request_count  -- cantidad total de peticiones realizadas al sistema
        payload_bytes  -- peso total del payload en bytes (para cálculo de costos)
    """
    report_date: date
    statuses: List[ServiceStatus] = field(default_factory=list)
    request_count: int = 0
    payload_bytes: int = 0

    def add_status(self, status: ServiceStatus) -> None:
        self.statuses.append(status)

    @property
    def healthy_count(self) -> int:
        return sum(1 for s in self.statuses if s.is_healthy)

    @property
    def failed_count(self) -> int:
        return len(self.statuses) - self.healthy_count


@dataclass(frozen=True)
class OperationCost:
    """
    Costo calculado de una operación, desglosado por componente.

    Inmutable porque un costo ya calculado es un registro contable.

    Atributos:
        region         -- región donde se ejecutó la operación
        base_price     -- precio base = (requests / 10) × 120
        regional_extra -- recargo regional aplicado sobre el precio base
        payload_cost   -- costo adicional por peso del payload
        total          -- suma de todos los componentes
    """
    region: str
    base_price: float
    regional_extra: float
    payload_cost: float

    @property
    def total(self) -> float:
        return self.base_price + self.regional_extra + self.payload_cost