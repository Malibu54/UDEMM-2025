"""
adapters/monitoring_system.py
==============================
MonitoringSystem: orquestador de recolección de datos.

Responsabilidades:
    - Iterar sobre los adaptadores activos
    - Llamar a obtener_estado() en cada uno de forma resiliente
    - Construir el MonitoringReport con todos los resultados
    - Registrar el peso del payload usando get_sizeoff() del módulo externo

El sistema no conoce los detalles de ningún proveedor: solo habla
con IMonitorAdapter. Esto es el beneficio central del patrón Adapter.
"""

from __future__ import annotations

import logging
from datetime import date, datetime
from typing import List

from adapters.monitor_adapters import IMonitorAdapter
from domain.entities import MonitoringReport, ServiceStatus

logger = logging.getLogger(__name__)


# Simula la función externa get_sizeoff del módulo prize_by_payload
# En producción: from prize_by_payload import get_sizeoff
def get_sizeoff(payload: str) -> int:
    """Retorna el peso del payload en bytes."""
    return len(payload.encode("utf-8"))


class MonitoringSystem:
    """
    Orquestador del sistema de monitoreo.

    Recibe una lista de adaptadores (inyección de dependencias) y
    los utiliza para recolectar estados. La lista puede cambiar en
    tiempo de ejecución sin modificar esta clase (OCP).

    La resiliencia está garantizada porque:
    - Cada adaptador ya captura sus propias excepciones internamente
    - MonitoringSystem agrega una capa extra por si el adaptador mismo falla
      de forma no anticipada (doble protección)
    """

    def __init__(self, adapters: List[IMonitorAdapter]) -> None:
        if not adapters:
            raise ValueError("Se requiere al menos un adaptador activo.")
        self._adapters = adapters

    def collect_all(self) -> List[ServiceStatus]:
        """
        Consulta todos los adaptadores activos y retorna sus estados.

        Si un adaptador falla de forma inesperada (no capturada por él mismo),
        se registra el error y se continúa con los demás. El sistema nunca
        se bloquea por el fallo de un proveedor individual.
        """
        results: List[ServiceStatus] = []
        for adapter in self._adapters:
            try:
                status = adapter.obtener_estado()
                results.append(status)
                if status.error:
                    logger.warning(
                        "Proveedor '%s' reportó error: %s",
                        status.provider,
                        status.error,
                    )
                else:
                    logger.info(
                        "Proveedor '%s': disponible=%s, latencia=%.1fms",
                        status.provider,
                        status.available,
                        status.latency_ms,
                    )
            except Exception as exc:
                # Capa de seguridad extra: si el adaptador mismo lanzó
                # una excepción no capturada, la contenemos aquí.
                logger.error(
                    "Error crítico en adaptador '%s': %s",
                    adapter.provider_name,
                    exc,
                )
                results.append(
                    ServiceStatus(
                        provider=adapter.provider_name,
                        available=False,
                        latency_ms=0.0,
                        timestamp=datetime.now(),
                        error=f"Error crítico: {exc}",
                    )
                )
        return results

    def build_report(self, request_count: int = 1) -> MonitoringReport:
        """
        Recolecta estados y construye el reporte diario.

        Args:
            request_count: Número de peticiones realizadas al sistema
                           en este ciclo (para cálculo de costos).
        """
        statuses = self.collect_all()
        # Serialización simple del payload para calcular su peso
        payload_text = str([
            {"provider": s.provider, "available": s.available, "latency": s.latency_ms}
            for s in statuses
        ])
        payload_bytes = get_sizeoff(payload_text)

        report = MonitoringReport(
            report_date=date.today(),
            request_count=request_count,
            payload_bytes=payload_bytes,
        )
        for status in statuses:
            report.add_status(status)

        return report