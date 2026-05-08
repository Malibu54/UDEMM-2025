"""
adapters/adapter_factory.py
============================
Patrón: FACTORY METHOD (GoF - Creational)

Problema que resuelve:
    El sistema necesita cargar dinámicamente los adaptadores activos según
    una configuración externa (archivo, base de datos, variables de entorno),
    sin que el código principal conozca qué adaptadores existen o cómo
    construirlos. Si se añade un nuevo proveedor, solo se registra aquí.

Solución:
    AdapterFactory centraliza la creación. El código cliente solo llama
    AdapterFactory.create(config_entry) y obtiene un IMonitorAdapter listo.

    El registro ADAPTER_REGISTRY desacopla el nombre del tipo (string de config)
    de la clase concreta, cumpliendo OCP: para agregar un nuevo proveedor
    se agrega una entrada al registro, sin modificar create().
"""

from __future__ import annotations

from typing import Callable

from adapters.monitor_adapters import (
    IMonitorAdapter,
    ServerWatchAdapter,
    WebApiAdapter,
    WebIntegralAdapter,
)


# Registro: mapea el tipo de config → función constructora
# Permite agregar nuevos adaptadores sin modificar create()
ADAPTER_REGISTRY: dict[str, Callable[[dict], IMonitorAdapter]] = {
    "webapi": lambda cfg: WebApiAdapter(service_id=cfg["service_id"]),
    "webintegral": lambda cfg: WebIntegralAdapter(
        credential={"user": cfg["user"], "token": cfg["token"]}
    ),
    "serverwatch": lambda cfg: ServerWatchAdapter(
        preferred_format=cfg.get("format", "json")
    ),
}


class AdapterFactory:
    """
    Fábrica de adaptadores de monitoreo.

    Uso:
        config = {"type": "webapi", "service_id": "svc-001"}
        adapter = AdapterFactory.create(config)
        status = adapter.obtener_estado()
    """

    @staticmethod
    def create(config: dict) -> IMonitorAdapter:
        """
        Construye el adaptador correspondiente al tipo especificado en config.

        Args:
            config: Diccionario con al menos la clave "type" y los
                    parámetros específicos del proveedor.

        Raises:
            KeyError: Si el tipo no está registrado.
        """
        adapter_type = config.get("type", "").lower()
        builder = ADAPTER_REGISTRY.get(adapter_type)
        if builder is None:
            registered = list(ADAPTER_REGISTRY.keys())
            raise KeyError(
                f"Tipo de adaptador desconocido: '{adapter_type}'. "
                f"Registrados: {registered}"
            )
        return builder(config)

    @staticmethod
    def create_all(configs: list[dict]) -> list[IMonitorAdapter]:
        """
        Construye todos los adaptadores habilitados de la configuración.

        Cada entrada puede tener 'enabled: false' para desactivarse
        sin eliminarla de la configuración.
        """
        return [
            AdapterFactory.create(cfg)
            for cfg in configs
            if cfg.get("enabled", True)
        ]