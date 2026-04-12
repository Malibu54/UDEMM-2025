from __future__ import annotations

import threading
from typing import Any

# ─────────────────────────────────────────────
# 1. Metaclass — controla la creación de la instancia
# ─────────────────────────────────────────────

_instances: dict [type, object] = {}
_lock: threading.Lock = threading.Lock()

def __call__ (cls, *args: Any, **kwargs: Any) -> object:

    if cls not in cls._instances:
        with cls._lock:

            if cls not in cls.instances:
                instances = super() .__call__(*args, **kwargs)
                cls._instances [cls] = instances
    return cls._instances[cls]