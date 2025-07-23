class Pago:
    def __init__(self, monto):
        self.monto = monto

class PagoEfectivo(Pago):
    def __init__(self, monto):
        super().__init__(monto)

class PagoTarjeta(Pago):
    def __init__(self, monto, banco, fecha, autorizada, tipo_tarjeta):
        super().__init__(monto)
        self.banco = banco
        self.fecha = fecha
        self.autorizada = autorizada
        self.tipo_tarjeta = tipo_tarjeta  # 'crédito' o 'débito'

class PagoTransferencia(Pago):
    def __init__(self, monto, fecha, autorizada, numero_transferencia):
        super().__init__(monto)
        self.fecha = fecha
        self.autorizada = autorizada
        self.numero_transferencia = numero_transferencia
