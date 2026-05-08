"""
main.py
========
Punto de entrada del sistema GloberX26.

Demuestra los tres casos de uso principales:
    UC1: Obtener estado unificado de todos los proveedores
    UC2: Calcular costo de operación por región
    UC3: Generar reporte diario en el formato elegido por el usuario

La función run() orquesta el flujo sin conocer los detalles de
ningún adaptador, calculadora ni estrategia de reporte.
El código principal es estable: los cambios futuros se realizan
en las estrategias, adaptadores o calculadoras, no aquí.
"""

from __future__ import annotations

import logging
import sys

from adapters.adapter_factory import AdapterFactory
from adapters.monitoring_system import MonitoringSystem
from config.settings import SystemConfig
from cost.calculators import get_calculator
from reports.strategies import ReportGenerator, get_strategy


def setup_logging(level: str) -> None:
    logging.basicConfig(
        level=getattr(logging, level.upper(), logging.INFO),
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        datefmt="%H:%M:%S",
    )


def run(report_format: str = "txt", region: str | None = None) -> None:
    """
    Ejecuta el ciclo completo del sistema:
        1. Carga configuración
        2. Construye adaptadores activos
        3. Recolecta estados (UC1)
        4. Calcula costo de operación (UC2)
        5. Genera reporte en el formato indicado (UC3)

    Args:
        report_format: Formato del reporte ("txt", "md", "pdf")
        region: Región para el cálculo de costos (None usa la del config)
    """
    # ── 1. Cargar configuración ────────────────────────────────────────────────
    config = SystemConfig.load()
    setup_logging(config.log_level)
    logger = logging.getLogger(__name__)

    logger.info("GloberX26 iniciado — región: %s, formato: %s",
                config.default_region, report_format)

    # ── 2. Construir adaptadores activos ──────────────────────────────────────
    try:
        adapters = AdapterFactory.create_all(config.providers)
    except KeyError as exc:
        logger.error("Error de configuración de adaptadores: %s", exc)
        sys.exit(1)

    if not adapters:
        logger.error("No hay adaptadores activos en la configuración.")
        sys.exit(1)

    logger.info("Adaptadores activos: %s", [a.provider_name for a in adapters])

    # ── UC1: Recolectar estados unificados ────────────────────────────────────
    system = MonitoringSystem(adapters)
    report = system.build_report(request_count=30)

    print(f"\n{'─' * 50}")
    print(f"  Recolección completada: {len(report.statuses)} proveedores")
    print(f"  Disponibles: {report.healthy_count} | Errores: {report.failed_count}")
    print(f"{'─' * 50}\n")

    # ── UC2: Calcular costo de operación ──────────────────────────────────────
    effective_region = region or config.default_region
    try:
        calculator = get_calculator(effective_region)
        cost = calculator.calculate(report)
    except KeyError as exc:
        logger.error("Error de región: %s", exc)
        sys.exit(1)

    print(f"COSTO DE OPERACIÓN ({cost.region})")
    print(f"  Precio base     : $ {cost.base_price:>8.2f}")
    print(f"  Extra regional  : $ {cost.regional_extra:>8.2f}")
    print(f"  Costo payload   : $ {cost.payload_cost:>8.2f}")
    print(f"  {'─' * 30}")
    print(f"  TOTAL           : $ {cost.total:>8.2f}")
    print()

    # ── UC3: Generar reporte diario ───────────────────────────────────────────
    try:
        strategy = get_strategy(report_format)
    except KeyError as exc:
        logger.error("Formato no soportado: %s", exc)
        sys.exit(1)

    generator = ReportGenerator(strategy)
    output = generator.generate(report)

    print(f"REPORTE ({generator.current_format})")
    print(output)


if __name__ == "__main__":
    # El formato se selecciona en tiempo de ejecución
    # Uso: python main.py [txt|md|pdf] [latam|europa]
    fmt = sys.argv[1] if len(sys.argv) > 1 else "txt"
    reg = sys.argv[2] if len(sys.argv) > 2 else None
    run(report_format=fmt, region=reg)