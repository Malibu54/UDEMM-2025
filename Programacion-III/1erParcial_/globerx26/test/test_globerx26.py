"""
tests/test_globerx26.py
========================
Tests unitarios del sistema GloberX26.

Cubre:
    - Entidades de dominio
    - Cada adaptador (happy path y manejo de errores)
    - AdapterFactory con tipos válidos e inválidos
    - MonitoringSystem (resiliencia ante fallos)
    - Calculadoras (ejemplo del enunciado + ambas regiones)
    - Estrategias de reporte (los tres formatos)
    - Flujo end-to-end
"""

from __future__ import annotations

import sys
import os
import unittest
from datetime import date, datetime
from unittest.mock import MagicMock, patch

# Asegura que el directorio raíz esté en el path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from adapters.adapter_factory import AdapterFactory
from adapters.monitor_adapters import (
    ServerWatchAdapter,
    WebApiAdapter,
    WebIntegralAdapter,
)
from adapters.monitoring_system import MonitoringSystem
from cost.calculators import EuropeCostCalculator, LatamCostCalculator, get_calculator
from domain.entities import MonitoringReport, OperationCost, ServiceStatus
from reports.strategies import (
    MarkdownStrategy,
    PdfStrategy,
    PlainTextStrategy,
    ReportGenerator,
    get_strategy,
)


# ─────────────────────────────────────────────────────────────────────────────
# Helpers
# ─────────────────────────────────────────────────────────────────────────────

def make_status(provider="Test", available=True, latency=100.0, error=None):
    return ServiceStatus(
        provider=provider,
        available=available,
        latency_ms=latency,
        timestamp=datetime.now(),
        error=error,
    )


def make_report(request_count=30, payload_bytes=500, statuses=None):
    r = MonitoringReport(
        report_date=date.today(),
        request_count=request_count,
        payload_bytes=payload_bytes,
    )
    for s in (statuses or [make_status()]):
        r.add_status(s)
    return r


# ─────────────────────────────────────────────────────────────────────────────
# Tests: Entidades de dominio
# ─────────────────────────────────────────────────────────────────────────────

class TestServiceStatus(unittest.TestCase):

    def test_healthy_status(self):
        s = make_status(available=True, error=None)
        self.assertTrue(s.is_healthy)

    def test_unhealthy_when_error(self):
        s = make_status(available=False, error="Timeout")
        self.assertFalse(s.is_healthy)

    def test_immutable(self):
        s = make_status()
        with self.assertRaises(Exception):
            s.provider = "other"  # frozen=True


class TestMonitoringReport(unittest.TestCase):

    def test_healthy_count(self):
        r = make_report(statuses=[
            make_status(available=True),
            make_status(available=False, error="err"),
            make_status(available=True),
        ])
        self.assertEqual(r.healthy_count, 2)
        self.assertEqual(r.failed_count, 1)

    def test_add_status(self):
        r = MonitoringReport(report_date=date.today())
        self.assertEqual(len(r.statuses), 0)
        r.add_status(make_status())
        self.assertEqual(len(r.statuses), 1)


class TestOperationCost(unittest.TestCase):

    def test_total_property(self):
        cost = OperationCost(
            region="LATAM",
            base_price=360.0,
            regional_extra=126.0,
            payload_cost=500.0,
        )
        self.assertAlmostEqual(cost.total, 986.0)


# ─────────────────────────────────────────────────────────────────────────────
# Tests: Adaptadores
# ─────────────────────────────────────────────────────────────────────────────

class TestWebApiAdapter(unittest.TestCase):

    def test_happy_path(self):
        adapter = WebApiAdapter(service_id="svc-001")
        status = adapter.obtener_estado()
        self.assertEqual(status.provider, "WebAPI")
        self.assertTrue(status.available)
        self.assertIsNone(status.error)

    def test_handles_malformed_xml(self):
        adapter = WebApiAdapter(service_id="bad")
        with patch(
            "adapters.monitor_adapters._webapi_get_xml_data",
            return_value="<<invalid xml>>"
        ):
            status = adapter.obtener_estado()
        self.assertFalse(status.available)
        self.assertIsNotNone(status.error)
        self.assertIn("XML", status.error)

    def test_handles_timeout(self):
        adapter = WebApiAdapter(service_id="slow")
        with patch(
            "adapters.monitor_adapters._webapi_get_xml_data",
            side_effect=TimeoutError("connection timed out")
        ):
            status = adapter.obtener_estado()
        self.assertFalse(status.available)
        self.assertIn("Timeout", status.error)


