"""
adapters/monitor_adapters.py
============================
Patrón: ADAPTER (GoF - Structural)

Problema que resuelve:
    Tres proveedores externos con interfaces incompatibles (XML legacy, JSON con auth,
    REST con parámetros propios) deben ser utilizados de forma uniforme por el resto
    del sistema. Sin este patrón, el sistema tendría que conocer los detalles de cada
    proveedor en múltiples lugares.

Solución:
    - IMonitorAdapter define la interfaz esperada por el sistema: obtener_estado().
    - Cada adaptador concreto encapsula la traducción entre la API real del proveedor
      y la entidad ServiceStatus del dominio.
    - El sistema nunca llama directamente a las APIs externas: solo conoce IMonitorAdapter.

Resiliencia:
    Cada adaptador captura sus propias excepciones y retorna un ServiceStatus con
    available=False y el mensaje de error. Así el sistema nunca se bloquea por
    el fallo de un proveedor individual.
    Los errores se registran vía el módulo estándar logging (no print), permitiendo
    configurar handlers de forma externa sin modificar este código (OCP).
"""

from __future__ import annotations

import logging
import xml.etree.ElementTree as ET
from abc import ABC, abstractmethod
from datetime import datetime
from typing import Any

from domain.entities import ServiceStatus

logger = logging.getLogger(__name__)


# ──────────────────────────────────────────────────────────────────────────────
# Interfaz — Target del patrón Adapter
# ──────────────────────────────────────────────────────────────────────────────

class IMonitorAdapter(ABC):
    """
    Interfaz que el sistema espera de cualquier proveedor de monitoreo.

    Define el contrato: dado que se llame a obtener_estado(), se obtiene
    un ServiceStatus normalizado, sin importar el proveedor de origen.
    """

    @abstractmethod
    def obtener_estado(self) -> ServiceStatus:
        """Consulta el proveedor y retorna el estado normalizado."""
        ...

    @property
    @abstractmethod
    def provider_name(self) -> str:
        """Nombre identificador del proveedor."""
        ...


# ──────────────────────────────────────────────────────────────────────────────
# Simulación de APIs externas (en producción serían llamadas reales HTTP/XML-RPC)
# ──────────────────────────────────────────────────────────────────────────────

def _webapi_get_xml_data(service_id: str) -> str:
    """Simula WebAPI.get_xml_data(id) → XML string."""
    return f"""<?xml version="1.0"?>
<response>
    <service_id>{service_id}</service_id>
    <status>UP</status>
    <latency>142.5</latency>
    <checked_at>2025-01-15T10:30:00</checked_at>
</response>"""


def _webintegral_get_status_today(credential: dict) -> dict:
    """Simula webintegral.get_status_today(credential) → dict JSON."""
    if not credential.get("token"):
        raise PermissionError("Invalid credentials for WebIntegral")
    return {
        "is_up": True,
        "response_time_ms": 87.3,
        "timestamp": "2025-01-15T10:30:05"
    }


def _serverwatch_get_all_server_status(today: str, fmt: str) -> Any:
    """Simula serverwatch.get_all_server_status(today, format) → JSON o XML."""
    if fmt == "json":
        return {"online": True, "latency": 55.1, "date": today}
    return f"""<servers><server><online>true</online><latency>55.1</latency></server></servers>"""


# ──────────────────────────────────────────────────────────────────────────────
# Adaptadores
# ──────────────────────────────────────────────────────────────────────────────

class WebApiAdapter(IMonitorAdapter):
    """
    Adapta WebAPI (XML legacy, método get_xml_data) a IMonitorAdapter.

    El service_id viene de la configuración externa; este adaptador no sabe
    ni le importa de dónde vino esa configuración.
    """

    def __init__(self, service_id: str) -> None:
        self._service_id = service_id

    @property
    def provider_name(self) -> str:
        return "WebAPI"

    def obtener_estado(self) -> ServiceStatus:
        try:
            raw_xml = _webapi_get_xml_data(self._service_id)
            return self._parse_xml(raw_xml)
        except ET.ParseError as exc:
            logger.error("[WebApiAdapter] XML malformado: %s", exc)
            return self._error_status(f"XML malformado: {exc}")
        except TimeoutError as exc:
            logger.error("[WebApiAdapter] Timeout: %s", exc)
            return self._error_status(f"Timeout de conexión: {exc}")
        except Exception as exc:
            logger.error("[WebApiAdapter] Error inesperado: %s", exc)
            return self._error_status(str(exc))

    def _parse_xml(self, raw: str) -> ServiceStatus:
        """Traduce el XML del proveedor al modelo de dominio."""
        root = ET.fromstring(raw)
        available = root.findtext("status", "").upper() == "UP"
        latency = float(root.findtext("latency", "0") or 0)
        ts_text = root.findtext("checked_at", "")
        timestamp = datetime.fromisoformat(ts_text) if ts_text else datetime.now()
        return ServiceStatus(
            provider=self.provider_name,
            available=available,
            latency_ms=latency,
            timestamp=timestamp,
        )

    def _error_status(self, message: str) -> ServiceStatus:
        return ServiceStatus(
            provider=self.provider_name,
            available=False,
            latency_ms=0.0,
            timestamp=datetime.now(),
            error=message,
        )


