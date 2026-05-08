"""
config/settings.py
===================
Gestión de configuración externa del sistema.

Permite al administrador controlar qué proveedores están activos
y sus parámetros (credenciales, IDs, etc.) sin modificar código.

En producción, SystemConfig.load() leería desde:
  - Archivo YAML/JSON en disco
  - Variables de entorno
  - Servicio de configuración centralizado (Consul, AWS Parameter Store, etc.)

La configuración está desacoplada del código: cambiar un proveedor
o desactivarlo es solo editar un archivo o variable de entorno.
"""

from __future__ import annotations

import json
import os
from dataclasses import dataclass, field
from typing import List


@dataclass
class SystemConfig:
    """
    Configuración central del sistema GloberX26.

    Atributos:
        providers      -- lista de configuraciones de proveedores activos
        default_region -- región por defecto para cálculo de costos
        log_level      -- nivel de logging del sistema
    """
    providers: List[dict] = field(default_factory=list)
    default_region: str = "latam"
    log_level: str = "INFO"

    @classmethod
    def load(cls, path: str | None = None) -> "SystemConfig":
        """
        Carga la configuración desde archivo JSON o usa valores por defecto.

        Si no se especifica ruta y no existe CONFIG_PATH en el entorno,
        retorna una configuración de ejemplo con los tres proveedores activos.
        """
        config_path = path or os.environ.get("GLOBERX26_CONFIG")

        if config_path and os.path.isfile(config_path):
            with open(config_path, encoding="utf-8") as f:
                data = json.load(f)
            return cls(
                providers=data.get("providers", []),
                default_region=data.get("default_region", "latam"),
                log_level=data.get("log_level", "INFO"),
            )

        # Configuración de ejemplo cuando no hay archivo externo
        return cls(
            providers=[
                {
                    "type": "webapi",
                    "enabled": True,
                    "service_id": "svc-001",
                },
                {
                    "type": "webintegral",
                    "enabled": True,
                    "user": "admin@globerx26.com",
                    "token": "tok_abc123xyz",
                },
                {
                    "type": "serverwatch",
                    "enabled": True,
                    "format": "json",
                },
            ],
            default_region="latam",
            log_level="INFO",
        )

    def to_json(self) -> str:
        """Serializa la configuración actual a JSON (útil para inspección)."""
        return json.dumps(
            {
                "providers": self.providers,
                "default_region": self.default_region,
                "log_level": self.log_level,
            },
            indent=2,
        )