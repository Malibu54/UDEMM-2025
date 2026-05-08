"""
reports/strategies.py
======================
Patrón: STRATEGY (GoF - Behavioral)

Problema que resuelve:
    El sistema debe generar reportes en tres formatos distintos (PDF, TXT, Markdown)
    y el formato se elige en tiempo de ejecución según preferencia del usuario.
    Sin Strategy, habría un método con condicionales (if fmt == "pdf": ...)
    que crece cada vez que se agrega un formato, violando OCP.

Solución:
    - IReportStrategy define la interfaz generate(report) → str.
    - Cada estrategia concreta encapsula la lógica de formateo.
    - ReportGenerator recibe la estrategia en construcción o vía set_strategy()
      y la delega sin conocer sus detalles.
    - Agregar Markdown nuevo o HTML en el futuro: crear clase, registrar, listo.

Nota sobre "PDF":
    En una implementación real se usaría una librería como reportlab o weasyprint.
    Aquí la estrategia genera el contenido estructurado que iría al PDF,
    representado como string para mantener el ejemplo autocontenido
    y demostrar el patrón sin dependencias externas.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from datetime import datetime
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from domain.entities import MonitoringReport


# ──────────────────────────────────────────────────────────────────────────────
# Interfaz — Strategy
# ──────────────────────────────────────────────────────────────────────────────

class IReportStrategy(ABC):
    """
    Interfaz de estrategia de generación de reportes.

    Contrato: dada una entidad MonitoringReport, produce su representación
    en el formato específico de la estrategia.
    """

    @abstractmethod
    def generate(self, report: "MonitoringReport") -> str:
        """Genera el reporte en el formato propio de la estrategia."""
        ...

    @property
    @abstractmethod
    def format_name(self) -> str:
        """Nombre del formato (para logging y diagnóstico)."""
        ...


# ──────────────────────────────────────────────────────────────────────────────
# Estrategias concretas
# ──────────────────────────────────────────────────────────────────────────────

class PlainTextStrategy(IReportStrategy):
    """Genera el reporte como texto plano estructurado (.txt)."""

    @property
    def format_name(self) -> str:
        return "TXT"

    def generate(self, report: "MonitoringReport") -> str:
        lines = [
            "=" * 60,
            f"  REPORTE DE MONITOREO — {report.report_date}",
            "=" * 60,
            f"Servicios monitoreados : {len(report.statuses)}",
            f"Servicios disponibles  : {report.healthy_count}",
            f"Servicios con error    : {report.failed_count}",
            f"Peticiones totales     : {report.request_count}",
            f"Peso del payload       : {report.payload_bytes} bytes",
            "-" * 60,
        ]
        for status in report.statuses:
            estado = "OK" if status.is_healthy else "ERROR"
            error_info = f" | {status.error}" if status.error else ""
            lines.append(
                f"[{estado}] {status.provider:<16} "
                f"latencia: {status.latency_ms:>7.1f}ms{error_info}"
            )
        lines.append("=" * 60)
        return "\n".join(lines)


class MarkdownStrategy(IReportStrategy):
    """Genera el reporte en formato Markdown (.md)."""

    @property
    def format_name(self) -> str:
        return "Markdown"

    def generate(self, report: "MonitoringReport") -> str:
        lines = [
            f"# Reporte de Monitoreo — {report.report_date}",
            "",
            "## Resumen",
            "",
            f"| Métrica | Valor |",
            f"|---|---|",
            f"| Servicios monitoreados | {len(report.statuses)} |",
            f"| Disponibles | {report.healthy_count} |",
            f"| Con error | {report.failed_count} |",
            f"| Peticiones totales | {report.request_count} |",
            f"| Peso del payload | {report.payload_bytes} bytes |",
            "",
            "## Detalle por proveedor",
            "",
            "| Proveedor | Estado | Latencia (ms) | Observaciones |",
            "|---|---|---|---|",
        ]
        for status in report.statuses:
            estado = "✅ Disponible" if status.is_healthy else "❌ Error"
            obs = status.error or "—"
            lines.append(
                f"| {status.provider} | {estado} | {status.latency_ms:.1f} | {obs} |"
            )
        lines.append("")
        lines.append(
            f"*Generado el {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*"
        )
        return "\n".join(lines)


class PdfStrategy(IReportStrategy):
    """
    Genera la representación estructurada del reporte para PDF.

    En producción, este método construiría el PDF usando reportlab o weasyprint.
    El string retornado representa el contenido que se pasaría al motor PDF.
    """

    @property
    def format_name(self) -> str:
        return "PDF"

    def generate(self, report: "MonitoringReport") -> str:
        # En producción: usar reportlab.platypus o weasyprint
        # Aquí retornamos la estructura de contenido como string descriptivo
        sections = [
            "[PDF] REPORTE DE MONITOREO",
            f"[HEADER] Fecha: {report.report_date}",
            "[SECTION] Resumen Ejecutivo",
            f"  Servicios totales  : {len(report.statuses)}",
            f"  Disponibilidad     : {report.healthy_count}/{len(report.statuses)}",
            f"  Peticiones         : {report.request_count}",
            f"  Payload            : {report.payload_bytes} bytes",
            "[SECTION] Detalle de Servicios",
        ]
        for status in report.statuses:
            icon = "[V]" if status.is_healthy else "[X]"
            sections.append(
                f"  {icon} {status.provider} — {status.latency_ms:.1f}ms"
                + (f" — ERROR: {status.error}" if status.error else "")
            )
        sections.append("[FOOTER] GloberX26 Monitoring System")
        return "\n".join(sections)


# ──────────────────────────────────────────────────────────────────────────────
# ReportGenerator — Context del patrón Strategy
# ──────────────────────────────────────────────────────────────────────────────

class ReportGenerator:
    """
    Contexto del patrón Strategy para generación de reportes.

    Delega completamente la generación a la estrategia activa.
    No conoce los detalles de ningún formato.
    La estrategia puede cambiarse en tiempo de ejecución mediante set_strategy().
    """

    def __init__(self, strategy: IReportStrategy) -> None:
        self._strategy = strategy

    def set_strategy(self, strategy: IReportStrategy) -> None:
        """Permite cambiar el formato en tiempo de ejecución."""
        self._strategy = strategy

    def generate(self, report: "MonitoringReport") -> str:
        """Genera el reporte usando la estrategia activa."""
        return self._strategy.generate(report)

    @property
    def current_format(self) -> str:
        return self._strategy.format_name


# Registro de estrategias disponibles (extensible sin modificar el sistema)
REPORT_STRATEGIES: dict[str, type[IReportStrategy]] = {
    "txt": PlainTextStrategy,
    "md": MarkdownStrategy,
    "pdf": PdfStrategy,
}


def get_strategy(fmt: str) -> IReportStrategy:
    """
    Retorna la estrategia de reporte para el formato solicitado.

    Args:
        fmt: Formato del reporte ("txt", "md", "pdf").

    Raises:
        KeyError: Si el formato no está registrado.
    """
    key = fmt.strip().lower()
    strategy_class = REPORT_STRATEGIES.get(key)
    if strategy_class is None:
        available = list(REPORT_STRATEGIES.keys())
        raise KeyError(
            f"Formato no soportado: '{fmt}'. Disponibles: {available}"
        )
    return strategy_class()