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
 
def __init__(self, adaptee: BancaPay) -> None:
        self._adaptee = adaptee
 
    def process(self, amount: float, currency_info: str) -> bool:
        print(f"\n[Adapter] Solicitud recibida → amount={amount}, info='{currency_info}'")
 
        currency, rate, date = self._parse_currency_info(currency_info)
 
        # Convertir al valor base ARS para el sistema legado
        amount_ars = amount * rate
        print(f"[Adapter] Conversión: {amount} {currency} × {rate} = {amount_ars:.2f} ARS (cotización {date})")
 
        # Adaptar tipo: float64 → np.float32
        legacy_amount = np.float32(amount_ars)
        print(f"[Adapter] Tipo adaptado: float64({amount_ars:.2f}) → np.float32({legacy_amount:.2f})")
 
        # Delegar al sistema legado sin modificarlo
        return self._adaptee.pay(legacy_amount)
 
    # ── helpers privados ──────────────────────
 
    def _parse_currency_info(self, currency_info: str) -> tuple[str, float, str]:

        match = self._CURRENCY_PATTERN.match(currency_info.strip())
        if not match:
            raise ValueError(
                f"Formato inválido de currency_info: '{currency_info}'. "
                "Esperado: 'MONEDA:COTIZACION:YYYY-MM-DD'  (ej: 'USD:1180.50:2025-01-15')"
            )
        currency = match.group("currency")
        rate = float(match.group("rate"))
        date = match.group("date")
        return currency, rate, date
 
 
# ─────────────────────────────────────────────
# 3. IMPLEMENTACIÓN NATIVA DEL NUEVO GATEWAY
# ─────────────────────────────────────────────
 
class NewPaymentGateway(PaymentGateway):

 
    def process(self, amount: float, currency_info: str) -> bool:
        currency = currency_info.split(":")[0] if ":" in currency_info else "???"
        print(f"\n[NewGateway] Procesando {amount:.2f} {currency} con info='{currency_info}'")
        approved = amount > 0
        print(f"[NewGateway] Resultado: {'APROBADO' if approved else 'RECHAZADO'}")
        return approved
 
 
# ─────────────────────────────────────────────
# 4. CLIENTE  (trabaja solo con PaymentGateway)
# ─────────────────────────────────────────────
 
def run_payment(gateway: PaymentGateway, amount: float, currency_info: str) -> None:

    result = gateway.process(amount, currency_info)
    print(f"{'✓ Pago exitoso' if result else '✗ Pago rechazado'}\n")