class TestWebIntegralAdapter(unittest.TestCase):

    def test_happy_path(self):
        adapter = WebIntegralAdapter(credential={"user": "u", "token": "t"})
        status = adapter.obtener_estado()
        self.assertEqual(status.provider, "WebIntegral")
        self.assertTrue(status.available)

    def test_handles_invalid_credentials(self):
        adapter = WebIntegralAdapter(credential={"user": "u", "token": ""})
        status = adapter.obtener_estado()
        self.assertFalse(status.available)
        self.assertIn("Autenticación", status.error)


class TestServerWatchAdapter(unittest.TestCase):

    def test_happy_path_json(self):
        adapter = ServerWatchAdapter(preferred_format="json")
        status = adapter.obtener_estado()
        self.assertEqual(status.provider, "ServerWatch")
        self.assertTrue(status.available)

    def test_happy_path_xml(self):
        adapter = ServerWatchAdapter(preferred_format="xml")
        status = adapter.obtener_estado()
        self.assertTrue(status.available)

    def test_invalid_format_raises(self):
        with self.assertRaises(ValueError):
            ServerWatchAdapter(preferred_format="csv")

    def test_handles_error(self):
        adapter = ServerWatchAdapter(preferred_format="json")
        with patch(
            "adapters.monitor_adapters._serverwatch_get_all_server_status",
            side_effect=ConnectionError("network unreachable")
        ):
            status = adapter.obtener_estado()
        self.assertFalse(status.available)


# ─────────────────────────────────────────────────────────────────────────────
# Tests: AdapterFactory
# ─────────────────────────────────────────────────────────────────────────────

class TestAdapterFactory(unittest.TestCase):

    def test_creates_webapi(self):
        cfg = {"type": "webapi", "service_id": "x"}
        a = AdapterFactory.create(cfg)
        self.assertIsInstance(a, WebApiAdapter)

    def test_creates_webintegral(self):
        cfg = {"type": "webintegral", "user": "u", "token": "t"}
        a = AdapterFactory.create(cfg)
        self.assertIsInstance(a, WebIntegralAdapter)

    def test_creates_serverwatch(self):
        cfg = {"type": "serverwatch"}
        a = AdapterFactory.create(cfg)
        self.assertIsInstance(a, ServerWatchAdapter)

    def test_unknown_type_raises(self):
        with self.assertRaises(KeyError):
            AdapterFactory.create({"type": "unknown_provider"})

    def test_create_all_respects_enabled_flag(self):
        configs = [
            {"type": "webapi", "service_id": "x", "enabled": True},
            {"type": "serverwatch", "enabled": False},
        ]
        adapters = AdapterFactory.create_all(configs)
        self.assertEqual(len(adapters), 1)
        self.assertIsInstance(adapters[0], WebApiAdapter)


# ─────────────────────────────────────────────────────────────────────────────
# Tests: MonitoringSystem (resiliencia)
# ─────────────────────────────────────────────────────────────────────────────

class TestMonitoringSystem(unittest.TestCase):

    def test_collects_from_all_adapters(self):
        adapters = [
            WebApiAdapter("svc-1"),
            WebIntegralAdapter({"user": "u", "token": "t"}),
            ServerWatchAdapter("json"),
        ]
        system = MonitoringSystem(adapters)
        report = system.build_report(request_count=10)
        self.assertEqual(len(report.statuses), 3)

    def test_continues_when_adapter_raises(self):
        """Si un adaptador lanza excepción crítica, el sistema continúa."""
        good_adapter = WebApiAdapter("ok")
        bad_adapter = MagicMock()
        bad_adapter.provider_name = "BadProvider"
        bad_adapter.obtener_estado.side_effect = RuntimeError("boom")

        system = MonitoringSystem([good_adapter, bad_adapter])
        statuses = system.collect_all()

        self.assertEqual(len(statuses), 2)
        bad = next(s for s in statuses if s.provider == "BadProvider")
        self.assertFalse(bad.available)
        self.assertIsNotNone(bad.error)

    def test_requires_at_least_one_adapter(self):
        with self.assertRaises(ValueError):
            MonitoringSystem([])


# ─────────────────────────────────────────────────────────────────────────────
# Tests: Calculadoras de costo (Template Method)
# ─────────────────────────────────────────────────────────────────────────────

