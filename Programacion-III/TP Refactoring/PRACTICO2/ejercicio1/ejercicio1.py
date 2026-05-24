from enum import Enum
import unittest

class ClientType(Enum):

    PARTICULAR  = 0.05  
    EMPRESA     = 0.10  
    ESTUDIANTE  = 0.15   


class PaymentMethod(Enum):
    """
    Métodos de pago con su comisión asociada.
    Refactoring aplicado: Replace Magic Number with Symbolic Constant.
    """
    TARJETA       = 0.02  
    TRANSFERENCIA = 0.01  
    PAYPAL        = 0.03  


class PriceCalculator:

    @staticmethod
    def apply_discount(price: float, client_type: ClientType) -> float:

        return price * (1 - client_type.value)

    @staticmethod
    def apply_commission(price: float, payment_method: PaymentMethod) -> float:
        return price + (price * payment_method.value)

    @classmethod
    def calculate(cls, base_price: float, client_type: ClientType,
                  payment_method: PaymentMethod) -> float:

        price = cls.apply_discount(base_price, client_type)
        price = cls.apply_commission(price, payment_method)
        return round(price, 2)


class Subscription:


    def __init__(self, client_type: ClientType, payment_method: PaymentMethod,
                 base_price: float):
        if base_price <= 0:
            raise ValueError("El precio base debe ser mayor a cero.")
        self._client_type    = client_type
        self._payment_method = payment_method
        self._base_price     = base_price

    def calculate_price(self) -> float:
        """Delega el cálculo al PriceCalculator."""
        return PriceCalculator.calculate(
            self._base_price,
            self._client_type,
            self._payment_method
        )

    def __repr__(self) -> str:
        return (
            f"Subscription(client={self._client_type.name}, "
            f"payment={self._payment_method.name}, "
            f"base_price={self._base_price})"
        )

if __name__ == "__main__":
    sub = Subscription(ClientType.EMPRESA, PaymentMethod.PAYPAL, 100)
    print(sub)
    print(f"Precio final: {sub.calculate_price()}")

# Pruebas Unitarias

class TestPriceCalculator(unittest.TestCase):

    def test_apply_discount_particular(self):
        result = PriceCalculator.apply_discount(100, ClientType.PARTICULAR)
        self.assertAlmostEqual(result, 95.0)

    def test_apply_discount_empresa(self):
        result = PriceCalculator.apply_discount(100, ClientType.EMPRESA)
        self.assertAlmostEqual(result, 90.0)

    def test_apply_discount_estudiante(self):
        result = PriceCalculator.apply_discount(100, ClientType.ESTUDIANTE)
        self.assertAlmostEqual(result, 85.0)

    def test_apply_commission_tarjeta(self):
        result = PriceCalculator.apply_commission(100, PaymentMethod.TARJETA)
        self.assertAlmostEqual(result, 102.0)

    def test_apply_commission_transferencia(self):
        result = PriceCalculator.apply_commission(100, PaymentMethod.TRANSFERENCIA)
        self.assertAlmostEqual(result, 101.0)

    def test_apply_commission_paypal(self):
        result = PriceCalculator.apply_commission(100, PaymentMethod.PAYPAL)
        self.assertAlmostEqual(result, 103.0)

    def test_calculate_empresa_paypal(self):
        result = PriceCalculator.calculate(100, ClientType.EMPRESA, PaymentMethod.PAYPAL)
        self.assertEqual(result, 92.70)

    def test_calculate_estudiante_transferencia(self):
        result = PriceCalculator.calculate(200, ClientType.ESTUDIANTE, PaymentMethod.TRANSFERENCIA)
        self.assertEqual(result, 171.70)


class TestSubscription(unittest.TestCase):

    def test_calculate_price_particular_tarjeta(self):
        sub = Subscription(ClientType.PARTICULAR, PaymentMethod.TARJETA, 100)
        # 100 * 0.95 * 1.02 = 96.90
        self.assertEqual(sub.calculate_price(), 96.90)

    def test_calculate_price_empresa_paypal(self):
        sub = Subscription(ClientType.EMPRESA, PaymentMethod.PAYPAL, 100)
        self.assertEqual(sub.calculate_price(), 92.70)

    def test_calculate_price_estudiante_transferencia(self):
        sub = Subscription(ClientType.ESTUDIANTE, PaymentMethod.TRANSFERENCIA, 50)
        # 50 * 0.85 * 1.01 = 42.925 → redondeado a 2 decimales = 42.92
        self.assertEqual(sub.calculate_price(), 42.92)

    def test_invalid_base_price_raises(self):

        with self.assertRaises(ValueError):
            Subscription(ClientType.PARTICULAR, PaymentMethod.TARJETA, 0)

    def test_invalid_base_price_negative(self):
        with self.assertRaises(ValueError):
            Subscription(ClientType.PARTICULAR, PaymentMethod.TARJETA, -50)

    def test_repr(self):
        sub = Subscription(ClientType.EMPRESA, PaymentMethod.PAYPAL, 100)
        self.assertIn("EMPRESA", repr(sub))
        self.assertIn("PAYPAL", repr(sub))

    def test_enum_prevents_invalid_client_type(self):
        with self.assertRaises(AttributeError):
            Subscription(ClientType.INVALIDO, PaymentMethod.PAYPAL, 100)