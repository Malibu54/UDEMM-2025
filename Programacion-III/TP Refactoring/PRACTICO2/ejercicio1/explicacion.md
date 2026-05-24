"""
Clase: Subscription - versión refactorizada

PROBLEMAS IDENTIFICADOS EN EL CÓDIGO ORIGINAL:
-----------------------------------------------
1. Long Method: calculate_price() mezcla lógica de descuento, comisión y retorno.
2. Magic Numbers: valores como 0.95, 0.02 sin nombre ni contexto.
3. Ausencia del patrón Strategy: lógica de negocio embebida en if/elif/else.
4. Datos como strings literales: susceptibles a errores de tipeo en tiempo de ejecución.
5. Violación del SRP: la clase mezcla datos del cliente con lógica de precios.
6. Violación del OCP: agregar un nuevo tipo de cliente requiere modificar el método.

REFACTORIZACIONES APLICADAS:
------------------------------
class ClientType(Enum):
    """
    Tipos de cliente con su descuento asociado.
    Refactoring aplicado: Replace Magic Number with Symbolic Constant.
    """

    class PaymentMethod(Enum):
    """
    Métodos de pago con su comisión asociada.
    Refactoring aplicado: Replace Magic Number with Symbolic Constant.
    """

    class PriceCalculator:
    """
    Responsabilidad única: calcular el precio final dado un precio base,
    un tipo de cliente y un método de pago.
 
    Refactoring aplicado:
    - Extract Method: los pasos del cálculo están separados en métodos específicos.
    - Single Responsibility Principle: esta clase sólo sabe calcular precios.
    """
class Subscription:
    """
    Representa una suscripción con tipo de cliente y método de pago.
 
    Refactoring aplicado:
    - La clase ya no contiene lógica de cálculo (delegada a PriceCalculator).
    - Los tipos son Enum, no strings: errores de tipeo se detectan en el acto.
    - calculate_price() es simple y legible.
    """