class TestCostCalculators(unittest.TestCase):

    def test_latam_example_from_spec(self):
        """
        Caso de ejemplo del enunciado:
            30 peticiones, 500 bytes de payload, región LATAM
            precio_base = (30/10) × 120 = 360
            extra       = 360 × 0.35   = 126
            total       = 360 + 126 + 500 = 986
        """
        report = make_report(request_count=30, payload_bytes=500)
        calc = LatamCostCalculator()
        cost = calc.calculate(report)

        self.assertAlmostEqual(cost.base_price, 360.0)
        self.assertAlmostEqual(cost.regional_extra, 126.0)
        self.assertAlmostEqual(cost.payload_cost, 500.0)
        self.assertAlmostEqual(cost.total, 986.0)

    def test_europe_calculation(self):
        report = make_report(request_count=10, payload_bytes=200)
        calc = EuropeCostCalculator()
        cost = calc.calculate(report)

        self.assertAlmostEqual(cost.base_price, 120.0)
        self.assertAlmostEqual(cost.regional_extra, 31.2)
        self.assertAlmostEqual(cost.total, 120.0 + 31.2 + 200.0)

    def test_get_calculator_case_insensitive(self):
        calc = get_calculator("LATAM")
        self.assertIsInstance(calc, LatamCostCalculator)

        calc2 = get_calculator("europa")
        self.assertIsInstance(calc2, EuropeCostCalculator)

    def test_unknown_region_raises(self):
        with self.assertRaises(KeyError):
            get_calculator("oriente")


# ─────────────────────────────────────────────────────────────────────────────
# Tests: Estrategias de reporte (Strategy)
# ─────────────────────────────────────────────────────────────────────────────

class TestReportStrategies(unittest.TestCase):

    def setUp(self):
        self.report = make_report(
            request_count=10,
            payload_bytes=300,
            statuses=[
                make_status("WebAPI", True, 142.0),
                make_status("WebIntegral", False, 0.0, error="Auth error"),
            ],
        )

    def test_plain_text_contains_key_info(self):
        output = PlainTextStrategy().generate(self.report)
        self.assertIn("WebAPI", output)
        self.assertIn("WebIntegral", output)
        self.assertIn("ERROR", output)
        self.assertIn("OK", output)

    def test_markdown_has_table(self):
        output = MarkdownStrategy().generate(self.report)
        self.assertIn("| Proveedor |", output)
        self.assertIn("WebAPI", output)
        self.assertIn("Auth error", output)

    def test_pdf_strategy_generates(self):
        output = PdfStrategy().generate(self.report)
        self.assertIn("[PDF]", output)
        self.assertIn("WebAPI", output)

    def test_report_generator_delegates(self):
        gen = ReportGenerator(PlainTextStrategy())
        self.assertEqual(gen.current_format, "TXT")
        output = gen.generate(self.report)
        self.assertIn("REPORTE DE MONITOREO", output)

    def test_strategy_switch_at_runtime(self):
        gen = ReportGenerator(PlainTextStrategy())
        gen.set_strategy(MarkdownStrategy())
        self.assertEqual(gen.current_format, "Markdown")

    def test_get_strategy_all_formats(self):
        for fmt in ("txt", "md", "pdf"):
            s = get_strategy(fmt)
            self.assertIsNotNone(s)

    def test_unsupported_format_raises(self):
        with self.assertRaises(KeyError):
            get_strategy("html")


# ─────────────────────────────────────────────────────────────────────────────
# Test: Flujo end-to-end
# ─────────────────────────────────────────────────────────────────────────────

class TestEndToEnd(unittest.TestCase):

    def test_full_flow_txt(self):
        """Ciclo completo: config → adapters → report → cost → output."""
        adapters = AdapterFactory.create_all([
            {"type": "webapi", "service_id": "e2e-01"},
            {"type": "webintegral", "user": "u", "token": "t"},
            {"type": "serverwatch"},
        ])
        system = MonitoringSystem(adapters)
        report = system.build_report(request_count=30)

        cost = LatamCostCalculator().calculate(report)
        self.assertGreater(cost.total, 0)

        output = ReportGenerator(PlainTextStrategy()).generate(report)
        self.assertIn("WebAPI", output)
        self.assertIn("WebIntegral", output)
        self.assertIn("ServerWatch", output)

    def test_full_flow_markdown(self):
        adapters = [WebApiAdapter("e2e-02")]
        report = MonitoringSystem(adapters).build_report(request_count=10)
        output = ReportGenerator(MarkdownStrategy()).generate(report)
        self.assertIn("# Reporte", output)
        self.assertIn("WebAPI", output)


if __name__ == "__main__":
    unittest.main(verbosity=2)