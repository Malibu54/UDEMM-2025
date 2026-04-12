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
    
        self._config: dict[str, Any] = {}

# ── Lectura ──────────────────────────────

