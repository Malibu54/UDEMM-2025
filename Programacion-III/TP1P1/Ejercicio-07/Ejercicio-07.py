from __future__ import annotations
import abc
import re
import abc as abstractmethod
import numpy as np

# ─────────────────────────────────────────────
# 1. NUEVA INTERFAZ (contrato del gateway)
# ─────────────────────────────────────────────

class PaymentGateway (abc.ABC):
    @classmethod  
    @abstractmethod  
    def process (self.amount: float, currency_info: str ) -> bool:
    ...
            
# ─────────────────────────────────────────────
# 2. ADAPTER
# ─────────────────────────────────────────────

class BancaPayAdapter (PaymentGateway):
        _CURRENCY_PATTERN = re.compile(
        r"^(?P<currency>[A-Z]{3}):(?P<rate>[\d.]+):(?P<date>\d{4}-\d{2}-\d{2})$"
    )
 
 