# Clase para el detalle de cada ítem
class DetalleOrden:
    def __init__(self, nombre, descripcion, precio_unitario, stock, impuesto, activo=True, peso=0):
        self.nombre = nombre
        self.descripcion = descripcion
        self.precio_unitario = precio_unitario
        self.stock = stock  # cantidad disponible
        self.impuesto = impuesto  # porcentaje, ejemplo 10 para 10%
        self.activo = activo
        self.peso = peso  # peso unitario para cálculos

    def hay_stock(self, cantidad=1):
        return self.stock >= cantidad and self.activo

    def descontar_stock(self, cantidad=1):
        if self.hay_stock(cantidad):
            self.stock -= cantidad
            return True
        return False

    def agregar_stock(self, cantidad=1):
        self.stock += cantidad