class WebIntegralAdapter(IMonitorAdapter):
    """
    Adapta WebIntegral (JSON con autenticación) a IMonitorAdapter.

    La credencial se inyecta en construcción desde la configuración externa.
    Captura PermissionError específicamente para credenciales inválidas,
    además de errores genéricos.
    """

    def __init__(self, credential: dict) -> None:
        self._credential = credential

    @property
    def provider_name(self) -> str:
        return "WebIntegral"

    def obtener_estado(self) -> ServiceStatus:
        try:
            data = _webintegral_get_status_today(self._credential)
            return self._parse_json(data)
        except PermissionError as exc:
            logger.error("[WebIntegralAdapter] Autenticación inválida: %s", exc)
            return self._error_status(f"Autenticación inválida: {exc}")
        except (KeyError, ValueError) as exc:
            logger.error("[WebIntegralAdapter] Respuesta JSON inválida: %s", exc)
            return self._error_status(f"Respuesta inválida: {exc}")
        except Exception as exc:
            logger.error("[WebIntegralAdapter] Error inesperado: %s", exc)
            return self._error_status(str(exc))

    def _parse_json(self, data: dict) -> ServiceStatus:
        """Traduce el JSON del proveedor al modelo de dominio."""
        ts_text = data.get("timestamp", "")
        timestamp = datetime.fromisoformat(ts_text) if ts_text else datetime.now()
        return ServiceStatus(
            provider=self.provider_name,
            available=bool(data.get("is_up", False)),
            latency_ms=float(data.get("response_time_ms", 0.0)),
            timestamp=timestamp,
        )

    def _error_status(self, message: str) -> ServiceStatus:
        return ServiceStatus(
            provider=self.provider_name,
            available=False,
            latency_ms=0.0,
            timestamp=datetime.now(),
            error=message,
        )


class ServerWatchAdapter(IMonitorAdapter):
    """
    Adapta ServerWatch (REST moderno, puede retornar JSON o XML) a IMonitorAdapter.

    Demuestra que el adaptador también puede tomar decisiones internas
    sobre el formato que prefiere solicitar, sin exponer ese detalle al sistema.
    """

    def __init__(self, preferred_format: str = "json") -> None:
        if preferred_format not in ("json", "xml"):
            raise ValueError(f"Formato no soportado: {preferred_format}")
        self._format = preferred_format

    @property
    def provider_name(self) -> str:
        return "ServerWatch"

    def obtener_estado(self) -> ServiceStatus:
        try:
            today = datetime.now().strftime("%Y-%m-%d")
            raw = _serverwatch_get_all_server_status(today, self._format)
            return self._parse_response(raw)
        except ET.ParseError as exc:
            logger.error("[ServerWatchAdapter] XML malformado: %s", exc)
            return self._error_status(f"XML malformado: {exc}")
        except (KeyError, TypeError, ValueError) as exc:
            logger.error("[ServerWatchAdapter] Datos inválidos: %s", exc)
            return self._error_status(f"Datos inválidos: {exc}")
        except Exception as exc:
            logger.error("[ServerWatchAdapter] Error inesperado: %s", exc)
            return self._error_status(str(exc))

    def _parse_response(self, raw: Any) -> ServiceStatus:
        """Delega al parser correcto según el formato configurado."""
        if self._format == "json":
            return self._parse_json(raw)
        return self._parse_xml(raw)

    def _parse_json(self, data: dict) -> ServiceStatus:
        return ServiceStatus(
            provider=self.provider_name,
            available=bool(data.get("online", False)),
            latency_ms=float(data.get("latency", 0.0)),
            timestamp=datetime.now(),
        )

    def _parse_xml(self, raw: str) -> ServiceStatus:
        root = ET.fromstring(raw)
        server = root.find("server")
        available = (server.findtext("online", "false").lower() == "true") if server is not None else False
        latency = float(server.findtext("latency", "0") or 0) if server is not None else 0.0
        return ServiceStatus(
            provider=self.provider_name,
            available=available,
            latency_ms=latency,
            timestamp=datetime.now(),
        )

    def _error_status(self, message: str) -> ServiceStatus:
        return ServiceStatus(
            provider=self.provider_name,
            available=False,
            latency_ms=0.0,
            timestamp=datetime.now(),
            error=message,
        )