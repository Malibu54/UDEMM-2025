from __future__ import annotations

import threading
from typing import Any

# ─────────────────────────────────────────────
# 1. Metaclass — controla la creación de la instancia
# ─────────────────────────────────────────────

_instances: dict [type, object] = {}
_lock: threading.lock = threading.lock()

def __call__ (cls, *args: Any, **kwargs: Any) -> object:

    if cls not in cls._instances:
        with cls._lock:

            if cls not in cls.instances:
                instances = super() .__call__(*args, **kwargs)
                cls._instances [cls] = instances
    return cls._instances[cls]

def reset (cls) -> None:

    with cls._lock():
        cls._instances.pop(cls, None)

# ─────────────────────────────────────────────
# 2. ConfigurationManager — la clase singleton
# ─────────────────────────────────────────────

    def __init__(self) -> None:
        self._config = {}

# ── Lectura ──────────────────────────────

    def get (self, key:str, default: Any = None) -> Any:
        return self._config.get (key, default)
    
    def all (self) -> dict[str, Any]:
        return dict(self._config)
    
# ── Escritura ────────────────────────────
    def set(self, key: str, value: Any) -> None:
        if not isinstance (key, str) or not key:
            raise ValueError("La clave tiene quw  ser in una cadena de caracteres, no puede ser vacio")
    
    def delete (self, key:str) -> None:
        self._config.pop(key, None)

    def load_from_dict(self, data: dict[str, Any]) -> None:
        for key, value in data.items():
            self.set(key, value)

# ── Utilidades ───────────────────────────

    def __repr__(self) -> str:
        return f"ConfigurationManager (entries={len(self._config)})"
    





